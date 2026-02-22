# -*- coding: utf-8 -*-
"""
intelligence.py
───────────────
Four-layer intelligence engine for Rewrite Academy.

  Layer 1  Observational  – behavioural metrics & narrative insights
  Layer 2  Predictive     – pass probability, dropout risk score
  Layer 3  Prescriptive   – ranked action recommendations
  Layer 4  Automation     – hooks into automation.py; here we surface
                            the aggregated picture for the dashboard

All functions are stateless and pool-safe: they acquire + release their
own connection.  Nothing is cached – call as needed from the route.
"""

from datetime import date, timedelta
import json
from backend.db_adapter import get_connection, release_connection, fetchall, fetchone, qexec, PH


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _attendance_window(conn, student_id, days=14):
    """Return (recent_rate, prior_rate, delta) for two consecutive windows."""
    today = date.today()
    mid   = today - timedelta(days=days)
    start = today - timedelta(days=days * 2)

    def _rate(row):
        if row and row['total']:
            return round((row['present'] / row['total']) * 100, 1)
        return None

    recent = fetchone(conn, f"""
        SELECT COUNT(*) total,
               SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) present
        FROM attendance
        WHERE student_id={PH} AND date>{PH} AND date<={PH}
    """, (student_id, mid.isoformat(), today.isoformat()))

    prior = fetchone(conn, f"""
        SELECT COUNT(*) total,
               SUM(CASE WHEN status='present' THEN 1 ELSE 0 END) present
        FROM attendance
        WHERE student_id={PH} AND date>{PH} AND date<={PH}
    """, (student_id, start.isoformat(), mid.isoformat()))

    r = _rate(recent)
    p = _rate(prior)
    delta = round(r - p, 1) if (r is not None and p is not None) else None
    return r, p, delta


def _score_trend(conn, student_id, subject=None, n=3):
    """Compare recency-weighted avg of last n vs prior n (EWMA-smoothed points)."""
    where  = f"student_id={PH}"
    params = [student_id]
    if subject:
        where  += f" AND subject={PH}"
        params.append(subject)

    rows = fetchall(conn, f"""
        SELECT (score * 1.0 / NULLIF(max_score, 0)) * 100 AS pct
        FROM assessments
        WHERE {where}
        ORDER BY date DESC, id DESC
        LIMIT {n * 2}
    """, tuple(params))

    if len(rows) < 2:
        return None, None, None

    vals = [r['pct'] for r in rows if r['pct'] is not None]
    smoothed = _ewma(list(reversed(vals)))   # chronological order for EWMA
    smoothed = list(reversed(smoothed))      # back to newest-first

    recent = smoothed[:n]
    prior  = smoothed[n:n * 2]
    if not prior:
        return None, None, None

    ra = round(sum(recent) / len(recent), 1)
    pa = round(sum(prior)  / len(prior),  1)
    return ra, pa, round(ra - pa, 1)


# ── Smoothing utilities ───────────────────────────────────────────────────────

def _linear_slope(pairs: list) -> float:
    """
    Ordinary least-squares slope for a list of (x, y) pairs.
    Returns slope in y-units per x-unit, or 0.0 if < 2 points.
    """
    n = len(pairs)
    if n < 2:
        return 0.0
    sx  = sum(x for x, _ in pairs)
    sy  = sum(y for _, y in pairs)
    sxy = sum(x * y for x, y in pairs)
    sxx = sum(x * x for x, _ in pairs)
    denom = n * sxx - sx * sx
    return 0.0 if denom == 0 else (n * sxy - sx * sy) / denom


def _ewma(values: list, alpha: float = 0.35) -> list:
    """
    Exponential weighted moving average (oldest → newest order).
    Higher alpha = more weight on recent observations.
    """
    if not values:
        return []
    result = [values[0]]
    for v in values[1:]:
        result.append(alpha * v + (1 - alpha) * result[-1])
    return result


