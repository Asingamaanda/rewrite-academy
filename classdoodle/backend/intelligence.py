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
from backend.db_adapter import get_connection, release_connection, fetchall, fetchone, PH


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
    """Compare avg of last n assessments vs the n before that for a subject."""
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

    recent = rows[:n]
    prior  = rows[n:n * 2]
    if not prior:
        return None, None, None

    ra = round(sum(r['pct'] for r in recent) / len(recent), 1)
    pa = round(sum(r['pct'] for r in prior)  / len(prior),  1)
    return ra, pa, round(ra - pa, 1)


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
    Estimate probability (0–100) of passing a subject.

    Model:
        base       = current subject average
        att_bonus  = +10 if ≥80% attendance, +5 if 60–80%, -5 if <60%
        trend_bonus= up to ±10 (half of trend delta, clamped)
        clamped to [5, 97]

    Also returns improved_probability if attendance were brought to ≥80%.
    """
    conn = get_connection()
    try:
        row = fetchone(conn, f"""
            SELECT ROUND(AVG((score*1.0/NULLIF(max_score,0))*100), 1) AS avg
            FROM assessments
            WHERE student_id={PH} AND subject={PH}
        """, (student_id, subject))

        if not row or row['avg'] is None:
            return {'subject': subject, 'probability': None, 'status': 'no_data'}

        base = row['avg']
        att, _, _ = _attendance_window(conn, student_id)
        if att is None:
            att_bonus = 0
        elif att >= 80:
            att_bonus = 10
        elif att >= 60:
            att_bonus = 5
        else:
            att_bonus = -5

        _, _, trend_delta = _score_trend(conn, student_id, subject)
        trend_bonus = max(-10, min(10, (trend_delta or 0) * 0.5))

        prob = max(5, min(97, round(base + att_bonus + trend_bonus, 1)))

        improved_prob = None
        if att is not None and att < 80:
            improved_prob = max(5, min(97, round(base + 10 + trend_bonus, 1)))

        return {
            'subject':             subject,
            'current_avg':         round(base, 1),
            'probability':         prob,
            'improved_probability': improved_prob,
            'attendance_rate':     att,
            'status':              'pass' if prob >= 50 else 'at_risk',
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

        # ── Weekly performance trend ─────────────────────────────────────────
        trend = fetchall(conn, """
            SELECT week,
                   ROUND(AVG(average), 1) AS class_avg,
                   COUNT(DISTINCT student_id) AS student_count
            FROM progress_snapshots
            GROUP BY week
            ORDER BY week DESC
            LIMIT 8
        """)
        trend = list(reversed(trend))

        # ── Live alerts ──────────────────────────────────────────────────────
        alerts = fetchall(conn, """
            SELECT al.id, al.student_id, s.name, al.alert_type, al.message, al.created_at
            FROM automation_alerts al
            JOIN students s ON s.student_id = al.student_id
            WHERE al.resolved = 0
            ORDER BY al.created_at DESC
            LIMIT 12
        """)

        return {
            'total_students':    total_students,
            'subject_heatmap':   list(subject_heatmap),
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
            'alerts':            list(alerts),
        }
    finally:
        release_connection(conn)
