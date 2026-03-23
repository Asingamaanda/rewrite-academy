"""
ClassDoodle Web Dashboard
Role-based access: admin (teacher) + student login
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session, Response
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, date, timedelta
from pathlib import Path
from io import BytesIO
from urllib.parse import quote_plus
import os
import secrets

from backend.db_adapter import get_connection, release_connection, qexec, PH, managed_connection
from backend.api import ClassDoodleAPI
from backend import automation, intelligence
from backend.mailer import send_application_email, send_whatsapp_notification
from timetable_generator import (generate_daily_timetable, WEEKLY_SCHEDULE,
                                 CORE_SUBJECTS, generate_smart_timetable,
                                 SUBJECT_DEFAULT_FREQS, PERIOD_TIMES, DAYS as TT_DAYS)
from backend.premium import premium_bp

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
app.config['SESSION_COOKIE_SECURE']   = bool(os.environ.get('RENDER'))   # HTTPS-only on Render
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True

# School branding
app.config['BRAND_NAME'] = os.environ.get('BRAND_NAME', 'Vele Secondary School')
app.config['BRAND_SHORT'] = os.environ.get('BRAND_SHORT', 'Vele Secondary')
app.config['BRAND_INITIAL'] = os.environ.get('BRAND_INITIAL', 'V')
app.config['BRAND_LOGO'] = os.environ.get('BRAND_LOGO', '/static/images/vele-logo.svg')
app.config['BRAND_ACCENT'] = os.environ.get('BRAND_ACCENT', '#800020')
app.config['BRAND_ACCENT_DARK'] = os.environ.get('BRAND_ACCENT_DARK', '#5a0016')
app.config['SITE_URL'] = os.environ.get('SITE_URL', '').rstrip('/')
app.config['SCHOOL_SCOPE'] = os.environ.get('SCHOOL_SCOPE', app.config['BRAND_NAME']).strip()
app.config['OFFLINE_MODE'] = os.environ.get('OFFLINE_MODE', '').strip().lower() in ('1', 'true', 'yes', 'on')

# File upload config
UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'uploads' / 'manlib'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'mov', 'avi', 'mkv'}
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)

# Register SEO blueprints
from backend.seo import seo_bp
from backend.seo_dashboard import seo_dashboard
app.register_blueprint(seo_bp)
app.register_blueprint(seo_dashboard)
app.register_blueprint(premium_bp)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

CONTENT_UPLOAD_FOLDER = Path(__file__).parent / 'static' / 'uploads' / 'subject_content'
CONTENT_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
CONTENT_ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'txt', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

TUTOR_MODEL = os.environ.get('ANTHROPIC_TUTOR_MODEL', 'claude-sonnet-4-20250514')
MAX_TUTOR_MESSAGES = 24
MAX_TUTOR_MESSAGE_CHARS = 4000
DEFAULT_TUTOR_SUBJECT = 'Mathematics'
TUTOR_SUBJECT_PROMPTS = {
    'Mathematics': (
        "You are a patient Matric Mathematics tutor for South African NSC rewrite students "
        "following CAPS. Explain Algebra, Functions, Calculus, Statistics, Trigonometry and "
        "Geometry with clear step-by-step working. Ask guiding questions before giving full "
        "solutions, and keep tone encouraging."
    ),
    'Physical Sciences': (
        "You are a Matric Physical Sciences tutor for South African NSC rewrite students "
        "following CAPS. Cover Physics and Chemistry topics with clear formula use, SI units, "
        "and step-by-step calculations. Build confidence while correcting mistakes clearly."
    ),
    'Life Sciences': (
        "You are a Matric Life Sciences tutor for South African NSC rewrite students following "
        "CAPS. Explain core concepts, help with diagrams, and support short and essay responses. "
        "Teach clearly and keep feedback encouraging."
    ),
    'English Home Language': (
        "You are a Matric English Home Language tutor for South African NSC rewrite students. "
        "Help with comprehension, language, essay structure, literature analysis, and argument "
        "quality. Give practical writing feedback and examples."
    ),
    'Accounting': (
        "You are a Matric Accounting tutor for South African NSC rewrite students following CAPS. "
        "Teach Financial Statements, reconciliations, cash flow, budgets, cost accounting, and "
        "ethics. Show methodical workings and explain double-entry logic."
    ),
    'Business Studies': (
        "You are a Matric Business Studies tutor for South African NSC rewrite students. "
        "Cover ownership, business environments, functions, leadership, ethics, and "
        "entrepreneurship. Help students structure exam-ready long answers."
    ),
    'Geography': (
        "You are a Matric Geography tutor for South African NSC rewrite students following CAPS. "
        "Teach physical and human geography, mapwork, and data interpretation with local context. "
        "Guide concise, structured responses for exam questions."
    ),
    'History': (
        "You are a Matric History tutor for South African NSC rewrite students following CAPS. "
        "Support source-based questions and essay writing with argument, evidence, and causation. "
        "Coach exam technique and clarity."
    ),
}
GRADE_LEVELS = [f"Grade {grade}" for grade in range(8, 13)]

# Custom Jinja filter
@app.template_filter('format_number')
def format_number(value):
    try:
        return f"{float(value):,.2f}"
    except:
        return value


@app.context_processor
def inject_branding():
    site_url = _resolve_site_url()
    return {
        'brand_name': app.config.get('BRAND_NAME', 'Vele Secondary School'),
        'brand_short': app.config.get('BRAND_SHORT', 'Vele Secondary'),
        'brand_initial': app.config.get('BRAND_INITIAL', 'V'),
        'brand_logo': app.config.get('BRAND_LOGO', '/static/images/vele-logo.svg'),
        'brand_accent': app.config.get('BRAND_ACCENT', '#800020'),
        'brand_accent_dark': app.config.get('BRAND_ACCENT_DARK', '#5a0016'),
        'site_url': site_url,
    }


def _resolve_site_url():
    site_url = app.config.get('SITE_URL', '').rstrip('/')
    if not site_url:
        site_url = request.url_root.rstrip('/')
    return site_url


def _public_apply_url():
    return f"{_resolve_site_url()}/apply"


def _is_offline_mode():
    return bool(app.config.get('OFFLINE_MODE'))

# schema is handled entirely by ClassDoodleDB.initialize_database() via db_adapter
api = ClassDoodleAPI()   # DB init is fault-tolerant; retried on first request if DB not ready


# ==================== STARTUP RETRY ====================

@app.before_request
def _ensure_db():
    """If the DB wasn't ready at startup, retry on each request until it is."""
    try:
        api.db.ensure_initialized()
    except Exception as e:
        # Still not ready — log and let Flask serve the request.
        # Routes that actually need the DB will fail gracefully.
        print(f"DB not ready yet: {e}")


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


