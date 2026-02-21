"""
ClassDoodle Backend API
Clean API for all backend operations
"""

from pathlib import Path

from backend.database import (
    ClassDoodleDB, StudentManager, AttendanceManager, 
    AssessmentManager, PaymentManager
)
from datetime import datetime, date
import csv
import json


class ClassDoodleAPI:
    """Main API for ClassDoodle operations"""
    
    def __init__(self, db_path="classdoodle/data/classdoodle.db"):
        self.db = ClassDoodleDB(db_path)
        self.students = StudentManager(self.db)
        self.attendance = AttendanceManager(self.db)
        self.assessments = AssessmentManager(self.db)
        self.payments = PaymentManager(self.db)
    
    # ==================== STUDENT OPERATIONS ====================
    
    def register_student(self, name, email, phone=None, parent_name=None,
                        parent_phone=None, parent_email=None, 
                        subjects=None, notes=None):
        """Register a new student"""
        return self.students.add_student(
            name=name, email=email, phone=phone,
            parent_name=parent_name, parent_phone=parent_phone,
            parent_email=parent_email, subjects=subjects, notes=notes
        )
    
    def get_student_info(self, student_id):
        """Get complete student information"""
        student, subjects = self.students.get_student(student_id)
        
        if not student:
            return None
        
        # Add performance data
        overall_avg = self.assessments.get_student_average(student_id)
        attendance_rate = self.attendance.get_attendance_rate(student_id)
        
        student['subjects'] = subjects
        student['overall_average'] = round(overall_avg, 1)
        student['attendance_rate'] = round(attendance_rate, 1)
        
        # Determine risk level
        if overall_avg < 50:
            student['risk_level'] = 'high'
        elif overall_avg < 70:
            student['risk_level'] = 'medium'
        else:
            student['risk_level'] = 'low'
        
        return student
    
    def get_all_students_summary(self):
        """Get summary of all students with key metrics"""
        students = self.students.get_all_students()
        
        summary = []
        for student in students:
            student['overall_average'] = round(
                self.assessments.get_student_average(student['student_id']), 1
            )
            student['attendance_rate'] = round(
                self.attendance.get_attendance_rate(student['student_id']), 1
            )
            
            # Determine risk level
            avg = student['overall_average']
            if avg < 50:
                student['risk_level'] = 'high'
            elif avg < 70:
                student['risk_level'] = 'medium'
            else:
                student['risk_level'] = 'low'
            
            summary.append(student)
        
        return summary
    
    def import_students_from_csv(self, csv_file_path):
        """Import students from CSV file"""
        students_data = []
        
        with open(csv_file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip example rows
                if 'Example' in row.get('name', ''):
                    continue
                
                subjects = row.get('subjects', '').split(',') if row.get('subjects') else []
                subjects = [s.strip() for s in subjects if s.strip()]
                
                students_data.append({
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row.get('phone', ''),
                    'parent_name': row.get('parent_name', ''),
                    'parent_phone': row.get('parent_phone', ''),
                    'parent_email': row.get('parent_email', ''),
                    'subjects': subjects,
                    'notes': row.get('notes', '')
                })
        
        return self.students.bulk_import(students_data)
    
    # ==================== ATTENDANCE OPERATIONS ====================
    
    def mark_class_attendance(self, present_student_ids, date_str, 
                             time_slot, subject):
        """Mark attendance for a class - present students only"""
        
        # Get all active students
        all_students = self.students.get_all_students(status='active')
        all_ids = [s['student_id'] for s in all_students]
        
        # Mark present students
        self.attendance.mark_attendance(
            present_student_ids, date_str, time_slot, subject, 'present'
        )
        
        # Mark absent students
        absent_ids = [sid for sid in all_ids if sid not in present_student_ids]
        self.attendance.mark_attendance(
            absent_ids, date_str, time_slot, subject, 'absent'
        )
        
        return {
            'present': len(present_student_ids),
            'absent': len(absent_ids),
            'total': len(all_ids)
        }
    
    def get_daily_attendance_report(self, date_str=None):
        """Get attendance report for a specific day"""
        if date_str is None:
            date_str = date.today().isoformat()
        
        records = self.attendance.get_attendance(date_str=date_str)
        
        # Group by subject
        by_subject = {}
        for record in records:
            subject = record['subject']
            if subject not in by_subject:
                by_subject[subject] = {'present': 0, 'absent': 0, 'total': 0}
            
            by_subject[subject]['total'] += 1
            if record['status'] == 'present':
                by_subject[subject]['present'] += 1
            else:
                by_subject[subject]['absent'] += 1
        
        return {
            'date': date_str,
            'by_subject': by_subject,
            'total_records': len(records)
        }
    
    def get_student_attendance_history(self, student_id, limit=30):
        """Get recent attendance history for a student"""
        records = self.attendance.get_attendance(student_id=student_id)
        return records[:limit]
    
    # ==================== ASSESSMENT OPERATIONS ====================
    
    def record_assessment(self, student_id, subject, assessment_type, 
                         score, max_score=100, notes=None):
        """Record an assessment score"""
        return self.assessments.add_assessment(
            student_id=student_id,
            subject=subject,
            assessment_type=assessment_type,
            score=score,
            max_score=max_score,
            notes=notes
        )
    
    def get_student_performance(self, student_id):
        """Get complete performance data for a student"""
        assessments = self.assessments.get_assessments(student_id=student_id)
        
        # Group by subject
        by_subject = {}
        for assessment in assessments:
            subject = assessment['subject']
            percentage = (assessment['score'] / assessment['max_score']) * 100
            
            if subject not in by_subject:
                by_subject[subject] = {
                    'scores': [],
                    'assessments': []
                }
            
            by_subject[subject]['scores'].append(percentage)
            by_subject[subject]['assessments'].append(assessment)
        
        # Calculate averages and trends
        performance = {}
        for subject, data in by_subject.items():
            scores = data['scores']
            performance[subject] = {
                'average': round(sum(scores) / len(scores), 1),
                'latest': round(scores[0], 1) if scores else 0,
                'count': len(scores),
                'trend': self._calculate_trend(scores),
                'assessments': data['assessments'][:5]  # Last 5 assessments
            }
        
        return performance
    
    def _calculate_trend(self, scores):
        """Calculate if scores are improving, declining, or stable"""
        if len(scores) < 2:
            return 'stable'
        
        recent = scores[:3]  # Last 3 scores
        older = scores[3:6] if len(scores) > 3 else scores
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        diff = recent_avg - older_avg
        
        if diff > 5:
            return 'improving'
        elif diff < -5:
            return 'declining'
        else:
            return 'stable'
    
    def get_class_performance_summary(self):
        """Get performance summary for entire class"""
        students = self.get_all_students_summary()
        
        # Calculate class statistics
        averages = [s['overall_average'] for s in students if s['overall_average'] > 0]
        
        if not averages:
            return {
                'class_average': 0,
                'students': students,
                'risk_breakdown': {}
            }
        
        class_avg = sum(averages) / len(averages)
        
        # Risk breakdown
        risk_breakdown = {
            'high': len([s for s in students if s.get('risk_level') == 'high']),
            'medium': len([s for s in students if s.get('risk_level') == 'medium']),
            'low': len([s for s in students if s.get('risk_level') == 'low'])
        }
        
        return {
            'class_average': round(class_avg, 1),
            'total_students': len(students),
            'students': students,
            'risk_breakdown': risk_breakdown
        }
    
    # ==================== PAYMENT OPERATIONS ====================
    
    def record_payment(self, student_id, amount, month_for, 
                      payment_method=None, reference=None):
        """Record a student payment"""
        payment_date = date.today().isoformat()
        return self.payments.record_payment(
            student_id=student_id,
            amount=amount,
            payment_date=payment_date,
            month_for=month_for,
            payment_method=payment_method,
            reference=reference
        )
    
    def get_payment_status(self, month_for):
        """Get payment status for all students for a specific month"""
        all_students = self.students.get_all_students(status='active')
        paid_students = self.payments.get_payments(month_for=month_for, status='paid')
        paid_ids = {p['student_id'] for p in paid_students}
        
        paid = []
        outstanding = []
        
        for student in all_students:
            if student['student_id'] in paid_ids:
                # Get payment details
                payment = next(p for p in paid_students if p['student_id'] == student['student_id'])
                paid.append({
                    'student': student,
                    'payment': payment
                })
            else:
                outstanding.append(student)
        
        return {
            'month': month_for,
            'paid': paid,
            'outstanding': outstanding,
            'paid_count': len(paid),
            'outstanding_count': len(outstanding),
            'total_revenue': sum(p['payment']['amount'] for p in paid)
        }
    
    def get_revenue_summary(self):
        """Get overall revenue summary"""
        return self.payments.get_revenue_report()
    
    # ==================== ANALYTICS ====================
    
    def get_dashboard_stats(self):
        """Get key statistics for dashboard"""
        students = self.students.get_all_students(status='active')
        total_students = len(students)
        
        # Performance stats
        performance = self.get_class_performance_summary()
        
        # Attendance stats for today
        today = date.today().isoformat()
        attendance_today = self.get_daily_attendance_report(today)
        
        # Payment stats for current month
        current_month = date.today().strftime('%Y-%m')
        payment_status = self.get_payment_status(current_month)
        
        return {
            'total_students': total_students,
            'class_average': performance['class_average'],
            'at_risk': performance['risk_breakdown'].get('high', 0),
            'medium_risk': performance['risk_breakdown'].get('medium', 0),
            'on_track': performance['risk_breakdown'].get('low', 0),
            'attendance_today': attendance_today,
            'payments_this_month': {
                'paid': payment_status['paid_count'],
                'outstanding': payment_status['outstanding_count'],
                'revenue': payment_status['total_revenue']
            }
        }
    
    def close(self):
        """Close database connection"""
        self.db.close()


# ==================== CONVENIENCE FUNCTIONS ====================

def get_api():
    """Get API instance"""
    return ClassDoodleAPI()


if __name__ == "__main__":
    # Test backend
    api = ClassDoodleAPI()
    
    print("\n" + "=" * 70)
    print("✅ ClassDoodle Backend API Ready")
    print("=" * 70)
    print("\nAvailable operations:")
    print("\n📚 STUDENT MANAGEMENT:")
    print("  • register_student()")
    print("  • get_student_info()")
    print("  • get_all_students_summary()")
    print("  • import_students_from_csv()")
    print("\n✅ ATTENDANCE:")
    print("  • mark_class_attendance()")
    print("  • get_daily_attendance_report()")
    print("  • get_student_attendance_history()")
    print("\n📈 ASSESSMENTS:")
    print("  • record_assessment()")
    print("  • get_student_performance()")
    print("  • get_class_performance_summary()")
    print("\n💰 PAYMENTS:")
    print("  • record_payment()")
    print("  • get_payment_status()")
    print("  • get_revenue_summary()")
    print("\n📊 ANALYTICS:")
    print("  • get_dashboard_stats()")
    print("\n" + "=" * 70)
