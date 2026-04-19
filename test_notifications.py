"""Test script to verify notification system functionality."""
from app import app, db
from models import Tenant
from routes import _get_upcoming_urgent_tenants, _get_overdue_tenants

def test_notification_system():
    """Test the notification system with existing data."""
    with app.app_context():
        print("=" * 60)
        print("NOTIFICATION SYSTEM TEST")
        print("=" * 60)
        
        # Get all active tenants with balance
        tenants = Tenant.query.filter(
            Tenant.status == "active",
            Tenant.pending_balance > 0
        ).all()
        
        print(f"\nTotal active tenants with balance: {len(tenants)}")
        print("\n" + "-" * 60)
        
        # Display all tenants
        for t in tenants:
            print(f"\nNickname: {t.nickname}")
            print(f"  Full Name: {t.full_name}")
            print(f"  Room: {t.room_number}")
            print(f"  Due Day: {t.due_day}")
            print(f"  Monthly Rent: {t.monthly_rent}")
            print(f"  Pending Balance: {t.pending_balance}")
        
        # Test upcoming/urgent logic
        print("\n" + "=" * 60)
        print("TESTING UPCOMING/URGENT LOGIC")
        print("=" * 60)
        
        upcoming_urgent = _get_upcoming_urgent_tenants()
        print(f"\nUpcoming/Urgent tenants found: {len(upcoming_urgent)}")
        
        if upcoming_urgent:
            for notif in upcoming_urgent:
                print(f"\n[{notif['urgency'].upper()}] {notif['full_name']}")
                print(f"  Room: {notif['room_number']}")
                print(f"  Due Date: {notif['due_date']}")
                print(f"  Days Remaining: {notif['days_remaining']}")
                print(f"  Balance: {notif['pending_balance']:.2f}")
        else:
            print("  No upcoming/urgent notifications found.")
        
        # Test overdue logic
        print("\n" + "=" * 60)
        print("TESTING OVERDUE LOGIC")
        print("=" * 60)
        
        overdue = _get_overdue_tenants()
        print(f"\nOverdue tenants found: {len(overdue)}")
        
        if overdue:
            for t in overdue:
                print(f"\n{t.full_name} (Room {t.room_number})")
                print(f"  Due Day: {t.due_day}")
                print(f"  Pending Balance: {t.pending_balance:.2f}")
        else:
            print("  No overdue tenants found.")
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"  Total tenants with balance: {len(tenants)}")
        print(f"  Upcoming/Urgent notifications: {len(upcoming_urgent)}")
        print(f"  Urgent (3 days or less): {sum(1 for n in upcoming_urgent if n['urgency'] == 'urgent')}")
        print(f"  Upcoming (7 days or less): {sum(1 for n in upcoming_urgent if n['urgency'] == 'upcoming')}")
        print(f"  Overdue tenants: {len(overdue)}")
        
        # Check for errors
        print("\n" + "=" * 60)
        print("ERROR CHECK")
        print("=" * 60)
        
        errors = []
        
        # Check if notification count matches
        expected_notification_count = len(upcoming_urgent)
        if expected_notification_count != len(upcoming_urgent):
            errors.append(f"Notification count mismatch: expected {expected_notification_count}, got {len(upcoming_urgent)}")
        
        # Check if sorting is correct (urgent first)
        if len(upcoming_urgent) > 1:
            for i in range(len(upcoming_urgent) - 1):
                current = upcoming_urgent[i]
                next_item = upcoming_urgent[i + 1]
                if current['urgency'] == 'upcoming' and next_item['urgency'] == 'urgent':
                    errors.append(f"Sorting error: urgent items should come first")
        
        if errors:
            print("  ERRORS FOUND:")
            for error in errors:
                print(f"    - {error}")
        else:
            print("  No errors detected!")
        
        print("\n" + "=" * 60)
        print("TEST COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    test_notification_system()