def _admin_school_scope():
    return (app.config.get('SCHOOL_SCOPE') or app.config.get('BRAND_NAME') or '').strip()


def _student_in_scope(student, school_name=None):
    if not student:
        return False
    scope = (school_name or _admin_school_scope()).strip()
    if not scope:
        return True
    return (student.get('school_name') or '').strip().lower() == scope.lower()


def _get_scoped_student(student_id):
    student = api.get_student_info(student_id)
    if not student:
        return None
    return student if _student_in_scope(student) else None


def _student_school_scope(student, fallback=None):
    if student and (student.get('school_name') or '').strip():
        return student['school_name'].strip()
    if fallback:
        return fallback.strip()
    return _admin_school_scope()


def _assessment_row_to_card(row):
    max_score = row.get('max_score') or 0
    percentage = round((row['score'] / max_score) * 100, 1) if max_score else 0
    return {
        'subject': row['subject'],
        'type': row['assessment_type'],
        'score': row['score'],
        'max_score': row['max_score'],
        'percentage': percentage,
        'date': row['date'],
    }


def _recent_assessment_cards(student_id, per_subject_limit=3, overall_limit=None, subject_filter=None):
    """Fetch once and build assessment cards without N+1 subject queries."""
    rows = api.assessments.get_assessments(student_id=student_id)
    counts_by_subject = {}
    cards = []
    for row in rows:
        subject = row['subject']
        if subject_filter and subject != subject_filter:
            continue
        used = counts_by_subject.get(subject, 0)
        if used >= per_subject_limit:
            continue
        counts_by_subject[subject] = used + 1
        cards.append(_assessment_row_to_card(row))
        if overall_limit and len(cards) >= overall_limit:
            break
    return cards


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


def _available_tutor_subjects(student):
    subjects = [s for s in (student.get('subjects') or []) if s in TUTOR_SUBJECT_PROMPTS]
    return subjects or list(TUTOR_SUBJECT_PROMPTS.keys())


def _normalize_tutor_messages(raw_messages):
    if not isinstance(raw_messages, list):
        return []

    clean = []
    for message in raw_messages[-MAX_TUTOR_MESSAGES:]:
        if not isinstance(message, dict):
            continue

        role = (message.get('role') or '').strip().lower()
        if role not in {'user', 'assistant'}:
            continue

        content = message.get('content', '')
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict) and block.get('type') == 'text':
                    part_text = str(block.get('text') or '').strip()
                    if part_text:
                        parts.append(part_text)
            content = '\n'.join(parts)
        else:
            content = str(content or '')

        content = content.strip()
        if not content:
            continue
        if len(content) > MAX_TUTOR_MESSAGE_CHARS:
            content = content[:MAX_TUTOR_MESSAGE_CHARS]

        clean.append({'role': role, 'content': content})

    return clean


def _create_tutor_client():
    api_key = (os.environ.get('ANTHROPIC_API_KEY') or '').strip()
    if not api_key:
        return None, 'Tutor AI is not configured yet. Ask your teacher to set ANTHROPIC_API_KEY.'
    try:
        from anthropic import Anthropic
    except Exception:
        return None, 'Tutor AI dependency missing. Install anthropic in the server environment.'
    return Anthropic(api_key=api_key), None


def _extract_tutor_text(response):
    parts = []
    for block in getattr(response, 'content', []) or []:
        text = getattr(block, 'text', '')
        text = str(text or '').strip()
        if text:
            parts.append(text)
    return '\n'.join(parts).strip()


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


# ==================== ONBOARDING ====================

