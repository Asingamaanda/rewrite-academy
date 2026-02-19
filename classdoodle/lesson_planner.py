"""
ClassDoodle - Standardized Lesson Plan Generator
Automated lesson planning with templates for all subjects
"""

from datetime import datetime, timedelta
import json
from pathlib import Path

class LessonPlanner:
    """Automated lesson plan generation for ClassDoodle"""
    
    def __init__(self, data_dir="classdoodle/lesson_plans"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Matric curriculum topics (simplified)
        self.curriculum = {
            "Mathematics": [
                "Patterns, Sequences & Series",
                "Functions & Graphs",
                "Algebra & Equations",
                "Calculus (Differentiation)",
                "Calculus (Integration)",
                "Finance, Growth & Decay",
                "Statistics & Probability",
                "Trigonometry",
                "Analytical Geometry",
                "Euclidean Geometry"
            ],
            "Physical Sciences": [
                "Mechanics (Vectors, Motion)",
                "Newton's Laws & Forces",
                "Work, Energy & Power",
                "Momentum & Impulse",
                "Electrostatics",
                "Electric Circuits",
                "Electromagnetism",
                "Waves & Sound",
                "Chemical Reactions",
                "Organic Chemistry"
            ],
            "Life Sciences": [
                "DNA & Protein Synthesis",
                "Meiosis & Genetics",
                "Evolution & Speciation",
                "Human Impact on Environment",
                "Plant & Animal Tissues",
                "Human Nervous System",
                "Human Endocrine System",
                "Human Reproduction",
                "Human Excretion",
                "Population Ecology"
            ],
            "English Home Language": [
                "Poetry Analysis",
                "Novel Study",
                "Drama/Shakespeare",
                "Comprehension Skills",
                "Essay Writing",
                "Visual Literacy",
                "Grammar & Language",
                "Creative Writing",
                "Oral Presentation",
                "Exam Techniques"
            ],
            "Accounting": [
                "GAAP Principles",
                "General Ledger & Trial Balance",
                "Financial Statements",
                "Cash Flow Statements",
                "VAT & Reconciliations",
                "Fixed Assets",
                "Partnerships",
                "Companies",
                "Manufacturing",
                "Budgeting"
            ]
        }
    
    def create_lesson_plan(self, subject, topic, date_str, time_slot, week_number):
        """Generate standardized lesson plan"""
        
        lesson_plan = {
            "school": "ClassDoodle - Matric Rewrite School",
            "subject": subject,
            "topic": topic,
            "date": date_str,
            "time": time_slot,
            "week": week_number,
            "duration": "50 minutes",
            
            "learning_objectives": [
                f"Understand core concepts of {topic}",
                f"Apply {topic} to exam-style questions",
                f"Identify common mistakes in {topic}"
            ],
            
            "lesson_structure": {
                "00:00-05:00": {
                    "activity": "Recap & Activation",
                    "description": "Quick recap of previous lesson, check homework",
                    "resources": "Previous notes, homework solutions"
                },
                "05:00-20:00": {
                    "activity": "Direct Instruction",
                    "description": f"Teach new concept: {topic}",
                    "resources": "PowerPoint slides, Manim animations, textbook"
                },
                "20:00-35:00": {
                    "activity": "Guided Practice",
                    "description": "Work through examples together",
                    "resources": "Practice worksheets, past papers"
                },
                "35:00-45:00": {
                    "activity": "Independent Practice",
                    "description": "Students solve problems individually",
                    "resources": "Exercise book, past paper questions"
                },
                "45:00-50:00": {
                    "activity": "Review & Exit Ticket",
                    "description": "Summarize key points, assign homework",
                    "resources": "Exit ticket questions, homework sheet"
                }
            },
            
            "assessment": {
                "formative": "Exit ticket with 3 quick questions",
                "homework": f"Complete {topic} worksheet (10-15 questions)",
                "next_assessment": "Weekly quiz on Friday"
            },
            
            "differentiation": {
                "support": "Provide formula sheet, pair with stronger student",
                "extension": "Challenge questions from advanced past papers"
            },
            
            "resources_needed": [
                "Laptop with projector",
                "Whiteboard & markers",
                "Student workbooks",
                "Past paper questions",
                "Manim animations (if applicable)"
            ],
            
            "notes": "",
            "reflection": ""
        }
        
        # Save lesson plan
        filename = f"{date_str}_{subject.replace(' ', '_')}_{time_slot.replace(':','').replace('-','_')}.json"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(lesson_plan, f, indent=2)
        
        return lesson_plan, filepath
    
    def generate_weekly_plans(self, week_start_date, week_number):
        """Generate all lesson plans for the week"""
        
        from timetable_generator import WEEKLY_SCHEDULE, TIME_SLOTS
        
        week_start = datetime.strptime(week_start_date, "%Y-%m-%d")
        
        print("=" * 80)
        print(f"GENERATING LESSON PLANS - WEEK {week_number}")
        print(f"Starting: {week_start.strftime('%A, %d %B %Y')}")
        print("=" * 80)
        print()
        
        plans_created = 0
        
        for day_offset, day_name in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
            current_date = week_start + timedelta(days=day_offset)
            date_str = current_date.strftime("%Y-%m-%d")
            
            print(f"\n📅 {day_name}, {current_date.strftime('%d %B %Y')}")
            print("-" * 70)
            
            schedule = WEEKLY_SCHEDULE[day_name]
            period_slots = [slot for slot in TIME_SLOTS if slot["type"] == "period" or slot["type"] == "wrap-up"]
            
            for i, subject in enumerate(schedule):
                if i < len(period_slots):
                    time_slot = f"{period_slots[i]['start']}-{period_slots[i]['end']}"
                    
                    # Skip non-academic sessions
                    if subject in ["Study Skills Workshop", "Exam Prep Session", "Mental Health Check-in", "Past Papers Practice", "Weekly Review & Goal Setting"]:
                        print(f"  {time_slot}  →  {subject} (no lesson plan needed)")
                        continue
                    
                    # Get topic for this subject
                    if subject in self.curriculum:
                        topic_index = (week_number - 1) % len(self.curriculum[subject])
                        topic = self.curriculum[subject][topic_index]
                        
                        plan, filepath = self.create_lesson_plan(
                            subject=subject,
                            topic=topic,
                            date_str=date_str,
                            time_slot=time_slot,
                            week_number=week_number
                        )
                        
                        print(f"  ✅ {time_slot}  →  {subject}: {topic}")
                        plans_created += 1
        
        print("\n" + "=" * 80)
        print(f"✨ Created {plans_created} lesson plans for Week {week_number}")
        print(f"📁 Saved to: {self.data_dir}")
        print("=" * 80)
    
    def print_lesson_plan(self, filepath):
        """Print formatted lesson plan"""
        
        with open(filepath, 'r') as f:
            plan = json.load(f)
        
        print("\n" + "=" * 80)
        print("LESSON PLAN")
        print("=" * 80)
        print(f"School: {plan['school']}")
        print(f"Subject: {plan['subject']}")
        print(f"Topic: {plan['topic']}")
        print(f"Date: {plan['date']}")
        print(f"Time: {plan['time']}")
        print(f"Duration: {plan['duration']}")
        print()
        
        print("LEARNING OBJECTIVES:")
        for obj in plan['learning_objectives']:
            print(f"  • {obj}")
        print()
        
        print("LESSON STRUCTURE:")
        for time, activity in plan['lesson_structure'].items():
            print(f"\n  ⏰ {time}")
            print(f"     Activity: {activity['activity']}")
            print(f"     {activity['description']}")
        print()
        
        print("ASSESSMENT:")
        print(f"  Formative: {plan['assessment']['formative']}")
        print(f"  Homework: {plan['assessment']['homework']}")
        print()
        
        print("RESOURCES NEEDED:")
        for resource in plan['resources_needed']:
            print(f"  ☑ {resource}")
        
        print("=" * 80)


if __name__ == "__main__":
    planner = LessonPlanner()
    
    # Generate lesson plans for Week 1
    planner.generate_weekly_plans(
        week_start_date="2026-02-23",  # Next Monday
        week_number=1
    )
    
    # Show example lesson plan
    sample_plans = list(planner.data_dir.glob("*.json"))
    if sample_plans:
        print("\n\n--- SAMPLE LESSON PLAN ---")
        planner.print_lesson_plan(sample_plans[0])
