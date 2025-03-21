import psycopg2
from psycopg2 import Error
import csv
import os
from cryptography.fernet import Fernet
import datetime
import logging
from config import DB_CONFIG, ENCRYPTION_KEY, EXPORT_DIR, EXPORT_FILENAME, DEFAULT_DUE_DATE_DAYS, DEFAULT_PAYMENT_STATUS, LOG_LEVEL, LOG_FILE

# Set up logging
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)
logger = logging.getLogger(__name__)

def setup_encryption():
    """Set up encryption with proper key handling."""
    try:
        if not ENCRYPTION_KEY:
            # Generate a new key if none exists
            key = Fernet.generate_key()
            logger.warning("No encryption key found. Generated new key. Please save this key in your .env file:")
            logger.warning(f"ENCRYPTION_KEY={key.decode()}")
            return Fernet(key)
        
        # Try to use the provided key
        try:
            if isinstance(ENCRYPTION_KEY, str):
                return Fernet(ENCRYPTION_KEY.encode())
            return Fernet(ENCRYPTION_KEY)
        except ValueError as e:
            logger.error(f"Invalid encryption key format: {e}")
            raise ValueError("Invalid encryption key format. Please generate a new key using: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'")
    except Exception as e:
        logger.error(f"Error setting up encryption: {e}")
        raise

# Initialize encryption
cipher = setup_encryption()

def connect_db():
    """Connect to PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("Successfully connected to database")
        return conn
    except Error as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def analyze_bills(conn):
    """Analyze existing bills and print summary."""
    try:
        with conn.cursor() as cur:
            # Total revenue from paid bills
            cur.execute("SELECT SUM(total_amount) FROM bills WHERE payment_status = 'Paid';")
            total_revenue = cur.fetchone()[0] or 0
            logger.info(f"Total Revenue from Paid Bills: ${total_revenue:.2f}")
            
            # Overdue bills (due_date < today and status = 'Overdue')
            cur.execute("""
                SELECT COUNT(*) FROM bills 
                WHERE payment_status = 'Overdue' AND due_date < %s;
            """, (datetime.date.today(),))
            overdue_count = cur.fetchone()[0]
            logger.info(f"Overdue Bills: {overdue_count}")
    except Error as e:
        logger.error(f"Error analyzing bills: {e}")
        raise

def generate_new_bill(conn, customer_id, service_id, usage_amount):
    """Generate a new bill based on usage."""
    try:
        with conn.cursor() as cur:
            # Get service price
            cur.execute("SELECT price FROM services WHERE service_id = %s;", (service_id,))
            price = cur.fetchone()
            if not price:
                raise ValueError(f"Service ID {service_id} not found.")
            price = price[0]
            
            # Calculate cost
            cost = usage_amount * price
            
            # Generate new bill_id
            cur.execute("SELECT COALESCE(MAX(bill_id), 0) + 1 FROM bills;")
            bill_id = cur.fetchone()[0]
            
            # Insert into bills first
            cur.execute("""
                INSERT INTO bills (bill_id, customer_id, bill_date, due_date, total_amount, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (bill_id, customer_id, datetime.date.today(), 
                  datetime.date.today() + datetime.timedelta(days=DEFAULT_DUE_DATE_DAYS), 
                  cost, DEFAULT_PAYMENT_STATUS))
            
            # Now insert into bill_details with the same bill_id
            cur.execute("""
                INSERT INTO bill_details (bill_id, service_id, usage_amount, cost)
                VALUES (%s, %s, %s, %s);
            """, (bill_id, service_id, usage_amount, cost))
            
            conn.commit()
            logger.info(f"Generated Bill ID {bill_id} for Customer ID {customer_id}")
            return bill_id
    except Error as e:
        conn.rollback()
        logger.error(f"Error generating bill: {e}")
        raise

def export_bills(conn, output_file=None):
    """Export all bills with encrypted customer data."""
    try:
        output_file = output_file or os.path.join(EXPORT_DIR, EXPORT_FILENAME)
        
        with conn.cursor() as cur:
            cur.execute("""
                SELECT c.customer_id, c.name, c.phone, b.bill_id, b.total_amount, b.payment_status
                FROM customers c JOIN bills b ON c.customer_id = b.customer_id;
            """)
            rows = cur.fetchall()
        
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Customer ID', 'Encrypted Name', 'Encrypted Phone', 'Bill ID', 'Total Amount', 'Status'])
            for row in rows:
                encrypted_name = cipher.encrypt(row[1].encode()).decode()
                encrypted_phone = cipher.encrypt(row[2].encode()).decode()
                writer.writerow([row[0], encrypted_name, encrypted_phone, row[3], row[4], row[5]])
        
        logger.info(f"Bills exported to {output_file}")
        return output_file
    except Error as e:
        logger.error(f"Error exporting bills: {e}")
        raise

def main():
    """Main function to demonstrate usage."""
    try:
        conn = connect_db()
        if conn:
            # Analyze existing bills
            analyze_bills(conn)
            
            # Generate a new bill (Customer 1, Service 1, 50 units)
            generate_new_bill(conn, 1, 1, 50)
            
            # Export all bills
            export_bills(conn)
            conn.close()
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()