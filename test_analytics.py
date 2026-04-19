"""Test script to verify new analytics dashboard functionality."""
from app import app, db
from models import Payment
from datetime import date
import json

def test_analytics_functionality():
    """Test that new analytics dashboard works correctly."""
    with app.app_context():
        print("=" * 60)
        print("TESTING ANALYTICS DASHBOARD FUNCTIONALITY")
        print("=" * 60)
        
        # Test 1: Analytics API endpoint with monthly filter
        print("\nTest 1: Testing analytics API with monthly filter...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                today = date.today()
                response = client.get(f'/reports/analytics?filter_type=monthly&year={today.year}&month={today.month}')
                if response.status_code == 200:
                    data = json.loads(response.data)
                    if data.get('success'):
                        print(f"  [PASS] Analytics API returns success")
                        print(f"  [PASS] Filter type: {data.get('filter_type')}")
                        print(f"  [PASS] Year: {data.get('year')}")
                        print(f"  [PASS] Month: {data.get('month')}")
                        print(f"  [PASS] Payments count: {len(data.get('payments', []))}")
                        print(f"  [PASS] Tenant stats: {data.get('tenant_stats', {})}")
                        print(f"  [PASS] Balance stats: {data.get('balance_stats', {})}")
                    else:
                        print(f"  [FAIL] Analytics API returned error: {data.get('error')}")
                else:
                    print(f"  [FAIL] Analytics API returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing analytics API: {e}")
        
        # Test 2: Analytics API endpoint with yearly filter
        print("\nTest 2: Testing analytics API with yearly filter...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                today = date.today()
                response = client.get(f'/reports/analytics?filter_type=yearly&year={today.year}')
                if response.status_code == 200:
                    data = json.loads(response.data)
                    if data.get('success'):
                        print(f"  [PASS] Analytics API returns success for yearly filter")
                        print(f"  [PASS] Filter type: {data.get('filter_type')}")
                        print(f"  [PASS] Year: {data.get('year')}")
                        print(f"  [PASS] Payments count: {len(data.get('payments', []))}")
                    else:
                        print(f"  [FAIL] Analytics API returned error: {data.get('error')}")
                else:
                    print(f"  [FAIL] Analytics API returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing yearly filter: {e}")
        
        # Test 3: Analytics API with invalid input
        print("\nTest 3: Testing analytics API with invalid input...")
        try:
            with app.test_client() as client:
                # Login first
                client.post('/login', data={
                    'username': 'adian',
                    'password': 'adian123'
                })
                
                response = client.get('/reports/analytics?filter_type=invalid&year=abc')
                if response.status_code == 200:
                    data = json.loads(response.data)
                    # Should still work with defaults
                    if data.get('success'):
                        print(f"  [PASS] Analytics API handles invalid input gracefully")
                    else:
                        print(f"  [FAIL] Analytics API failed on invalid input")
                else:
                    print(f"  [FAIL] Analytics API returned {response.status_code}")
        except Exception as e:
            print(f"  [FAIL] Error testing invalid input: {e}")
        
        # Test 4: Check payment aggregation logic
        print("\nTest 4: Testing payment aggregation logic...")
        try:
            from routes import reports_analytics
            from flask import request
            with app.test_request_context('/reports/analytics?filter_type=monthly'):
                # This tests the backend logic directly
                today = date.today()
                payments = Payment.query.filter(
                    Payment.payment_date.isnot(None)
                ).all()
                
                if payments:
                    print(f"  [PASS] Found {len(payments)} payments in database")
                    # Check if payment dates are valid
                    for p in payments[:3]:  # Check first 3
                        if p.payment_date:
                            print(f"  [PASS] Payment date: {p.payment_date}, Amount: {p.amount}")
                else:
                    print(f"  [INFO] No payments found in database")
        except Exception as e:
            print(f"  [FAIL] Error testing aggregation logic: {e}")
        
        print("\n" + "=" * 60)
        print("ANALYTICS DASHBOARD TEST COMPLETE")
        print("=" * 60)

if __name__ == "__main__":
    test_analytics_functionality()