def _score_slope(conn, student_id: str, subject: str = None) -> float:
    """
    Linear regression slope (percentage-points per assessment) over all
    chronological scores.  Positive = improving, negative = declining.
    """
    where  = f"student_id={PH}"
    params = [student_id]
    if subject:
        where  += f" AND subject={PH}"
        params.append(subject)

    rows = fetchall(conn, f"""
        SELECT (score * 1.0 / NULLIF(max_score, 0)) * 100 AS pct
        FROM assessments
        WHERE {where}
        ORDER BY date ASC, id ASC
    """, tuple(params))

    if len(rows) < 2:
        return 0.0
    pairs = [(i + 1, r['pct']) for i, r in enumerate(rows) if r['pct'] is not None]
    return round(_linear_slope(pairs), 3)


def _recency_weighted_avg(conn, student_id: str, subject: str = None) -> float | None:
    """
    Weighted average where the most recent assessment counts 2× more than
    the oldest.  Returns None if no data.
    """
    where  = f"student_id={PH}"
    params = [student_id]
    if subject:
        where  += f" AND subject={PH}"
        params.append(subject)

    rows = fetchall(conn, f"""
        SELECT (score * 1.0 / NULLIF(max_score, 0)) * 100 AS pct
        FROM assessments
        WHERE {where}
        ORDER BY date ASC, id ASC
    """, tuple(params))

    pts = [r['pct'] for r in rows if r['pct'] is not None]
    if not pts:
        return None
    n = len(pts)
    # weight rises linearly from 1 (oldest) to 2 (newest)
    weights = [1 + i / max(n - 1, 1) for i in range(n)]
    return round(sum(w * v for w, v in zip(weights, pts)) / sum(weights), 1)


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 1 — OBSERVATIONAL INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def get_student_insights(student_id: str) -> list:
    """
    Return a list of narrative insight dicts for one student.
    Each dict: { level: 'info'|'warning'|'critical', category, message, delta }
    """
    conn = get_connection()
    try:
        insights = []
        student  = fetchone(conn,
            f"SELECT name, academic_risk, attendance_risk, payment_risk FROM students WHERE student_id={PH}",
            (student_id,))
        if not student:
            return []

        first = student['name'].split()[0]

        # ── Attendance ──────────────────────────────────────────────────────
        att, _, att_delta = _attendance_window(conn, student_id)
        if att is not None:
            if att < 60:
                insights.append({'level': 'critical', 'category': 'attendance',
                    'message': f"{first} attended only {att}% of sessions in the last 2 weeks.",
                    'delta': att_delta})
            elif att < 75:
                insights.append({'level': 'warning', 'category': 'attendance',
                    'message': f"{first}'s attendance is {att}% — below the 75% threshold.",
                    'delta': att_delta})
            if att_delta is not None and att_delta < -10:
                insights.append({'level': 'warning', 'category': 'attendance',
                    'message': f"{first}'s attendance dropped {abs(att_delta):.0f}% vs the previous 2 weeks.",
                    'delta': att_delta})

        # ── Per-subject score trends ─────────────────────────────────────────
        subj_rows = fetchall(conn,
            f"SELECT subject FROM student_subjects WHERE student_id={PH}", (student_id,))
        for row in subj_rows:
            subj = row['subject']
            recent_s, _, s_delta = _score_trend(conn, student_id, subj)
            if s_delta is not None:
                if s_delta <= -10:
                    insights.append({'level': 'warning', 'category': 'academic',
                        'message': f"{subj} performance dropped {abs(s_delta):.0f}% over last 3 assessments.",
                        'delta': s_delta})
                elif s_delta >= 10:
                    insights.append({'level': 'info', 'category': 'academic',
                        'message': f"{subj} improving — up {s_delta:.0f}% over last 3 assessments.",
                        'delta': s_delta})
            if recent_s is not None and recent_s < 50:
                insights.append({'level': 'critical', 'category': 'academic',
                    'message': f"{first} averaging {recent_s:.0f}% in {subj} — intervention required.",
                    'delta': s_delta})

        # ── Payment ──────────────────────────────────────────────────────────
        pr = student['payment_risk']
        if pr == 'restricted':
            insights.append({'level': 'critical', 'category': 'payment',
                'message': f"{first}'s account is restricted due to outstanding payment.", 'delta': None})
        elif pr == 'outstanding':
            insights.append({'level': 'warning', 'category': 'payment',
                'message': f"{first} has an outstanding balance this month.", 'delta': None})

        return insights
    finally:
        release_connection(conn)


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 2 — PREDICTIVE INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def predict_pass_probability(student_id: str, subject: str) -> dict:
    """
    Enhanced subject-level predictive model.

    Components
    ----------
    base          recency-weighted average (recent assessments count 2x more)
    att_bonus     +12 / +5 / 0 / -8  based on attendance band
    slope_bonus   regression slope x 3, clamped +/-15
                  (captures trajectory better than a single window delta)
    confidence    shrinks outlier predictions when n < 4 assessments
                  (pulls estimate toward 50 with factor = n/4, max 1.0)
    improved      what-if with perfect attendance (+12 bonus)

    Result clamped [3, 97].
    """
    conn = get_connection()
    try:
        rows = fetchall(conn, f"""
            SELECT (score * 1.0 / NULLIF(max_score, 0)) * 100 AS pct
            FROM assessments
            WHERE student_id={PH} AND subject={PH}
            ORDER BY date ASC, id ASC
        """, (student_id, subject))

        pts = [r['pct'] for r in rows if r['pct'] is not None]
        if not pts:
            return {'subject': subject, 'probability': None, 'status': 'no_data',
                    'n_assessments': 0}

        n      = len(pts)
        # Recency-weighted average
        weights = [1 + i / max(n - 1, 1) for i in range(n)]
        base   = sum(w * v for w, v in zip(weights, pts)) / sum(weights)

        # Attendance bonus
        att, _, _ = _attendance_window(conn, student_id)
        if att is None:
            att_bonus = 0
        elif att >= 85:
            att_bonus = 12
        elif att >= 70:
            att_bonus = 5
        elif att >= 55:
            att_bonus = 0
        else:
            att_bonus = -8

        # Slope bonus — linear regression over all assessments
        slope     = _score_slope(conn, student_id, subject)
        slope_bonus = max(-15, min(15, slope * 3))

        # Confidence shrinkage: pulls toward 50 when few data points
        confidence  = min(1.0, n / 4.0)
        raw_prob    = base + att_bonus + slope_bonus
        prob        = 50 + confidence * (raw_prob - 50)
        prob        = max(3, min(97, round(prob, 1)))

        # What-if improved attendance
        improved_prob = None
        if att is not None and att < 85:
            raw_imp    = base + 12 + slope_bonus
            imp        = 50 + confidence * (raw_imp - 50)
            improved_prob = max(3, min(97, round(imp, 1)))

        # EWMA-smoothed score series for the caller to display
        smoothed_series = [round(v, 1) for v in _ewma(pts)]

        return {
            'subject':              subject,
            'current_avg':          round(base, 1),
            'probability':          prob,
            'improved_probability': improved_prob,
            'attendance_rate':      att,
            'slope':                slope,
            'n_assessments':        n,
            'smoothed_series':      smoothed_series,
            'status':               'pass' if prob >= 50 else 'at_risk',
        }
    finally:
        release_connection(conn)


