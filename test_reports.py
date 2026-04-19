"""Test script to verify existing reports functionality is not broken."""
from app import app, db
from models import Tenant, Payment
from routes import reports
from datetime import date
import random

def test_existing_reports_functionality():
    """Test that existing reports functionality still works correctly."""
    with app.app_context():
        print("=" * 60)
        print("TESTING EXISTING REPORTS FUNCTIONALITY")
        print("=" * 60)
        
        # Test 1: Check that reports route still exists and returns data
        print("\nTest 1: Testing reports route...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                response = client.get('/reports')
                if response.status_code == 200:
                    print("  [PASS] Reports route returns 200")
                else:
                    print(f"  [FAIL] Reports route returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing reports route: {e}")
        
        # Test 2: Check that export endpoints still exist
        print("\nTest 2: Testing export endpoints...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                response = client.get('/export/tenants.xlsx')
                if response.status_code in [200, 302]:  # 302 for redirect if not logged in
                    print("  [PASS] Export tenants endpoint exists")
                else:
                    print(f"  [FAIL] Export tenants returned {response.status_code}")
                
                response = client.get('/export/payments.xlsx')
                if response.status_code in [200, 302]:
                    print("  [PASS] Export payments endpoint exists")
                else:
                    print(f"  [FAIL] Export payments returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing export endpoints: {e}")
        
        # Test 3: Check that analytics endpoint exists
        print("\nTest 3: Testing analytics endpoint...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                response = client.get('/reports/analytics?filter_type=monthly')
                if response.status_code in [200, 401]:  # 401 if not authenticated
                    print(f"  [PASS] Analytics endpoint exists (status: {response.status_code})")
                else:
                    print(f"  [FAIL] Analytics endpoint returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing analytics endpoint: {e}")
        
        # Test 4: Check that database queries still work
        print("\nTest 4: Testing database queries...")
        try:
            total_tenants = Tenant.query.count()
            active_tenants = Tenant.query.filter_by(status="active").count()
            print(f"  [PASS] Total tenants: {total_tenants}")
            print(f"  [PASS] Active tenants: {active_tenants}")
        except Exception as e:
            print(f"  [FAIL] Error querying tenants: {e}")
        
        print("\n" + "=" * 60)
        print("EXISTING FUNCTIONALITY TEST COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    test_existing_reports_functionality()
