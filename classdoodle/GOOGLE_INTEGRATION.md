# ClassDoodle - Google Integration Guide

## 🔗 Integrating with Google Workspace

### Prerequisites
```bash
pip install gspread oauth2client google-auth google-auth-oauthlib google-auth-httplib2
```

---

## 1. 📊 Google Sheets Attendance Integration

### Setup Steps:

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project: "ClassDoodle"
   - Enable Google Sheets API
   - Enable Google Drive API

2. **Create Service Account**
   - Go to "IAM & Admin" → "Service Accounts"
   - Create service account: `classdoodle-automation@...`
   - Download JSON credentials
   - Save as: `classdoodle/credentials/google-credentials.json`

3. **Create Google Sheet**
   - Create new sheet: "ClassDoodle Attendance 2026"
   - Share with service account email (Editor access)
   - Copy the Sheet ID from URL

### Code Implementation:

```python
# classdoodle/google_sheets_sync.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import csv
from pathlib import Path

class GoogleSheetsSync:
    """Sync attendance data to Google Sheets"""
    
    def __init__(self, credentials_file='classdoodle/credentials/google-credentials.json'):
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
        self.client = gspread.authorize(creds)
    
    def sync_attendance(self, sheet_name='ClassDoodle Attendance 2026'):
        """Sync local attendance CSV to Google Sheets"""
        
        # Open the sheet
        sheet = self.client.open(sheet_name).sheet1
        
        # Read local attendance data
        today = datetime.now()
        attendance_file = Path(f"classdoodle/data/attendance_{today.strftime('%Y_%m')}.csv")
        
        if not attendance_file.exists():
            print("❌ No attendance data to sync")
            return
        
        # Clear existing data
        sheet.clear()
        
        # Upload data
        with open(attendance_file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        
        # Write to sheet
        sheet.update('A1', data)
        
        print(f"✅ Synced {len(data)-1} attendance records to Google Sheets")
        print(f"📊 View at: {sheet.url}")
        
        return sheet.url

# Usage:
# from google_sheets_sync import GoogleSheetsSync
# sync = GoogleSheetsSync()
# sync.sync_attendance()
```

---

## 2. 📚 Google Classroom Integration

### Setup Steps:

1. **Enable Google Classroom API**
   - In Google Cloud Console
   - Enable "Google Classroom API"
   - Use same service account

2. **Create Classes**
   - Create class for each subject
   - Add students
   - Note Class IDs

### Code Implementation:

```python
# classdoodle/google_classroom_sync.py

from googleapiclient.discovery import build
from google.oauth2 import service_account

class ClassroomSync:
    """Sync lesson materials to Google Classroom"""
    
    def __init__(self, credentials_file='classdoodle/credentials/google-credentials.json'):
        SCOPES = ['https://www.googleapis.com/auth/classroom.courses']
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=SCOPES)
        
        self.service = build('classroom', 'v1', credentials=credentials)
    
    def post_material(self, course_id, title, description, materials=[]):
        """Post lesson materials to Google Classroom"""
        
        material = {
            'title': title,
            'description': description,
            'materials': materials,
            'state': 'PUBLISHED'
        }
        
        result = self.service.courses().courseWork().create(
            courseId=course_id,
            body=material
        ).execute()
        
        print(f"✅ Posted to Google Classroom: {title}")
        return result

# Usage:
# from google_classroom_sync import ClassroomSync
# classroom = ClassroomSync()
# classroom.post_material(course_id='...', title='Week 1: Algebra', ...)
```

---

## 3. 📧 Automated Email Notifications

### Setup:

```python
# classdoodle/email_automation.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailAutomation:
    """Send automated emails to students and parents"""
    
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
        # Store credentials securely (use environment variables)
        import os
        self.email = os.getenv('CLASSDOODLE_EMAIL')
        self.password = os.getenv('CLASSDOODLE_EMAIL_PASSWORD')
    
    def send_absence_notification(self, student_name, parent_email, subject, date):
        """Notify parent of student absence"""
        
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = parent_email
        message['Subject'] = f'ClassDoodle: Absence Notification - {student_name}'
        
        body = f"""
        Dear Parent/Guardian,
        
        This is an automated notification from ClassDoodle.
        
        Student: {student_name}
        Subject: {subject}
        Date: {date}
        Status: ABSENT
        
        Please contact us if there are any concerns.
        
        Best regards,
        ClassDoodle Team
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
        
        print(f"✅ Sent absence notification for {student_name}")
    
    def send_daily_reminder(self, student_email, schedule):
        """Send daily schedule reminder"""
        
        message = MIMEMultipart()
        message['From'] = self.email
        message['To'] = student_email
        message['Subject'] = 'ClassDoodle: Today\'s Schedule'
        
        schedule_text = "\n".join([f"  {item['time']} - {item['subject']}" for item in schedule])
        
        body = f"""
        Good morning!
        
        Here's your schedule for today:
        
{schedule_text}
        
        Class link: [Your Zoom/Meet link]
        
        See you at 7:00 AM!
        
        ClassDoodle Team
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(message)
        
        print(f"✅ Sent daily reminder to {student_email}")

# Usage:
# from email_automation import EmailAutomation
# emailer = EmailAutomation()
# emailer.send_daily_reminder('student@example.com', schedule)
```

