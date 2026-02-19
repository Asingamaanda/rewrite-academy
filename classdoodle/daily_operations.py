"""
ClassDoodle - Daily Operations Automation Script
Run this every morning to prepare for the school day
"""

import os
import sys
from datetime import datetime, date
from pathlib import Path

# Import ClassDoodle modules
sys.path.append(str(Path(__file__).parent))
from attendance_system import AttendanceTracker, daily_report
from performance_dashboard import PerformanceDashboard
from timetable_generator import generate_daily_timetable

def print_banner():
    """Print ClassDoodle banner"""
    print("\n" + "=" * 80)
    print("   ____  _               ____                  _  _       ")
    print("  / ___|| |  __ _  ___ |  _ \\  ___   ___   __| || |  ___ ")
    print(" | |    | | / _` |/ __|| | | |/ _ \\ / _ \\ / _` || | / _ \\")
    print(" | |___ | || (_| |\\__ \\| |_| | (_) | (_) | (_| || ||  __/")
    print("  \\____||_| \\__,_||___/|____/ \\___/ \\___/ \\__,_||_| \\___|")
    print()
    print("  MATRIC REWRITE SCHOOL - Daily Operations Dashboard")
    print("=" * 80)

def show_daily_schedule():
    """Display today's schedule"""
    today = date.today()
    day_name = today.strftime("%A")
    
    print(f"\n📅 TODAY'S SCHEDULE - {today.strftime('%A, %d %B %Y')}")
    print("=" * 80)
    
    if day_name in ["Saturday", "Sunday"]:
        print("🎉 WEEKEND - No classes scheduled")
        return
    
    schedule = generate_daily_timetable(day_name)
    
    if schedule:
        print("\n  TIME          | SUBJECT / ACTIVITY")
        print("  " + "-" * 76)
        for item in schedule:
            subject = item['subject']
            if item['type'] == 'break':
                print(f"  {item['time']:12s} | {subject}")
            elif item['type'] == 'wrap-up':
                print(f"  {item['time']:12s} | 🎯 {subject}")
            else:
                print(f"  {item['time']:12s} | 📚 {subject}")
    
    print()

def show_quick_stats():
    """Show essential daily stats"""
    print("\n📊 QUICK STATS")
    print("=" * 80)
    
    # Load student data
    tracker = AttendanceTracker()
    dashboard = PerformanceDashboard()
    
    students = dashboard.load_student_data()
    
    if students:
        print(f"👥 Total Students: {len(students)}")
        
        # Calculate at-risk count
        at_risk_count = 0
        for student in students:
            metrics = dashboard.calculate_metrics(student)
            if metrics.get("overall_risk") in ["high", "medium"]:
                at_risk_count += 1
        
        print(f"⚠️  At-Risk Students: {at_risk_count}")
        
        # Show who needs attention TODAY
        if at_risk_count > 0:
            print(f"\n💡 Priority: Check in with at-risk students during breaks")
    else:
        print("ℹ️  No student data available yet")
    
    print()

def show_attendance_reminder():
    """Remind to mark attendance"""
    print("\n✅ ATTENDANCE CHECKLIST")
    print("=" * 80)
    print("Remember to mark attendance after each class:")
    print()
    print("  Python command:")
    print("  >>> from attendance_system import quick_mark")
    print("  >>> quick_mark('Mathematics', '07:00-07:50', ['CD001', 'CD002', ...])")
    print()
    print("  Or use your Google Form/Sheets integration")
    print()

def show_preparation_tasks():
    """Show what to prepare before first class"""
    print("\n📝 BEFORE FIRST CLASS (7:00 AM)")
    print("=" * 80)
    print("  ☐ Check all lesson plans are ready")
    print("  ☐ Open Google Classroom / LMS")
    print("  ☐ Test video/audio setup")
    print("  ☐ Upload today's materials")
    print("  ☐ Send reminder to students (WhatsApp/Email)")
    print()

def show_end_of_day_tasks():
    """Show end-of-day checklist"""
    print("\n🌙 END OF DAY CHECKLIST (After 1:00 PM)")
    print("=" * 80)
    print("  ☐ Generate attendance report (daily_report())")
    print("  ☐ Check performance dashboard")
    print("  ☐ Follow up with absent students")
    print("  ☐ Grade assignments/assessments")
    print("  ☐ Plan interventions for struggling students")
    print("  ☐ Prepare materials for tomorrow")
    print()

def main():
    """Main daily operations dashboard"""
    print_banner()
    
    # Check if it's a school day
    today = date.today()
    day_name = today.strftime("%A")
    
    if day_name in ["Saturday", "Sunday"]:
        print(f"\n✨ Happy {day_name}! Enjoy your weekend!")
        print("\nUse this time to:")
        print("  • Review last week's performance data")
        print("  • Plan next week's lessons")
        print("  • Create Manim animations for tough concepts")
        print("  • Marketing & admin automation")
        return
    
    # Show daily info
    show_daily_schedule()
    show_quick_stats()
    show_preparation_tasks()
    show_attendance_reminder()
    show_end_of_day_tasks()
    
    print("=" * 80)
    print("🚀 Ready to change lives! Let's make today count.")
    print("=" * 80)

if __name__ == "__main__":
    main()