def predict_dropout_risk(student_id: str) -> dict:
    """
    Composite dropout risk score (0–100).
    academic critical → +40, needs_support → +20
    attendance at_risk → +30
    payment restricted → +30, outstanding → +15, pending → +5
    """
    conn = get_connection()
    try:
        student = fetchone(conn,
            f"SELECT academic_risk, attendance_risk, payment_risk FROM students WHERE student_id={PH}",
            (student_id,))
        if not student:
            return {'score': 0, 'level': 'low'}

        score  = 0
        score += {'critical': 40, 'needs_support': 20, 'on_track': 0}.get(student['academic_risk'],   0)
        score += {'at_risk':  30, 'ok': 0}.get(student['attendance_risk'], 0)
        score += {'restricted': 30, 'outstanding': 15, 'pending': 5, 'paid': 0}.get(student['payment_risk'], 0)
        score  = min(100, score)
        level  = ('critical' if score >= 70 else
                  'high'     if score >= 40 else
                  'medium'   if score >= 20 else 'low')
        return {'score': score, 'level': level}
    finally:
        release_connection(conn)


def predict_all_subjects(student_id: str) -> dict:
    """
    Run predict_pass_probability for every enrolled subject.
    Returns a dict keyed by subject name, sorted by probability ASC
    (lowest / most at-risk first).
    """
    conn = get_connection()
    try:
        subjects = fetchall(conn,
            f"SELECT subject FROM student_subjects WHERE student_id={PH}",
            (student_id,))
    finally:
        release_connection(conn)

    results = {
        row['subject']: predict_pass_probability(student_id, row['subject'])
        for row in subjects
    }
    return dict(sorted(
        results.items(),
        key=lambda kv: (kv[1].get('probability') or 99)
    ))


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3 — PRESCRIPTIVE INTELLIGENCE
# ─────────────────────────────────────────────────────────────────────────────