@app.route('/onboarding')
def onboarding():
    """Getting-started guide for admins and students."""
    return render_template('onboarding.html')


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
        return render_template('apply.html', submitted=False, grade_levels=GRADE_LEVELS)

    # POST — save + email
    full_name      = request.form.get('full_name', '').strip()
    phone          = request.form.get('phone', '').strip()
    email          = request.form.get('email', '').strip()
    parent_name    = request.form.get('parent_name', '').strip()
    parent_phone   = request.form.get('parent_phone', '').strip()
    subjects_list  = request.form.getlist('subjects')
    grade_level    = request.form.get('grade_level', '').strip()
    previous_school = request.form.get('previous_school', '').strip()
    year_failed    = request.form.get('year_failed', '').strip()
    message        = request.form.get('message', '').strip()

    if not full_name or not phone or not subjects_list or not grade_level:
        flash('Please fill in your name, phone number, grade, and select at least one subject.', 'error')
        return render_template('apply.html', submitted=False, grade_levels=GRADE_LEVELS)

    subjects_str = ', '.join(subjects_list)

    # Save to DB
    try:
        with managed_connection() as conn:
            qexec(conn, f"""
                INSERT INTO applications
                  (full_name, phone, email, parent_name, parent_phone,
                        subjects, previous_school, year_failed, grade_level, message, school_name)
                    VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})
            """, (full_name, phone, email, parent_name, parent_phone,
                        subjects_str, previous_school, year_failed, grade_level, message, _admin_school_scope()))
    except Exception as e:
        flash(f'Database error: {e}', 'error')
        return render_template('apply.html', submitted=False, grade_levels=GRADE_LEVELS)

    # Send email (non-blocking — silently log failure, don't break UX)
    application_data = dict(
        full_name=full_name, phone=phone, email=email,
        parent_name=parent_name, parent_phone=parent_phone,
        subjects=subjects_list, previous_school=previous_school,
        year_failed=year_failed, grade_level=grade_level, message=message
    )
    if _is_offline_mode():
        app.logger.info('OFFLINE_MODE enabled: skipped email/WhatsApp notification for /apply')
    else:
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
    school_name = _admin_school_scope()
    stats = api.get_dashboard_stats(school_name=school_name)
    schedule = generate_daily_timetable(day_name) if day_name not in ["Saturday", "Sunday"] else []
    current_month = today.strftime('%Y-%m')
    payment_status = api.get_payment_status(current_month, school_name=school_name)
    class_summary = api.get_class_performance_summary(school_name=school_name)
    at_risk_students = [s for s in class_summary['students'] if s['risk_level'] == 'high'][:5]
    intel = intelligence.get_dashboard_intelligence(school_name=school_name)
    return render_template('dashboard.html',
                         today=today.strftime('%A, %d %B %Y'),
                         schedule=schedule, stats=stats,
                         payment_status=payment_status,
                         at_risk_students=at_risk_students,
                         day_name=day_name,
                         intel=intel)


# === MASTER TIMETABLE VIEW ===
@app.route('/admin/master-timetable')
@admin_required
def master_timetable():
    school_name = _admin_school_scope()
    students = api.get_all_students_summary(school_name=school_name)
    conn = get_db()
    all_slots = qexec(conn,
        f"""SELECT t.*
            FROM timetable_slots t
            JOIN students s ON s.student_id = t.student_id
            WHERE LOWER(COALESCE(s.school_name, '')) = LOWER({PH})
            ORDER BY t.day, t.period, t.student_id""",
        (school_name,)).fetchall()
    release_connection(conn)
    slots_by_student = {}
    for slot in all_slots:
        slots_by_student.setdefault(slot['student_id'], []).append(dict(slot))
    return render_template('admin/master_timetable.html', students=students, slots_by_student=slots_by_student)


if os.environ.get('ENABLE_DEBUG_ROUTES') == '1':
    # Explicitly opt-in only; never enabled in production by default.
    @app.route('/admin/debug/cd003')
    @admin_required
    def debug_cd003():
        try:
            conn = get_db()
            student = qexec(conn, f"SELECT * FROM students WHERE student_id={PH}", ('CD003',)).fetchone()
            subjects = qexec(conn, f"SELECT subject FROM student_subjects WHERE student_id={PH}", ('CD003',)).fetchall()
            slots = qexec(conn, f"SELECT * FROM timetable_slots WHERE student_id={PH}", ('CD003',)).fetchall()
            release_connection(conn)
            return f"<pre>STUDENT:\n{student}\n\nSUBJECTS:\n{subjects}\n\nTIMETABLE SLOTS:\n{slots}</pre>"
        except Exception as e:
            import traceback
            return f"<pre>ERROR: {e}\n\nTRACEBACK:\n{traceback.format_exc()}</pre>"


# ==================== STUDENTS (ADMIN) ====================

