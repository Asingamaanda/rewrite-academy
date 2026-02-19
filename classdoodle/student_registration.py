"""
ClassDoodle - Bulk Student Registration System
Handle 100+ student registrations easily
"""

import csv
import json
from pathlib import Path
from datetime import datetime

class StudentRegistration:
    """Manage student registration and onboarding"""
    
    def __init__(self, data_dir="classdoodle/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.roster_file = self.data_dir / "student_roster.json"
        self.registration_csv = self.data_dir / "pending_registrations.csv"
    
    def create_registration_template(self):
        """Create CSV template for bulk student registration"""
        
        template_file = self.data_dir / "student_registration_template.csv"
        
        with open(template_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'name', 'email', 'phone', 'parent_name', 'parent_phone', 
                'parent_email', 'subjects', 'notes'
            ])
            writer.writeheader()
            
            # Add example rows
            writer.writerow({
                'name': 'Example Student 1',
                'email': 'student1@example.com',
                'phone': '0712345678',
                'parent_name': 'Parent Name',
                'parent_phone': '0823456789',
                'parent_email': 'parent1@example.com',
                'subjects': 'Math,Physics,English,Life Sciences,Accounting',
                'notes': 'Struggled with algebra last year'
            })
            writer.writerow({
                'name': 'Example Student 2',
                'email': 'student2@example.com',
                'phone': '0734567890',
                'parent_name': 'Parent Name 2',
                'parent_phone': '0845678901',
                'parent_email': 'parent2@example.com',
                'subjects': 'Math,Physics,English,Life Sciences,Afrikaans',
                'notes': 'Needs extra support in sciences'
            })
        
        print(f"✅ Created registration template: {template_file}")
        print("\nInstructions:")
        print("1. Open the CSV file in Excel")
        print("2. Fill in student details (one per row)")
        print("3. Save the file")
        print("4. Run import_students() to add them to ClassDoodle")
        
        return template_file
    
    def import_students(self, csv_file=None):
        """Import students from CSV file"""
        
        if csv_file is None:
            csv_file = self.data_dir / "student_registration_template.csv"
        
        csv_file = Path(csv_file)
        
        if not csv_file.exists():
            print(f"❌ File not found: {csv_file}")
            return
        
        # Load existing students
        if self.roster_file.exists():
            with open(self.roster_file, 'r') as f:
                existing_students = json.load(f)
        else:
            existing_students = []
        
        # Get next student ID
        if existing_students:
            last_id = max([int(s['id'].replace('CD', '')) for s in existing_students])
            next_id = last_id + 1
        else:
            next_id = 1
        
        # Read new students from CSV
        new_students = []
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip example rows
                if 'Example Student' in row['name']:
                    continue
                
                student = {
                    'id': f'CD{next_id:03d}',
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row.get('phone', ''),
                    'parent_name': row.get('parent_name', ''),
                    'parent_phone': row.get('parent_phone', ''),
                    'parent_email': row.get('parent_email', ''),
                    'subjects': row.get('subjects', '').split(','),
                    'notes': row.get('notes', ''),
                    'registration_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                new_students.append(student)
                next_id += 1
        
        # Merge with existing students
        all_students = existing_students + new_students
        
        # Save to roster
        with open(self.roster_file, 'w') as f:
            json.dump(all_students, f, indent=2)
        
        print(f"\n✅ Imported {len(new_students)} new student(s)")
        print(f"📊 Total students: {len(all_students)}")
        
        for student in new_students:
            print(f"   • {student['id']}: {student['name']} ({student['email']})")
        
        # Initialize their assessment records
        self._initialize_assessments(new_students)
        
        return new_students
    
    def _initialize_assessments(self, students):
        """Create empty assessment records for new students"""
        
        assessments_file = self.data_dir / "assessments.json"
        
        if assessments_file.exists():
            with open(assessments_file, 'r') as f:
                assessments = json.load(f)
        else:
            assessments = {}
        
        # Add empty assessment records
        for student in students:
            if student['id'] not in assessments:
                assessments[student['id']] = {
                    "Mathematics": [],
                    "Physical Sciences": [],
                    "English Home Language": [],
                    "Life Sciences": [],
                    "Afrikaans FAL": [],
                    "Accounting": [],
                    "Life Orientation": []
                }
        
        with open(assessments_file, 'w') as f:
            json.dump(assessments, f, indent=2)
        
        print(f"✅ Initialized assessment tracking for {len(students)} student(s)")
    
    def generate_welcome_emails(self, students=None):
        """Generate welcome email text for new students"""
        
        if students is None:
            # Load all students
            if self.roster_file.exists():
                with open(self.roster_file, 'r') as f:
                    students = json.load(f)
            else:
                print("❌ No students found")
                return
        
        welcome_file = self.data_dir / "welcome_emails.txt"
        
        with open(welcome_file, 'w') as f:
            for student in students:
                email_text = f"""
{'='*70}
TO: {student['name']} <{student['email']}>
SUBJECT: Welcome to ClassDoodle - Matric Rewrite School!
{'='*70}

Dear {student['name']},

Welcome to ClassDoodle! 🎓

We're excited to have you join South Africa's first 7am-1pm online matric rewrite school.

YOUR DETAILS:
Student ID: {student['id']}
Name: {student['name']}
Email: {student['email']}

WHAT HAPPENS NEXT:
1. Classes start on [INSERT DATE]
2. Daily schedule: 7:00 AM - 1:00 PM (Mon-Fri)
3. You'll receive your Zoom/Google Meet link 24 hours before first class
4. Download the class timetable: [INSERT LINK]

SUBJECTS YOU'RE REGISTERED FOR:
{', '.join(student.get('subjects', ['All core subjects']))}

IMPORTANT REMINDERS:
✅ Be online by 6:55 AM daily
✅ Have your workbook and stationery ready
✅ Stable internet connection required
✅ Camera on during classes (builds accountability)

We're here to help you succeed. Let's make 2026 your year!

Best regards,
ClassDoodle Team

---
PARENT INFORMATION:
Parent: {student.get('parent_name', 'N/A')}
Parent Email: {student.get('parent_email', 'N/A')}
Parent Phone: {student.get('parent_phone', 'N/A')}

{'='*70}


"""
                f.write(email_text)
        
        print(f"✅ Generated welcome emails: {welcome_file}")
        print(f"📧 {len(students)} email(s) ready to send")
        
        return welcome_file
    
    def create_student_info_sheet(self):
        """Create a detailed student information sheet"""
        
        if self.roster_file.exists():
            with open(self.roster_file, 'r') as f:
                students = json.load(f)
        else:
            print("❌ No students found")
            return
        
        info_file = self.data_dir / "student_info_sheet.csv"
        
        with open(info_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'ID', 'Name', 'Email', 'Phone', 'Parent Name', 
                'Parent Phone', 'Parent Email', 'Subjects', 'Notes', 'Registration Date'
            ])
            writer.writeheader()
            
            for student in students:
                writer.writerow({
                    'ID': student['id'],
                    'Name': student['name'],
                    'Email': student['email'],
                    'Phone': student.get('phone', ''),
                    'Parent Name': student.get('parent_name', ''),
                    'Parent Phone': student.get('parent_phone', ''),
                    'Parent Email': student.get('parent_email', ''),
                    'Subjects': ', '.join(student.get('subjects', [])),
                    'Notes': student.get('notes', ''),
                    'Registration Date': student.get('registration_date', '')
                })
        
        print(f"✅ Created student info sheet: {info_file}")
        print(f"📊 Total students: {len(students)}")
        
        return info_file


# ========== QUICK FUNCTIONS ==========

def setup_for_100_students():
    """Prepare system for 100 students"""
    
    print("=" * 70)
    print("🚀 PREPARING CLASSDOODLE FOR 100 STUDENTS")
    print("=" * 70)
    print()
    
    reg = StudentRegistration()
    
    # Create registration template
    template = reg.create_registration_template()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print(f"1. Open: {template}")
    print("2. Delete the example rows")
    print("3. Add your 10 pending students (then more as they come)")
    print("4. Save the file")
    print("5. Run: python classdoodle/student_registration.py")
    print()
    print("OR import directly:")
    print("   from student_registration import StudentRegistration")
    print("   reg = StudentRegistration()")
    print("   reg.import_students()")
    print("=" * 70)


if __name__ == "__main__":
    # Run setup
    setup_for_100_students()
    
    # Example: Import students (if template has been filled)
    # reg = StudentRegistration()
    # reg.import_students()
    # reg.generate_welcome_emails()
