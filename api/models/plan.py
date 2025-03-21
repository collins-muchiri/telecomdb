from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Plan:
    """Plan model representing a telecom service plan"""
    plan_id: str
    name: str
    base_price: float
    data_limit: float  # in GB
    voice_minutes: int
    sms_limit: int
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    description: Optional[str] = None
    features: Optional[list] = None
    is_active: bool = True

    def __post_init__(self):
        """Validate plan data after initialization"""
        if not self.plan_id:
            raise ValueError("Plan ID is required")
        if not self.name:
            raise ValueError("Plan name is required")
        if self.base_price < 0:
            raise ValueError("Base price cannot be negative")
        if self.data_limit < 0:
            raise ValueError("Data limit cannot be negative")
        if self.voice_minutes < 0:
            raise ValueError("Voice minutes cannot be negative")
        if self.sms_limit < 0:
            raise ValueError("SMS limit cannot be negative")

    def calculate_overage(self, data_used: float, voice_used: int, sms_used: int) -> dict:
        """Calculate usage overage charges"""
        data_overage = max(0, data_used - self.data_limit)
        voice_overage = max(0, voice_used - self.voice_minutes)
        sms_overage = max(0, sms_used - self.sms_limit)

        # Example overage rates (these should be configurable)
        data_rate = 10.0  # $10 per GB
        voice_rate = 0.10  # $0.10 per minute
        sms_rate = 0.05  # $0.05 per SMS

        return {
            "data_overage": data_overage,
            "voice_overage": voice_overage,
            "sms_overage": sms_overage,
            "data_charge": data_overage * data_rate,
            "voice_charge": voice_overage * voice_rate,
            "sms_charge": sms_overage * sms_rate
        }

    def update(self, **kwargs):
        """Update plan information"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def deactivate(self):
        """Deactivate the plan"""
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self):
        """Activate the plan"""
        self.is_active = True
        self.updated_at = datetime.now() 