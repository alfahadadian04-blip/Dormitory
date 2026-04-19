"""Script to create test tenants for notification system testing."""
from datetime import date, timedelta
from app import app, db
from models import Tenant
import random

def create_test_tenants():
    """Create test tenants with various due dates to test notification system."""
    with app.app_context():
        # Clear existing test tenants (optional - comment out if you want to keep existing data)
        # Tenant.query.filter(Tenant.nickname.like('test%')).delete()
        
        test_tenants = [
            {
                'nickname': 'test_tenant_1',
                'full_name': 'John Doe',
                'room_number': '101',
                'contact_number': '123-456-7890',
                'monthly_rent': 5000.00,
                'due_day': (date.today() + timedelta(days=1)).day,  # Due tomorrow (urgent)
                'pending_balance': 5000.00,
                'status': 'active'
            },
            {
                'nickname': 'test_tenant_2',
                'full_name': 'Jane Smith',
                'room_number': '102',
                'contact_number': '123-456-7891',
                'monthly_rent': 4500.00,
                'due_day': (date.today() + timedelta(days=2)).day,  # Due in 2 days (urgent)
                'pending_balance': 4500.00,
                'status': 'active'
            },
            {
                'nickname': 'test_tenant_3',
                'full_name': 'Bob Johnson',
                'room_number': '103',
                'contact_number': '123-456-7892',
                'monthly_rent': 6000.00,
                'due_day': (date.today() + timedelta(days=5)).day,  # Due in 5 days (upcoming)
                'pending_balance': 6000.00,
                'status': 'active'
            },
            {
                'nickname': 'test_tenant_4',
                'full_name': 'Alice Williams',
                'room_number': '104',
                'contact_number': '123-456-7893',
                'monthly_rent': 5500.00,
                'due_day': (date.today() + timedelta(days=7)).day,  # Due in 7 days (upcoming)
                'pending_balance': 5500.00,
                'status': 'active'
            },
            {
                'nickname': 'test_tenant_5',
                'full_name': 'Charlie Brown',
                'room_number': '105',
                'contact_number': '123-456-7894',
                'monthly_rent': 4800.00,
                'due_day': (date.today() + timedelta(days=10)).day,  # Due in 10 days (no notification)
                'pending_balance': 4800.00,
                'status': 'active'
            },
            {
                'nickname': 'test_tenant_6',
                'full_name': 'Diana Prince',
                'room_number': '106',
                'contact_number': '123-456-7895',
                'monthly_rent': 5200.00,
                'due_day': (date.today() - timedelta(days=2)).day,  # Overdue (past due)
                'pending_balance': 5200.00,
                'status': 'active'
            },
        ]
        
        created_count = 0
        for tenant_data in test_tenants:
            # Check if tenant already exists
            existing = Tenant.query.filter_by(nickname=tenant_data['nickname']).first()
            if existing:
                print(f"Tenant {tenant_data['nickname']} already exists, skipping...")
                continue
            
            tenant = Tenant(**tenant_data)
            db.session.add(tenant)
            created_count += 1
            print(f"Created tenant: {tenant_data['full_name']} (Room {tenant_data['room_number']}) - Due in {(tenant_data['due_day'] - date.today().day) if tenant_data['due_day'] >= date.today().day else 'overdue'} days")
        
        db.session.commit()
        print(f"\nTotal test tenants created: {created_count}")
        print("\nNotification System Test Data Summary:")
        print("  - Urgent (3 days or less): 2 tenants")
        print("  - Upcoming (7 days or less): 2 tenants")
        print("  - No notification (more than 7 days): 1 tenant")
        print("  - Overdue: 1 tenant")

if __name__ == "__main__":
    print("Creating test tenants for notification system testing...")
    create_test_tenants()
    print("\nDone! Refresh your browser to see the notification badge and dropdown.")