@app.route('/students')
@admin_required
def students():
    search = request.args.get('search', '').strip()
    risk_filter = request.args.get('risk', '')
    payment_filter = request.args.get('payment', '')
    subject_filter = request.args.get('subject', '')
    grade_filter = request.args.get('grade', '')
    all_students = api.get_all_students_summary(school_name=_admin_school_scope())
    filtered_students = all_students

    if search:
        sl = search.lower()
        filtered_students = [s for s in filtered_students if sl in s['name'].lower() or sl in s['student_id'].lower()]
    if risk_filter:
        filtered_students = [s for s in filtered_students if s.get('risk_level') == risk_filter]
    if subject_filter:
        filtered_students = [s for s in filtered_students if subject_filter in s.get('subjects', [])]
    if grade_filter:
        filtered_students = [s for s in filtered_students if (s.get('grade_level') or '').strip().lower() == grade_filter.lower()]
    if payment_filter:
        current_month = date.today().strftime('%Y-%m')
        payment_data = api.get_payment_status(current_month, school_name=_admin_school_scope())
        if payment_filter == 'paid':
            paid_ids = {s['student_id'] for s in payment_data['paid']}
            filtered_students = [s for s in filtered_students if s['student_id'] in paid_ids]
        elif payment_filter == 'outstanding':
            out_ids = {s['student_id'] for s in payment_data['outstanding']}
            filtered_students = [s for s in filtered_students if s['student_id'] in out_ids]

    return render_template('students.html', students=filtered_students,
                          total_count=len(all_students), filtered_count=len(filtered_students),
                          subjects=CORE_SUBJECTS, grade_levels=GRADE_LEVELS,
                          filters={'search': search, 'risk': risk_filter, 'payment': payment_filter, 'subject': subject_filter, 'grade': grade_filter})


@app.route('/student/<student_id>')
@admin_required
def student_detail(student_id):
    student = _get_scoped_student(student_id)
    if not student:
        flash(f"Student {student_id} not found in this school", "error")
        return redirect(url_for('students'))
    performance = api.get_student_performance(student_id)
    attendance_history = api.get_student_attendance_history(student_id, limit=30)
    payments = api.payments.get_payments(student_id)[-6:]
    recent_assessments = _recent_assessment_cards(student_id, per_subject_limit=5, overall_limit=10)
    return render_template('student_detail.html', student=student, performance=performance,
                         attendance=attendance_history, payments=payments, assessments=recent_assessments)


