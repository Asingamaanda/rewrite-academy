"""
Rewrite Academy — Self-Running Automation Engine
=================================================
Three rules run automatically after every mark, attendance record, or payment:

  Rule 1 — Academic Risk
      weighted_average = SUM(score * weight) / SUM(weight)
      < 50%  → 'critical'
      50–59% → 'needs_support'
      60%+   → 'on_track'

  Rule 2 — Attendance Risk
      attendance rate over last 7 days < 75% → 'at_risk'

  Rule 3 — Payment Enforcement
      No paid payment for current month AND past the 15th → 'outstanding'
      Outstanding for > 7 days → 'restricted' (access blocked)

Progress snapshots are saved weekly per student for trend graphs.
"""

import sqlite3
from datetime import date, timedelta, datetime
from pathlib import Path

_DB_PATH = Path(__file__).parent.parent / "data" / "classdoodle.db"

# ── Thresholds ────────────────────────────────────────────────────────────────
ACADEMIC_CRITICAL_THRESHOLD  = 50   # < 50% → critical
ACADEMIC_WARN_THRESHOLD      = 60   # 50–59 → needs_support
ATTENDANCE_THRESHOLD         = 75   # < 75% last 7 days → at_risk
RESTRICT_AFTER_DAYS          = 7    # overdue > 7 days → restricted
PAYMENT_DUE_DAY              = 15   # fee due on the 15th of each month


def _conn():
    conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


# ─────────────────────────────────────────────────────────────────────────────
# ALERT LOGGER  (deduplicated: one alert per student + type + calendar day)
# ─────────────────────────────────────────────────────────────────────────────

def _log_alert(conn, student_id, alert_type, message):
    today = date.today().isoformat()
    existing = conn.execute(
        "SELECT id FROM automation_alerts "
        "WHERE student_id=? AND alert_type=? AND DATE(created_at)=?",
        (student_id, alert_type, today)
    ).fetchone()
    if not existing:
        conn.execute(
            "INSERT INTO automation_alerts (student_id, alert_type, message) VALUES (?,?,?)",
            (student_id, alert_type, message)
        )


# ─────────────────────────────────────────────────────────────────────────────
# RULE 1 — ACADEMIC RISK
# ─────────────────────────────────────────────────────────────────────────────

def _check_academic_risk(conn, student_id):
    """
    Compute weighted average.
    weight column added to assessments; falls back to equal weighting if all NULL.
    """
    row = conn.execute("""
        SELECT
            CASE
                WHEN SUM(COALESCE(weight, 0)) > 0
                THEN ROUND(
                    SUM((score * 1.0 / max_score) * 100 * COALESCE(weight, 1)) /
                    SUM(COALESCE(weight, 1)), 1)
                ELSE ROUND(AVG((score * 1.0 / max_score) * 100), 1)
            END AS weighted_avg,
            COUNT(*) AS assessment_count
        FROM assessments
        WHERE student_id = ?
    """, (student_id,)).fetchone()

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

    conn.execute(
        "UPDATE students SET academic_risk = ? WHERE student_id = ?",
        (risk, student_id)
    )

    if risk in ('critical', 'needs_support') and count > 0:
        _log_alert(
            conn, student_id, 'academic_risk',
            f"Weighted average is {avg:.1f}% — flagged as '{risk}'."
        )

    return {'avg': avg, 'risk': risk, 'assessments': count}


# ─────────────────────────────────────────────────────────────────────────────
# RULE 2 — ATTENDANCE RISK
# ─────────────────────────────────────────────────────────────────────────────

