from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Customer:
    """Customer model representing a telecom customer"""
    customer_id: str
    name: str
    email: str
    phone: str
    address: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    status: str = "active"
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate customer data after initialization"""
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.name:
            raise ValueError("Name is required")
        if not self.email:
            raise ValueError("Email is required")
        if not self.phone:
            raise ValueError("Phone number is required")
        if not self.address:
            raise ValueError("Address is required")

    def update(self, **kwargs):
        """Update customer information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def deactivate(self):
        """Deactivate the customer account"""
        self.status = "inactive"
        self.updated_at = datetime.now()

    def activate(self):
        """Activate the customer account"""
        self.status = "active"
        self.updated_at = datetime.now() 