---

## 4. 💬 WhatsApp Automation (Twilio)

### Setup:

```bash
pip install twilio
```

```python
# classdoodle/whatsapp_notifications.py

from twilio.rest import Client
import os

class WhatsAppNotifications:
    """Send WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_absence_alert(self, parent_number, student_name, subject):
        """Send absence alert to parent"""
        
        message_body = f"""
🚨 ClassDoodle Alert

{student_name} was absent from {subject} today.

Please confirm if everything is okay.
        """
        
        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{parent_number}'
        )
        
        print(f"✅ Sent WhatsApp alert to {parent_number}")
        return message.sid
    
    def send_performance_update(self, parent_number, student_name, subject, score, trend):
        """Send performance update"""
        
        emoji = "📈" if trend == "improving" else "📉" if trend == "declining" else "➡️"
        
        message_body = f"""
📊 ClassDoodle Performance Update

Student: {student_name}
Subject: {subject}
Latest Score: {score}%
Trend: {trend} {emoji}

Keep up the good work!
        """
        
        message = self.client.messages.create(
            from_=f'whatsapp:{self.whatsapp_number}',
            body=message_body,
            to=f'whatsapp:{parent_number}'
        )
        
        return message.sid

# Usage:
# from whatsapp_notifications import WhatsAppNotifications
# whatsapp = WhatsAppNotifications()
# whatsapp.send_absence_alert('+27123456789', 'Thabo', 'Mathematics')
```

---

## 5. 🔄 Automated Daily Workflow

### Master Automation Script:

```python
# classdoodle/auto_morning_routine.py

from datetime import datetime, date
from timetable_generator import generate_daily_timetable
from email_automation import EmailAutomation
from google_sheets_sync import GoogleSheetsSync
from attendance_system import AttendanceTracker

def morning_routine():
    """Run this at 6:30 AM every morning"""
    
    today = date.today()
    day_name = today.strftime("%A")
    
    # Skip weekends
    if day_name in ["Saturday", "Sunday"]:
        return
    
    print("🌅 Running morning routine...")
    
    # 1. Get today's schedule
    schedule = generate_daily_timetable(day_name)
    
    # 2. Load students
    tracker = AttendanceTracker()
    students = tracker.students
    
    # 3. Send daily reminders
    emailer = EmailAutomation()
    
    for student in students:
        try:
            emailer.send_daily_reminder(student['email'], schedule)
        except Exception as e:
            print(f"⚠️  Failed to send email to {student['name']}: {e}")
    
    # 4. Sync yesterday's attendance to Google Sheets
    try:
        sync = GoogleSheetsSync()
        sync.sync_attendance()
    except Exception as e:
        print(f"⚠️  Failed to sync to Google Sheets: {e}")
    
    print("✅ Morning routine complete!")

if __name__ == "__main__":
    morning_routine()
```

### Schedule with Windows Task Scheduler:

```powershell
# Run at 6:30 AM every weekday
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\Users\NefefLocal\Documents\class\classdoodle\auto_morning_routine.py"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday,Tuesday,Wednesday,Thursday,Friday -At 6:30AM
Register-ScheduledTask -TaskName "ClassDoodle Morning Routine" -Action $action -Trigger $trigger
```

---

## 6. 🎯 Complete Integration Checklist

### Phase 1: Basic Setup (Week 1)
- [ ] Set up Google Cloud Project
- [ ] Create service account
- [ ] Enable APIs (Sheets, Classroom, Drive)
- [ ] Download credentials JSON
- [ ] Test Google Sheets sync

### Phase 2: Automation (Week 2)
- [ ] Set up email automation (Gmail/SMTP)
- [ ] Create email templates
- [ ] Test daily reminders
- [ ] Test absence notifications

### Phase 3: Advanced (Week 3)
- [ ] Set up Twilio for WhatsApp
- [ ] Create WhatsApp message templates
- [ ] Test WhatsApp alerts
- [ ] Set up Task Scheduler for morning routine

### Phase 4: Monitoring (Week 4)
- [ ] Create dashboards in Google Sheets
- [ ] Set up automated reporting
- [ ] Monitor integration health
- [ ] Optimize based on feedback

---

## 💡 Quick Start

1. **Install dependencies:**
```bash
pip install gspread oauth2client google-auth google-auth-oauthlib twilio
```

2. **Set environment variables:**
```bash
# In PowerShell
$env:CLASSDOODLE_EMAIL="your-email@gmail.com"
$env:CLASSDOODLE_EMAIL_PASSWORD="your-app-password"
$env:TWILIO_ACCOUNT_SID="your-sid"
$env:TWILIO_AUTH_TOKEN="your-token"
$env:TWILIO_WHATSAPP_NUMBER="+14155238886"
```

3. **Test integrations:**
```python
python classdoodle/google_sheets_sync.py
python classdoodle/email_automation.py
```

---

**You're building something incredible! 🚀**
