"""
ClassDoodle - Marketing & Conversion Tracking
Track where students come from and conversion rates
"""

import csv
import json
from pathlib import Path
from datetime import datetime

class MarketingTracker:
    """Track marketing performance and student acquisition"""
    
    def __init__(self, data_dir="classdoodle/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def log_lead(self, name, phone, email, source, notes=""):
        """Log a new lead/inquiry"""
        
        leads_file = self.data_dir / "leads.csv"
        
        # Create file with headers if doesn't exist
        if not leads_file.exists():
            with open(leads_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Time', 'Name', 'Phone', 'Email', 'Source', 'Status', 'Notes'])
        
        # Append new lead
        with open(leads_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d'),
                datetime.now().strftime('%H:%M:%S'),
                name,
                phone,
                email,
                source,  # e.g., "Facebook Ad", "WhatsApp", "Word of Mouth", "Instagram"
                'New',
                notes
            ])
        
        print(f"✅ Lead logged: {name} from {source}")
    
    def update_lead_status(self, phone, new_status):
        """Update lead status (New → Contacted → Enrolled → Dropped)"""
        
        leads_file = self.data_dir / "leads.csv"
        
        if not leads_file.exists():
            print("❌ No leads file found")
            return
        
        # Read all leads
        leads = []
        with open(leads_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Phone'] == phone:
                    row['Status'] = new_status
                    row['Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                leads.append(row)
        
        # Write back
        with open(leads_file, 'w', newline='') as f:
            fieldnames = list(leads[0].keys())
            if 'Updated' not in fieldnames:
                fieldnames.append('Updated')
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(leads)
        
        print(f"✅ Updated {phone} to: {new_status}")
    
    def show_conversion_funnel(self):
        """Show marketing conversion funnel"""
        
        leads_file = self.data_dir / "leads.csv"
        
        if not leads_file.exists():
            print("❌ No leads data yet")
            return
        
        # Count by status
        stats = {
            'New': 0,
            'Contacted': 0,
            'Enrolled': 0,
            'Dropped': 0
        }
        
        source_stats = {}
        
        with open(leads_file, 'r') as f:
            reader = csv.DictReader(f)
            total_leads = 0
            
            for row in reader:
                total_leads += 1
                status = row.get('Status', 'New')
                stats[status] = stats.get(status, 0) + 1
                
                source = row.get('Source', 'Unknown')
                if source not in source_stats:
                    source_stats[source] = {'total': 0, 'enrolled': 0}
                source_stats[source]['total'] += 1
                if status == 'Enrolled':
                    source_stats[source]['enrolled'] += 1
        
        print("\n" + "=" * 70)
        print("📊 CLASSDOODLE MARKETING FUNNEL")
        print("=" * 70)
        print(f"\nTotal Leads: {total_leads}")
        print()
        
        # Funnel visualization
        for status in ['New', 'Contacted', 'Enrolled']:
            count = stats.get(status, 0)
            percentage = (count / total_leads * 100) if total_leads > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"{status:12s} │ {bar} {count} ({percentage:.1f}%)")
        
        dropped = stats.get('Dropped', 0)
        print(f"\nDropped: {dropped}")
        
        # Conversion rate
        enrolled = stats.get('Enrolled', 0)
        conversion_rate = (enrolled / total_leads * 100) if total_leads > 0 else 0
        
        print(f"\n🎯 CONVERSION RATE: {conversion_rate:.1f}%")
        print(f"   ({enrolled} enrolled out of {total_leads} leads)")
        
        # Source performance
        print("\n" + "=" * 70)
        print("📱 LEAD SOURCES")
        print("=" * 70)
        
        for source, data in source_stats.items():
            source_conversion = (data['enrolled'] / data['total'] * 100) if data['total'] > 0 else 0
            print(f"{source:20s} → {data['total']:3d} leads, {data['enrolled']:3d} enrolled ({source_conversion:.1f}%)")
        
        print("=" * 70)


def quick_log_lead(name, phone, email, source):
    """Quick function to log a lead"""
    tracker = MarketingTracker()
    tracker.log_lead(name, phone, email, source)


def show_funnel():
    """Quick function to show conversion funnel"""
    tracker = MarketingTracker()
    tracker.show_conversion_funnel()


if __name__ == "__main__":
    print("=" * 70)
    print("CLASSDOODLE MARKETING TRACKER")
    print("=" * 70)
    print()
    print("SAMPLE USAGE:")
    print()
    print("Log a new lead:")
    print('  quick_log_lead("Thabo M", "0712345678", "thabo@email.com", "Facebook Ad")')
    print()
    print("Update lead status:")
    print('  tracker = MarketingTracker()')
    print('  tracker.update_lead_status("0712345678", "Enrolled")')
    print()
    print("View conversion funnel:")
    print('  show_funnel()')
    print()
    print("=" * 70)
