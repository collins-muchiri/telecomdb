# Database Guide

## Overview

This guide provides comprehensive information about database management, migrations, and best practices for the Telecom Billing API. We use SQLAlchemy for ORM and Alembic for migrations.

## Database Structure

### 1. Models

```python
# database/models.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    address = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bills = relationship("Bill", back_populates="customer")

class Bill(Base):
    __tablename__ = "bills"
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum("pending", "paid", "overdue"), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="bills")
    payments = relationship("Payment", back_populates="bill")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50))
    transaction_id = Column(String(100))
    
    # Relationships
    bill = relationship("Bill", back_populates="payments")
```

### 2. Database Configuration

```python
# database/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

def get_database_url():
    """Get database URL from environment variables."""
    return (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

def create_db_engine():
    """Create database engine with connection pooling."""
    return create_engine(
        get_database_url(),
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )

def get_db_session():
    """Create database session."""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()
```

## Migrations

### 1. Alembic Configuration

```ini
# alembic.ini

[alembic]
script_location = migrations
sqlalchemy.url = driver://user:pass@localhost/dbname

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### 2. Migration Scripts

```python
# migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from database.models import Base
from database.config import get_database_url

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 3. Creating Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show migration history
alembic history

# Show current migration
alembic current
```

## Database Operations

### 1. CRUD Operations

```python
# database/operations.py

class DatabaseOperations:
    def __init__(self, session):
        self.session = session
    
    def create_customer(self, name: str, email: str, phone: str = None, address: str = None) -> Customer:
        """Create a new customer."""
        customer = Customer(
            name=name,
            email=email,
            phone=phone,
            address=address
        )
        self.session.add(customer)
        self.session.commit()
        return customer
    
    def get_customer(self, customer_id: int) -> Customer:
        """Get customer by ID."""
        return self.session.query(Customer).get(customer_id)
    
    def update_customer(self, customer_id: int, **kwargs) -> Customer:
        """Update customer details."""
        customer = self.get_customer(customer_id)
        if customer:
            for key, value in kwargs.items():
                setattr(customer, key, value)
            self.session.commit()
        return customer
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete customer."""
        customer = self.get_customer(customer_id)
        if customer:
            self.session.delete(customer)
            self.session.commit()
            return True
        return False
```

### 2. Query Operations

```python
# database/queries.py

class DatabaseQueries:
    def __init__(self, session):
        self.session = session
    
    def get_customer_bills(self, customer_id: int) -> List[Bill]:
        """Get all bills for a customer."""
        return (
            self.session.query(Bill)
            .filter(Bill.customer_id == customer_id)
            .order_by(Bill.created_at.desc())
            .all()
        )
    
    def get_overdue_bills(self) -> List[Bill]:
        """Get all overdue bills."""
        return (
            self.session.query(Bill)
            .filter(
                Bill.status == "pending",
                Bill.due_date < datetime.utcnow()
            )
            .all()
        )
    
    def get_customer_payments(self, customer_id: int) -> List[Payment]:
        """Get all payments for a customer's bills."""
        return (
            self.session.query(Payment)
            .join(Bill)
            .filter(Bill.customer_id == customer_id)
            .order_by(Payment.payment_date.desc())
            .all()
        )
```

## Database Maintenance

### 1. Backup and Restore

```python
# scripts/backup_db.py

def backup_database():
    """Create database backup."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.sql"
    
    # Create backup
    os.makedirs("backups", exist_ok=True)
    subprocess.run([
        "pg_dump",
        "-U", os.getenv("DB_USER"),
        "-h", os.getenv("DB_HOST"),
        "-p", os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
        "-f", backup_file
    ])
    
    # Compress backup
    with zipfile.ZipFile(f"{backup_file}.zip", "w") as zipf:
        zipf.write(backup_file, os.path.basename(backup_file))
    
    # Remove uncompressed file
    os.remove(backup_file)
    
    # Rotate old backups
    rotate_backups()

def restore_database(backup_file: str):
    """Restore database from backup."""
    # Extract backup
    with zipfile.ZipFile(backup_file, "r") as zipf:
        zipf.extractall("backups")
    
    # Restore database
    subprocess.run([
        "psql",
        "-U", os.getenv("DB_USER"),
        "-h", os.getenv("DB_HOST"),
        "-p", os.getenv("DB_PORT"),
        os.getenv("DB_NAME"),
        "-f", backup_file.replace(".zip", "")
    ])
```

### 2. Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_bills_customer_id ON bills(customer_id);
CREATE INDEX idx_bills_status ON bills(status);
CREATE INDEX idx_payments_bill_id ON payments(bill_id);

-- Analyze tables
ANALYZE customers;
ANALYZE bills;
ANALYZE payments;

-- Vacuum tables
VACUUM ANALYZE customers;
VACUUM ANALYZE bills;
VACUUM ANALYZE payments;
```

## Best Practices

### 1. Database Design

1. **Normalization**
   - Use appropriate normal forms
   - Avoid redundant data
   - Maintain referential integrity

2. **Indexing**
   - Index frequently queried columns
   - Index foreign keys
   - Monitor index usage

3. **Constraints**
   - Use primary keys
   - Add foreign key constraints
   - Add unique constraints
   - Add check constraints

### 2. Query Optimization

1. **Query Structure**
   - Use appropriate joins
   - Limit result sets
   - Use indexes effectively
   - Avoid SELECT *

2. **Performance**
   - Monitor query execution plans
   - Use connection pooling
   - Implement caching
   - Optimize slow queries

### 3. Data Management

1. **Data Integrity**
   - Validate input data
   - Use transactions
   - Implement error handling
   - Regular backups

2. **Data Security**
   - Encrypt sensitive data
   - Implement access controls
   - Audit data access
   - Secure connections

## Troubleshooting

### 1. Common Issues

1. **Connection Issues**
   - Check credentials
   - Verify network connectivity
   - Check firewall settings
   - Monitor connection pool

2. **Performance Issues**
   - Check query execution plans
   - Monitor resource usage
   - Review indexes
   - Check for locks

3. **Data Issues**
   - Verify data integrity
   - Check constraints
   - Review transactions
   - Monitor deadlocks

### 2. Monitoring

1. **Database Metrics**
   - Connection count
   - Query performance
   - Resource usage
   - Error rates

2. **Logging**
   - Error logs
   - Slow query logs
   - Access logs
   - Audit logs

## Resources

### 1. Internal Resources

- Database documentation
- Migration scripts
- Backup procedures
- Monitoring tools

### 2. External Resources

- SQLAlchemy documentation
- Alembic documentation
- PostgreSQL documentation
- Database best practices 