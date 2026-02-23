"""
ClassDoodle - Matric Rewrite School Timetable Generator
7:00 AM - 1:00 PM Daily Schedule
Includes intelligent smart-schedule generator with variable subject frequencies.
"""

from datetime import datetime, timedelta
from collections import Counter
import json

# ========== MATRIC SUBJECTS ==========
# periods_per_week = NSC-aligned default weekly contact frequency
CORE_SUBJECTS = {
    "English":               {"periods_per_week": 5, "color": "#45B7D1"},
    "Life Sciences":         {"periods_per_week": 5, "color": "#96CEB4"},
    "Math Lit":              {"periods_per_week": 5, "color": "#FDCB6E"},
    "Business Studies":      {"periods_per_week": 4, "color": "#A29BFE"},
    "Geography":             {"periods_per_week": 4, "color": "#55EFC4"},
    "History":               {"periods_per_week": 4, "color": "#FAB1A0"},
    "Physical Sciences":     {"periods_per_week": 5, "color": "#74B9FF"},
    "Mathematics":           {"periods_per_week": 5, "color": "#FF6B6B"},
    "Economics":             {"periods_per_week": 4, "color": "#FFEAA7"},
    "EGD":                   {"periods_per_week": 3, "color": "#B2BEC3"},
    "Agriculture":           {"periods_per_week": 3, "color": "#6AB04C"},
    "Hospitality Studies":   {"periods_per_week": 3, "color": "#E84393"},
    "Technical Mathematics": {"periods_per_week": 5, "color": "#F0932B"},
    "Technical Sciences":    {"periods_per_week": 5, "color": "#686DE0"},
    "Afrikaans":             {"periods_per_week": 3, "color": "#FD79A8"},
    "Zulu":                  {"periods_per_week": 3, "color": "#BADC58"},
    "Xhosa":                 {"periods_per_week": 3, "color": "#E17055"},
    "Setswana":              {"periods_per_week": 3, "color": "#FDCB6E"},
}

# ========== SUBJECT DEFAULT PERIODS (for smart generator UI) ==========
SUBJECT_DEFAULT_FREQS = {s: v["periods_per_week"] for s, v in CORE_SUBJECTS.items()}

