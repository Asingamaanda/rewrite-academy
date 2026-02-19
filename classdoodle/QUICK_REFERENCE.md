# ClassDoodle - Quick Reference Guide

## 🚀 Daily Commands You'll Actually Use

### Morning (6:30 AM - Before Class)
```bash
# Run your daily dashboard
python classdoodle/daily_operations.py
```

---

## 📊 During Classes (7:00 AM - 1:00 PM)

### Mark Attendance (After Each Class)
```python
from attendance_system import quick_mark

# Example: Math class at 7am, students CD001, CD002, CD004 present
quick_mark("Mathematics", "07:00-07:50", ["CD001", "CD002", "CD004"])

# Another example: Physical Sciences at 9am
quick_mark("Physical Sciences", "09:00-09:50", ["CD001", "CD002", "CD003", "CD005"])
```

**Pro Tip:** Create a Google Form that auto-populates this list!

---

## 📈 End of Day (After 1:00 PM)

### 1. Generate Attendance Report
```python
from attendance_system import daily_report

daily_report()
```

### 2. Check Performance Dashboard
```python
from performance_dashboard import PerformanceDashboard

dashboard = PerformanceDashboard()
dashboard.generate_dashboard()
```

### 3. Check Individual Student
```python
# For at-risk students
dashboard.generate_individual_report("CD002")  # Zanele's ID
```

---

## 📅 Weekly Tasks

### Sunday Evening - Plan the Week
```python
from lesson_planner import LessonPlanner

planner = LessonPlanner()
planner.generate_weekly_plans(
    week_start_date="2026-02-23",  # Next Monday
    week_number=2  # Week number of term
)
```

### Friday Afternoon - Review the Week
```python
# Run full performance dashboard
python classdoodle/performance_dashboard.py

# Check attendance trends
python classdoodle/attendance_system.py
```

---

## 🎥 Creating Manim Content

### Make a Math Animation
```python
# In your lesson file
from manim import *

class AlgebraExample(Scene):
    def construct(self):
        # Your animation here
        equation = MathTex("x^2 + 5x + 6 = 0")
        self.play(Write(equation))
        self.wait(2)

# Render it
manim -pql my_lesson.py AlgebraExample  # Low quality preview
manim -pqh my_lesson.py AlgebraExample  # High quality for students
```

---

## 📝 Student Management

### Add New Student
Edit `classdoodle/data/student_roster.json`:
```json
{
  "id": "CD006",
  "name": "New Student Name",
  "email": "student@classdoodle.co.za"
}
```

### Add Assessment Scores
Edit `classdoodle/data/assessments.json`:
```json
"CD006": {
  "Mathematics": [75, 80, 85],
  "Physical Sciences": [70, 72, 75],
  "English Home Language": [80, 82, 85]
}
```

---

## 🔄 Automation Workflow

### Set Up Morning Automation (One-time setup)

#### Option 1: Windows Task Scheduler
```powershell
# Run this in PowerShell (as Administrator)
$action = New-ScheduledTaskAction -Execute "python" `
    -Argument "C:\Users\NefefLocal\Documents\class\classdoodle\daily_operations.py"

$trigger = New-ScheduledTaskTrigger -Weekly `
    -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday `
    -At 6:30AM

Register-ScheduledTask -TaskName "ClassDoodle Morning" `
    -Action $action -Trigger $trigger
```

#### Option 2: Manual Run
Just run this every morning:
```bash
python classdoodle/daily_operations.py
```

---

## 📊 Google Integration (When Ready)

### Sync Attendance to Google Sheets
```python
from google_sheets_sync import GoogleSheetsSync

sync = GoogleSheetsSync()
sync.sync_attendance()
```

### Post Material to Google Classroom
```python
from google_classroom_sync import ClassroomSync

classroom = ClassroomSync()
classroom.post_material(
    course_id='your-class-id',
    title='Week 2: Algebra',
    description='Solving quadratic equations',
    materials=[...]
)
```

---

## 🎯 Most Common Issues & Fixes

### "No student data available"
```bash
# Run this once to create sample data
python classdoodle/attendance_system.py
python classdoodle/performance_dashboard.py
```