def _check_attendance_risk(conn, student_id):
    """Attendance rate across all sessions in the last 7 calendar days."""
    seven_days_ago = (date.today() - timedelta(days=7)).isoformat()

    row = conn.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) AS present
        FROM attendance
        WHERE student_id = ? AND date >= ?
    """, (student_id, seven_days_ago)).fetchone()

    if not row or not row['total']:
        return None

    rate    = round((row['present'] / row['total']) * 100, 1)
    at_risk = rate < ATTENDANCE_THRESHOLD

    conn.execute(
        "UPDATE students SET attendance_risk = ? WHERE student_id = ?",
        ('at_risk' if at_risk else 'ok', student_id)
    )

    if at_risk:
        _log_alert(
            conn, student_id, 'attendance_risk',
            f"Attendance last 7 days: {rate:.1f}% (threshold: {ATTENDANCE_THRESHOLD}%)."
        )

    return {'rate': rate, 'at_risk': at_risk}


# ─────────────────────────────────────────────────────────────────────────────
# RULE 3 — PAYMENT ENFORCEMENT
# ─────────────────────────────────────────────────────────────────────────────

def _check_payment_risk(conn, student_id):
    """
    1. If a paid record exists for this month → status = 'paid'  (clear risk)
    2. No paid record + today > due_day (15th) → 'outstanding'
    3. Outstanding for > RESTRICT_AFTER_DAYS → 'restricted'
    """
    today         = date.today()
    current_month = today.strftime('%Y-%m')
    due_date      = date(today.year, today.month, PAYMENT_DUE_DAY)

    paid = conn.execute(
        "SELECT id FROM payments WHERE student_id=? AND month_for=? AND status='paid' LIMIT 1",
        (student_id, current_month)
    ).fetchone()

    if paid:
        conn.execute(
            "UPDATE students SET payment_risk='paid' WHERE student_id=?",
            (student_id,)
        )
        return {'status': 'paid'}

    if today <= due_date:
        # Not yet due this month
        conn.execute(
            "UPDATE students SET payment_risk='pending' WHERE student_id=?",
            (student_id,)
        )
        return {'status': 'pending'}

    days_overdue = (today - due_date).days

    if days_overdue > RESTRICT_AFTER_DAYS:
        conn.execute(
            "UPDATE students SET payment_risk='restricted' WHERE student_id=?",
            (student_id,)
        )
        _log_alert(
            conn, student_id, 'payment_restricted',
            f"Payment overdue by {days_overdue} days. Subject access restricted."
        )
        return {'status': 'restricted', 'days_overdue': days_overdue}

    conn.execute(
        "UPDATE students SET payment_risk='outstanding' WHERE student_id=?",
        (student_id,)
    )
    _log_alert(
        conn, student_id, 'payment_overdue',
        f"No payment for {current_month}. Overdue by {days_overdue} days."
    )
    return {'status': 'outstanding', 'days_overdue': days_overdue}


# ─────────────────────────────────────────────────────────────────────────────
# PROGRESS SNAPSHOT  (weekly trend data)
# ─────────────────────────────────────────────────────────────────────────────

def _snapshot_progress(conn, student_id):
    """Save this ISO-week's weighted average for trend charts."""
    row = conn.execute("""
        SELECT
            CASE
                WHEN SUM(COALESCE(weight, 0)) > 0
                THEN ROUND(
                    SUM((score * 1.0 / max_score) * 100 * COALESCE(weight, 1)) /
                    SUM(COALESCE(weight, 1)), 1)
                ELSE ROUND(AVG((score * 1.0 / max_score) * 100), 1)
            END AS avg
        FROM assessments WHERE student_id = ?
    """, (student_id,)).fetchone()

    if not row or row['avg'] is None:
        return

    week = datetime.now().strftime('%Y-W%V')
    conn.execute(
        "INSERT OR REPLACE INTO progress_snapshots (student_id, week, average) VALUES (?,?,?)",
        (student_id, week, row['avg'])
    )


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────

def run_for_student(student_id: str) -> dict:
    """
    Run all three automation rules for a single student.
    Call this after saving any mark, attendance record, or payment.
    """
    conn = _conn()
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
        conn.close()


def run_all() -> dict:
    """
    Run automation for every non-suspended student.
    Call this from the daily /admin/run-automation endpoint.
    """
    conn = _conn()
    try:
        students = conn.execute(
            "SELECT student_id FROM students WHERE status != 'suspended'"
        ).fetchall()

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
        return results
    finally:
        conn.close()


def get_risk_summary() -> dict:
    """
    Return aggregated risk counts + unresolved alerts for the admin dashboard.
    """
    conn = _conn()
    try:
        academic   = conn.execute(
            "SELECT academic_risk, COUNT(*) cnt FROM students "
            "WHERE status != 'suspended' GROUP BY academic_risk"
        ).fetchall()
        attendance = conn.execute(
            "SELECT attendance_risk, COUNT(*) cnt FROM students "
            "WHERE status != 'suspended' GROUP BY attendance_risk"
        ).fetchall()
        payment    = conn.execute(
            "SELECT payment_risk, COUNT(*) cnt FROM students "
            "WHERE status != 'suspended' GROUP BY payment_risk"
        ).fetchall()

        alerts = conn.execute("""
            SELECT a.id, a.student_id, s.name, a.alert_type, a.message,
                   a.created_at, a.resolved
            FROM automation_alerts a
            JOIN students s ON s.student_id = a.student_id
            WHERE a.resolved = 0
            ORDER BY a.created_at DESC
            LIMIT 100
        """).fetchall()

        snapshots = conn.execute("""
            SELECT student_id, week, average
            FROM progress_snapshots
            ORDER BY student_id, week
        """).fetchall()

        return {
            'academic':   {r['academic_risk']:   r['cnt'] for r in academic},
            'attendance': {r['attendance_risk']:  r['cnt'] for r in attendance},
            'payment':    {r['payment_risk']:     r['cnt'] for r in payment},
            'alerts':     [dict(r) for r in alerts],
            'snapshots':  [dict(r) for r in snapshots],
        }
    finally:
        conn.close()


def resolve_alert(alert_id: int):
    """Mark an alert as resolved."""
    conn = _conn()
    try:
        conn.execute(
            "UPDATE automation_alerts SET resolved = 1 WHERE id = ?",
            (alert_id,)
        )
        conn.commit()
    finally:
        conn.close()


def is_restricted(student_id: str) -> bool:
    """
    Returns True if student's payment_risk = 'restricted'.
    Used by the student portal to block access gracefully.
    """
    conn = _conn()
    try:
        row = conn.execute(
            "SELECT payment_risk FROM students WHERE student_id = ?",
            (student_id,)
        ).fetchone()
        return row and row['payment_risk'] == 'restricted'
    finally:
        conn.close()
