"""SQLAlchemy models for the Dormitory Management System."""
from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Admin(db.Model, UserMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<Admin {self.username}>"


class Tenant(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), unique=True, nullable=False, index=True)
    full_name = db.Column(db.String(255), nullable=False)
    room_number = db.Column(db.String(32), nullable=False)
    contact_number = db.Column(db.String(32))
    move_in_date = db.Column(db.Date, nullable=False, default=date.today)
    monthly_rent = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    due_day = db.Column(db.Integer, nullable=False, default=1)  # day of month (1-31)
    pending_balance = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    status = db.Column(db.String(16), nullable=False, default="active")  # active / inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    payments = db.relationship(
        "Payment",
        backref="tenant",
        cascade="all, delete-orphan",
        lazy="dynamic",
        order_by="Payment.payment_date.desc()",
    )

    @property
    def is_overdue(self) -> bool:
        """A tenant is overdue if they are active, have a pending balance,
        and today's date is past the due day of the current month."""
        if self.status != "active":
            return False
        if float(self.pending_balance or 0) <= 0:
            return False
        today = date.today()
        return today.day > (self.due_day or 1)

    @property
    def payment_status(self) -> str:
        if self.status != "active":
            return "inactive"
        if float(self.pending_balance or 0) <= 0:
            return "paid"
        if self.is_overdue:
            return "overdue"
        return "unpaid"

    def __repr__(self) -> str:
        return f"<Tenant {self.nickname} room={self.room_number}>"


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(
        db.Integer,
        db.ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=date.today)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Payment tenant={self.tenant_id} amount={self.amount}>"
