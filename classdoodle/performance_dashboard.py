"""
ClassDoodle - Real-time Performance Dashboard
Track student progress, attendance, and identify at-risk students
"""

import csv
import json
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict

class PerformanceDashboard:
    """Monitor student performance and generate insights"""
    
    def __init__(self, data_dir="classdoodle/data"):
        self.data_dir = Path(data_dir)
        
    def load_student_data(self):
        """Load all student performance data"""
        
        # Load roster
        roster_file = self.data_dir / "student_roster.json"
        if not roster_file.exists():
            return []
        
        with open(roster_file, 'r') as f:
            students = json.load(f)
        
        # Load assessment data (create if doesn't exist)
        assessments_file = self.data_dir / "assessments.json"
        if not assessments_file.exists():
            # Create sample assessment data
            sample_assessments = {
                "CD001": {
                    "Mathematics": [85, 78, 92, 88],
                    "Physical Sciences": [72, 75, 80, 77],
                    "English Home Language": [65, 68, 70, 72]
                },
                "CD002": {
                    "Mathematics": [45, 52, 48, 50],
                    "Physical Sciences": [55, 58, 60, 62],
                    "English Home Language": [70, 72, 75, 78]
                },
                "CD003": {
                    "Mathematics": [90, 92, 88, 95],
                    "Physical Sciences": [88, 90, 87, 91],
                    "English Home Language": [82, 85, 87, 89]
                },
                "CD004": {
                    "Mathematics": [62, 65, 68, 70],
                    "Physical Sciences": [58, 60, 62, 65],
                    "English Home Language": [75, 77, 80, 82]
                },
                "CD005": {
                    "Mathematics": [78, 80, 82, 85],
                    "Physical Sciences": [80, 82, 85, 87],
                    "English Home Language": [88, 90, 92, 93]
                }
            }
            
            with open(assessments_file, 'w') as f:
                json.dump(sample_assessments, f, indent=2)
        
        with open(assessments_file, 'r') as f:
            assessments = json.load(f)
        
        # Merge data
        for student in students:
            student['assessments'] = assessments.get(student['id'], {})
        
        return students
    
    def calculate_metrics(self, student):
        """Calculate key performance metrics for a student"""
        
        metrics = {
            "student_id": student['id'],
            "student_name": student['name'],
            "subjects": {}
        }
        
        for subject, scores in student['assessments'].items():
            if scores:
                avg_score = sum(scores) / len(scores)
                latest_score = scores[-1]
                trend = "improving" if len(scores) > 1 and scores[-1] > scores[0] else "declining" if len(scores) > 1 and scores[-1] < scores[0] else "stable"
                
                metrics["subjects"][subject] = {
                    "average": round(avg_score, 1),
                    "latest": latest_score,
                    "trend": trend,
                    "num_assessments": len(scores),
                    "risk_level": "high" if avg_score < 50 else "medium" if avg_score < 70 else "low"
                }
        
        # Overall metrics
        all_scores = [score for scores in student['assessments'].values() for score in scores]
        if all_scores:
            metrics["overall_average"] = round(sum(all_scores) / len(all_scores), 1)
            metrics["overall_risk"] = "high" if metrics["overall_average"] < 50 else "medium" if metrics["overall_average"] < 70 else "low"
        
        return metrics
    
    def generate_dashboard(self):
        """Generate comprehensive dashboard"""
        
        students = self.load_student_data()
        
        if not students:
            print("❌ No student data available")
            return
        
        print("\n" + "=" * 90)
        print("CLASSDOODLE PERFORMANCE DASHBOARD")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 90)
        
        # Calculate metrics for all students
        all_metrics = [self.calculate_metrics(student) for student in students]
        
        # ===== OVERALL CLASS STATISTICS =====
        print("\n📊 CLASS OVERVIEW")
        print("-" * 90)
        print(f"Total Students: {len(students)}")
        
        overall_averages = [m["overall_average"] for m in all_metrics if "overall_average" in m]
        if overall_averages:
            class_avg = sum(overall_averages) / len(overall_averages)
            print(f"Class Average: {class_avg:.1f}%")
        
        # Risk levels
        high_risk = sum(1 for m in all_metrics if m.get("overall_risk") == "high")
        medium_risk = sum(1 for m in all_metrics if m.get("overall_risk") == "medium")
        low_risk = sum(1 for m in all_metrics if m.get("overall_risk") == "low")
        
        print(f"\n🚨 Risk Levels:")
        print(f"   High Risk (< 50%): {high_risk} students")
        print(f"   Medium Risk (50-70%): {medium_risk} students")
        print(f"   On Track (> 70%): {low_risk} students")
        
        # ===== SUBJECT PERFORMANCE =====
        print("\n📚 SUBJECT PERFORMANCE")
        print("-" * 90)
        
        subject_stats = defaultdict(list)
        for metrics in all_metrics:
            for subject, data in metrics["subjects"].items():
                subject_stats[subject].append(data["average"])
        
        for subject, averages in subject_stats.items():
            subj_avg = sum(averages) / len(averages)
            print(f"{subject:30s} → Class Avg: {subj_avg:5.1f}%")
        
        # ===== AT-RISK STUDENTS =====
        print("\n⚠️  AT-RISK STUDENTS (Require Immediate Attention)")
        print("-" * 90)
        
        at_risk = [m for m in all_metrics if m.get("overall_risk") in ["high", "medium"]]
        at_risk.sort(key=lambda x: x.get("overall_average", 0))
        
        if at_risk:
            for student in at_risk:
                print(f"\n{student['student_name']} ({student['student_id']})")
                print(f"   Overall Average: {student.get('overall_average', 'N/A')}% - {student.get('overall_risk', 'unknown').upper()} RISK")
                print(f"   Struggling in:")
                
                struggling_subjects = [(subj, data) for subj, data in student["subjects"].items() if data["risk_level"] in ["high", "medium"]]
                for subj, data in struggling_subjects:
                    print(f"      • {subj}: {data['average']}% ({data['trend']})")
        else:
            print("✅ No at-risk students - excellent work!")
        
        # ===== TOP PERFORMERS =====
        print("\n🌟 TOP PERFORMERS")
        print("-" * 90)
        
        top_students = sorted(all_metrics, key=lambda x: x.get("overall_average", 0), reverse=True)[:3]
        
        for i, student in enumerate(top_students, 1):
            print(f"{i}. {student['student_name']}: {student.get('overall_average', 'N/A')}%")
        
        # ===== RECOMMENDATIONS =====
        print("\n💡 AUTOMATED RECOMMENDATIONS")
        print("-" * 90)
        
        if high_risk > 0:
            print(f"⚠️  {high_risk} student(s) at HIGH RISK - Schedule intervention meetings")
        
        if medium_risk > 3:
            print(f"📝 {medium_risk} students at MEDIUM RISK - Consider group tutoring sessions")
        
        # Subject-specific recommendations
        for subject, averages in subject_stats.items():
            subj_avg = sum(averages) / len(averages)
            if subj_avg < 60:
                print(f"📚 {subject} class average is low ({subj_avg:.1f}%) - Review teaching strategy")
        
        print("\n" + "=" * 90)
    
    def generate_individual_report(self, student_id):
        """Generate detailed report for individual student"""
        
        students = self.load_student_data()
        student = next((s for s in students if s['id'] == student_id), None)
        
        if not student:
            print(f"❌ Student {student_id} not found")
            return
        
        metrics = self.calculate_metrics(student)
        
        print("\n" + "=" * 90)
        print(f"STUDENT PERFORMANCE REPORT")
        print("=" * 90)
        print(f"Student: {metrics['student_name']} ({metrics['student_id']})")
        print(f"Overall Average: {metrics.get('overall_average', 'N/A')}%")
        print(f"Risk Level: {metrics.get('overall_risk', 'unknown').upper()}")
        print()
        
        print("SUBJECT BREAKDOWN:")
        print("-" * 90)
        
        for subject, data in metrics["subjects"].items():
            print(f"\n📚 {subject}")
            print(f"   Average: {data['average']}%")
            print(f"   Latest Score: {data['latest']}%")
            print(f"   Trend: {data['trend'].upper()}")
            print(f"   Risk Level: {data['risk_level'].upper()}")
            print(f"   Assessments Completed: {data['num_assessments']}")
        
        print("\n" + "=" * 90)


if __name__ == "__main__":
    dashboard = PerformanceDashboard()
    
    # Generate full dashboard
    dashboard.generate_dashboard()
    
    # Example: Individual student report
    print("\n\n--- INDIVIDUAL STUDENT REPORT ---")
    dashboard.generate_individual_report("CD002")
