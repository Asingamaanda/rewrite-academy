"""
ClassDoodle Backend - Database Models
Works with both PostgreSQL (Render) and SQLite (local dev).
Connection management is handled by backend.db_adapter.
"""

from datetime import datetime, date
from backend.db_adapter import (
    get_connection, release_connection, qexec, fetchone, fetchall,
    _make_cursor, PH, SERIAL_PK, POSTGRES
)


class ClassDoodleDB:
    """Main database manager -- connection-per-operation, pool-safe."""

    def __init__(self, db_path=None):   # db_path kept for backward compat, ignored
        try:
            self.initialize_database()
        except Exception as e:
            print(f"WARNING: DB init deferred — {e}")
            self._init_done = False
        else:
            self._init_done = True

    def ensure_initialized(self):
        """Called on first real request if __init__ deferred."""
        if not getattr(self, '_init_done', True):
            self.initialize_database()
            self._init_done = True

    def initialize_database(self):
        """Create all tables and seed defaults. Idempotent."""
        conn  = get_connection()
        cur   = _make_cursor(conn)
        today = date.today().isoformat()

        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS students (
                id              {SERIAL_PK},
                student_id      TEXT UNIQUE NOT NULL,
                name            TEXT NOT NULL,
                email           TEXT UNIQUE NOT NULL,
                phone           TEXT,
                parent_name     TEXT,
                parent_phone    TEXT,
                parent_email    TEXT,
                registration_date DATE NOT NULL,
                status          TEXT DEFAULT 'active',
                academic_risk   TEXT DEFAULT 'on_track',
                attendance_risk TEXT DEFAULT 'ok',
                payment_risk    TEXT DEFAULT 'pending',
                notes           TEXT,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS student_subjects (
                id         {SERIAL_PK},
                student_id TEXT NOT NULL
                           REFERENCES students(student_id) ON DELETE CASCADE,
                subject    TEXT NOT NULL,
                UNIQUE(student_id, subject)
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS attendance (
                id         {SERIAL_PK},
                student_id TEXT NOT NULL
                           REFERENCES students(student_id) ON DELETE CASCADE,
                date       DATE NOT NULL,
                time_slot  TEXT NOT NULL,
                subject    TEXT NOT NULL,
                status     TEXT NOT NULL,
                marked_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, date, time_slot, subject)
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS assessments (
                id              {SERIAL_PK},
                student_id      TEXT NOT NULL
                                REFERENCES students(student_id) ON DELETE CASCADE,
                subject         TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                score           REAL NOT NULL,
                max_score       REAL NOT NULL DEFAULT 100,
                weight          REAL NOT NULL DEFAULT 1,
                date            DATE NOT NULL,
                notes           TEXT,
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS payments (
                id             {SERIAL_PK},
                student_id     TEXT NOT NULL
                               REFERENCES students(student_id) ON DELETE CASCADE,
                amount         REAL NOT NULL,
                payment_date   DATE,
                due_date       DATE,
                payment_method TEXT,
                reference      TEXT,
                month_for      TEXT NOT NULL,
                status         TEXT NOT NULL DEFAULT 'pending',
                notes          TEXT,
                created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS leads (
                id           {SERIAL_PK},
                name         TEXT NOT NULL,
                phone        TEXT NOT NULL,
                email        TEXT,
                source       TEXT NOT NULL,
                status       TEXT DEFAULT 'new',
                contacted_at TIMESTAMP,
                enrolled_at  TIMESTAMP,
                notes        TEXT,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS lesson_plans (
                id         {SERIAL_PK},
                date       DATE NOT NULL,
                subject    TEXT NOT NULL,
                time_slot  TEXT NOT NULL,
                topic      TEXT NOT NULL,
                objectives TEXT,
                materials  TEXT,
                homework   TEXT,
                notes      TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, subject, time_slot)
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS settings (
                key        TEXT PRIMARY KEY,
                value      TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS applications (
                id              {SERIAL_PK},
                full_name       TEXT NOT NULL,
                phone           TEXT NOT NULL,
                email           TEXT DEFAULT '',
                parent_name     TEXT DEFAULT '',
                parent_phone    TEXT DEFAULT '',
                subjects        TEXT NOT NULL,
                previous_school TEXT DEFAULT '',
                year_failed     TEXT DEFAULT '',
                message         TEXT DEFAULT '',
                status          TEXT DEFAULT 'new',
                created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS user_accounts (
                id            {SERIAL_PK},
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role          TEXT NOT NULL CHECK(role IN ('admin','teacher','student')),
                student_id    TEXT
                              REFERENCES students(student_id) ON DELETE SET NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS manlib_videos (
                id            {SERIAL_PK},
                subject       TEXT NOT NULL,
                title         TEXT NOT NULL,
                description   TEXT,
                video_type    TEXT NOT NULL CHECK(video_type IN ('youtube','upload')),
                video_url     TEXT,
                file_path     TEXT,
                thumbnail_url TEXT,
                duration      TEXT,
                order_num     INTEGER DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS timetable_slots (
                id         {SERIAL_PK},
                student_id TEXT                              -- nullable = global slot
                           REFERENCES students(student_id) ON DELETE CASCADE,
                day        TEXT NOT NULL,
                period     INTEGER NOT NULL,
                subject    TEXT NOT NULL,
                time_from  TEXT NOT NULL,
                time_to    TEXT NOT NULL,
                room       TEXT NOT NULL DEFAULT '',
                teacher    TEXT NOT NULL DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS subject_content (
                id           {SERIAL_PK},
                subject      TEXT NOT NULL,
                content_type TEXT NOT NULL CHECK(content_type IN ('notes','question_paper','critical_work','exam_prep')),
                title        TEXT NOT NULL,
                description  TEXT DEFAULT '',
                content_text TEXT DEFAULT '',
                file_path    TEXT DEFAULT '',
                link_url     TEXT DEFAULT '',
                order_num    INTEGER DEFAULT 0,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS subjects (
                id         {SERIAL_PK},
                name       TEXT UNIQUE NOT NULL,
                teacher    TEXT DEFAULT '',
                weight     REAL DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS progress_snapshots (
                id         {SERIAL_PK},
                student_id TEXT NOT NULL
                           REFERENCES students(student_id) ON DELETE CASCADE,
                week       TEXT NOT NULL,
                average    REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(student_id, week)
            )
        """)
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS automation_alerts (
                id         {SERIAL_PK},
                student_id TEXT NOT NULL
                           REFERENCES students(student_id) ON DELETE CASCADE,
                alert_type TEXT NOT NULL,
                message    TEXT NOT NULL,
                resolved   INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

        # ── Indexes ──────────────────────────────────────────────────────────
        # CREATE INDEX IF NOT EXISTS is a no-op if the index already exists,
        # so these are safe to run on every startup.
        _indexes = [
            # students — lookup by student_id and risk filters
            "CREATE INDEX IF NOT EXISTS idx_students_student_id     ON students(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_students_academic_risk  ON students(academic_risk)",
            "CREATE INDEX IF NOT EXISTS idx_students_attendance_risk ON students(attendance_risk)",
            "CREATE INDEX IF NOT EXISTS idx_students_payment_risk   ON students(payment_risk)",
            "CREATE INDEX IF NOT EXISTS idx_students_status         ON students(status)",
            # student_subjects — join / filter by student and subject
            "CREATE INDEX IF NOT EXISTS idx_ss_student_id           ON student_subjects(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_ss_subject              ON student_subjects(subject)",
            # assessments — the most queried table
            "CREATE INDEX IF NOT EXISTS idx_assess_student_id       ON assessments(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_assess_subject          ON assessments(subject)",
            "CREATE INDEX IF NOT EXISTS idx_assess_date             ON assessments(date)",
            "CREATE INDEX IF NOT EXISTS idx_assess_student_subject  ON assessments(student_id, subject)",
            # attendance
            "CREATE INDEX IF NOT EXISTS idx_attend_student_id       ON attendance(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_attend_date             ON attendance(date)",
            "CREATE INDEX IF NOT EXISTS idx_attend_subject          ON attendance(subject)",
            # payments
            "CREATE INDEX IF NOT EXISTS idx_payments_student_id     ON payments(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_payments_status         ON payments(status)",
            # progress snapshots
            "CREATE INDEX IF NOT EXISTS idx_snapshots_student_id    ON progress_snapshots(student_id)",
            # automation alerts
            "CREATE INDEX IF NOT EXISTS idx_alerts_student_id       ON automation_alerts(student_id)",
            "CREATE INDEX IF NOT EXISTS idx_alerts_resolved         ON automation_alerts(resolved)",
            # timetable
            "CREATE INDEX IF NOT EXISTS idx_tt_student_id           ON timetable_slots(student_id)",
            # user accounts
            "CREATE INDEX IF NOT EXISTS idx_users_student_id        ON user_accounts(student_id)",
        ]
        for _idx_sql in _indexes:
            try:
                cur.execute(_idx_sql)
            except Exception:
                pass  # index may already exist under a different engine
        conn.commit()

        # Live migrations
        if POSTGRES:
            for sql in [
                "ALTER TABLE students ADD COLUMN IF NOT EXISTS academic_risk TEXT DEFAULT 'on_track'",
                "ALTER TABLE students ADD COLUMN IF NOT EXISTS attendance_risk TEXT DEFAULT 'ok'",
                "ALTER TABLE students ADD COLUMN IF NOT EXISTS payment_risk TEXT DEFAULT 'pending'",
                "ALTER TABLE assessments ADD COLUMN IF NOT EXISTS weight REAL DEFAULT 1",
                "ALTER TABLE payments ADD COLUMN IF NOT EXISTS due_date DATE",
            ]:
                try: cur.execute(sql)
                except Exception: pass

            # ── FK constraints for existing Render DB ──────────────────────
            # Uses DO $$ BEGIN ... END; $$ so the block is skipped if the
            # constraint already exists (PG <15 has no ADD CONSTRAINT IF NOT EXISTS).
            _fk_migrations = [
                ("fk_ss_student",    "student_subjects",   "student_id", "CASCADE"),
                ("fk_attend_student","attendance",         "student_id", "CASCADE"),
                ("fk_assess_student","assessments",        "student_id", "CASCADE"),
                ("fk_pay_student",   "payments",           "student_id", "CASCADE"),
                ("fk_snap_student",  "progress_snapshots", "student_id", "CASCADE"),
                ("fk_alert_student", "automation_alerts",  "student_id", "CASCADE"),
                ("fk_tt_student",    "timetable_slots",    "student_id", "CASCADE"),
            ]
            for cname, table, col, on_delete in _fk_migrations:
                try:
                    cur.execute(f"""
                        DO $$ BEGIN
                            IF NOT EXISTS (
                                SELECT 1 FROM pg_constraint WHERE conname = '{cname}'
                            ) THEN
                                ALTER TABLE {table}
                                ADD CONSTRAINT {cname}
                                FOREIGN KEY ({col}) REFERENCES students(student_id)
                                ON DELETE {on_delete};
                            END IF;
                        END; $$
                    """)
                except Exception:
                    pass
            # user_accounts.student_id is nullable → SET NULL on delete
            try:
                cur.execute("""
                    DO $$ BEGIN
                        IF NOT EXISTS (
                            SELECT 1 FROM pg_constraint WHERE conname = 'fk_ua_student'
                        ) THEN
                            ALTER TABLE user_accounts
                            ADD CONSTRAINT fk_ua_student
                            FOREIGN KEY (student_id) REFERENCES students(student_id)
                            ON DELETE SET NULL;
                        END IF;
                    END; $$
                """)
            except Exception:
                pass
        else:
            for sql in [
                "ALTER TABLE students ADD COLUMN academic_risk TEXT DEFAULT 'on_track'",
                "ALTER TABLE students ADD COLUMN attendance_risk TEXT DEFAULT 'ok'",
                "ALTER TABLE students ADD COLUMN payment_risk TEXT DEFAULT 'pending'",
                "ALTER TABLE assessments ADD COLUMN weight REAL DEFAULT 1",
                "ALTER TABLE payments ADD COLUMN due_date DATE",
            ]:
                try: cur.execute(sql); conn.commit()
                except Exception: pass

        conn.commit()

        # Seed admin
        from werkzeug.security import generate_password_hash
        row = fetchone(conn, f"SELECT id FROM user_accounts WHERE username={PH}", ('admin',))
        if not row:
            cur.execute(
                f"INSERT INTO user_accounts (username, password_hash, role) VALUES ({PH},{PH},{PH})",
                ('admin', generate_password_hash('Classdoodle@password'), 'admin'))
            conn.commit()

        # Seed ASI001
        row = fetchone(conn, f"SELECT id FROM students WHERE student_id={PH}", ('ASI001',))
        if not row:
            cur.execute(f"""
                INSERT INTO students (student_id, name, email, registration_date, status)
                VALUES ({PH},{PH},{PH},{PH},{PH})
            """, ('ASI001','Asingamaanda Nefefe','asi001@rewriteacademy.local', today,'active'))
            for subj in ('Mathematics','Life Sciences','Geography'):
                cur.execute(f"INSERT INTO student_subjects (student_id,subject) VALUES ({PH},{PH})",
                            ('ASI001', subj))
            cur.execute(
                f"INSERT INTO user_accounts (username,password_hash,role,student_id) VALUES ({PH},{PH},{PH},{PH})",
                ('ASI001', generate_password_hash('student123'), 'student', 'ASI001'))
            for day,period,subject,t_from,t_to in [
                ('Monday',1,'Mathematics','07:00','07:50'),('Monday',2,'Life Sciences','07:50','08:40'),
                ('Monday',3,'Geography','09:00','09:50'),('Monday',4,'Mathematics','09:50','10:40'),
                ('Monday',5,'Life Sciences','10:40','11:30'),('Monday',6,'Geography','11:30','12:20'),
                ('Tuesday',1,'Geography','07:00','07:50'),('Tuesday',2,'Mathematics','07:50','08:40'),
                ('Tuesday',3,'Life Sciences','09:00','09:50'),('Tuesday',4,'Geography','09:50','10:40'),
                ('Tuesday',5,'Mathematics','10:40','11:30'),('Tuesday',6,'Life Sciences','11:30','12:20'),
                ('Wednesday',1,'Mathematics','07:00','07:50'),('Wednesday',2,'Geography','07:50','08:40'),
                ('Wednesday',3,'Life Sciences','09:00','09:50'),('Wednesday',4,'Mathematics','09:50','10:40'),
                ('Wednesday',5,'Geography','10:40','11:30'),('Wednesday',6,'Life Sciences','11:30','12:20'),
                ('Thursday',1,'Life Sciences','07:00','07:50'),('Thursday',2,'Mathematics','07:50','08:40'),
                ('Thursday',3,'Geography','09:00','09:50'),('Thursday',4,'Life Sciences','09:50','10:40'),
                ('Thursday',5,'Mathematics','10:40','11:30'),('Thursday',6,'Geography','11:30','12:20'),
                ('Friday',1,'Mathematics','07:00','07:50'),('Friday',2,'Life Sciences','07:50','08:40'),
                ('Friday',3,'Geography','09:00','09:50'),('Friday',4,'Mathematics','09:50','10:40'),
                ('Friday',5,'Life Sciences','10:40','11:30'),('Friday',6,'Geography','11:30','12:20'),
            ]:
                cur.execute(f"""
                    INSERT INTO timetable_slots (student_id,day,period,subject,time_from,time_to)
                    VALUES ({PH},{PH},{PH},{PH},{PH},{PH})
                """, ('ASI001',day,period,subject,t_from,t_to))
            conn.commit()

        print("Database initialized successfully")
        release_connection(conn)

    def execute_query(self, query, params=None):
        conn   = get_connection()
        result = qexec(conn, query, params)
        conn.commit()
        release_connection(conn)
        return result

    def get_next_student_id(self):
        row    = self.execute_query("SELECT MAX(id) as max_id FROM students").fetchone()
        max_id = row['max_id'] if (row and row['max_id']) else 0
        return f"CD{(max_id + 1):03d}"

    def close(self):
        pass  # no-op: connections are per-operation


class StudentManager:
    def __init__(self, db: ClassDoodleDB):
        self.db = db

    def add_student(self, name, email, phone=None, parent_name=None,
                    parent_phone=None, parent_email=None, subjects=None, notes=None):
        student_id        = self.db.get_next_student_id()
        registration_date = date.today().isoformat()
        try:
            self.db.execute_query(f"""
                INSERT INTO students
                  (student_id, name, email, phone, parent_name, parent_phone,
                   parent_email, registration_date, notes)
                VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})
            """, (student_id, name, email, phone, parent_name, parent_phone,
                  parent_email, registration_date, notes))
            if subjects:
                for subject in subjects:
                    self.db.execute_query(
                        f"INSERT INTO student_subjects (student_id,subject) VALUES ({PH},{PH})",
                        (student_id, subject.strip()))
            return student_id
        except Exception as e:
            print(f"Error adding student: {e}")
            return None

    def get_student(self, student_id):
        result  = self.db.execute_query(
            f"SELECT * FROM students WHERE student_id = {PH}", (student_id,))
        student = result.fetchone()
        if student:
            subj_result = self.db.execute_query(
                f"SELECT subject FROM student_subjects WHERE student_id = {PH}", (student_id,))
            return dict(student), [r['subject'] for r in subj_result.fetchall()]
        return None, None

    def get_all_students(self, status='active'):
        if status:
            result = self.db.execute_query(
                f"SELECT * FROM students WHERE status = {PH} ORDER BY name", (status,))
        else:
            result = self.db.execute_query("SELECT * FROM students ORDER BY name")
        students = []
        for row in result.fetchall():
            student = dict(row)
            subj_result = self.db.execute_query(
                f"SELECT subject FROM student_subjects WHERE student_id = {PH}",
                (student['student_id'],))
            student['subjects'] = [r['subject'] for r in subj_result.fetchall()]
            students.append(student)
        return students

    def update_student(self, student_id, **kwargs):
        allowed = ['name','email','phone','parent_name','parent_phone','parent_email','status','notes']
        updates, values = [], []
        for field, value in kwargs.items():
            if field in allowed and value is not None:
                updates.append(f"{field} = {PH}"); values.append(value)
        if not updates:
            return False
        values.append(student_id)
        self.db.execute_query(
            f"UPDATE students SET {', '.join(updates)} WHERE student_id = {PH}", tuple(values))
        return True

    def bulk_import(self, students_data):
        imported, failed = [], []
        for student in students_data:
            try:
                sid = self.add_student(
                    name=student['name'], email=student['email'],
                    phone=student.get('phone'), parent_name=student.get('parent_name'),
                    parent_phone=student.get('parent_phone'), parent_email=student.get('parent_email'),
                    subjects=student.get('subjects', []), notes=student.get('notes'))
                (imported if sid else failed).append(sid or student['email'])
            except Exception as e:
                failed.append(f"{student['email']}: {e}")
        return imported, failed


class AttendanceManager:
    def __init__(self, db: ClassDoodleDB):
        self.db = db

    def mark_attendance(self, student_ids, date_str, time_slot, subject, status='present'):
        if POSTGRES:
            sql = f"""INSERT INTO attendance (student_id,date,time_slot,subject,status)
                      VALUES ({PH},{PH},{PH},{PH},{PH})
                      ON CONFLICT (student_id,date,time_slot,subject)
                      DO UPDATE SET status=EXCLUDED.status, marked_at=NOW()"""
        else:
            sql = f"""INSERT OR REPLACE INTO attendance (student_id,date,time_slot,subject,status)
                      VALUES ({PH},{PH},{PH},{PH},{PH})"""
        marked = 0
        for sid in student_ids:
            try:
                self.db.execute_query(sql, (sid, date_str, time_slot, subject, status))
                marked += 1
            except Exception as e:
                print(f"Attendance error for {sid}: {e}")
        return marked

    def get_attendance(self, date_str=None, student_id=None, subject=None):
        query, params = "SELECT * FROM attendance WHERE 1=1", []
        if date_str:   query += f" AND date = {PH}";       params.append(date_str)
        if student_id: query += f" AND student_id = {PH}"; params.append(student_id)
        if subject:    query += f" AND subject = {PH}";    params.append(subject)
        query += " ORDER BY date DESC, time_slot"
        return self.db.execute_query(query, tuple(params) if params else None).fetchall()

    def get_attendance_rate(self, student_id, start_date=None, end_date=None):
        query  = f"SELECT COUNT(*) as total, SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) as present FROM attendance WHERE student_id={PH}"
        params = [student_id]
        if start_date: query += f" AND date >= {PH}"; params.append(start_date)
        if end_date:   query += f" AND date <= {PH}"; params.append(end_date)
        result = self.db.execute_query(query, tuple(params)).fetchone()
        if result and result['total']:
            return (result['present'] / result['total']) * 100
        return 0.0


class AssessmentManager:
    def __init__(self, db: ClassDoodleDB):
        self.db = db

    def add_assessment(self, student_id, subject, assessment_type, score,
                       max_score=100, date_str=None, notes=None):
        if date_str is None:
            date_str = date.today().isoformat()
        self.db.execute_query(f"""
            INSERT INTO assessments (student_id,subject,assessment_type,score,max_score,date,notes)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH})
        """, (student_id, subject, assessment_type, score, max_score, date_str, notes))
        return True

    def get_assessments(self, student_id=None, subject=None):
        query, params = "SELECT * FROM assessments WHERE 1=1", []
        if student_id: query += f" AND student_id = {PH}"; params.append(student_id)
        if subject:    query += f" AND subject = {PH}";    params.append(subject)
        query += " ORDER BY date DESC"
        return self.db.execute_query(query, tuple(params) if params else None).fetchall()

    def get_student_average(self, student_id, subject=None):
        query  = f"SELECT AVG((score/max_score)*100) as average FROM assessments WHERE student_id={PH}"
        params = [student_id]
        if subject: query += f" AND subject={PH}"; params.append(subject)
        result = self.db.execute_query(query, tuple(params)).fetchone()
        return result['average'] if (result and result['average']) else 0.0

    def bulk_add_assessments(self, assessments_data):
        added = 0
        for a in assessments_data:
            try:
                self.add_assessment(student_id=a['student_id'], subject=a['subject'],
                    assessment_type=a['assessment_type'], score=a['score'],
                    max_score=a.get('max_score', 100), date_str=a.get('date'), notes=a.get('notes'))
                added += 1
            except Exception as e:
                print(f"Assessment error: {e}")
        return added


class PaymentManager:
    def __init__(self, db: ClassDoodleDB):
        self.db = db

    def record_payment(self, student_id, amount, payment_date, month_for,
                       payment_method=None, reference=None, notes=None):
        self.db.execute_query(f"""
            INSERT INTO payments (student_id,amount,payment_date,month_for,payment_method,reference,status,notes)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH},'paid',{PH})
        """, (student_id, amount, payment_date, month_for, payment_method, reference, notes))
        return True

    def get_payments(self, student_id=None, month_for=None, status=None):
        query, params = "SELECT * FROM payments WHERE 1=1", []
        if student_id: query += f" AND student_id={PH}"; params.append(student_id)
        if month_for:  query += f" AND month_for={PH}";  params.append(month_for)
        if status:     query += f" AND status={PH}";     params.append(status)
        query += " ORDER BY payment_date DESC"
        return self.db.execute_query(query, tuple(params) if params else None).fetchall()

    def get_outstanding_payments(self, month_for):
        return self.db.execute_query(f"""
            SELECT s.student_id, s.name, s.email, s.parent_phone FROM students s
            WHERE s.status='active' AND s.student_id NOT IN (
                SELECT student_id FROM payments WHERE month_for={PH} AND status='paid')
        """, (month_for,)).fetchall()

    def get_revenue_report(self, start_date=None, end_date=None):
        query  = f"SELECT COUNT(*) as payment_count, SUM(amount) as total_revenue, AVG(amount) as avg_payment FROM payments WHERE status='paid'"
        params = []
        if start_date: query += f" AND payment_date>={PH}"; params.append(start_date)
        if end_date:   query += f" AND payment_date<={PH}"; params.append(end_date)
        return self.db.execute_query(query, tuple(params) if params else None).fetchone() or {}
