"""
ClassDoodle - Automated Attendance Tracking System
Real-time attendance with automated Google Sheets integration
"""

import csv
from datetime import datetime, date
from pathlib import Path
import json

class AttendanceTracker:
    """Automated attendance tracking for ClassDoodle"""
    
    def __init__(self, data_dir="classdoodle/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Load student roster
        self.students = self.load_students()
        
    def load_students(self):
        """Load student list from JSON"""
        roster_file = self.data_dir / "student_roster.json"
        
        # Create sample roster if doesn't exist
        if not roster_file.exists():
            sample_students = [
                {"id": "CD001", "name": "Thabo Molefe", "email": "thabo@classdoodle.co.za"},
                {"id": "CD002", "name": "Zanele Dlamini", "email": "zanele@classdoodle.co.za"},
                {"id": "CD003", "name": "Liam van der Merwe", "email": "liam@classdoodle.co.za"},
                {"id": "CD004", "name": "Ayanda Nkosi", "email": "ayanda@classdoodle.co.za"},
                {"id": "CD005", "name": "Zinhle Khumalo", "email": "zinhle@classdoodle.co.za"}
            ]
            
            with open(roster_file, 'w') as f:
                json.dump(sample_students, f, indent=2)
            
            print(f"✅ Created sample student roster: {roster_file}")
            return sample_students
        
        with open(roster_file, 'r') as f:
            return json.load(f)
    
    def mark_attendance(self, subject, time_slot, present_students):
        """Mark attendance for a specific class"""
        today = date.today()
        attendance_file = self.data_dir / f"attendance_{today.strftime('%Y_%m')}.csv"
        
        # Create CSV if doesn't exist
        if not attendance_file.exists():
            with open(attendance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Date", "Day", "Time", "Subject", 
                    "Student ID", "Student Name", "Status", "Timestamp"
                ])
        
        # Record attendance
        with open(attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            day_name = today.strftime("%A")
            
            for student in self.students:
                status = "Present" if student["id"] in present_students else "Absent"
                writer.writerow([
                    today.strftime("%Y-%m-%d"),
                    day_name,
                    time_slot,
                    subject,
                    student["id"],
                    student["name"],
                    status,
                    timestamp
                ])
        
        print(f"✅ Attendance recorded for {subject} at {time_slot}")
        print(f"   Present: {len(present_students)}/{len(self.students)}")
        
        return attendance_file
    
    def generate_daily_report(self):
        """Generate attendance report for today"""
        today = date.today()
        attendance_file = self.data_dir / f"attendance_{today.strftime('%Y_%m')}.csv"
        
        if not attendance_file.exists():
            print("❌ No attendance data for today")
            return
        
        # Read attendance data
        with open(attendance_file, 'r') as f:
            reader = csv.DictReader(f)
            today_str = today.strftime("%Y-%m-%d")
            today_records = [row for row in reader if row["Date"] == today_str]
        
        if not today_records:
            print("❌ No attendance records for today")
            return
        
        # Calculate statistics
        print("\n" + "=" * 70)
        print(f"ATTENDANCE REPORT - {today.strftime('%A, %d %B %Y')}")
        print("=" * 70)
        
        # Group by subject
        subjects = {}
        for record in today_records:
            subject = record["Subject"]
            if subject not in subjects:
                subjects[subject] = {"present": 0, "absent": 0, "total": 0}
            
            subjects[subject]["total"] += 1
            if record["Status"] == "Present":
                subjects[subject]["present"] += 1
            else:
                subjects[subject]["absent"] += 1
        
        # Print subject-wise attendance
        for subject, stats in subjects.items():
            attendance_rate = (stats["present"] / stats["total"] * 100) if stats["total"] > 0 else 0
            print(f"\n📚 {subject}")
            print(f"   Present: {stats['present']}/{stats['total']} ({attendance_rate:.1f}%)")
        
        # Overall statistics
        total_present = sum(s["present"] for s in subjects.values())
        total_records = sum(s["total"] for s in subjects.values())
        overall_rate = (total_present / total_records * 100) if total_records > 0 else 0
        
        print("\n" + "-" * 70)
        print(f"OVERALL ATTENDANCE: {overall_rate:.1f}%")
        print("=" * 70)
    
    def generate_student_report(self, student_id):
        """Generate attendance report for specific student"""
        today = date.today()
        attendance_file = self.data_dir / f"attendance_{today.strftime('%Y_%m')}.csv"
        
        if not attendance_file.exists():
            print("❌ No attendance data available")
            return
        
        # Read attendance data
        with open(attendance_file, 'r') as f:
            reader = csv.DictReader(f)
            student_records = [row for row in reader if row["Student ID"] == student_id]
        
        if not student_records:
            print(f"❌ No records found for student {student_id}")
            return
        
        student_name = student_records[0]["Student Name"]
        
        print("\n" + "=" * 70)
        print(f"STUDENT ATTENDANCE REPORT - {student_name} ({student_id})")
        print("=" * 70)
        
        # Calculate statistics
        total_classes = len(student_records)
        present_count = sum(1 for r in student_records if r["Status"] == "Present")
        attendance_rate = (present_count / total_classes * 100) if total_classes > 0 else 0
        
        print(f"\nTotal Classes: {total_classes}")
        print(f"Present: {present_count}")
        print(f"Absent: {total_classes - present_count}")
        print(f"Attendance Rate: {attendance_rate:.1f}%")
        
        # Recent absences
        absences = [r for r in student_records if r["Status"] == "Absent"]
        if absences:
            print(f"\nRecent Absences:")
            for absence in absences[-5:]:  # Last 5 absences
                print(f"  • {absence['Date']} - {absence['Subject']} at {absence['Time']}")
        
        print("=" * 70)


# ========== QUICK ATTENDANCE FUNCTIONS ==========

def quick_mark(subject, time_slot, present_ids):
    """Quick attendance marking - use this during class"""
    tracker = AttendanceTracker()
    tracker.mark_attendance(subject, time_slot, present_ids)


def daily_report():
    """Generate today's attendance report"""
    tracker = AttendanceTracker()
    tracker.generate_daily_report()


def student_report(student_id):
    """Check specific student's attendance"""
    tracker = AttendanceTracker()
    tracker.generate_student_report(student_id)


if __name__ == "__main__":
    print("=" * 70)
    print("CLASSDOODLE ATTENDANCE SYSTEM")
    print("=" * 70)
    
    # Initialize system
    tracker = AttendanceTracker()
    
    print(f"\n✅ System initialized")
    print(f"📊 Students loaded: {len(tracker.students)}")
    
    # Demo: Mark attendance for a class
    print("\n--- DEMO: Marking Attendance ---")
    quick_mark(
        subject="Mathematics",
        time_slot="07:00-07:50",
        present_ids=["CD001", "CD002", "CD004", "CD005"]  # Thabo, Zanele, Ayanda, Zinhle present
    )
    
    # Generate daily report
    print("\n--- DAILY REPORT ---")
    daily_report()
    
    # Check individual student
    print("\n--- STUDENT REPORT ---")
    student_report("CD001")
    
    print("\n" + "=" * 70)
    print("USAGE:")
    print("  quick_mark('Mathematics', '07:00-07:50', ['CD001', 'CD002', ...])")
    print("  daily_report()")
    print("  student_report('CD001')")
    print("=" * 70)