def get_recommendations(student_id: str) -> list:
    """
    Return prioritised action recommendations for admin.
    Each item: { priority, type, action, message, icon }
    """
    conn = get_connection()
    try:
        student = fetchone(conn,
            f"SELECT name, academic_risk, attendance_risk, payment_risk FROM students WHERE student_id={PH}",
            (student_id,))
        if not student:
            return []

        first = student['name'].split()[0]
        recs  = []

        # Attendance recommendations
        att, _, att_delta = _attendance_window(conn, student_id)
        if att is not None and att < 75:
            recs.append({'priority': 'high', 'type': 'attendance', 'action': 'send_reminder',
                'message': f"Send attendance reminder to {first} — currently {att}%.",
                'icon': '📲'})
        if att_delta is not None and att_delta < -15:
            recs.append({'priority': 'high', 'type': 'attendance', 'action': 'one_on_one',
                'message': f"Schedule one-on-one with {first} — attendance fell {abs(att_delta):.0f}% this fortnight.",
                'icon': '🧑‍🏫'})

        # Per-subject academic recommendations
        subj_rows = fetchall(conn,
            f"SELECT subject FROM student_subjects WHERE student_id={PH}", (student_id,))
        for row in subj_rows:
            subj = row['subject']
            avg_row = fetchone(conn, f"""
                SELECT ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) avg
                FROM assessments WHERE student_id={PH} AND subject={PH}
            """, (student_id, subj))
            if avg_row and avg_row['avg'] is not None:
                avg = avg_row['avg']
                if avg < 50:
                    recs.append({'priority': 'high', 'type': 'academic', 'action': 'extra_session',
                        'message': f"Schedule extra {subj} session for {first} — averaging {avg:.0f}%.",
                        'icon': '📚'})
                    recs.append({'priority': 'medium', 'type': 'academic', 'action': 'recommend_video',
                        'message': f"Recommend {subj} revision videos for {first}.",
                        'icon': '🎬'})
                elif avg < 60:
                    recs.append({'priority': 'medium', 'type': 'academic', 'action': 'motivational_nudge',
                        'message': f"Send motivational message to {first} about {subj} ({avg:.0f}%).",
                        'icon': '💬'})

        # Payment
        if student['payment_risk'] in ('outstanding', 'restricted'):
            recs.append({'priority': 'high', 'type': 'payment', 'action': 'payment_followup',
                'message': f"Follow up with {first} regarding outstanding payment.",
                'icon': '💳'})

        recs.sort(key=lambda r: {'high': 0, 'medium': 1, 'low': 2}.get(r['priority'], 9))
        return recs
    finally:
        release_connection(conn)


# ─────────────────────────────────────────────────────────────────────────────
# LAYER 3.5 — INTERVENTION IMPACT TRACKING  &  FEEDBACK LOOPS
# ─────────────────────────────────────────────────────────────────────────────

