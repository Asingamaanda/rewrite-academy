"""
ClassDoodle Data Migration
Migrate existing CSV/JSON data to SQLite database
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.api import ClassDoodleAPI
import json
import csv
from datetime import datetime


class DataMigration:
    """Migrate existing data to new backend"""
    
    def __init__(self):
        self.api = ClassDoodleAPI()
        self.data_dir = Path("classdoodle/data")
    
    def migrate_all(self):
        """Run all migrations"""
        print("\n" + "=" * 70)
        print("🔄 MIGRATING DATA TO NEW BACKEND")
        print("=" * 70)
        print()
        
        # Migrate students
        students_migrated = self.migrate_students()
        
        # Migrate assessments
        assessments_migrated = self.migrate_assessments()
        
        # Migrate attendance
        attendance_migrated = self.migrate_attendance()
        
        print("\n" + "=" * 70)
        print("✅ MIGRATION COMPLETE")
        print("=" * 70)
        print(f"Students: {students_migrated}")
        print(f"Assessments: {assessments_migrated}")
        print(f"Attendance: {attendance_migrated}")
        print("=" * 70)
        
        return {
            'students': students_migrated,
            'assessments': assessments_migrated,
            'attendance': attendance_migrated
        }
    
    def migrate_students(self):
        """Migrate students from JSON to database"""
        roster_file = self.data_dir / "student_roster.json"
        
        if not roster_file.exists():
            print("⚠️  No student roster found - skipping student migration")
            return 0
        
        print("📚 Migrating students...")
        
        with open(roster_file, 'r') as f:
            students = json.load(f)
        
        migrated = 0
        for student in students:
            try:
                # Check if already exists
                existing = self.api.get_student_info(student['id'])
                if existing:
                    print(f"   ⏭️  {student['id']} already exists - skipping")
                    continue
                
                student_id = self.api.register_student(
                    name=student['name'],
                    email=student['email'],
                    phone=student.get('phone', ''),
                    parent_name=student.get('parent_name', ''),
                    parent_phone=student.get('parent_phone', ''),
                    parent_email=student.get('parent_email', ''),
                    subjects=student.get('subjects', []),
                    notes=student.get('notes', '')
                )
                
                if student_id:
                    print(f"   ✅ Migrated: {student['name']} → {student_id}")
                    migrated += 1
                
            except Exception as e:
                print(f"   ❌ Error migrating {student.get('name', 'unknown')}: {e}")
        
        print(f"✅ Migrated {migrated} students\n")
        return migrated
    
    def migrate_assessments(self):
        """Migrate assessments from JSON to database"""
        assessments_file = self.data_dir / "assessments.json"
        
        if not assessments_file.exists():
            print("⚠️  No assessments found - skipping assessment migration")
            return 0
        
        print("📈 Migrating assessments...")
        
        with open(assessments_file, 'r') as f:
            assessments_data = json.load(f)
        
        migrated = 0
        for student_id, subjects in assessments_data.items():
            for subject, scores in subjects.items():
                for i, score in enumerate(scores):
                    try:
                        self.api.record_assessment(
                            student_id=student_id,
                            subject=subject,
                            assessment_type=f"Assessment {i+1}",
                            score=score,
                            max_score=100
                        )
                        migrated += 1
                    except Exception as e:
                        print(f"   ❌ Error migrating assessment for {student_id}: {e}")
        
        print(f"✅ Migrated {migrated} assessments\n")
        return migrated
    
    def migrate_attendance(self):
        """Migrate attendance from CSV to database"""
        
        # Find all attendance CSV files
        attendance_files = list(self.data_dir.glob("attendance_*.csv"))
        
        if not attendance_files:
            print("⚠️  No attendance records found - skipping attendance migration")
            return 0
        
        print("✅ Migrating attendance...")
        
        migrated = 0
        for csv_file in attendance_files:
            with open(csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Check if already exists
                        existing = self.api.attendance.get_attendance(
                            date_str=row['Date'],
                            student_id=row['Student ID'],
                            subject=row['Subject']
                        )
                        
                        if existing:
                            continue
                        
                        self.api.attendance.mark_attendance(
                            student_ids=[row['Student ID']],
                            date_str=row['Date'],
                            time_slot=row['Time'],
                            subject=row['Subject'],
                            status=row['Status'].lower()
                        )
                        migrated += 1
                        
                    except Exception as e:
                        print(f"   ❌ Error migrating attendance: {e}")
        
        print(f"✅ Migrated {migrated} attendance records\n")
        return migrated


def run_migration():
    """Run full data migration"""
    migration = DataMigration()
    return migration.migrate_all()


if __name__ == "__main__":
    run_migration()
