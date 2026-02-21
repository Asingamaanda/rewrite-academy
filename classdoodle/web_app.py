"""
ClassDoodle Web Dashboard
Role-based access: admin (teacher) + student login
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from pathlib import Path
import os

from backend.db_adapter import get_connection, release_connection, qexec, PH
from backend.api import ClassDoodleAPI
from backend import automation
from backend.mailer import send_application_email, send_whatsapp_notification
from timetable_generator import generate_daily_timetable, WEEKLY_SCHEDULE, CORE_SUBJECTS

app = Flask(__name__)
_secret = os.environ.get('SECRET_KEY')
if not _secret:
    import sys as _sys
    if os.environ.get('RENDER') or os.environ.get('PRODUCTION'):
        print('FATAL: SECRET_KEY env var is not set. Refusing to start.', file=_sys.stderr)
        _sys.exit(1)
    # Local dev only — deterministic fallback, never used in production.
    _secret = 'classdoodle-dev-only-2026'
app.secret_key = _secret

# File upload config
UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'uploads' / 'manlib'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

CONTENT_UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'uploads' / 'subject_content'
CONTENT_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
CONTENT_ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

# Custom Jinja filter
@app.template_filter('format_number')
def format_number(value):
    try:
        return f"{float(value):,.2f}"
    except:
        return value

# schema is handled entirely by ClassDoodleDB.initialize_database() via db_adapter
api = ClassDoodleAPI()


# ==================== AUTH HELPERS ====================

def get_db():
    return get_connection()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_role' not in session:
            flash('Please log in to continue.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'admin':
            flash('Access denied. Teacher login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def student_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') != 'student':
            flash('Access denied. Please log in as a student.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def teacher_required(f):
    """Allows both admin and teacher roles."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user_role') not in ('admin', 'teacher'):
            flash('Access denied. Teacher login required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def youtube_embed(url):
    """Convert YouTube URL to embed URL"""
    if not url:
        return ''
    if 'youtu.be/' in url:
        vid = url.split('youtu.be/')[1].split('?')[0]
        return f'https://www.youtube.com/embed/{vid}'
    if 'v=' in url:
        vid = url.split('v=')[1].split('&')[0]
        return f'https://www.youtube.com/embed/{vid}'
    if 'youtube.com/embed' in url:
        return url
    return url


# ==================== LOGIN / LOGOUT ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_role' in session:
        if session['user_role'] == 'admin':
            return redirect(url_for('dashboard'))
        return redirect(url_for('student_home'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        conn = get_db()
        user = qexec(conn, f"SELECT * FROM user_accounts WHERE username={PH}", (username,)).fetchone()
        release_connection(conn)

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_role'] = user['role']
            session['username'] = user['username']
            if user['role'] == 'student':
                session['student_id'] = user['student_id']
                return redirect(url_for('student_home'))
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/health')
def health():
    return 'OK', 200


# ==================== PUBLIC LANDING PAGE ====================

@app.route('/')
def landing():
    role = session.get('user_role', '')
    if role == 'admin':
        portal_url = url_for('dashboard')
    elif role == 'student':
        portal_url = url_for('student_home')
    else:
        portal_url = url_for('login')
    return render_template('landing.html', user_role=role, portal_url=portal_url)


# ==================== PUBLIC APPLICATION FORM ====================

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'GET':
        return render_template('apply.html', submitted=False)

    # POST — save + email
    full_name      = request.form.get('full_name', '').strip()
    phone          = request.form.get('phone', '').strip()
    email          = request.form.get('email', '').strip()
    parent_name    = request.form.get('parent_name', '').strip()
    parent_phone   = request.form.get('parent_phone', '').strip()
    subjects_list  = request.form.getlist('subjects')
    previous_school = request.form.get('previous_school', '').strip()
    year_failed    = request.form.get('year_failed', '').strip()
    message        = request.form.get('message', '').strip()

    if not full_name or not phone or not subjects_list:
        flash('Please fill in your name, phone number, and select at least one subject.', 'error')
        return render_template('apply.html', submitted=False)

    subjects_str = ', '.join(subjects_list)

    # Save to DB
    try:
        conn = get_db()
        qexec(conn, f"""
            INSERT INTO applications
              (full_name, phone, email, parent_name, parent_phone,
               subjects, previous_school, year_failed, message)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})
        """, (full_name, phone, email, parent_name, parent_phone,
               subjects_str, previous_school, year_failed, message))
        conn.commit()
        release_connection(conn)
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('apply.html', submitted=False)

    # Send email (non-blocking — silently log failure, don't break UX)
    application_data = dict(
        full_name=full_name, phone=phone, email=email,
        parent_name=parent_name, parent_phone=parent_phone,
        subjects=subjects_list, previous_school=previous_school,
        year_failed=year_failed, message=message
    )
    ok, err = send_application_email(application_data)
    if not ok:
        app.logger.warning(f'Email send failed: {err}')

    wa_ok, wa_err = send_whatsapp_notification(application_data)
    if not wa_ok:
        app.logger.warning(f'WhatsApp notification failed: {wa_err}')

    return render_template('apply.html', submitted=True, app_name=full_name)


# ==================== ADMIN DASHBOARD ====================

@app.route('/dashboard')
@admin_required
def dashboard():
    today = date.today()
    day_name = today.strftime("%A")
    stats = api.get_dashboard_stats()
    schedule = generate_daily_timetable(day_name) if day_name not in ["Saturday", "Sunday"] else []
    current_month = today.strftime('%Y-%m')
    payment_status = api.get_payment_status(current_month)
    class_summary = api.get_class_performance_summary()
    at_risk_students = [s for s in class_summary['students'] if s['risk_level'] == 'high'][:5]
    return render_template('dashboard.html',
                         today=today.strftime('%A, %d %B %Y'),
                         schedule=schedule, stats=stats,
                         payment_status=payment_status,
                         at_risk_students=at_risk_students,
                         day_name=day_name)


# ==================== STUDENTS (ADMIN) ====================

@app.route('/students')
@admin_required
def students():
    search = request.args.get('search', '').strip()
    risk_filter = request.args.get('risk', '')
    payment_filter = request.args.get('payment', '')
    subject_filter = request.args.get('subject', '')
    all_students = api.get_all_students_summary()
    filtered_students = all_students

    if search:
        sl = search.lower()
        filtered_students = [s for s in filtered_students if sl in s['name'].lower() or sl in s['student_id'].lower()]
    if risk_filter:
        filtered_students = [s for s in filtered_students if s.get('risk_level') == risk_filter]
    if subject_filter:
        filtered_students = [s for s in filtered_students if subject_filter in s.get('subjects', [])]
    if payment_filter:
        current_month = date.today().strftime('%Y-%m')
        payment_data = api.get_payment_status(current_month)
        if payment_filter == 'paid':
            paid_ids = {s['student_id'] for s in payment_data['paid']}
            filtered_students = [s for s in filtered_students if s['student_id'] in paid_ids]
        elif payment_filter == 'outstanding':
            out_ids = {s['student_id'] for s in payment_data['outstanding']}
            filtered_students = [s for s in filtered_students if s['student_id'] in out_ids]

    return render_template('students.html', students=filtered_students,
                         total_count=len(all_students), filtered_count=len(filtered_students),
                         subjects=CORE_SUBJECTS,
                         filters={'search': search, 'risk': risk_filter, 'payment': payment_filter, 'subject': subject_filter})


@app.route('/student/<student_id>')
@admin_required
def student_detail(student_id):
    student = api.get_student_info(student_id)
    if not student:
        flash(f"Student {student_id} not found", "error")
        return redirect(url_for('students'))
    performance = api.get_student_performance(student_id)
    attendance_history = api.get_student_attendance_history(student_id, limit=30)
    payments = api.payments.get_payments(student_id)[-6:]
    recent_assessments = []
    for subject in student['subjects']:
        for a in api.assessments.get_assessments(student_id, subject)[-5:]:
            recent_assessments.append({
                'subject': subject, 'type': a['assessment_type'], 'score': a['score'],
                'max_score': a['max_score'], 'percentage': round((a['score'] / a['max_score']) * 100, 1),
                'date': a['date']
            })
    recent_assessments.sort(key=lambda x: x['date'], reverse=True)
    return render_template('student_detail.html', student=student, performance=performance,
                         attendance=attendance_history, payments=payments, assessments=recent_assessments[:10])


@app.route('/student/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    if request.method == 'POST':
        try:
            student_id = api.register_student(
                name=request.form.get('name'), email=request.form.get('email'),
                phone=request.form.get('phone'), parent_name=request.form.get('parent_name'),
                parent_phone=request.form.get('parent_phone'), parent_email=request.form.get('parent_email'),
                subjects=request.form.getlist('subjects'), notes=request.form.get('notes', '')
            )
            flash(f"Student registered: {student_id}", "success")
            return redirect(url_for('student_detail', student_id=student_id))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    return render_template('add_student.html', subjects=CORE_SUBJECTS)


# ==================== ATTENDANCE (ADMIN) ====================

@app.route('/attendance')
@admin_required
def attendance():
    today = date.today()
    selected_date = request.args.get('date', today.isoformat())
    all_students = api.students.get_all_students(status='active')
    attendance_report = api.get_daily_attendance_report(selected_date)
    day_name = datetime.fromisoformat(selected_date).strftime("%A")
    schedule = generate_daily_timetable(day_name) if day_name not in ["Saturday", "Sunday"] else []
    return render_template('attendance.html', students=all_students, schedule=schedule,
                         selected_date=selected_date, attendance_report=attendance_report, subjects=CORE_SUBJECTS)


@app.route('/attendance/mark', methods=['POST'])
@admin_required
def mark_attendance():
    try:
        present_ids = request.form.getlist('present[]')
        result = api.mark_class_attendance(
            present_student_ids=present_ids,
            date_str=request.form.get('date'),
            time_slot=request.form.get('time_slot'),
            subject=request.form.get('subject')
        )
        # Automation Rule 2 — attendance risk check for every student marked
        all_ids = request.form.getlist('all_student_ids[]') or present_ids
        for sid in all_ids:
            try:
                automation.run_for_student(sid)
            except Exception:
                pass
        flash(f"Attendance marked: {result['present']} present, {result['absent']} absent", "success")
        return redirect(url_for('attendance', date=request.form.get('date')))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('attendance'))


# ==================== ASSESSMENTS (ADMIN) ====================

@app.route('/assessments')
@admin_required
def assessments():
    subject_filter = request.args.get('subject', '')
    class_summary = api.get_class_performance_summary()
    all_students = api.students.get_all_students(status='active')
    recent_assessments = []
    for student in all_students:
        subjects_to_check = [subject_filter] if subject_filter else student['subjects']
        for subject in subjects_to_check:
            for a in api.assessments.get_assessments(student['student_id'], subject)[-3:]:
                recent_assessments.append({
                    'student_id': student['student_id'], 'student_name': student['name'],
                    'subject': subject, 'type': a['assessment_type'], 'score': a['score'],
                    'max_score': a['max_score'], 'percentage': round((a['score'] / a['max_score']) * 100, 1),
                    'date': a['date']
                })
    recent_assessments.sort(key=lambda x: x['date'], reverse=True)
    return render_template('assessments.html', assessments=recent_assessments[:50],
                         class_summary=class_summary, subjects=CORE_SUBJECTS, subject_filter=subject_filter)


@app.route('/assessment/add', methods=['POST'])
@admin_required
def add_assessment():
    try:
        student_id = request.form.get('student_id')
        score = float(request.form.get('score'))
        max_score = float(request.form.get('max_score', 100))
        weight = float(request.form.get('weight', 1))
        api.record_assessment(
            student_id=student_id, subject=request.form.get('subject'),
            assessment_type=request.form.get('assessment_type'), score=score, max_score=max_score,
            date_str=request.form.get('date', date.today().isoformat()), notes=request.form.get('notes', '')
        )
        # Store weight on the just-inserted row
        try:
            conn = get_db()
            qexec(conn,
                f"UPDATE assessments SET weight={PH} WHERE student_id={PH} AND id=("
                f"SELECT MAX(id) FROM assessments WHERE student_id={PH})",
                (weight, student_id, student_id))
            conn.commit()
            release_connection(conn)
        except Exception:
            pass
        # Automation Rule 1 — academic risk check
        try:
            automation.run_for_student(student_id)
        except Exception:
            pass
        flash(f"Assessment recorded: {round((score/max_score)*100, 1)}%", "success")
        return redirect(url_for('student_detail', student_id=student_id) if request.form.get('from') == 'student' else url_for('assessments'))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('assessments'))


# ==================== PAYMENTS (ADMIN) ====================

@app.route('/payments')
@admin_required
def payments():
    selected_month = request.args.get('month', date.today().strftime('%Y-%m'))
    payment_status = api.get_payment_status(selected_month)
    revenue_summary = api.get_revenue_summary()
    return render_template('payments.html', payment_status=payment_status,
                         revenue_summary=revenue_summary, selected_month=selected_month)


@app.route('/payment/record', methods=['POST'])
@admin_required
def record_payment():
    try:
        student_id = request.form.get('student_id')
        amount = float(request.form.get('amount'))
        month_for = request.form.get('month_for')
        api.record_payment(student_id=student_id, amount=amount, month_for=month_for,
                         payment_method=request.form.get('payment_method', 'Cash'),
                         reference=request.form.get('reference', ''))
        # Automation Rule 3 — payment risk check
        try:
            automation.run_for_student(student_id)
        except Exception:
            pass
        flash(f"Payment recorded: R{amount:,.2f} for {month_for}", "success")
        return redirect(url_for('student_detail', student_id=student_id) if request.form.get('from') == 'student' else url_for('payments', month=month_for))
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('payments'))


# ==================== AUTOMATION ENGINE ====================

@app.route('/admin/run-automation', methods=['POST'])
@admin_required
def run_automation():
    """Manually trigger the full automation engine across all students."""
    try:
        results = automation.run_all()
        counts = {'critical': 0, 'needs_support': 0, 'at_risk': 0, 'restricted': 0}
        for sid, r in results.items():
            if r.get('academic') and r['academic'].get('risk') in ('critical', 'needs_support'):
                counts[r['academic']['risk']] += 1
            if r.get('attendance') and r['attendance'].get('at_risk'):
                counts['at_risk'] += 1
            if r.get('payment') and r['payment'].get('status') == 'restricted':
                counts['restricted'] += 1
        flash(
            f"Automation complete — {len(results)} students checked. "
            f"{counts['critical']} critical, {counts['needs_support']} need support, "
            f"{counts['at_risk']} attendance warnings, {counts['restricted']} restricted.",
            'success'
        )
    except Exception as e:
        flash(f"Automation error: {str(e)}", 'error')
    return redirect(url_for('risk_alerts'))


@app.route('/admin/risk-alerts')
@admin_required
def risk_alerts():
    """Risk and alerts dashboard."""
    summary = automation.get_risk_summary()
    all_students = api.get_all_students_summary()
    return render_template('risk_alerts.html', summary=summary, students=all_students)


@app.route('/admin/risk-alerts/resolve/<int:alert_id>', methods=['POST'])
@admin_required
def resolve_alert(alert_id):
    automation.resolve_alert(alert_id)
    flash('Alert resolved.', 'success')
    return redirect(url_for('risk_alerts'))


# ==================== APPLICATIONS (ADMIN) ====================

@app.route('/admin/applications')
@admin_required
def admin_applications():
    status_filter = request.args.get('status', '')
    conn = get_db()
    if status_filter:
        apps = qexec(conn,
            f"SELECT * FROM applications WHERE status={PH} ORDER BY created_at DESC",
            (status_filter,)).fetchall()
    else:
        apps = qexec(conn,
            "SELECT * FROM applications ORDER BY created_at DESC").fetchall()
    new_count   = qexec(conn, "SELECT COUNT(*) as cnt FROM applications WHERE status='new'").fetchone()['cnt']
    total_count = qexec(conn, "SELECT COUNT(*) as cnt FROM applications").fetchone()['cnt']
    release_connection(conn)
    return render_template('admin_applications.html',
                           applications=[dict(a) for a in apps],
                           new_count=new_count, total_count=total_count,
                           status_filter=status_filter)


@app.route('/admin/applications/<int:app_id>/status', methods=['POST'])
@admin_required
def update_application_status(app_id):
    new_status = request.form.get('status', 'new')
    conn = get_db()
    qexec(conn, f"UPDATE applications SET status={PH} WHERE id={PH}", (new_status, app_id))
    conn.commit()
    release_connection(conn)
    flash(f'Application marked as {new_status}.', 'success')
    return redirect(url_for('admin_applications', status=request.args.get('status', '')))


# ==================== TIMETABLE (ADMIN) ====================

@app.route('/timetable')
@admin_required
def timetable():
    return render_template('timetable.html', weekly_schedule=WEEKLY_SCHEDULE, subjects=CORE_SUBJECTS)


# ==================== STUDENT ACCOUNTS (ADMIN) ====================

@app.route('/admin/student-accounts')
@admin_required
def student_accounts():
    """Manage student login credentials"""
    all_students = api.get_all_students_summary()
    conn = get_db()
    accounts = {row['student_id']: dict(row) for row in
                qexec(conn, "SELECT * FROM user_accounts WHERE role='student'").fetchall()}
    release_connection(conn)
    account_ids = set(accounts.keys())
    students_no_account = [s for s in all_students if s['student_id'] not in account_ids]
    return render_template('admin/student_accounts.html',
                         students=all_students, accounts=accounts,
                         students_no_account=students_no_account)


@app.route('/admin/student-accounts/create', methods=['POST'])
@admin_required
def create_student_account():
    """Create or update a student login"""
    student_id = request.form.get('student_id', '').strip()
    password = request.form.get('password', '').strip()
    if not student_id or not password:
        flash('Student ID and password are required.', 'error')
        return redirect(url_for('student_accounts'))

    student = api.get_student_info(student_id)
    if not student:
        flash(f'Student {student_id} not found.', 'error')
        return redirect(url_for('student_accounts'))

    conn = get_db()
    existing = qexec(conn,
        f"SELECT id FROM user_accounts WHERE username={PH}", (student_id,)).fetchone()
    if existing:
        qexec(conn,
            f"UPDATE user_accounts SET password_hash={PH} WHERE username={PH}",
            (generate_password_hash(password), student_id))
        conn.commit()
        flash(f"Password updated for {student['name']} ({student_id})", 'success')
    else:
        qexec(conn,
            f"INSERT INTO user_accounts (username, password_hash, role, student_id) VALUES ({PH},{PH},{PH},{PH})",
            (student_id, generate_password_hash(password), 'student', student_id))
        conn.commit()
        flash(f"Login created for {student['name']} -- Username: {student_id}", 'success')
    release_connection(conn)
    return redirect(url_for('student_accounts'))


@app.route('/admin/student-accounts/delete/<username>', methods=['POST'])
@admin_required
def delete_student_account(username):
    conn = get_db()
    qexec(conn, f"DELETE FROM user_accounts WHERE username={PH} AND role='student'", (username,))
    conn.commit()
    release_connection(conn)
    flash(f'Login removed for {username}', 'success')
    return redirect(url_for('student_accounts'))


# ==================== MANLIB VIDEOS (ADMIN) ====================

@app.route('/admin/manlib')
@admin_required
def admin_manlib():
    """Manage Manlib educational videos"""
    subject_filter = request.args.get('subject', '')
    conn = get_db()
    if subject_filter:
        videos = qexec(conn,
            f"SELECT * FROM manlib_videos WHERE subject={PH} ORDER BY subject, order_num, created_at",
            (subject_filter,)).fetchall()
    else:
        videos = qexec(conn,
            "SELECT * FROM manlib_videos ORDER BY subject, order_num, created_at").fetchall()
    release_connection(conn)

    # Group by subject
    grouped = {}
    for v in videos:
        subj = v['subject']
        if subj not in grouped:
            grouped[subj] = []
        grouped[subj].append(dict(v))

    return render_template('admin/manlib.html',
                         grouped=grouped, subjects=CORE_SUBJECTS,
                         subject_filter=subject_filter)


@app.route('/admin/manlib/add', methods=['POST'])
@admin_required
def add_manlib_video():
    """Add a video (YouTube link or file upload)"""
    subject = request.form.get('subject', '').strip()
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    video_type = request.form.get('video_type', 'youtube')
    duration = request.form.get('duration', '').strip()
    order_num = int(request.form.get('order_num', 0) or 0)

    if not subject or not title:
        flash('Subject and title are required.', 'error')
        return redirect(url_for('admin_manlib'))

    video_url = None
    file_path = None

    if video_type == 'youtube':
        raw_url = request.form.get('video_url', '').strip()
        if not raw_url:
            flash('YouTube URL is required.', 'error')
            return redirect(url_for('admin_manlib'))
        video_url = youtube_embed(raw_url)

    elif video_type == 'upload':
        if 'video_file' not in request.files or request.files['video_file'].filename == '':
            flash('Please select a video file to upload.', 'error')
            return redirect(url_for('admin_manlib'))
        f = request.files['video_file']
        if not allowed_file(f.filename):
            flash('Invalid file type. Allowed: mp4, webm, mov, avi, mkv', 'error')
            return redirect(url_for('admin_manlib'))
        safe_name = secure_filename(f.filename)
        subj_dir = UPLOAD_FOLDER / subject.replace(' ', '_')
        subj_dir.mkdir(parents=True, exist_ok=True)
        save_path = subj_dir / safe_name
        f.save(str(save_path))
        file_path = f'uploads/manlib/{subject.replace(" ", "_")}/{safe_name}'

    conn = get_db()
    qexec(conn,
        f"INSERT INTO manlib_videos (subject, title, description, video_type, video_url, file_path, duration, order_num) VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})",
        (subject, title, description, video_type, video_url, file_path, duration, order_num))
    conn.commit()
    release_connection(conn)

    flash(f'Video added: "{title}" [{subject}]', 'success')
    return redirect(url_for('admin_manlib', subject=subject))


@app.route('/admin/manlib/delete/<int:video_id>', methods=['POST'])
@admin_required
def delete_manlib_video(video_id):
    conn = get_db()
    video = qexec(conn, f"SELECT * FROM manlib_videos WHERE id={PH}", (video_id,)).fetchone()
    if video and video['file_path']:
        try:
            os.remove(str(Path(__file__).parent / 'static' / video['file_path']))
        except:
            pass
    qexec(conn, f"DELETE FROM manlib_videos WHERE id={PH}", (video_id,))
    conn.commit()
    release_connection(conn)
    flash('Video deleted.', 'success')
    return redirect(url_for('admin_manlib'))


# ==================== SUBJECT CONTENT (ADMIN) ====================

@app.route('/admin/subject-content')
@admin_required
def admin_subject_content():
    """Manage subject content: notes, question papers, critical work, exam prep"""
    subject_filter = request.args.get('subject', '')
    type_filter = request.args.get('content_type', '')
    conn = get_db()
    query = "SELECT * FROM subject_content WHERE 1=1"
    params = []
    if subject_filter:
        query += f" AND subject={PH}"; params.append(subject_filter)
    if type_filter:
        query += f" AND content_type={PH}"; params.append(type_filter)
    query += " ORDER BY subject, content_type, order_num, created_at"
    items = qexec(conn, query, params).fetchall()
    release_connection(conn)

    # Group by subject → content_type
    grouped = {}
    for item in items:
        s = item['subject']
        ct = item['content_type']
        grouped.setdefault(s, {}).setdefault(ct, []).append(dict(item))

    CONTENT_TYPES = [
        ('notes',          'Notes'),
        ('question_paper', 'Question Papers'),
        ('critical_work',  'Critical Work'),
        ('exam_prep',      'Exam Prep'),
    ]
    return render_template('admin/subject_content.html',
                           grouped=grouped, subjects=CORE_SUBJECTS,
                           content_types=CONTENT_TYPES,
                           subject_filter=subject_filter, type_filter=type_filter)


@app.route('/admin/subject-content/add', methods=['POST'])
@admin_required
def add_subject_content():
    subject      = request.form.get('subject', '').strip()
    content_type = request.form.get('content_type', '').strip()
    title        = request.form.get('title', '').strip()
    description  = request.form.get('description', '').strip()
    content_text = request.form.get('content_text', '').strip()
    link_url     = request.form.get('link_url', '').strip()
    order_num    = int(request.form.get('order_num', 0) or 0)

    if not subject or not content_type or not title:
        flash('Subject, type and title are required.', 'error')
        return redirect(url_for('admin_subject_content'))

    file_path = ''
    if 'content_file' in request.files and request.files['content_file'].filename:
        f = request.files['content_file']
        ext = f.filename.rsplit('.', 1)[-1].lower() if '.' in f.filename else ''
        if ext not in CONTENT_ALLOWED_EXTENSIONS:
            flash(f'File type .{ext} not allowed.', 'error')
            return redirect(url_for('admin_subject_content'))
        safe_name = secure_filename(f.filename)
        dest_dir = CONTENT_UPLOAD_FOLDER / subject.replace(' ', '_') / content_type
        dest_dir.mkdir(parents=True, exist_ok=True)
        save_path = dest_dir / safe_name
        f.save(str(save_path))
        file_path = f'uploads/subject_content/{subject.replace(" ", "_")}/{content_type}/{safe_name}'

    conn = get_db()
    qexec(conn,
        f"INSERT INTO subject_content (subject, content_type, title, description, content_text, file_path, link_url, order_num) VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})",
        (subject, content_type, title, description, content_text, file_path, link_url, order_num))
    conn.commit()
    release_connection(conn)
    flash(f'Content added: "{title}" [{subject} / {content_type}]', 'success')
    return redirect(url_for('admin_subject_content', subject=subject, content_type=content_type))


@app.route('/admin/subject-content/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_subject_content(item_id):
    conn = get_db()
    item = qexec(conn, f"SELECT * FROM subject_content WHERE id={PH}", (item_id,)).fetchone()
    if item and item['file_path']:
        try:
            os.remove(str(Path(__file__).parent / 'static' / item['file_path']))
        except:
            pass
    qexec(conn, f"DELETE FROM subject_content WHERE id={PH}", (item_id,))
    conn.commit()
    release_connection(conn)
    flash('Content deleted.', 'success')
    return redirect(url_for('admin_subject_content'))

@app.route('/admin/timetable/<student_id>', methods=['GET', 'POST'])
@admin_required
def admin_student_timetable(student_id):
    """Set a student's personal timetable"""
    student = api.get_student_info(student_id)
    if not student:
        flash(f'Student {student_id} not found.', 'error')
        return redirect(url_for('students'))

    conn = get_db()

    if request.method == 'POST':
        # Delete existing and replace
        qexec(conn, f"DELETE FROM timetable_slots WHERE student_id={PH}", (student_id,))
        days = request.form.getlist('day')
        periods = request.form.getlist('period')
        subjects_list = request.form.getlist('subject')
        time_froms = request.form.getlist('time_from')
        time_tos = request.form.getlist('time_to')
        rooms = request.form.getlist('room')
        teachers = request.form.getlist('teacher')
        for i in range(len(days)):
            if days[i] and subjects_list[i]:
                qexec(conn,
                    f"INSERT INTO timetable_slots (student_id, day, period, subject, time_from, time_to, room, teacher) VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})",
                    (student_id, days[i], int(periods[i] or i+1), subjects_list[i],
                     time_froms[i], time_tos[i], rooms[i] if i < len(rooms) else '',
                     teachers[i] if i < len(teachers) else ''))
        conn.commit()
        flash(f"Timetable saved for {student['name']}", 'success')
        release_connection(conn)
        return redirect(url_for('admin_student_timetable', student_id=student_id))

    slots = qexec(conn,
        f"SELECT * FROM timetable_slots WHERE student_id={PH} ORDER BY day, period", (student_id,)
    ).fetchall()
    release_connection(conn)

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    timetable_grid = {day: [] for day in DAYS}
    for slot in slots:
        timetable_grid[slot['day']].append(dict(slot))

    return render_template('admin/student_timetable.html',
                         student=student, timetable_grid=timetable_grid,
                         days=DAYS, subjects=CORE_SUBJECTS, slots=[dict(s) for s in slots])


# ==================== ADMIN: STUDENT PORTAL SELECTOR ====================

@app.route('/portal')
@admin_required
def student_portal():
    students = api.get_all_students_summary()
    return render_template('student_portal_select.html', students=students)


@app.route('/portal/<student_id>')
@admin_required
def student_homepage_admin(student_id):
    """Admin view of a student's portal page"""
    return _render_student_portal(student_id)


# ==================== STUDENT PORTAL (STUDENT LOGIN) ====================

@app.route('/my-portal')
@student_required
def student_home():
    """Student's personal home page after login"""
    student_id = session['student_id']
    restricted = automation.is_restricted(student_id)
    return _render_student_portal(student_id, payment_restricted=restricted)


@app.route('/my-portal/videos')
@student_required
def student_videos():
    """Student views Manlib videos for their subjects"""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return redirect(url_for('logout'))

    conn = get_db()
    # Only show videos for subjects this student is enrolled in
    placeholders = ','.join([PH] * len(student['subjects']))
    videos = qexec(conn,
        f"SELECT * FROM manlib_videos WHERE subject IN ({placeholders}) ORDER BY subject, order_num, created_at",
        student['subjects']
    ).fetchall() if student['subjects'] else []
    release_connection(conn)

    grouped = {}
    for v in videos:
        subj = v['subject']
        if subj not in grouped:
            grouped[subj] = []
        grouped[subj].append(dict(v))

    return render_template('student_videos.html', student=student, grouped=grouped,
                         today=date.today().strftime('%A, %d %B %Y'))


@app.route('/my-portal/subjects')
@student_required
def student_subjects():
    """Student subject hub — videos, notes, question papers, critical work, exam prep per subject"""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return redirect(url_for('logout'))

    subjects = student['subjects'] or []
    conn = get_db()

    # Videos per subject
    if subjects:
        placeholders = ','.join([PH] * len(subjects))
        videos = qexec(conn,
            f"SELECT * FROM manlib_videos WHERE subject IN ({placeholders}) ORDER BY subject, order_num, created_at",
            subjects
        ).fetchall()
    else:
        videos = []

    # All subject content for this student's subjects
    if subjects:
        placeholders = ','.join([PH] * len(subjects))
        content_rows = qexec(conn,
            f"SELECT * FROM subject_content WHERE subject IN ({placeholders}) ORDER BY subject, content_type, order_num, created_at",
            subjects
        ).fetchall()
    else:
        content_rows = []
    release_connection(conn)

    # Build hub: subject → { videos: [], notes: [], question_paper: [], critical_work: [], exam_prep: [] }
    hub = {}
    for s in subjects:
        hub[s] = {'videos': [], 'notes': [], 'question_paper': [], 'critical_work': [], 'exam_prep': []}
    for v in videos:
        if v['subject'] in hub:
            hub[v['subject']]['videos'].append(dict(v))
    for c in content_rows:
        if c['subject'] in hub and c['content_type'] in hub[c['subject']]:
            hub[c['subject']][c['content_type']].append(dict(c))

    CONTENT_LABELS = {
        'videos':        ('Videos',          '▶'),
        'notes':         ('Notes',           '📄'),
        'question_paper':('Question Papers', '📋'),
        'critical_work': ('Critical Work',   '⚡'),
        'exam_prep':     ('Exam Prep',       '🎯'),
    }
    return render_template('student_subjects.html',
                           student=student, hub=hub,
                           subjects=subjects,
                           content_labels=CONTENT_LABELS,
                           today=date.today().strftime('%A, %d %B %Y'))


@app.route('/my-portal/timetable')
@student_required
def student_timetable():
    """Student's personal timetable"""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return redirect(url_for('logout'))

    conn = get_db()
    slots = qexec(conn,
        f"SELECT * FROM timetable_slots WHERE student_id={PH} ORDER BY day, period", (student_id,)
    ).fetchall()
    release_connection(conn)

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    timetable_grid = {day: [] for day in DAYS}
    for slot in slots:
        timetable_grid[slot['day']].append(dict(slot))

    today_name = date.today().strftime('%A')
    today_slots = timetable_grid.get(today_name, [])

    return render_template('student_timetable.html', student=student,
                         timetable_grid=timetable_grid, days=DAYS,
                         today_name=today_name, today_slots=today_slots,
                         today=date.today().strftime('%A, %d %B %Y'))


@app.route('/my-portal/progress')
@student_required
def student_progress():
    """Student's private progress report"""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return redirect(url_for('logout'))

    performance = api.get_student_performance(student_id)
    attendance_history = api.get_student_attendance_history(student_id, limit=20)

    all_assessments = []
    for subject in student['subjects']:
        for a in api.assessments.get_assessments(student_id, subject):
            all_assessments.append({
                'subject': subject, 'type': a['assessment_type'],
                'score': a['score'], 'max_score': a['max_score'],
                'percentage': round((a['score'] / a['max_score']) * 100, 1),
                'date': a['date']
            })
    all_assessments.sort(key=lambda x: x['date'], reverse=True)

    return render_template('student_progress.html', student=student,
                         performance=performance, assessments=all_assessments,
                         attendance=attendance_history,
                         today=date.today().strftime('%A, %d %B %Y'))


# ==================== SHARED HELPER ====================

def _render_student_portal(student_id, payment_restricted=False):
    student = api.get_student_info(student_id)
    if not student:
        flash(f"Student {student_id} not found", "error")
        if session.get('user_role') == 'admin':
            return redirect(url_for('student_portal'))
        return redirect(url_for('logout'))

    performance = api.get_student_performance(student_id)
    recent_assessments = []
    for subject in student['subjects']:
        for a in api.assessments.get_assessments(student_id, subject)[-3:]:
            recent_assessments.append({
                'subject': subject, 'type': a['assessment_type'],
                'score': a['score'], 'max_score': a['max_score'],
                'percentage': round((a['score'] / a['max_score']) * 100, 1),
                'date': a['date']
            })
    recent_assessments.sort(key=lambda x: x['date'], reverse=True)

    today = date.today()
    day_name = today.strftime("%A")
    schedule = generate_daily_timetable(day_name) if day_name not in ["Saturday", "Sunday"] else []
    attendance_history = api.get_student_attendance_history(student_id, limit=10)

    # Get student's personal timetable
    conn = get_db()
    tmt_slots = qexec(conn,
        f"SELECT * FROM timetable_slots WHERE student_id={PH} AND day={PH} ORDER BY period",
        (student_id, day_name)
    ).fetchall()

    # Count unread manlib videos for student's subjects
    video_counts = {}
    if student['subjects']:
        placeholders = ','.join([PH] * len(student['subjects']))
        rows = qexec(conn,
            f"SELECT subject, COUNT(*) as cnt FROM manlib_videos WHERE subject IN ({placeholders}) GROUP BY subject",
            student['subjects']
        ).fetchall()
        video_counts = {r['subject']: r['cnt'] for r in rows}
    release_connection(conn)

    return render_template('student_homepage.html',
                         student=student, performance=performance,
                         assessments=recent_assessments[:5],
                         schedule=[dict(s) for s in tmt_slots] or schedule,
                         attendance=attendance_history,
                         video_counts=video_counts,
                         payment_restricted=payment_restricted,
                         today=today.strftime('%A, %d %B %Y'))


# ==================== API ====================

@app.route('/api/dashboard-stats')
@admin_required
def api_dashboard_stats():
    return jsonify(api.get_dashboard_stats())


# ==================== CLEANUP ====================

@app.teardown_appcontext
def cleanup(error=None):
    pass


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  CLASSDOODLE — Role-Based Dashboard")
    print("="*70)
    print("\n  Admin login : username=admin  password=Classdoodle@password")
    print("  Student login: username=<student_id>  password=set via admin panel")
    print("\n  Open: http://localhost:5000")
    print("="*70 + "\n")
    app.run(debug=True, port=5000, use_reloader=False)