def log_intervention(student_id: str, rec_type: str, rec_action: str,
                     note: str = '', alert_id: int = None) -> int:
    """
    Record that an admin acted on a recommendation.

    Snapshots the student's current attendance rate and overall avg score
    so we can compare them after 14 days to measure impact.

    Returns the new intervention_log.id.
    """
    conn = get_connection()
    try:
        att, _, _ = _attendance_window(conn, student_id)
        avg_row   = fetchone(conn, f"""
            SELECT ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) AS avg
            FROM assessments WHERE student_id={PH}
        """, (student_id,))
        snapshot = json.dumps({
            'attendance': att,
            'avg_score':  avg_row['avg'] if avg_row else None,
        })
        qexec(conn, f"""
            INSERT INTO intervention_log
                (student_id, alert_id, rec_type, rec_action, note, metric_snapshot)
            VALUES ({PH},{PH},{PH},{PH},{PH},{PH})
        """, (student_id, alert_id, rec_type, rec_action, note, snapshot))
        row = fetchone(conn,
            "SELECT last_insert_rowid() AS id" if not _is_postgres() else
            f"SELECT id FROM intervention_log WHERE student_id={PH} ORDER BY created_at DESC LIMIT 1",
            () if not _is_postgres() else (student_id,))
        return row['id'] if row else None
    finally:
        release_connection(conn)


def _is_postgres():
    """Check if we're running on PostgreSQL (vs SQLite)."""
    try:
        from backend.db_adapter import POSTGRES
        return POSTGRES
    except ImportError:
        return False


def get_intervention_history(student_id: str) -> list:
    """
    Return all logged interventions for a student, newest first,
    with outcome and metric delta fields populated if evaluated.
    """
    conn = get_connection()
    try:
        rows = fetchall(conn, f"""
            SELECT id, rec_type, rec_action, note, metric_snapshot,
                   outcome, evaluated_at, created_at
            FROM intervention_log
            WHERE student_id={PH}
            ORDER BY created_at DESC
        """, (student_id,))
        result = []
        for r in rows:
            d = dict(r)
            snap = json.loads(r['metric_snapshot'] or '{}')
            d['snapshot_attendance'] = snap.get('attendance')
            d['snapshot_avg']        = snap.get('avg_score')
            result.append(d)
        return result
    finally:
        release_connection(conn)


def evaluate_feedback_loops() -> int:
    """
    Called by automation.run_all() or on a schedule.

    For every intervention that is ≥14 days old and has no outcome yet,
    compares the *current* attendance rate and avg score against the
    snapshot taken at intervention time, then writes one of:
        'improved'   — at least one metric improved meaningfully
        'no_change'  — metrics stable
        'declined'   — metrics worsened overall

    Returns the number of interventions evaluated this run.
    """
    conn = get_connection()
    evaluated = 0
    try:
        cutoff  = (date.today() - timedelta(days=14)).isoformat()
        pending = fetchall(conn, f"""
            SELECT id, student_id, metric_snapshot, rec_type
            FROM intervention_log
            WHERE outcome IS NULL AND created_at <= {PH}
        """, (cutoff,))

        for row in pending:
            snap    = json.loads(row['metric_snapshot'] or '{}')
            old_att = snap.get('attendance')
            old_avg = snap.get('avg_score')

            att, _, _ = _attendance_window(conn, row['student_id'])
            avg_row   = fetchone(conn, f"""
                SELECT ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) AS avg
                FROM assessments WHERE student_id={PH}
            """, (row['student_id'],))
            new_avg  = avg_row['avg'] if avg_row else None

            improvements = 0
            declines     = 0

            if att is not None and old_att is not None:
                if att >= old_att + 5:
                    improvements += 1
                elif att <= old_att - 7:
                    declines += 1

            if new_avg is not None and old_avg is not None:
                if new_avg >= old_avg + 3:
                    improvements += 1
                elif new_avg <= old_avg - 5:
                    declines += 1

            if improvements > 0 and improvements >= declines:
                outcome = 'improved'
            elif declines > improvements:
                outcome = 'declined'
            else:
                outcome = 'no_change'

            qexec(conn, f"""
                UPDATE intervention_log
                SET outcome={PH}, evaluated_at=CURRENT_TIMESTAMP
                WHERE id={PH}
            """, (outcome, row['id']))
            evaluated += 1

        return evaluated
    finally:
        release_connection(conn)


