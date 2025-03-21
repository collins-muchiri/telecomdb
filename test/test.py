import unittest
import os
import sys
from datetime import datetime

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.models.customer import Customer
from api.models.bill import Bill
from api.models.payment import Payment
from api.models.usage import Usage
from api.models.plan import Plan

class TestTelecomBillingSystem(unittest.TestCase):
    """Test cases for the Telecom Billing System"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Initialize test data
        self.test_customer = Customer(
            customer_id="TEST001",
            name="Test User",
            email="test@example.com",
            phone="1234567890",
            address="123 Test St"
        )
        
        self.test_plan = Plan(
            plan_id="BASIC",
            name="Basic Plan",
            base_price=29.99,
            data_limit=5,  # GB
            voice_minutes=500,
            sms_limit=1000
        )

    def test_customer_creation(self):
        """Test customer object creation and validation"""
        self.assertEqual(self.test_customer.customer_id, "TEST001")
        self.assertEqual(self.test_customer.name, "Test User")
        self.assertEqual(self.test_customer.email, "test@example.com")
        self.assertEqual(self.test_customer.phone, "1234567890")
        self.assertEqual(self.test_customer.address, "123 Test St")

    def test_bill_creation(self):
        """Test bill object creation and calculation"""
        bill = Bill(
            bill_id="BILL001",
            customer_id=self.test_customer.customer_id,
            plan_id=self.test_plan.plan_id,
            billing_date=datetime.now(),
            due_date=datetime.now().replace(day=1),
            base_amount=self.test_plan.base_price
        )
        
        self.assertEqual(bill.bill_id, "BILL001")
        self.assertEqual(bill.customer_id, self.test_customer.customer_id)
        self.assertEqual(bill.plan_id, self.test_plan.plan_id)
        self.assertEqual(bill.base_amount, self.test_plan.base_price)

    def test_payment_processing(self):
        """Test payment processing and bill status update"""
        bill = Bill(
            bill_id="BILL001",
            customer_id=self.test_customer.customer_id,
            plan_id=self.test_plan.plan_id,
            billing_date=datetime.now(),
            due_date=datetime.now().replace(day=1),
            base_amount=self.test_plan.base_price
        )
        
        payment = Payment(
            payment_id="PAY001",
            bill_id=bill.bill_id,
            amount=self.test_plan.base_price,
            payment_date=datetime.now(),
            payment_method="CREDIT_CARD"
        )
        
        self.assertEqual(payment.payment_id, "PAY001")
        self.assertEqual(payment.bill_id, bill.bill_id)
        self.assertEqual(payment.amount, self.test_plan.base_price)
        self.assertEqual(payment.payment_method, "CREDIT_CARD")

    def test_usage_tracking(self):
        """Test usage tracking and overage calculation"""
        usage = Usage(
            usage_id="USE001",
            customer_id=self.test_customer.customer_id,
            bill_id="BILL001",
            data_used=6.5,  # GB
            voice_minutes_used=600,
            sms_used=1200,
            usage_date=datetime.now()
        )
        
        # Calculate overages
        data_overage = max(0, usage.data_used - self.test_plan.data_limit)
        voice_overage = max(0, usage.voice_minutes_used - self.test_plan.voice_minutes)
        sms_overage = max(0, usage.sms_used - self.test_plan.sms_limit)
        
        self.assertEqual(data_overage, 1.5)  # 6.5 - 5 GB
        self.assertEqual(voice_overage, 100)  # 600 - 500 minutes
        self.assertEqual(sms_overage, 200)  # 1200 - 1000 SMS

    def test_plan_features(self):
        """Test plan features and limits"""
        self.assertEqual(self.test_plan.plan_id, "BASIC")
        self.assertEqual(self.test_plan.name, "Basic Plan")
        self.assertEqual(self.test_plan.base_price, 29.99)
        self.assertEqual(self.test_plan.data_limit, 5)
        self.assertEqual(self.test_plan.voice_minutes, 500)
        self.assertEqual(self.test_plan.sms_limit, 1000)

if __name__ == '__main__':
    unittest.main() 