# ========== TIME SLOT MAPPING (period number → time range) ==========
PERIOD_TIMES = {
    1: ("07:00", "07:50"),
    2: ("07:50", "08:40"),
    3: ("09:00", "09:50"),   # after tea break
    4: ("09:50", "10:40"),
    5: ("10:40", "11:30"),
    6: ("11:30", "12:20"),
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
PERIODS_PER_DAY = 6
TOTAL_SLOTS = len(DAYS) * PERIODS_PER_DAY  # 30


# ========== INTELLIGENT TIMETABLE GENERATOR ==========

def _spread_across_days(freq: int, n_days: int = 5) -> list:
    """Distribute freq periods across n_days as evenly as possible."""
    base, extra = divmod(freq, n_days)
    return [base + (1 if i < extra else 0) for i in range(n_days)]


def _reorder_no_consecutive(pool: list) -> list:
    """
    Given a list of subjects for one day, reorder so no two consecutive
    periods are the same subject.  Uses a greedy most-remaining approach.
    """
    counts = Counter(pool)
    result = []
    prev = None
    while counts:
        # Prefer subjects that are not the same as the previous period
        candidates = [(s, c) for s, c in counts.items() if s != prev]
        if not candidates:
            # Forced repeat — unavoidable (e.g. only one subject left)
            candidates = list(counts.items())
        chosen = max(candidates, key=lambda x: x[1])[0]
        result.append(chosen)
        counts[chosen] -= 1
        if counts[chosen] == 0:
            del counts[chosen]
        prev = chosen
    return result


def generate_smart_timetable(subjects_freq: dict) -> dict:
    """
    Intelligent weekly timetable generator.
    subjects_freq — {subject_name: periods_per_week, ...}
    e.g. {'Mathematics': 5, 'Life Sciences': 5, 'Agriculture': 3, 'English': 3}

    Rules:
    - Each subject gets exactly subjects_freq[subject] periods spread across 5 days.
    - No two consecutive periods on the same day are the same subject (where possible).
    - Remaining slots (if total < 30) are filled with 'Revision'.
    - If total > 30 the frequencies are proportionally scaled down.

    Returns:
        {day: [(period, subject, time_from, time_to), ...], ...}
    """
    freq = {s: f for s, f in subjects_freq.items() if f > 0}
    total_req = sum(freq.values())

    # Scale down if over-allocated
    if total_req > TOTAL_SLOTS:
        scale = TOTAL_SLOTS / total_req
        freq = {s: max(1, round(f * scale)) for s, f in freq.items()}
        # Trim/pad to exactly TOTAL_SLOTS
        diff = sum(freq.values()) - TOTAL_SLOTS
        for s in sorted(freq, key=lambda x: -freq[x]):
            if diff <= 0:
                break
            freq[s] = max(1, freq[s] - 1)
            diff -= 1

    # Fill remaining with Revision
    remaining = TOTAL_SLOTS - sum(freq.values())
    if remaining > 0:
        freq['Revision'] = remaining

    # Spread each subject evenly across 5 days → per-day pools
    day_pools = {day: [] for day in DAYS}
    for subj, f in freq.items():
        counts = _spread_across_days(f, len(DAYS))
        for i, day in enumerate(DAYS):
            day_pools[day].extend([subj] * counts[i])

    # Reorder each day's pool for no consecutive duplicates
    schedule = {}
    for day in DAYS:
        ordered = _reorder_no_consecutive(day_pools[day])
        schedule[day] = [
            (p, ordered[p - 1], PERIOD_TIMES[p][0], PERIOD_TIMES[p][1])
            for p in range(1, PERIODS_PER_DAY + 1)
            if (p - 1) < len(ordered)
        ]
    return schedule

# ========== TIME SLOTS (7:00 AM - 1:00 PM) ==========
TIME_SLOTS = [
    {"start": "07:00", "end": "07:50", "duration": 50, "type": "period"},
    {"start": "07:50", "end": "08:40", "duration": 50, "type": "period"},
    {"start": "08:40", "end": "09:00", "duration": 20, "type": "break"},  # Tea break
    {"start": "09:00", "end": "09:50", "duration": 50, "type": "period"},
    {"start": "09:50", "end": "10:40", "duration": 50, "type": "period"},
    {"start": "10:40", "end": "11:30", "duration": 50, "type": "period"},
    {"start": "11:30", "end": "12:20", "duration": 50, "type": "period"},
    {"start": "12:20", "end": "13:00", "duration": 40, "type": "wrap-up"}  # Review/Q&A
]

# ========== WEEKLY TIMETABLE ==========
WEEKLY_SCHEDULE = {
    "Monday": [
        "Mathematics",        # 07:00-07:50
        "English",            # 07:50-08:40
        # BREAK 08:40-09:00
        "Life Sciences",      # 09:00-09:50
        "Geography",          # 09:50-10:40
        "Physical Sciences",  # 10:40-11:30
        "Business Studies",   # 11:30-12:20
        "Past Papers Practice"  # 12:20-13:00
    ],
    "Tuesday": [
        "Mathematics",
        "Physical Sciences",
        # BREAK
        "English",
        "History",
        "Life Sciences",
        "Economics",
        "Exam Prep Session"
    ],
    "Wednesday": [
        "Math Lit",
        "English",
        # BREAK
        "Geography",
        "Business Studies",
        "EGD",
        "Mathematics",
        "Study Skills Workshop"
    ],
    "Thursday": [
        "Life Sciences",
        "Mathematics",
        # BREAK
        "Physical Sciences",
        "English",
        "History",
        "Economics",
        "Past Papers Practice"
    ],
    "Friday": [
        "Mathematics",
        "Math Lit",
        # BREAK
        "Life Sciences",
        "Geography",
        "Physical Sciences",
        "EGD",
        "Weekly Review & Goal Setting"
    ]
}


def generate_daily_timetable(day):
    """Generate formatted timetable for a specific day"""
    if day not in WEEKLY_SCHEDULE:
        return None
    
    schedule = WEEKLY_SCHEDULE[day]
    timetable = []
    
    period_index = 0
    for slot in TIME_SLOTS:
        if slot["type"] == "break":
            timetable.append({
                "time": f"{slot['start']} - {slot['end']}",
                "subject": "☕ TEA BREAK",
                "duration": slot["duration"],
                "type": "break"
            })
        elif slot["type"] == "wrap-up":
            timetable.append({
                "time": f"{slot['start']} - {slot['end']}",
                "subject": schedule[period_index] if period_index < len(schedule) else "Free Session",
                "duration": slot["duration"],
                "type": "wrap-up"
            })
            period_index += 1
        else:
            timetable.append({
                "time": f"{slot['start']} - {slot['end']}",
                "subject": schedule[period_index] if period_index < len(schedule) else "Free Period",
                "duration": slot["duration"],
                "type": "period"
            })
            period_index += 1
    
    return timetable


def print_weekly_timetable():
    """Print formatted weekly timetable"""
    print("=" * 90)
    print("CLASSDOODLE - MATRIC REWRITE SCHOOL")
    print("Weekly Timetable: 7:00 AM - 1:00 PM")
    print("=" * 90)
    print()
    
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        print(f"\n{'='*90}")
        print(f"  {day.upper()}")
        print(f"{'='*90}")
        
        daily = generate_daily_timetable(day)
        for item in daily:
            if item["type"] == "break":
                print(f"  {item['time']}  |  {item['subject']}")
            elif item["type"] == "wrap-up":
                print(f"  {item['time']}  |  🎯 {item['subject']}")
            else:
                subject_color = CORE_SUBJECTS.get(item['subject'], {}).get('color', '')
                print(f"  {item['time']}  |  📚 {item['subject']}")
    
    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"Total Teaching Hours per Day: 5 hours 20 minutes")
    print(f"Break Time: 20 minutes")
    print(f"Wrap-up/Review: 40 minutes")
    print(f"Total Contact Time: 6 hours")
    print()
    print("Weekly Period Distribution:")
    for subject, details in CORE_SUBJECTS.items():
        print(f"  • {subject}: {details['periods_per_week']} periods/week")


