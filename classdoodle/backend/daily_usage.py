"""
ClassDoodle Backend - Daily Usage Examples
Quick reference for common operations
"""

from api import ClassDoodleAPI
from datetime import date

# Initialize API (do this once)
api = ClassDoodleAPI()

print("=" * 70)
print("CLASSDOODLE BACKEND - DAILY OPERATIONS")
print("=" * 70)
print()

# ==================== MORNING ROUTINE ====================
print("🌅 MORNING ROUTINE")
print("-" * 70)

# 1. Get today's stats
stats = api.get_dashboard_stats()

print(f"\nTotal Students: {stats['total_students']}")
print(f"Class Average: {stats['class_average']}%")
print(f"Students needing attention: {stats['at_risk'] + stats['medium_risk']}")

# 2. Check who hasn't paid this month
current_month = date.today().strftime('%Y-%m')
payment_status = api.get_payment_status(current_month)

print(f"\nPayments this month:")
print(f"  Paid: {payment_status['paid_count']}")
print(f"  Outstanding: {payment_status['outstanding_count']}")
print(f"  Revenue: R{payment_status['total_revenue']:,.2f}")

if payment_status['outstanding']:
    print(f"\n⚠️  Students with outstanding payments:")
    for student in payment_status['outstanding'][:5]:  # Show first 5
        print(f"    • {student['name']} - {student['parent_phone']}")

# ==================== DURING CLASSES ====================
print("\n\n📚 DURING CLASSES (Mark Attendance)")
print("-" * 70)

# Example: Mark attendance for Mathematics class
today = date.today().isoformat()

# Get all active students first
all_students = api.students.get_all_students(status='active')
print(f"\nTotal active students: {len(all_students)}")

# Students present in this class (you'll get this from your web form)
present_ids = ["CD001", "CD002", "CD003"]  # Example

result = api.mark_class_attendance(
    present_student_ids=present_ids,
    date_str=today,
    time_slot="07:00-07:50",
    subject="Mathematics"
)

print(f"\nAttendance for Mathematics (07:00-07:50):")
print(f"  ✅ Present: {result['present']}")
print(f"  ❌ Absent: {result['absent']}")
if result['total'] > 0:
    print(f"  📊 Rate: {(result['present']/result['total']*100):.1f}%")
else:
    print(f"  📊 Rate: No students enrolled yet")

# ==================== RECORD ASSESSMENT ====================
print("\n\n📝 RECORD ASSESSMENT SCORES")
print("-" * 70)

# Example: Record test scores for Mathematics
print("\nRecording test scores...")

test_scores = {
    "CD001": 85,
    "CD002": 72,
    "CD003": 90,
    "CD004": 68,
    "CD005": 78
}

for student_id, score in test_scores.items():
    api.record_assessment(
        student_id=student_id,
        subject="Mathematics",
        assessment_type="Weekly Test",
        score=score
    )

print(f"✅ Recorded {len(test_scores)} test scores")

# ==================== STUDENT PERFORMANCE ====================
print("\n\n📈 CHECK STUDENT PERFORMANCE")
print("-" * 70)

# Get performance for a struggling student
performance = api.get_student_performance("CD002")

print("\nPerformance for CD002 (Zanele):")
for subject, data in performance.items():
    trend_emoji = "📈" if data['trend'] == 'improving' else "📉" if data['trend'] == 'declining' else "➡️"
    print(f"  {subject}:")
    print(f"    Average: {data['average']}%")
    print(f"    Latest: {data['latest']}%")
    print(f"    Trend: {trend_emoji} {data['trend']}")

# ==================== RECORD PAYMENT ====================
print("\n\n💰 RECORD PAYMENT")
print("-" * 70)

# Example: Student pays their monthly fee
api.record_payment(
    student_id="CD003",
    amount=1500.00,
    month_for=current_month,
    payment_method="EFT",
    reference="PAY-12345"
)

print(f"✅ Payment recorded: CD003 paid R1,500 for {current_month}")

# ==================== END OF DAY REPORT ====================
print("\n\n🌙 END OF DAY SUMMARY")
print("-" * 70)

# Get attendance for today
attendance_report = api.get_daily_attendance_report(today)

print(f"\nAttendance for {today}:")
for subject, stats in attendance_report['by_subject'].items():
    rate = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0
    print(f"  {subject}: {stats['present']}/{stats['total']} ({rate:.0f}%)")

# Get class performance summary
class_summary = api.get_class_performance_summary()

print(f"\nClass Performance:")
print(f"  Average: {class_summary['class_average']}%")
print(f"  🟢 On Track: {class_summary['risk_breakdown']['low']} students")
print(f"  🟡 Medium Risk: {class_summary['risk_breakdown']['medium']} students")
print(f"  🔴 High Risk: {class_summary['risk_breakdown']['high']} students")

# ==================== REGISTER NEW STUDENT ====================
print("\n\n👤 EXAMPLE: REGISTER NEW STUDENT")
print("-" * 70)

print("\nHow to register a new student:")
print("""
new_student_id = api.register_student(
    name="New Student Name",
    email="student@example.com",
    phone="0712345678",
    parent_name="Parent Name",
    parent_phone="0823456789",
    parent_email="parent@example.com",
    subjects=["Mathematics", "Physical Sciences", "English"],
    notes="Any special notes"
)
print(f"New student registered: {new_student_id}")
""")

# ==================== BULK IMPORT ====================
print("\n\n📋 EXAMPLE: BULK IMPORT STUDENTS")
print("-" * 70)

print("\nHow to import 100 students from CSV:")
print("""
# Format your CSV with columns:
# name, email, phone, parent_name, parent_phone, parent_email, subjects, notes

imported, failed = api.import_students_from_csv("student_list.csv")
print(f"Imported: {len(imported)}")
print(f"Failed: {len(failed)}")

# Send welcome emails to all new students
for student_id in imported:
    student = api.get_student_info(student_id)
    print(f"Send welcome email to: {student['name']} - {student['email']}")
""")

print("\n" + "=" * 70)
print("✅ BACKEND READY FOR YOUR 100 STUDENTS!")
print("=" * 70)
print()

# Close connection
api.close()
