# Adding Your 10 Students from Facebook

## Option 1: One-by-One (Recommended for now)

Create a file `add_students.py`:

```python
from backend.api import ClassDoodleAPI

api = ClassDoodleAPI()

# Student 1 from Facebook
student1 = api.register_student(
    name="Full Name",
    email="email@example.com",
    phone="0712345678",
    parent_name="Parent Full Name",
    parent_phone="0823456789",
    parent_email="parent@example.com",
    subjects=["Mathematics", "Physical Sciences", "English Home Language"],  # Add their chosen subjects
    notes="From Facebook ad - Feb 2026"
)
print(f"✅ Registered: {student1}")

# Student 2 from Facebook
student2 = api.register_student(
    name="Second Student Name",
    email="student2@example.com",
    phone="0712345678",
    parent_name="Parent Name",
    parent_phone="0823456789",
    parent_email="parent2@example.com",
    subjects=["Mathematics", "Life Sciences", "English Home Language"],
    notes="From Facebook ad - Feb 2026"
)
print(f"✅ Registered: {student2}")

# ... repeat for all 10 students

api.close()
print("\n✅ All 10 students registered!")
```

Then run: `python add_students.py`

## Option 2: Bulk CSV Import (For 100+ students)

1. Create `students.csv` with this format:

```csv
name,email,phone,parent_name,parent_phone,parent_email,subjects,notes
John Doe,john@example.com,0712345678,Jane Doe,0823456789,jane@example.com,"Mathematics|Physical Sciences|English","Facebook lead"
Mary Smith,mary@example.com,0734567890,Peter Smith,0845678901,peter@example.com,"Mathematics|Life Sciences|English","Facebook lead"
```

2. Import them:

```python
from backend.api import ClassDoodleAPI

api = ClassDoodleAPI()

imported, failed = api.import_students_from_csv("students.csv")

print(f"✅ Imported: {len(imported)} students")
print(f"❌ Failed: {len(failed)} students")

if failed:
    print("\nFailed entries:")
    for error in failed:
        print(f"  {error}")

# Show all students
all_students = api.get_all_students_summary()
for student in all_students:
    print(f"{student['student_id']}: {student['name']} - {student['email']}")

api.close()
```

## What Happens After Registration?

Each student gets:
- **Unique ID**: CD001, CD002, CD003, etc.
- **Subject enrollment**: Whatever subjects they registered for
- **Parent contact info**: Stored for payment reminders
- **Status**: 'active' by default

## Next: Send Them Welcome Messages

After registering all 10:

```python
from backend.api import ClassDoodleAPI

api = ClassDoodleAPI()

# Get all new students
all_students = api.students.get_all_students(status='active')

print("📧 SEND THESE WELCOME MESSAGES:\n")

for student in all_students:
    print(f"WhatsApp to {student['parent_phone']}:")
    print(f"  Hi {student['parent_name']}, welcome to ClassDoodle!")
    print(f"  {student['name']} is enrolled in: {', '.join(student['subjects'])}")
    print(f"  Student ID: {student['student_id']}")
    print(f"  Classes start 7am daily. Payment: R1,500/month")
    print()

api.close()
```

## Your Workflow This Week

1. **TODAY**: Register your 10 Facebook leads
2. **TOMORROW**: Start morning classes at 7am
3. **During week**: Mark attendance daily, record first test scores
4. **Friday**: Check payment status, send reminders for unpaid

## Database is Ready!

Your backend can handle:
- ✅ 100+ students (tested architecture)
- ✅ Daily attendance for all classes
- ✅ Unlimited assessments per student
- ✅ Payment tracking and reminders
- ✅ Performance analytics and trends

**Everything is saved in:** `classdoodle/data/classdoodle.db`

No need for internet - it's all on your computer!