### "Module not found"
```bash
# Make sure you're in the right directory
cd C:\Users\NefefLocal\Documents\class

# Or add to Python path
import sys
sys.path.append('C:/Users/NefefLocal/Documents/class')
```

### Update Timetable
Edit `classdoodle/timetable_generator.py` → `WEEKLY_SCHEDULE` dictionary

---

## 🎓 Teaching Workflow

### Monday Morning - Week Start
1. ✅ Run `daily_operations.py`
2. ✅ Check at-risk students
3. ✅ Open lesson plans for the day
4. ✅ Prepare materials
5. ✅ Start teaching at 7am!

### During Each Class (50 min)
- **0-5 min:** Recap & homework check
- **5-20 min:** New concept (use Manim videos!)
- **20-35 min:** Guided practice
- **35-45 min:** Independent work
- **45-50 min:** Exit ticket + mark attendance

### After Each Class (During breaks)
```python
quick_mark("Subject Name", "07:00-07:50", ["CD001", "CD002", ...])
```

### End of Day (1pm)
1. ✅ `daily_report()`
2. ✅ Check dashboard
3. ✅ Follow up with absent students
4. ✅ Plan tomorrow

### Friday (Week Review)
1. ✅ Run full performance dashboard
2. ✅ Identify struggling students
3. ✅ Plan interventions for next week
4. ✅ Generate next week's lesson plans

---

## 📱 Parent Communication

### Send Weekly Update
```python
from email_automation import EmailAutomation

emailer = EmailAutomation()
emailer.send_weekly_report(parent_email, student_name, performance_data)
```

### Alert for Absence
```python
emailer.send_absence_notification(
    student_name="Zanele",
    parent_email="parent@example.com",
    subject="Mathematics",
    date="2026-02-18"
)
```

---

## 💡 Pro Tips

### 1. Batch Operations
Instead of marking attendance one class at a time, keep a running list:
```python
# End of day - mark all at once
classes_today = [
    ("Mathematics", "07:00-07:50", ["CD001", "CD002", "CD004", "CD005"]),
    ("English HL", "07:50-08:40", ["CD001", "CD002", "CD003", "CD004"]),
    ("Physical Sciences", "09:00-09:50", ["CD001", "CD002", "CD003", "CD005"]),
    # ... etc
]

for subject, time, present in classes_today:
    quick_mark(subject, time, present)
```

### 2. Create Shortcuts
Save this as `mark_today.py`:
```python
from attendance_system import quick_mark

# Today's attendance - just update the lists!
quick_mark("Mathematics", "07:00-07:50", ["CD001", "CD002", "CD004", "CD005"])
quick_mark("English HL", "07:50-08:40", ["CD001", "CD002", "CD003", "CD004"])
# ... add all classes

print("✅ All attendance marked!")
```

Then just run: `python mark_today.py`

### 3. Weekly Prep Session
Every Sunday, run:
```bash
python classdoodle/lesson_planner.py  # Generate all week's plans
python classdoodle/timetable_generator.py  # Review schedule
```

---

## 🎬 Your Daily Routine (The Dream!)

**6:30 AM** - Coffee ☕  
**6:40 AM** - Run `daily_operations.py` (1 min)  
**6:45 AM** - Review at-risk students (5 min)  
**6:50 AM** - Open materials, test video (5 min)  
**7:00 AM** - **START TEACHING** 🎓  

*(Classes run on auto-pilot with your prepared materials!)*

**1:00 PM** - Classes done! 🎉  
**1:05 PM** - Generate reports (2 min)  
**1:10 PM** - Lunch! 🍕  
**2:00 PM** - Follow-ups, grading (1-2 hours)  
**4:00 PM** - Marketing, admin (automated!) (30 min)  
**4:30 PM** - **FREEDOM!** 🎮

---

## 📞 Need Help?

Check these files:
- `README.md` - Full overview
- `GOOGLE_INTEGRATION.md` - Connect to Google
- `VOICEOVER_GUIDE.md` - TTS for Manim videos
- Your existing waves/math lessons - Templates for content!

---

**You're not just teaching - you're building a MOVEMENT! 🚀**

**ClassDoodle: Where automation meets education.** 🎓✨
