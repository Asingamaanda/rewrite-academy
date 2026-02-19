"""
ClassDoodle Backend - Database Models
SQLite database for managing students, attendance, assessments, and payments
"""

import sqlite3
from pathlib import Path
from datetime import datetime, date
import json

class ClassDoodleDB:
    """Main database manager for ClassDoodle"""
    
    def __init__(self, db_path="classdoodle/data/classdoodle.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.initialize_database()
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn
    
    def initialize_database(self):
        """Create all tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                parent_name TEXT,
                parent_phone TEXT,
                parent_email TEXT,
                registration_date DATE NOT NULL,
                status TEXT DEFAULT 'active',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Student subjects (many-to-many relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                UNIQUE(student_id, subject)
            )
        """)
        
        # Attendance table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                date DATE NOT NULL,
                time_slot TEXT NOT NULL,
                subject TEXT NOT NULL,
                status TEXT NOT NULL,
                marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                UNIQUE(student_id, date, time_slot, subject)
            )
        """)
        
        # Assessments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL DEFAULT 100,
                date DATE NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)
        
        # Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                amount REAL NOT NULL,
                payment_date DATE NOT NULL,
                payment_method TEXT,
                reference TEXT,
                month_for TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)
        
        # Marketing leads table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                source TEXT NOT NULL,
                status TEXT DEFAULT 'new',
                contacted_at TIMESTAMP,
                enrolled_at TIMESTAMP,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Lesson plans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lesson_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                subject TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                topic TEXT NOT NULL,
                objectives TEXT,
                materials TEXT,
                homework TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, subject, time_slot)
            )
        """)
        
        # System settings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # ==================== AUTH & PORTAL TABLES ====================

        # User accounts (admin + students)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin','student')),
                student_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Manlib educational videos per subject
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS manlib_videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                video_type TEXT NOT NULL CHECK(video_type IN ('youtube','upload')),
                video_url TEXT,
                file_path TEXT,
                thumbnail_url TEXT,
                duration TEXT,
                order_num INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Student personal timetable slots
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timetable_slots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT,
                day TEXT NOT NULL,
                period INTEGER NOT NULL,
                subject TEXT NOT NULL,
                time_from TEXT NOT NULL,
                time_to TEXT NOT NULL,
                room TEXT DEFAULT '',
                teacher TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Subject content library (notes, question papers, critical work, exam prep)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subject_content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                content_type TEXT NOT NULL CHECK(content_type IN ('notes','question_paper','critical_work','exam_prep')),
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                content_text TEXT DEFAULT '',
                file_path TEXT DEFAULT '',
                link_url TEXT DEFAULT '',
                order_num INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()

        # Seed default admin account if not exists
        from werkzeug.security import generate_password_hash
        existing = cursor.execute(
            "SELECT id FROM user_accounts WHERE username='admin'"
        ).fetchone()
        if not existing:
            cursor.execute(
                "INSERT INTO user_accounts (username, password_hash, role) VALUES (?,?,?)",
                ('admin', generate_password_hash('Classdoodle@password'), 'admin')
            )
            conn.commit()

        # Seed Asingamaanda Nefefe (ASI001) if not exists
        existing_student = cursor.execute(
            "SELECT id FROM students WHERE student_id='ASI001'"
        ).fetchone()
        if not existing_student:
            cursor.execute("""
                INSERT INTO students
                  (student_id, name, email, registration_date, status)
                VALUES ('ASI001','Asingamaanda Nefefe','asi001@rewriteacademy.local',
                        date('now'),'active')
            """)
            for subj in ('Mathematics', 'Life Sciences', 'Geography'):
                cursor.execute(
                    "INSERT INTO student_subjects (student_id, subject) VALUES (?,?)",
                    ('ASI001', subj)
                )
            cursor.execute(
                "INSERT INTO user_accounts (username, password_hash, role, student_id) VALUES (?,?,?,?)",
                ('ASI001', generate_password_hash('student123'), 'student', 'ASI001')
            )
            # Seed timetable slots for ASI001
            _slots = [
                ('Monday',    1, 'Mathematics',  '07:00', '07:50'),
                ('Monday',    2, 'Life Sciences', '07:50', '08:40'),
                ('Monday',    3, 'Geography',     '09:00', '09:50'),
                ('Monday',    4, 'Mathematics',   '09:50', '10:40'),
                ('Monday',    5, 'Life Sciences', '10:40', '11:30'),
                ('Monday',    6, 'Geography',     '11:30', '12:20'),
                ('Tuesday',   1, 'Geography',     '07:00', '07:50'),
                ('Tuesday',   2, 'Mathematics',   '07:50', '08:40'),
                ('Tuesday',   3, 'Life Sciences', '09:00', '09:50'),
                ('Tuesday',   4, 'Geography',     '09:50', '10:40'),
                ('Tuesday',   5, 'Mathematics',   '10:40', '11:30'),
                ('Tuesday',   6, 'Life Sciences', '11:30', '12:20'),
                ('Wednesday', 1, 'Mathematics',   '07:00', '07:50'),
                ('Wednesday', 2, 'Geography',     '07:50', '08:40'),
                ('Wednesday', 3, 'Life Sciences', '09:00', '09:50'),
                ('Wednesday', 4, 'Mathematics',   '09:50', '10:40'),
                ('Wednesday', 5, 'Geography',     '10:40', '11:30'),
                ('Wednesday', 6, 'Life Sciences', '11:30', '12:20'),
                ('Thursday',  1, 'Life Sciences', '07:00', '07:50'),
                ('Thursday',  2, 'Mathematics',   '07:50', '08:40'),
                ('Thursday',  3, 'Geography',     '09:00', '09:50'),
                ('Thursday',  4, 'Life Sciences', '09:50', '10:40'),
                ('Thursday',  5, 'Mathematics',   '10:40', '11:30'),
                ('Thursday',  6, 'Geography',     '11:30', '12:20'),
                ('Friday',    1, 'Mathematics',   '07:00', '07:50'),
                ('Friday',    2, 'Life Sciences', '07:50', '08:40'),
                ('Friday',    3, 'Geography',     '09:00', '09:50'),
                ('Friday',    4, 'Mathematics',   '09:50', '10:40'),
                ('Friday',    5, 'Life Sciences', '10:40', '11:30'),
                ('Friday',    6, 'Geography',     '11:30', '12:20'),
            ]
            for day, period, subject, t_from, t_to in _slots:
                cursor.execute("""
                    INSERT INTO timetable_slots
                      (student_id, day, period, subject, time_from, time_to)
                    VALUES (?,?,?,?,?,?)
                """, ('ASI001', day, period, subject, t_from, t_to))
            conn.commit()

        print("Database initialized successfully")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        return cursor
    
    def get_next_student_id(self):
        """Generate next student ID (CD001, CD002, etc.)"""
        cursor = self.execute_query("SELECT MAX(id) as max_id FROM students")
        result = cursor.fetchone()
        max_id = result['max_id'] if result['max_id'] else 0
        return f"CD{(max_id + 1):03d}"
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


