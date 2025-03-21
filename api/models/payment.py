from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Payment:
    """Payment model representing a payment made on a bill"""
    payment_id: str
    bill_id: str
    amount: Decimal
    payment_date: datetime
    payment_method: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "completed"
    transaction_id: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate payment data after initialization"""
        if not self.payment_id:
            raise ValueError("Payment ID is required")
        if not self.bill_id:
            raise ValueError("Bill ID is required")
        if self.amount <= 0:
            raise ValueError("Payment amount must be positive")
        if not self.payment_date:
            raise ValueError("Payment date is required")
        if not self.payment_method:
            raise ValueError("Payment method is required")

    def mark_as_failed(self):
        """Mark the payment as failed"""
        self.status = "failed"
        self.updated_at = datetime.now()

    def mark_as_pending(self):
        """Mark the payment as pending"""
        self.status = "pending"
        self.updated_at = datetime.now()

    def mark_as_completed(self):
        """Mark the payment as completed"""
        self.status = "completed"
        self.updated_at = datetime.now()

    def update(self, **kwargs):
        """Update payment information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def is_successful(self) -> bool:
        """Check if the payment was successful"""
        return self.status == "completed" 