@app.route('/student/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    if request.method == 'POST':
        try:
            grade_level = request.form.get('grade_level', '').strip()
            if not grade_level:
                raise ValueError('Grade level is required')
            selected_subjects = request.form.getlist('subjects')
            if not selected_subjects:
                raise ValueError('Please select at least one subject')
            student_id = api.register_student(
                name=request.form.get('name'), email=request.form.get('email'),
                phone=request.form.get('phone'), parent_name=request.form.get('parent_name'),
                parent_phone=request.form.get('parent_phone'), parent_email=request.form.get('parent_email'),
                subjects=selected_subjects, notes=request.form.get('notes', ''),
                school_name=_admin_school_scope(),
                grade_level=grade_level
            )
            if not student_id:
                raise ValueError('Student registration failed')

            # 1) Create student account with a unique temporary password.
            # Admin can still replace it from the Student Accounts page.
            temporary_password = secrets.token_urlsafe(9)
            # 2) Assign default timetable in the same transaction.
            from timetable_generator import generate_smart_timetable, SUBJECT_DEFAULT_FREQS, PERIOD_TIMES
            timetable = generate_smart_timetable(
                {subject: SUBJECT_DEFAULT_FREQS.get(subject, 1) for subject in selected_subjects}
            )
            with managed_connection() as conn:
                qexec(conn,
                    f"INSERT INTO user_accounts (username, password_hash, role, student_id) VALUES ({PH},{PH},{PH},{PH})",
                    (student_id, generate_password_hash(temporary_password), 'student', student_id))
                for day, slots in timetable.items():
                    if isinstance(slots, dict):
                        slot_rows = [
                            (int(period), subject, PERIOD_TIMES[int(period)][0], PERIOD_TIMES[int(period)][1])
                            for period, subject in slots.items()
                        ]
                    else:
                        slot_rows = []
                        for entry in slots or []:
                            if not isinstance(entry, (list, tuple)) or len(entry) < 2:
                                continue
                            period = int(entry[0])
                            subject = entry[1]
                            t_from = entry[2] if len(entry) > 2 and entry[2] else PERIOD_TIMES.get(period, ("", ""))[0]
                            t_to = entry[3] if len(entry) > 3 and entry[3] else PERIOD_TIMES.get(period, ("", ""))[1]
                            slot_rows.append((period, subject, t_from, t_to))
                    for period, subject, t_from, t_to in slot_rows:
                        if subject:
                            qexec(conn,
                                f"INSERT INTO timetable_slots (student_id, day, period, subject, time_from, time_to) VALUES ({PH},{PH},{PH},{PH},{PH},{PH})",
                                (student_id, day, period, subject, t_from, t_to))
            try:
                automation.run_for_student(student_id)
            except Exception:
                pass
            # 3. Optionally: Initialize empty assessment records (optional, can be expanded)
            # (No-op: assessments are typically added after first test, but can be initialized here if needed)
            flash(
                f"Student registered: {student_id}. Temporary password: {temporary_password} "
                f"(set a new one immediately).",
                "success"
            )
            return redirect(url_for('student_detail', student_id=student_id))
        except Exception as e:
            flash(f"Error: {str(e)}", "error")
    return render_template('add_student.html', subjects=CORE_SUBJECTS, grade_levels=GRADE_LEVELS)


# ==================== ATTENDANCE (ADMIN) ====================

@app.route('/attendance')
@admin_required
def attendance():
    try:
        today = date.today()
        selected_date = request.args.get('date', today.isoformat())
        all_students = api.students.get_all_students(status='active', school_name=_admin_school_scope())
        attendance_report = api.get_daily_attendance_report(selected_date)
        day_name = datetime.fromisoformat(selected_date).strftime("%A")
        schedule = generate_daily_timetable(day_name) if day_name not in ["Saturday", "Sunday"] else []
        return render_template('attendance.html', students=all_students, schedule=schedule,
                             selected_date=selected_date, attendance_report=attendance_report, subjects=CORE_SUBJECTS)
    except Exception as e:
        import traceback
        return f"<pre>ERROR: {e}\n\nTRACEBACK:\n{traceback.format_exc()}</pre>"


@app.route('/attendance/mark', methods=['POST'])
@admin_required
def mark_attendance():
    try:
        school_name = _admin_school_scope()
        allowed_ids = {
            s['student_id'] for s in api.students.get_all_students(status='active', school_name=school_name)
        }
        present_ids = [sid for sid in request.form.getlist('present[]') if sid in allowed_ids]
        result = api.mark_class_attendance(
            present_student_ids=present_ids,
            date_str=request.form.get('date'),
            time_slot=request.form.get('time_slot'),
            subject=request.form.get('subject'),
            school_name=school_name
        )
        # Automation Rule 2 — attendance risk check for every student marked
        all_ids = [sid for sid in (request.form.getlist('all_student_ids[]') or present_ids) if sid in allowed_ids]
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
    school_name = _admin_school_scope()
    class_summary = api.get_class_performance_summary(school_name=school_name)
    all_students = api.students.get_all_students(status='active', school_name=school_name)
    recent_assessments = []
    for student in all_students:
        cards = _recent_assessment_cards(
            student['student_id'],
            per_subject_limit=3,
            subject_filter=(subject_filter or None),
        )
        for card in cards:
            recent_assessments.append({
                'student_id': student['student_id'],
                'student_name': student['name'],
                'subject': card['subject'],
                'type': card['type'],
                'score': card['score'],
                'max_score': card['max_score'],
                'percentage': card['percentage'],
                'date': card['date'],
            })
    recent_assessments.sort(key=lambda x: x['date'], reverse=True)
    return render_template('assessments.html', assessments=recent_assessments[:50],
                         class_summary=class_summary, subjects=CORE_SUBJECTS, subject_filter=subject_filter)


@app.route('/assessment/add', methods=['POST'])
@admin_required
def add_assessment():
    try:
        student_id = request.form.get('student_id')
        if not _get_scoped_student(student_id):
            flash('Student not found in this school.', 'error')
            return redirect(url_for('assessments'))
        score = float(request.form.get('score'))
        max_score = float(request.form.get('max_score', 100))
        weight = float(request.form.get('weight', 1))
        api.record_assessment(
            student_id=student_id, subject=request.form.get('subject'),
            assessment_type=request.form.get('assessment_type'), score=score, max_score=max_score,
            date=request.form.get('date', date.today().isoformat()), notes=request.form.get('notes', '')
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
        import traceback
        return f"<pre>ERROR: {e}\n\nTRACEBACK:\n{traceback.format_exc()}</pre>"


# ==================== PAYMENTS (ADMIN) ====================

@app.route('/payments')
@admin_required
def payments():
    selected_month = request.args.get('month', date.today().strftime('%Y-%m'))
    school_name = _admin_school_scope()
    payment_status = api.get_payment_status(selected_month, school_name=school_name)
    revenue_summary = api.get_revenue_summary(school_name=school_name)
    return render_template('payments.html', payment_status=payment_status,
                         revenue_summary=revenue_summary, selected_month=selected_month)


@app.route('/payment/record', methods=['POST'])
@admin_required
def record_payment():
    try:
        student_id = request.form.get('student_id')
        if not _get_scoped_student(student_id):
            flash('Student not found in this school.', 'error')
            return redirect(url_for('payments'))
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
        results = automation.run_all(school_name=_admin_school_scope())
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
    school_name = _admin_school_scope()
    summary = automation.get_risk_summary(school_name=school_name)
    all_students = api.get_all_students_summary(school_name=school_name)
    return render_template('risk_alerts.html', summary=summary, students=all_students)


@app.route('/admin/risk-alerts/resolve/<int:alert_id>', methods=['POST'])
@admin_required
def resolve_alert(alert_id):
    automation.resolve_alert(alert_id)
    flash('Alert resolved.', 'success')
    next_page = request.args.get('next') or request.form.get('next')
    if next_page and next_page.startswith('/'):
        return redirect(next_page)
    return redirect(url_for('risk_alerts'))


@app.route('/admin/intervention/log', methods=['POST'])
@admin_required
def log_intervention():
    """
    Record that an admin acted on a recommendation (from the student profile
    page or the intervention list).  POST fields: student_id, rec_type,
    rec_action, note (optional), alert_id (optional).
    Returns JSON { ok, id } so it can be called via fetch().
    """
    from flask import jsonify
    data       = request.get_json(silent=True) or request.form
    student_id = data.get('student_id', '').strip()
    rec_type   = data.get('rec_type',   'manual').strip()
    rec_action = data.get('rec_action', 'admin_action').strip()
    note       = data.get('note',       '').strip()
    alert_id   = data.get('alert_id')
    try:
        alert_id = int(alert_id) if alert_id else None
    except (ValueError, TypeError):
        alert_id = None

    if not student_id:
        return jsonify({'ok': False, 'error': 'student_id required'}), 400
    if not _get_scoped_student(student_id):
        return jsonify({'ok': False, 'error': 'student not found in this school'}), 403

    new_id = intelligence.log_intervention(student_id, rec_type, rec_action, note, alert_id)
    return jsonify({'ok': True, 'id': new_id})


@app.route('/admin/intervention/evaluate', methods=['POST'])
@admin_required
def run_feedback_evaluation():
    """Manually trigger feedback loop evaluation (normally called by automation)."""
    from flask import jsonify
    n = intelligence.evaluate_feedback_loops()
    return jsonify({'ok': True, 'evaluated': n})


# ==================== APPLICATIONS (ADMIN) ====================

@app.route('/admin/applications')
@admin_required
def admin_applications():
    status_filter = request.args.get('status', '')
    school_name = _admin_school_scope()
    apply_url = _public_apply_url()
    fallback_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=640x640&data={quote_plus(apply_url)}"
    conn = get_db()
    if status_filter:
        apps = qexec(conn,
            f"""SELECT * FROM applications
                WHERE status={PH}
                  AND LOWER(COALESCE(school_name, '')) = LOWER({PH})
                ORDER BY created_at DESC""",
            (status_filter, school_name)).fetchall()
    else:
        apps = qexec(conn,
            f"""SELECT * FROM applications
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                ORDER BY created_at DESC""",
            (school_name,)).fetchall()
    new_count = qexec(conn,
        f"""SELECT COUNT(*) as cnt FROM applications
            WHERE status='new'
              AND LOWER(COALESCE(school_name, '')) = LOWER({PH})""",
        (school_name,)).fetchone()['cnt']
    total_count = qexec(conn,
        f"SELECT COUNT(*) as cnt FROM applications WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})",
        (school_name,)).fetchone()['cnt']
    release_connection(conn)
    return render_template('admin_applications.html',
                           applications=[dict(a) for a in apps],
                           new_count=new_count, total_count=total_count,
                           status_filter=status_filter,
                           apply_url=apply_url,
                           fallback_qr_url=fallback_qr_url)


def _render_apply_qr_svg():
    """SVG QR for the public /apply form."""
    apply_url = _public_apply_url()
    try:
        import segno
    except Exception:
        return redirect(f"https://api.qrserver.com/v1/create-qr-code/?size=640x640&data={quote_plus(apply_url)}")

    out = BytesIO()
    segno.make(apply_url, error='h').save(
        out,
        kind='svg',
        scale=8,
        border=2,
        dark='#111827',
        light='#FFFFFF',
    )
    return Response(
        out.getvalue(),
        mimetype='image/svg+xml',
        headers={
            'Cache-Control': 'no-store',
            'Content-Disposition': 'inline; filename="learner-registration-qr.svg"',
        },
    )


@app.route('/qr/apply.svg')
def public_apply_qr():
    return _render_apply_qr_svg()


@app.route('/admin/applications/qr.svg')
@admin_required
def admin_applications_qr():
    return _render_apply_qr_svg()


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
    school_name = _admin_school_scope()
    all_students = api.get_all_students_summary(school_name=school_name)
    conn = get_db()
    accounts = {row['student_id']: dict(row) for row in
                qexec(conn,
                    f"""SELECT ua.*
                        FROM user_accounts ua
                        JOIN students s ON s.student_id = ua.student_id
                        WHERE ua.role='student'
                          AND LOWER(COALESCE(s.school_name, '')) = LOWER({PH})""",
                    (school_name,)).fetchall()}
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

    student = _get_scoped_student(student_id)
    if not student:
        flash(f'Student {student_id} not found in this school.', 'error')
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
    student = _get_scoped_student(username)
    if not student:
        flash(f'Student {username} not found in this school.', 'error')
        return redirect(url_for('student_accounts'))
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
    school_name = _admin_school_scope()
    conn = get_db()
    if subject_filter:
        videos = qexec(conn,
            f"""SELECT * FROM manlib_videos
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                  AND subject={PH}
                ORDER BY subject, order_num, created_at""",
            (school_name, subject_filter)).fetchall()
    else:
        videos = qexec(conn,
            f"""SELECT * FROM manlib_videos
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                ORDER BY subject, order_num, created_at""",
            (school_name,)).fetchall()
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

    school_name = _admin_school_scope()
    conn = get_db()
    qexec(conn,
        f"""INSERT INTO manlib_videos
            (school_name, subject, title, description, video_type, video_url, file_path, duration, order_num)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})""",
        (school_name, subject, title, description, video_type, video_url, file_path, duration, order_num))
    conn.commit()
    release_connection(conn)

    flash(f'Video added: "{title}" [{subject}]', 'success')
    return redirect(url_for('admin_manlib', subject=subject))


@app.route('/admin/manlib/delete/<int:video_id>', methods=['POST'])
@admin_required
def delete_manlib_video(video_id):
    school_name = _admin_school_scope()
    conn = get_db()
    video = qexec(conn,
        f"""SELECT * FROM manlib_videos
            WHERE id={PH}
              AND LOWER(COALESCE(school_name, '')) = LOWER({PH})""",
        (video_id, school_name)).fetchone()
    if not video:
        release_connection(conn)
        flash('Video not found in this school.', 'error')
        return redirect(url_for('admin_manlib'))
    if video and video['file_path']:
        try:
            os.remove(str(Path(__file__).parent / 'static' / video['file_path']))
        except:
            pass
    qexec(conn,
        f"""DELETE FROM manlib_videos
            WHERE id={PH}
              AND LOWER(COALESCE(school_name, '')) = LOWER({PH})""",
        (video_id, school_name))
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
    school_name = _admin_school_scope()
    conn = get_db()
    query = f"SELECT * FROM subject_content WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})"
    params = [school_name]
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

    school_name = _admin_school_scope()
    conn = get_db()
    qexec(conn,
        f"""INSERT INTO subject_content
            (school_name, subject, content_type, title, description, content_text, file_path, link_url, order_num)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH},{PH})""",
        (school_name, subject, content_type, title, description, content_text, file_path, link_url, order_num))
    conn.commit()
    release_connection(conn)
    flash(f'Content added: "{title}" [{subject} / {content_type}]', 'success')
    return redirect(url_for('admin_subject_content', subject=subject, content_type=content_type))


@app.route('/admin/subject-content/delete/<int:item_id>', methods=['POST'])
@admin_required
def delete_subject_content(item_id):
    school_name = _admin_school_scope()
    conn = get_db()
    item = qexec(conn,
        f"""SELECT * FROM subject_content
            WHERE id={PH}
              AND LOWER(COALESCE(school_name, '')) = LOWER({PH})""",
        (item_id, school_name)).fetchone()
    if not item:
        release_connection(conn)
        flash('Content item not found in this school.', 'error')
        return redirect(url_for('admin_subject_content'))
    if item and item['file_path']:
        try:
            os.remove(str(Path(__file__).parent / 'static' / item['file_path']))
        except:
            pass
    qexec(conn,
        f"""DELETE FROM subject_content
            WHERE id={PH}
              AND LOWER(COALESCE(school_name, '')) = LOWER({PH})""",
        (item_id, school_name))
    conn.commit()
    release_connection(conn)
    flash('Content deleted.', 'success')
    return redirect(url_for('admin_subject_content'))

@app.route('/admin/timetable/<student_id>', methods=['GET', 'POST'])
@admin_required
def admin_student_timetable(student_id):
    """Set a student's personal timetable"""
    student = _get_scoped_student(student_id)
    if not student:
        flash(f'Student {student_id} not found in this school.', 'error')
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
                         days=DAYS, subjects=CORE_SUBJECTS, slots=[dict(s) for s in slots],
                         default_freqs=SUBJECT_DEFAULT_FREQS)


@app.route('/admin/timetable/<student_id>/generate-smart', methods=['POST'])
@admin_required
def generate_smart_timetable_route(student_id):
    """Generate an intelligent timetable from per-subject frequency inputs."""
    student = _get_scoped_student(student_id)
    if not student:
        flash(f'Student {student_id} not found in this school.', 'error')
        return redirect(url_for('students'))

    # Build subjects_freq from form: enrolled subjects + any extra checked ones
    enrolled = student.get('subjects', [])
    subjects_freq = {}
    for subj in enrolled:
        key = f"freq_{subj.replace(' ', '_')}"
        raw = request.form.get(key, '').strip()
        freq = int(raw) if raw.isdigit() else SUBJECT_DEFAULT_FREQS.get(subj, 4)
        if freq > 0:
            subjects_freq[subj] = freq

    if not subjects_freq:
        flash('No subjects selected for generation.', 'warning')
        return redirect(url_for('admin_student_timetable', student_id=student_id))

    schedule = generate_smart_timetable(subjects_freq)

    conn = get_db()
    qexec(conn, f"DELETE FROM timetable_slots WHERE student_id={PH}", (student_id,))
    for day, periods in schedule.items():
        for (period, subject, time_from, time_to) in periods:
            qexec(conn,
                f"INSERT INTO timetable_slots (student_id, day, period, subject, time_from, time_to)"
                f" VALUES ({PH},{PH},{PH},{PH},{PH},{PH})",
                (student_id, day, period, subject, time_from, time_to))
    # Insert daily tea break rows so they show on the student view
    for day in TT_DAYS:
        qexec(conn,
            f"INSERT INTO timetable_slots (student_id, day, period, subject, time_from, time_to)"
            f" VALUES ({PH},{PH},{PH},{PH},{PH},{PH})",
            (student_id, day, 0, 'TEA BREAK', '08:40', '09:00'))
    conn.commit()
    release_connection(conn)
    total = sum(len(v) for v in schedule.values())
    flash(f"Smart timetable generated for {student['name']} ({total} slots across 5 days).", 'success')
    return redirect(url_for('admin_student_timetable', student_id=student_id))


# ==================== ADMIN: STUDENT PORTAL SELECTOR ====================

@app.route('/portal')
@admin_required
def student_portal():
    students = api.get_all_students_summary(school_name=_admin_school_scope())
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

    student_school = _student_school_scope(student)
    conn = get_db()
    # Only show videos for subjects this student is enrolled in
    placeholders = ','.join([PH] * len(student['subjects']))
    videos = qexec(conn,
        f"""SELECT * FROM manlib_videos
            WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
              AND subject IN ({placeholders})
            ORDER BY subject, order_num, created_at""",
        tuple([student_school, *student['subjects']])
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
    student_school = _student_school_scope(student)
    conn = get_db()

    # Videos per subject
    if subjects:
        placeholders = ','.join([PH] * len(subjects))
        videos = qexec(conn,
            f"""SELECT * FROM manlib_videos
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                  AND subject IN ({placeholders})
                ORDER BY subject, order_num, created_at""",
            tuple([student_school, *subjects])
        ).fetchall()
    else:
        videos = []

    # All subject content for this student's subjects
    if subjects:
        placeholders = ','.join([PH] * len(subjects))
        content_rows = qexec(conn,
            f"""SELECT * FROM subject_content
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                  AND subject IN ({placeholders})
                ORDER BY subject, content_type, order_num, created_at""",
            tuple([student_school, *subjects])
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


@app.route('/my-portal/tutor')
@student_required
def student_tutor():
    """Student AI tutor page."""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return redirect(url_for('logout'))

    tutor_ready = bool((os.environ.get('ANTHROPIC_API_KEY') or '').strip())
    return render_template(
        'student_tutor.html',
        student=student,
        subjects=_available_tutor_subjects(student),
        tutor_ready=tutor_ready,
        today=date.today().strftime('%A, %d %B %Y')
    )


@app.route('/my-portal/tutor/chat', methods=['POST'])
@student_required
def student_tutor_chat():
    """Chat endpoint for the student AI tutor."""
    student_id = session['student_id']
    student = api.get_student_info(student_id)
    if not student:
        return jsonify({'error': 'Student account not found'}), 404

    data = request.get_json(silent=True) or {}
    subject = str(data.get('subject') or '').strip()
    available_subjects = _available_tutor_subjects(student)
    if subject not in available_subjects:
        subject = available_subjects[0]

    messages = _normalize_tutor_messages(data.get('messages'))
    if not messages:
        return jsonify({'error': 'Please send at least one message'}), 400
    if messages[-1]['role'] != 'user':
        return jsonify({'error': 'Last message must be from the student'}), 400

    client, err = _create_tutor_client()
    if err:
        return jsonify({'error': err}), 503

    try:
        response = client.messages.create(
            model=TUTOR_MODEL,
            max_tokens=1000,
            system=TUTOR_SUBJECT_PROMPTS.get(subject, TUTOR_SUBJECT_PROMPTS[DEFAULT_TUTOR_SUBJECT]),
            messages=messages
        )
        reply = _extract_tutor_text(response)
        if not reply:
            return jsonify({'error': 'Tutor returned an empty response. Please try again.'}), 502
        return jsonify({'reply': reply, 'subject': subject})
    except Exception:
        app.logger.exception('Tutor chat failed for student %s', student_id)
        return jsonify({'error': 'Tutor is currently unavailable. Please try again shortly.'}), 500


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

    all_assessments = [_assessment_row_to_card(row) for row in api.assessments.get_assessments(student_id=student_id)]

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

    if session.get('user_role') == 'admin' and not _student_in_scope(student):
        flash('Access denied: learner belongs to a different school.', 'error')
        return redirect(url_for('student_portal'))

    performance = api.get_student_performance(student_id)
    recent_assessments = _recent_assessment_cards(student_id, per_subject_limit=3, overall_limit=5)

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
        student_school = _student_school_scope(student)
        rows = qexec(conn,
            f"""SELECT subject, COUNT(*) as cnt
                FROM manlib_videos
                WHERE LOWER(COALESCE(school_name, '')) = LOWER({PH})
                  AND subject IN ({placeholders})
                GROUP BY subject""",
            tuple([student_school, *student['subjects']])
        ).fetchall()
        video_counts = {r['subject']: r['cnt'] for r in rows}
    release_connection(conn)

    return render_template('student_homepage.html',
                         student=student, performance=performance,
                         assessments=recent_assessments,
                         schedule=[dict(s) for s in tmt_slots] or schedule,
                         attendance=attendance_history,
                         video_counts=video_counts,
                         payment_restricted=payment_restricted,
                         today=today.strftime('%A, %d %B %Y'))


# ==================== API ====================

@app.route('/api/dashboard-stats')
@admin_required
def api_dashboard_stats():
    return jsonify(api.get_dashboard_stats(school_name=_admin_school_scope()))


# ==================== CLEANUP ====================

@app.teardown_appcontext
def cleanup(error=None):
    pass


if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1').strip() or '127.0.0.1'
    port_raw = os.environ.get('PORT', '5000').strip()
    try:
        port = int(port_raw)
    except ValueError:
        port = 5000
    debug = os.environ.get('FLASK_DEBUG', '1').strip().lower() in ('1', 'true', 'yes', 'on')
    open_host = 'localhost' if host in ('127.0.0.1', 'localhost') else host

    print("\n" + "="*70)
    print("  CLASSDOODLE — Role-Based Dashboard")
    print("="*70)
    print("\n  Admin login : username=admin  password=<set via ADMIN_BOOTSTRAP_PASSWORD>")
    print("  Student login: username=<student_id>  password=<temporary/generated or set via admin panel>")
    print(f"\n  Open: http://{open_host}:{port}")
    if _is_offline_mode():
        print("  OFFLINE_MODE: enabled (email/WhatsApp notifications are skipped)")
    print("="*70 + "\n")
    app.run(debug=debug, host=host, port=port, use_reloader=False)
