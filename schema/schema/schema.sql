-- Create customers table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create services table
CREATE TABLE services (
    service_id SERIAL PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    is_active BOOLEAN DEFAULT true
);

-- Create bills table
CREATE TABLE bills (
    bill_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    bill_date DATE NOT NULL,
    due_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_status VARCHAR(20) CHECK (payment_status IN ('Pending', 'Paid', 'Overdue', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create bill_details table
CREATE TABLE bill_details (
    bill_id INTEGER REFERENCES bills(bill_id),
    service_id INTEGER REFERENCES services(service_id),
    usage_amount DECIMAL(10,2) NOT NULL,
    cost DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (bill_id, service_id)
);

-- Create payments table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    bill_id INTEGER REFERENCES bills(bill_id),
    amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(50),
    transaction_id VARCHAR(100)
);

-- Create indexes for better performance
CREATE INDEX idx_bills_customer_id ON bills(customer_id);
CREATE INDEX idx_bills_payment_status ON bills(payment_status);
CREATE INDEX idx_bill_details_bill_id ON bill_details(bill_id);
CREATE INDEX idx_payments_bill_id ON payments(bill_id);

-- Insert sample data
INSERT INTO customers (name, phone, email, address) VALUES
('John Doe', '+1234567890', 'john@example.com', '123 Main St'),
('Jane Smith', '+0987654321', 'jane@example.com', '456 Oak Ave');

INSERT INTO services (service_name, description, price) VALUES
('Basic Plan', 'Basic internet and phone service', 29.99),
('Premium Plan', 'High-speed internet and unlimited calls', 49.99),
('Business Plan', 'Enterprise-grade internet and phone service', 99.99); 