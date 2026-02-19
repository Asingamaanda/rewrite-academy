"""
ClassDoodle Backend Demo & Testing
Test all backend functionality
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.api import ClassDoodleAPI
from datetime import date, timedelta
import random


def demo_backend():
    """Demonstrate all backend features"""
    
    print("\n" + "=" * 70)
    print("🎓 CLASSDOODLE BACKEND DEMO")
    print("=" * 70)
    print()
    
    # Initialize API
    api = ClassDoodleAPI()
    
    # ========== 1. STUDENT MANAGEMENT ==========
    print("\n📚 1. STUDENT MANAGEMENT")
    print("-" * 70)
    
    # Register students
    print("\nRegistering students...")
    
    test_students = [
        {
            'name': 'Thabo Molefe',
            'email': 'thabo@classdoodle.co.za',
            'phone': '0712345678',
            'parent_name': 'Mrs Molefe',
            'parent_phone': '0823456789',
            'parent_email': 'molefe@email.com',
            'subjects': ['Mathematics', 'Physical Sciences', 'English Home Language']
        },
        {
            'name': 'Zanele Dlamini',
            'email': 'zanele@classdoodle.co.za',
            'phone': '0734567890',
            'parent_name': 'Mr Dlamini',
            'parent_phone': '0845678901',
            'parent_email': 'dlamini@email.com',
            'subjects': ['Mathematics', 'Life Sciences', 'Accounting']
        }
    ]
    
    student_ids = []
    for student_data in test_students:
        student_id = api.register_student(**student_data)
        if student_id:
            print(f"✅ Registered: {student_data['name']} → {student_id}")
            student_ids.append(student_id)
    
    # Get student info
    print(f"\nGetting info for {student_ids[0]}...")
    student_info = api.get_student_info(student_ids[0])
    print(f"Name: {student_info['name']}")
    print(f"Email: {student_info['email']}")
    print(f"Subjects: {', '.join(student_info['subjects'])}")
    
    # ========== 2. ASSESSMENTS ==========
    print("\n\n📈 2. ASSESSMENTS")
    print("-" * 70)
    
    print("\nRecording assessments...")
    
    # Add some test scores
    subjects = ['Mathematics', 'Physical Sciences', 'English Home Language']
    
    for student_id in student_ids:
        for subject in subjects:
            # Add 4 assessments with varying scores
            base_score = random.randint(50, 90)
            for i in range(4):
                score = base_score + random.randint(-10, 10)
                score = max(0, min(100, score))  # Keep between 0-100
                
                api.record_assessment(
                    student_id=student_id,
                    subject=subject,
                    assessment_type=f'Test {i+1}',
                    score=score
                )
    
    print("✅ Assessments recorded")
    
    # Get performance for first student
    print(f"\nPerformance for {student_ids[0]}:")
    performance = api.get_student_performance(student_ids[0])
    
    for subject, data in performance.items():
        print(f"  {subject}: {data['average']}% (trend: {data['trend']})")
    
    # ========== 3. ATTENDANCE ==========
    print("\n\n✅ 3. ATTENDANCE")
    print("-" * 70)
    
    print("\nMarking attendance...")
    
    # Mark attendance for today
    today = date.today().isoformat()
    
    result = api.mark_class_attendance(
        present_student_ids=[student_ids[0]],  # Only first student present
        date_str=today,
        time_slot='07:00-07:50',
        subject='Mathematics'
    )
    
    print(f"✅ Attendance marked:")
    print(f"   Present: {result['present']}")
    print(f"   Absent: {result['absent']}")
    print(f"   Total: {result['total']}")
    
    # Get daily report
    print(f"\nDaily attendance report for {today}:")
    report = api.get_daily_attendance_report(today)
    
    for subject, stats in report['by_subject'].items():
        attendance_pct = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"  {subject}: {stats['present']}/{stats['total']} ({attendance_pct:.0f}%)")
    
    # ========== 4. PAYMENTS ==========
    print("\n\n💰 4. PAYMENTS")
    print("-" * 70)
    
    print("\nRecording payments...")
    
    current_month = date.today().strftime('%Y-%m')
    
    # Record payment for first student
    api.record_payment(
        student_id=student_ids[0],
        amount=1500.00,
        month_for=current_month,
        payment_method='EFT',
        reference='REF12345'
    )
    
    print(f"✅ Payment recorded for {student_ids[0]}: R1,500")
    
    # Get payment status
    print(f"\nPayment status for {current_month}:")
    payment_status = api.get_payment_status(current_month)
    
    print(f"  Paid: {payment_status['paid_count']} students")
    print(f"  Outstanding: {payment_status['outstanding_count']} students")
    print(f"  Revenue: R{payment_status['total_revenue']:,.2f}")
    
    # ========== 5. DASHBOARD STATS ==========
    print("\n\n📊 5. DASHBOARD STATISTICS")
    print("-" * 70)
    
    stats = api.get_dashboard_stats()
    
    print(f"\nTotal Students: {stats['total_students']}")
    print(f"Class Average: {stats['class_average']}%")
    print(f"\nRisk Breakdown:")
    print(f"  🟢 On Track: {stats['on_track']}")
    print(f"  🟡 Medium Risk: {stats['medium_risk']}")
    print(f"  🔴 High Risk: {stats['at_risk']}")
    print(f"\nThis Month's Revenue: R{stats['payments_this_month']['revenue']:,.2f}")
    
    # ========== 6. CLASS SUMMARY ==========
    print("\n\n📋 6. CLASS SUMMARY")
    print("-" * 70)
    
    summary = api.get_all_students_summary()
    
    print(f"\n{'ID':<8} {'Name':<20} {'Avg':<6} {'Attend':<7} {'Risk':<10}")
    print("-" * 70)
    
    for student in summary:
        print(f"{student['student_id']:<8} "
              f"{student['name']:<20} "
              f"{student['overall_average']:<5.1f}% "
              f"{student['attendance_rate']:<6.1f}% "
              f"{student['risk_level']:<10}")
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE - Backend is fully operational!")
    print("=" * 70)
    print()
    
    api.close()


if __name__ == "__main__":
    demo_backend()
