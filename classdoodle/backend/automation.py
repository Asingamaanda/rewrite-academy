"""
Rewrite Academy -- Self-Running Automation Engine
Three rules run after every mark, attendance record, or payment.
Works with both PostgreSQL (Render) and SQLite (local dev).
"""

from datetime import date, timedelta, datetime
from backend.db_adapter import get_connection, release_connection, qexec, fetchone, PH, POSTGRES

ACADEMIC_CRITICAL_THRESHOLD = 50
ACADEMIC_WARN_THRESHOLD      = 60
ATTENDANCE_THRESHOLD         = 75
RESTRICT_AFTER_DAYS          = 7
PAYMENT_DUE_DAY              = 15


def _log_alert(conn, student_id, alert_type, message):
    today = date.today().isoformat()
    existing = fetchone(conn,
        f"SELECT id FROM automation_alerts WHERE student_id={PH} AND alert_type={PH} AND DATE(created_at)={PH}",
        (student_id, alert_type, today))
    if not existing:
        qexec(conn,
            f"INSERT INTO automation_alerts (student_id, alert_type, message) VALUES ({PH},{PH},{PH})",
            (student_id, alert_type, message))


def _check_academic_risk(conn, student_id):
    row = fetchone(conn, f"""
        SELECT
            CASE WHEN SUM(COALESCE(weight,0)) > 0
                 THEN ROUND(SUM((score*1.0/max_score)*100*COALESCE(weight,1))/SUM(COALESCE(weight,1)),1)
                 ELSE ROUND(AVG((score*1.0/max_score)*100),1)
            END AS weighted_avg,
            COUNT(*) AS assessment_count
        FROM assessments WHERE student_id={PH}
    """, (student_id,))

    if not row or row['weighted_avg'] is None:
        return None

    avg   = row['weighted_avg']
    count = row['assessment_count']

    if avg < ACADEMIC_CRITICAL_THRESHOLD:
        risk = 'critical'
    elif avg < ACADEMIC_WARN_THRESHOLD:
        risk = 'needs_support'
    else:
        risk = 'on_track'

    qexec(conn, f"UPDATE students SET academic_risk={PH} WHERE student_id={PH}", (risk, student_id))

    if risk in ('critical', 'needs_support') and count > 0:
        _log_alert(conn, student_id, 'academic_risk',
                   f"Weighted average is {avg:.1f}% -- flagged as '{risk}'.")

    return {'avg': avg, 'risk': risk, 'assessments': count}


def _check_attendance_risk(conn, student_id):
    seven_days_ago = (date.today() - timedelta(days=7)).isoformat()
    row = fetchone(conn, f"""
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) AS present
        FROM attendance WHERE student_id={PH} AND date>={PH}
    """, (student_id, seven_days_ago))

    if not row or not row['total']:
        return None

    rate    = round((row['present'] / row['total']) * 100, 1)
    at_risk = rate < ATTENDANCE_THRESHOLD

    qexec(conn, f"UPDATE students SET attendance_risk={PH} WHERE student_id={PH}",
          ('at_risk' if at_risk else 'ok', student_id))

    if at_risk:
        _log_alert(conn, student_id, 'attendance_risk',
                   f"Attendance last 7 days: {rate:.1f}% (threshold: {ATTENDANCE_THRESHOLD}%).")

    return {'rate': rate, 'at_risk': at_risk}


def _check_payment_risk(conn, student_id):
    today         = date.today()
    current_month = today.strftime('%Y-%m')
    due_date      = date(today.year, today.month, PAYMENT_DUE_DAY)

    paid = fetchone(conn,
        f"SELECT id FROM payments WHERE student_id={PH} AND month_for={PH} AND status='paid' LIMIT 1",
        (student_id, current_month))

    if paid:
        qexec(conn, f"UPDATE students SET payment_risk='paid' WHERE student_id={PH}", (student_id,))
        return {'status': 'paid'}

    if today <= due_date:
        qexec(conn, f"UPDATE students SET payment_risk='pending' WHERE student_id={PH}", (student_id,))
        return {'status': 'pending'}

    days_overdue = (today - due_date).days

    if days_overdue > RESTRICT_AFTER_DAYS:
        qexec(conn, f"UPDATE students SET payment_risk='restricted' WHERE student_id={PH}", (student_id,))
        _log_alert(conn, student_id, 'payment_restricted',
                   f"Payment overdue by {days_overdue} days. Subject access restricted.")
        return {'status': 'restricted', 'days_overdue': days_overdue}

    qexec(conn, f"UPDATE students SET payment_risk='outstanding' WHERE student_id={PH}", (student_id,))
    _log_alert(conn, student_id, 'payment_overdue',
               f"No payment for {current_month}. Overdue by {days_overdue} days.")
    return {'status': 'outstanding', 'days_overdue': days_overdue}