class StudentManager:
    """Manage student operations"""
    
    def __init__(self, db: ClassDoodleDB):
        self.db = db
    
    def add_student(self, name, email, phone=None, parent_name=None, 
                   parent_phone=None, parent_email=None, subjects=None, notes=None):
        """Add a new student"""
        
        student_id = self.db.get_next_student_id()
        registration_date = date.today().isoformat()
        
        try:
            # Insert student
            self.db.execute_query("""
                INSERT INTO students 
                (student_id, name, email, phone, parent_name, parent_phone, 
                 parent_email, registration_date, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, email, phone, parent_name, parent_phone, 
                  parent_email, registration_date, notes))
            
            # Add subjects
            if subjects:
                for subject in subjects:
                    self.db.execute_query("""
                        INSERT INTO student_subjects (student_id, subject)
                        VALUES (?, ?)
                    """, (student_id, subject.strip()))
            
            return student_id
        
        except sqlite3.IntegrityError as e:
            print(f"❌ Error adding student: {e}")
            return None
    
    def get_student(self, student_id):
        """Get student details"""
        cursor = self.db.execute_query(
            "SELECT * FROM students WHERE student_id = ?", (student_id,)
        )
        student = cursor.fetchone()
        
        if student:
            # Get subjects
            cursor = self.db.execute_query(
                "SELECT subject FROM student_subjects WHERE student_id = ?",
                (student_id,)
            )
            subjects = [row['subject'] for row in cursor.fetchall()]
            
            return dict(student), subjects
        
        return None, None
    
    def get_all_students(self, status='active'):
        """Get all students"""
        if status:
            cursor = self.db.execute_query(
                "SELECT * FROM students WHERE status = ? ORDER BY name",
                (status,)
            )
        else:
            cursor = self.db.execute_query(
                "SELECT * FROM students ORDER BY name"
            )
        
        students = []
        for row in cursor.fetchall():
            student = dict(row)
            # Get subjects
            cursor2 = self.db.execute_query(
                "SELECT subject FROM student_subjects WHERE student_id = ?",
                (student['student_id'],)
            )
            student['subjects'] = [r['subject'] for r in cursor2.fetchall()]
            students.append(student)
        
        return students
    
    def update_student(self, student_id, **kwargs):
        """Update student information"""
        allowed_fields = ['name', 'email', 'phone', 'parent_name', 
                         'parent_phone', 'parent_email', 'status', 'notes']
        
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                updates.append(f"{field} = ?")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(student_id)
        query = f"UPDATE students SET {', '.join(updates)} WHERE student_id = ?"
        
        self.db.execute_query(query, tuple(values))
        return True
    
    def bulk_import(self, students_data):
        """Import multiple students at once"""
        imported = []
        failed = []
        
        for student in students_data:
            try:
                student_id = self.add_student(
                    name=student['name'],
                    email=student['email'],
                    phone=student.get('phone'),
                    parent_name=student.get('parent_name'),
                    parent_phone=student.get('parent_phone'),
                    parent_email=student.get('parent_email'),
                    subjects=student.get('subjects', []),
                    notes=student.get('notes')
                )
                
                if student_id:
                    imported.append(student_id)
                else:
                    failed.append(student['email'])
            
            except Exception as e:
                failed.append(f"{student['email']}: {str(e)}")
        
        return imported, failed


class AttendanceManager:
    """Manage attendance operations"""
    
    def __init__(self, db: ClassDoodleDB):
        self.db = db
    
    def mark_attendance(self, student_ids, date_str, time_slot, subject, status='present'):
        """Mark attendance for students"""
        
        marked = 0
        for student_id in student_ids:
            try:
                self.db.execute_query("""
                    INSERT OR REPLACE INTO attendance 
                    (student_id, date, time_slot, subject, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, date_str, time_slot, subject, status))
                marked += 1
            except Exception as e:
                print(f"❌ Error marking attendance for {student_id}: {e}")
        
        return marked
    
    def get_attendance(self, date_str=None, student_id=None, subject=None):
        """Get attendance records with filters"""
        
        query = "SELECT * FROM attendance WHERE 1=1"
        params = []
        
        if date_str:
            query += " AND date = ?"
            params.append(date_str)
        
        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        
        query += " ORDER BY date DESC, time_slot"
        
        cursor = self.db.execute_query(query, tuple(params) if params else None)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_attendance_rate(self, student_id, start_date=None, end_date=None):
        """Calculate attendance rate for a student"""
        
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) as present
            FROM attendance
            WHERE student_id = ?
        """
        params = [student_id]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        cursor = self.db.execute_query(query, tuple(params))
        result = cursor.fetchone()
        
        if result['total'] > 0:
            return (result['present'] / result['total']) * 100
        return 0.0


class AssessmentManager:
    """Manage assessments and grades"""
    
    def __init__(self, db: ClassDoodleDB):
        self.db = db
    
    def add_assessment(self, student_id, subject, assessment_type, score, 
                      max_score=100, date_str=None, notes=None):
        """Add an assessment record"""
        
        if date_str is None:
            date_str = date.today().isoformat()
        
        self.db.execute_query("""
            INSERT INTO assessments 
            (student_id, subject, assessment_type, score, max_score, date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_id, subject, assessment_type, score, max_score, date_str, notes))
        
        return True
    
    def get_assessments(self, student_id=None, subject=None):
        """Get assessment records"""
        
        query = "SELECT * FROM assessments WHERE 1=1"
        params = []
        
        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        
        query += " ORDER BY date DESC"
        
        cursor = self.db.execute_query(query, tuple(params) if params else None)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_student_average(self, student_id, subject=None):
        """Calculate average score for a student"""
        
        query = """
            SELECT AVG((score / max_score) * 100) as average
            FROM assessments
            WHERE student_id = ?
        """
        params = [student_id]
        
        if subject:
            query += " AND subject = ?"
            params.append(subject)
        
        cursor = self.db.execute_query(query, tuple(params))
        result = cursor.fetchone()
        
        return result['average'] if result['average'] else 0.0
    
    def bulk_add_assessments(self, assessments_data):
        """Import multiple assessment records"""
        
        added = 0
        for assessment in assessments_data:
            try:
                self.add_assessment(
                    student_id=assessment['student_id'],
                    subject=assessment['subject'],
                    assessment_type=assessment['assessment_type'],
                    score=assessment['score'],
                    max_score=assessment.get('max_score', 100),
                    date_str=assessment.get('date'),
                    notes=assessment.get('notes')
                )
                added += 1
            except Exception as e:
                print(f"❌ Error adding assessment: {e}")
        
        return added


