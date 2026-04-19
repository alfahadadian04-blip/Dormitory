from app import app, db
from models import Tenant, Payment
from datetime import date, timedelta

def create_test_payments():
    with app.app_context():
        # Create some test payments for the current month
        tenants = Tenant.query.filter_by(status="active").all()
        
        for i, tenant in enumerate(tenants[:4]):  # Create payments for first 4 tenants
            # Check if payment already exists
            existing = Payment.query.filter_by(tenant_id=tenant.id).first()
            if existing:
                print(f"Payment already exists for {tenant.nickname}, skipping...")
                continue
            
            payment = Payment(
                tenant_id=tenant.id,
                amount=float(tenant.monthly_rent) * 0.5,  # Partial payment
                payment_date=date.today() - timedelta(days=i),
                notes=f"Test payment {i+1}"
            )
            db.session.add(payment)
            print(f"Created payment for {tenant.nickname}: {payment.amount}")
        
        db.session.commit()
        print("\nTest payments created successfully!")

if __name__ == "__main__":
    print("Creating test payments...")
    create_test_payments()
