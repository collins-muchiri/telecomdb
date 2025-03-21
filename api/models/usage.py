from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Usage:
    """Usage model representing customer's service usage"""
    usage_id: str
    customer_id: str
    bill_id: str
    data_used: float  # in GB
    voice_minutes_used: int
    sms_used: int
    usage_date: datetime
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate usage data after initialization"""
        if not self.usage_id:
            raise ValueError("Usage ID is required")
        if not self.customer_id:
            raise ValueError("Customer ID is required")
        if not self.bill_id:
            raise ValueError("Bill ID is required")
        if self.data_used < 0:
            raise ValueError("Data usage cannot be negative")
        if self.voice_minutes_used < 0:
            raise ValueError("Voice minutes used cannot be negative")
        if self.sms_used < 0:
            raise ValueError("SMS usage cannot be negative")
        if not self.usage_date:
            raise ValueError("Usage date is required")

    def update(self, **kwargs):
        """Update usage information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def get_total_usage(self) -> dict:
        """Get total usage statistics"""
        return {
            "data_used": self.data_used,
            "voice_minutes_used": self.voice_minutes_used,
            "sms_used": self.sms_used
        }

    def is_within_limits(self, plan) -> bool:
        """Check if usage is within plan limits"""
        return (
            self.data_used <= plan.data_limit and
            self.voice_minutes_used <= plan.voice_minutes and
            self.sms_used <= plan.sms_limit
        ) 