def export_timetable_json():
    """Export timetable to JSON for automation"""
    timetable_data = {
        "school_name": "ClassDoodle",
        "schedule_type": "Matric Rewrite",
        "daily_hours": "7:00 AM - 1:00 PM",
        "subjects": CORE_SUBJECTS,
        "time_slots": TIME_SLOTS,
        "weekly_schedule": {}
    }
    
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        timetable_data["weekly_schedule"][day] = generate_daily_timetable(day)
    
    with open("classdoodle/timetable.json", "w") as f:
        json.dump(timetable_data, f, indent=2)
    
    print("✅ Timetable exported to: classdoodle/timetable.json")


def generate_student_view():
    """Generate student-friendly timetable"""
    print("\n" + "=" * 90)
    print("📱 STUDENT VIEW - THIS WEEK'S CLASSES")
    print("=" * 90)
    
    today = datetime.now()
    
    for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
        current_date = today + timedelta(days=i - today.weekday())
        date_str = current_date.strftime("%d %B %Y")
        
        print(f"\n{day}, {date_str}")
        print("-" * 70)
        
        daily = generate_daily_timetable(day)
        for item in daily:
            if item["type"] == "break":
                print(f"  {item['time']}  →  {item['subject']}")
            else:
                print(f"  {item['time']}  →  {item['subject']}")


if __name__ == "__main__":
    # Print weekly timetable
    print_weekly_timetable()
    
    # Generate student view
    generate_student_view()
    
    # Export to JSON for automation
    try:
        export_timetable_json()
    except:
        print("\n⚠️  Note: Create 'classdoodle' folder first for JSON export")