def _snapshot_progress(conn, student_id):
    row = fetchone(conn, f"""
        SELECT CASE WHEN SUM(COALESCE(weight,0)) > 0
                    THEN ROUND(SUM((score*1.0/max_score)*100*COALESCE(weight,1))/SUM(COALESCE(weight,1)),1)
                    ELSE ROUND(AVG((score*1.0/max_score)*100),1)
               END AS avg
        FROM assessments WHERE student_id={PH}
    """, (student_id,))

    if not row or row['avg'] is None:
        return

    week = datetime.now().strftime('%Y-W%V')
    if POSTGRES:
        qexec(conn, f"""
            INSERT INTO progress_snapshots (student_id, week, average)
            VALUES ({PH},{PH},{PH})
            ON CONFLICT (student_id, week) DO UPDATE SET average=EXCLUDED.average
        """, (student_id, week, row['avg']))
    else:
        qexec(conn, f"""
            INSERT OR REPLACE INTO progress_snapshots (student_id, week, average)
            VALUES ({PH},{PH},{PH})
        """, (student_id, week, row['avg']))


def run_for_student(student_id: str) -> dict:
    conn = get_connection()
    try:
        results = {
            'academic':   _check_academic_risk(conn, student_id),
            'attendance': _check_attendance_risk(conn, student_id),
            'payment':    _check_payment_risk(conn, student_id),
        }
        _snapshot_progress(conn, student_id)
        conn.commit()
        return results
    finally:
        release_connection(conn)


def run_all() -> dict:
    conn = get_connection()
    try:
        students = qexec(conn,
            "SELECT student_id FROM students WHERE status != 'suspended'").fetchall()
        results = {}
        for row in students:
            sid = row['student_id']
            results[sid] = {
                'academic':   _check_academic_risk(conn, sid),
                'attendance': _check_attendance_risk(conn, sid),
                'payment':    _check_payment_risk(conn, sid),
            }
            _snapshot_progress(conn, sid)
        conn.commit()
    finally:
        release_connection(conn)

    # Evaluate feedback loops for any interventions that are now ≥14 days old.
    # Import here to avoid a circular dependency (intelligence imports db_adapter,
    # not automation, so this direction is safe).
    try:
        from backend import intelligence as _intel
        _intel.evaluate_feedback_loops()
    except Exception:
        pass  # never let a feedback error block the main automation run

    return results


def get_risk_summary() -> dict:
    conn = get_connection()
    try:
        academic   = qexec(conn, "SELECT academic_risk, COUNT(*) cnt FROM students WHERE status!='suspended' GROUP BY academic_risk").fetchall()
        attendance = qexec(conn, "SELECT attendance_risk, COUNT(*) cnt FROM students WHERE status!='suspended' GROUP BY attendance_risk").fetchall()
        payment    = qexec(conn, "SELECT payment_risk, COUNT(*) cnt FROM students WHERE status!='suspended' GROUP BY payment_risk").fetchall()
        alerts     = qexec(conn, """
            SELECT a.id, a.student_id, s.name, a.alert_type, a.message, a.created_at, a.resolved
            FROM automation_alerts a
            JOIN students s ON s.student_id = a.student_id
            WHERE a.resolved = 0 ORDER BY a.created_at DESC LIMIT 100
        """).fetchall()
        return {
            'academic':   {r['academic_risk']:   r['cnt'] for r in academic},
            'attendance': {r['attendance_risk']: r['cnt'] for r in attendance},
            'payment':    {r['payment_risk']:    r['cnt'] for r in payment},
            'alerts':     alerts,
        }
    finally:
        release_connection(conn)


def resolve_alert(alert_id: int):
    conn = get_connection()
    try:
        qexec(conn, f"UPDATE automation_alerts SET resolved=1 WHERE id={PH}", (alert_id,))
        conn.commit()
    finally:
        release_connection(conn)


def is_restricted(student_id: str) -> bool:
    conn = get_connection()
    try:
        row = fetchone(conn, f"SELECT payment_risk FROM students WHERE student_id={PH}", (student_id,))
        return bool(row and row.get('payment_risk') == 'restricted')
    finally:
        release_connection(conn)