def get_feedback_summary() -> dict:
    """
    Aggregate outcome counts for the feedback loop panel.
    Returns: { improved, no_change, declined, pending }
    """
    conn = get_connection()
    try:
        rows = fetchall(conn, """
            SELECT outcome, COUNT(*) cnt
            FROM intervention_log
            GROUP BY outcome
        """)
        counts = {r['outcome']: r['cnt'] for r in rows}
        return {
            'improved':  counts.get('improved',  0),
            'no_change': counts.get('no_change', 0),
            'declined':  counts.get('declined',  0),
            'pending':   counts.get(None,         0) + counts.get('None', 0),
            'total':     sum(counts.values()),
        }
    finally:
        release_connection(conn)


# ─────────────────────────────────────────────────────────────────────────────
# DASHBOARD AGGREGATES  (feeds the intelligence dashboard)
# ─────────────────────────────────────────────────────────────────────────────

def get_dashboard_intelligence() -> dict:
    """
    Single call that returns everything needed by the intelligence dashboard:
      subject_heatmap, risk counts, revenue stability, top performers,
      intervention list, weekly performance trend, live alerts.
    """
    conn = get_connection()
    try:
        today         = date.today()
        current_month = today.strftime('%Y-%m')

        # ── Subject heatmap ──────────────────────────────────────────────────
        subject_heatmap = fetchall(conn, """
            SELECT subject,
                   ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) AS avg_pct,
                   COUNT(*) AS entry_count
            FROM assessments
            GROUP BY subject
            ORDER BY avg_pct ASC
        """)

        # ── Risk distribution ────────────────────────────────────────────────
        risk_rows = fetchall(conn, """
            SELECT academic_risk, attendance_risk, payment_risk, COUNT(*) cnt
            FROM students
            WHERE status != 'suspended'
            GROUP BY academic_risk, attendance_risk, payment_risk
        """)
        academic_counts   = {}
        attendance_counts = {}
        payment_counts    = {}
        for r in risk_rows:
            n = r['cnt']
            academic_counts[r['academic_risk']]     = academic_counts.get(r['academic_risk'], 0)     + n
            attendance_counts[r['attendance_risk']] = attendance_counts.get(r['attendance_risk'], 0) + n
            payment_counts[r['payment_risk']]       = payment_counts.get(r['payment_risk'], 0)       + n

        total_students = sum(academic_counts.values())

        # ── Revenue stability ────────────────────────────────────────────────
        rev = fetchone(conn, f"""
            SELECT
                SUM(CASE WHEN status='paid' AND month_for={PH} THEN amount ELSE 0 END) AS collected,
                SUM(CASE WHEN month_for={PH} THEN amount ELSE 0 END) AS expected
            FROM payments WHERE month_for={PH}
        """, (current_month, current_month, current_month))
        collected       = (rev['collected'] or 0) if rev else 0
        expected        = (rev['expected']  or 0) if rev else 0
        collection_rate = round(collected / expected * 100, 1) if expected > 0 else 0

        # ── Top performers ───────────────────────────────────────────────────
        top_performers = fetchall(conn, """
            SELECT s.student_id, s.name,
                   ROUND(AVG((a.score*1.0/NULLIF(a.max_score,0))*100), 1) AS avg_pct
            FROM students s
            JOIN assessments a ON a.student_id = s.student_id
            WHERE s.status != 'suspended'
            GROUP BY s.student_id, s.name
            HAVING COUNT(a.id) >= 2
            ORDER BY avg_pct DESC
            LIMIT 5
        """)

        # ── Students needing intervention ────────────────────────────────────
        intervention = fetchall(conn, """
            SELECT s.student_id, s.name,
                   s.academic_risk, s.attendance_risk, s.payment_risk,
                   ROUND(AVG((a.score*1.0/NULLIF(a.max_score,0))*100), 1) AS avg_pct
            FROM students s
            LEFT JOIN assessments a ON a.student_id = s.student_id
            WHERE s.status != 'suspended'
              AND (s.academic_risk IN ('critical','needs_support')
                OR s.attendance_risk = 'at_risk'
                OR s.payment_risk    IN ('outstanding','restricted'))
            GROUP BY s.student_id, s.name,
                     s.academic_risk, s.attendance_risk, s.payment_risk
            ORDER BY avg_pct ASC NULLS LAST
            LIMIT 8
        """)

        # Attach first insight to each intervention student
        intervention_with_insights = []
        for st in intervention:
            conn2 = get_connection()
            try:
                first_insight = None
                att, _, att_d = _attendance_window(conn2, st['student_id'])
                avg = st['avg_pct']
                if st['academic_risk'] == 'critical' and avg is not None:
                    first_insight = f"Averaging {avg:.0f}% — critical academic risk."
                elif st['attendance_risk'] == 'at_risk' and att is not None:
                    first_insight = f"Attendance at {att}% — below threshold."
                elif st['payment_risk'] in ('outstanding', 'restricted'):
                    first_insight = "Outstanding payment — account at risk of restriction."
                row_dict = dict(st)
                row_dict['insight'] = first_insight
                intervention_with_insights.append(row_dict)
            finally:
                release_connection(conn2)

        # ── Weekly performance trend (EWMA-smoothed) ────────────────────────
        trend_raw = fetchall(conn, """
            SELECT week,
                   ROUND(AVG(average), 1) AS class_avg,
                   COUNT(DISTINCT student_id) AS student_count
            FROM progress_snapshots
            GROUP BY week
            ORDER BY week DESC
            LIMIT 10
        """)
        trend_raw = list(reversed(trend_raw))
        if trend_raw:
            raw_avgs   = [float(r['class_avg'] or 0) for r in trend_raw]
            smoothed   = _ewma(raw_avgs, alpha=0.4)
            trend = [
                {**dict(r),
                 'smoothed_avg': round(smoothed[i], 1),
                 'raw_avg':      round(raw_avgs[i], 1)}
                for i, r in enumerate(trend_raw)
            ]
            # Overall class slope across weeks
            class_slope = round(_linear_slope([(i + 1, v) for i, v in enumerate(raw_avgs)]), 3)
        else:
            trend       = []
            class_slope = 0.0

        # ── Subject heatmap — enriched with per-subject slope ────────────────
        heatmap_raw = fetchall(conn, """
            SELECT subject,
                   ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) AS avg_pct,
                   COUNT(*) AS entry_count
            FROM assessments
            GROUP BY subject
            ORDER BY avg_pct ASC
        """)
        subject_heatmap = []
        for row in heatmap_raw:
            subj_slope = round(_linear_slope([
                (i + 1, r['pct'])
                for i, r in enumerate(
                    fetchall(conn, f"""
                        SELECT (score*1.0/NULLIF(max_score,0))*100 AS pct
                        FROM assessments WHERE subject={PH}
                        ORDER BY date ASC, id ASC
                    """, (row['subject'],))
                )
                if r['pct'] is not None
            ]), 3)
            subject_heatmap.append({**dict(row), 'slope': subj_slope})

        # ── Live alerts ──────────────────────────────────────────────────────
        alerts = fetchall(conn, """
            SELECT al.id, al.student_id, s.name, al.alert_type, al.message, al.created_at
            FROM automation_alerts al
            JOIN students s ON s.student_id = al.student_id
            WHERE al.resolved = 0
            ORDER BY al.created_at DESC
            LIMIT 12
        """)

        # ── Feedback loop summary ────────────────────────────────────────────
        fb_rows = fetchall(conn, """
            SELECT outcome, COUNT(*) cnt
            FROM intervention_log
            GROUP BY outcome
        """)
        fb_counts = {r['outcome']: r['cnt'] for r in fb_rows}
        feedback = {
            'improved':  fb_counts.get('improved',  0),
            'no_change': fb_counts.get('no_change', 0),
            'declined':  fb_counts.get('declined',  0),
            'pending':   fb_counts.get(None,         0) + fb_counts.get('None', 0),
            'total':     sum(fb_counts.values()),
        }

        return {
            'total_students':    total_students,
            'subject_heatmap':   subject_heatmap,
            'risk': {
                'academic':   academic_counts,
                'attendance': attendance_counts,
                'payment':    payment_counts,
            },
            'revenue': {
                'collected':       round(collected, 2),
                'expected':        round(expected, 2),
                'collection_rate': collection_rate,
            },
            'top_performers':    list(top_performers),
            'intervention':      intervention_with_insights,
            'performance_trend': trend,
            'class_slope':       class_slope,
            'alerts':            list(alerts),
            'feedback':          feedback,
        }
    finally:
        release_connection(conn)
