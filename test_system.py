from app import app
from models import db, Tenant, Payment
from datetime import date

with app.app_context():
    print("=" * 60)
    print("SYSTEM TEST REPORT")
    print("=" * 60)
    
    # Test 1: Check database connection and tenant data
    print("\n1. DATABASE CONNECTION & TENANT DATA")
    print("-" * 60)
    total_tenants = Tenant.query.count()
    active_tenants = Tenant.query.filter_by(status="active").count()
    print(f"Total tenants: {total_tenants}")
    print(f"Active tenants: {active_tenants}")
    
    # Test 2: Outstanding balance calculation
    print("\n2. OUTSTANDING BALANCE CALCULATION")
    print("-" * 60)
    tenants_with_balance = Tenant.query.filter(
        Tenant.status == "active",
        Tenant.pending_balance > 0
    ).all()
    
    total_balance = sum(float(t.pending_balance) for t in tenants_with_balance)
    print(f"Active tenants with positive balance: {len(tenants_with_balance)}")
    print(f"Total outstanding balance: {total_balance}")
    
    for t in tenants_with_balance:
        print(f"  - {t.nickname}: {t.pending_balance}")
    
    # Test 3: Payment data
    print("\n3. PAYMENT DATA")
    print("-" * 60)
    total_payments = Payment.query.count()
    all_time_income = sum(float(p.amount) for p in Payment.query.all())
    
    today = date.today()
    monthly_payments = Payment.query.filter(
        Payment.payment_date >= date(today.year, today.month, 1)
    ).all()
    monthly_income = sum(float(p.amount) for p in monthly_payments)
    
    print(f"Total payments recorded: {total_payments}")
    print(f"All-time income: {all_time_income}")
    print(f"This month's income: {monthly_income}")
    
    # Test 4: Backend API calculation verification
    print("\n4. BACKEND CALCULATION VERIFICATION")
    print("-" * 60)
    from sqlalchemy import func
    
    # Verify outstanding balance calculation matches routes.py
    backend_balance = db.session.query(func.coalesce(func.sum(Tenant.pending_balance), 0)) \
        .filter(Tenant.status == "active", Tenant.pending_balance > 0) \
        .scalar() or 0
    
    print(f"Backend calculated balance: {float(backend_balance)}")
    print(f"Manual calculation match: {total_balance == float(backend_balance)}")
    
    # Verify total income calculation
    backend_income = db.session.query(func.coalesce(func.sum(Payment.amount), 0)).scalar() or 0
    print(f"Backend calculated total income: {float(backend_income)}")
    print(f"Manual calculation match: {all_time_income == float(backend_income)}")
    
    print("\n" + "=" * 60)
    print("SYSTEM TEST COMPLETE")
    print("=" * 60)