class PaymentManager:
    """Manage payments and billing"""
    
    def __init__(self, db: ClassDoodleDB):
        self.db = db
    
    def record_payment(self, student_id, amount, payment_date, month_for,
                      payment_method=None, reference=None, notes=None):
        """Record a payment"""
        
        self.db.execute_query("""
            INSERT INTO payments 
            (student_id, amount, payment_date, month_for, payment_method, 
             reference, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, 'paid', ?)
        """, (student_id, amount, payment_date, month_for, payment_method, 
              reference, notes))
        
        return True
    
    def get_payments(self, student_id=None, month_for=None, status=None):
        """Get payment records"""
        
        query = "SELECT * FROM payments WHERE 1=1"
        params = []
        
        if student_id:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if month_for:
            query += " AND month_for = ?"
            params.append(month_for)
        
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY payment_date DESC"
        
        cursor = self.db.execute_query(query, tuple(params) if params else None)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_outstanding_payments(self, month_for):
        """Find students who haven't paid for a specific month"""
        
        cursor = self.db.execute_query("""
            SELECT s.student_id, s.name, s.email, s.parent_phone
            FROM students s
            WHERE s.status = 'active'
            AND s.student_id NOT IN (
                SELECT student_id FROM payments 
                WHERE month_for = ? AND status = 'paid'
            )
        """, (month_for,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_revenue_report(self, start_date=None, end_date=None):
        """Generate revenue report"""
        
        query = """
            SELECT 
                COUNT(*) as payment_count,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_payment
            FROM payments
            WHERE status = 'paid'
        """
        params = []
        
        if start_date:
            query += " AND payment_date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND payment_date <= ?"
            params.append(end_date)
        
        cursor = self.db.execute_query(query, tuple(params) if params else None)
        return dict(cursor.fetchone())


if __name__ == "__main__":
    # Initialize database
    db = ClassDoodleDB()
    
    print("\n" + "=" * 70)
    print("✅ ClassDoodle Backend Initialized")
    print("=" * 70)
    print("\nDatabase file:", db.db_path)
    print("\nTables created:")
    print("  • students")
    print("  • student_subjects")
    print("  • attendance")
    print("  • assessments")
    print("  • payments")
    print("  • leads")
    print("  • lesson_plans")
    print("  • settings")
    print("\n" + "=" * 70)
