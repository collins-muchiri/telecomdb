from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

@dataclass
class Bill:
    """Bill model representing a customer's billing statement"""
    bill_id: str
    customer_id: str
    plan_id: str
    billing_date: datetime
    due_date: datetime
    base_amount: Decimal
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "pending"
    data_overage: float = 0.0
    voice_overage: int = 0
    sms_overage: int = 0
    data_charge: Decimal = Decimal('0.00')
    voice_charge: Decimal = Decimal('0.00')
    sms_charge: Decimal = Decimal('0.00')
    total_amount: Decimal = Decimal('0.00')
    paid_amount: Decimal = Decimal('0.00')
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate bill data after initialization"""
        if not self.bill_id:
            raise ValueError("Bill ID is required")
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.plan_id:
            raise ValueError("Plan ID is required")
        if not self.billing_date:
            raise ValueError("Billing date is required")
        if not self.due_date:
            raise ValueError("Due date is required")
        if self.base_amount < 0:
            raise ValueError("Base amount cannot be negative")

    def calculate_total(self):
        """Calculate total bill amount including overages"""
        self.total_amount = (
            self.base_amount +
            self.data_charge +
            self.voice_charge +
            self.sms_charge
        )

    def apply_payment(self, amount: Decimal):
        """Apply a payment to the bill"""
        if amount <= 0:
            raise ValueError("Payment amount must be positive")
        
        self.paid_amount += amount
        self.updated_at = datetime.now()

        # Update bill status based on payment
        if self.paid_amount >= self.total_amount:
            self.status = "paid"
        elif self.paid_amount > 0:
            self.status = "partial"

    def is_overdue(self) -> bool:
        """Check if the bill is overdue"""
        return datetime.now() > self.due_date and self.status != "paid"

    def get_balance(self) -> Decimal:
        """Get remaining balance on the bill"""
        return self.total_amount - self.paid_amount

    def update(self, **kwargs):
        """Update bill information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        self.calculate_total() 