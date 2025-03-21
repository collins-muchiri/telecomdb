# Testing Guide

## Overview

This guide provides comprehensive information about testing the Telecom Billing API. We use pytest as our testing framework and follow best practices for writing and maintaining tests.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Test configuration and fixtures
├── test_api/            # API endpoint tests
│   ├── __init__.py
│   ├── test_customers.py
│   ├── test_bills.py
│   └── test_payments.py
├── test_models/         # Database model tests
│   ├── __init__.py
│   ├── test_customer.py
│   └── test_bill.py
├── test_security/       # Security feature tests
│   ├── __init__.py
│   ├── test_auth.py
│   └── test_audit.py
└── test_utils/          # Utility function tests
    ├── __init__.py
    └── test_helpers.py
```

## Test Configuration

### 1. conftest.py

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

@pytest.fixture(scope="session")
def test_db():
    """Create test database and run migrations."""
    # Create test database
    engine = create_engine("postgresql://test_user:test_pass@localhost/test_db")
    
    # Run migrations
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    yield engine
    
    # Cleanup
    command.downgrade(alembic_cfg, "base")
    engine.dispose()

@pytest.fixture
def db_session(test_db):
    """Create database session for each test."""
    Session = sessionmaker(bind=test_db)
    session = Session()
    
    yield session
    
    session.rollback()
    session.close()

@pytest.fixture
def test_client():
    """Create test client for API endpoints."""
    from api.app import app
    app.config["TESTING"] = True
    return app.test_client()

@pytest.fixture
def test_api_key():
    """Generate test API key."""
    from security.auth import APIKeyManager
    return APIKeyManager.generate_key("test_client", ["read:customers"])
```

## Writing Tests

### 1. API Tests

```python
# tests/test_api/test_customers.py

def test_get_customer(test_client, test_api_key, db_session):
    """Test getting customer details."""
    # Create test customer
    customer = Customer(name="Test User", email="test@example.com")
    db_session.add(customer)
    db_session.commit()
    
    # Make request
    response = test_client.get(
        f"/api/customers/{customer.id}",
        headers={"X-API-Key": test_api_key}
    )
    
    # Assert response
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"

def test_create_customer(test_client, test_api_key):
    """Test creating new customer."""
    # Test data
    customer_data = {
        "name": "New User",
        "email": "new@example.com",
        "phone": "1234567890"
    }
    
    # Make request
    response = test_client.post(
        "/api/customers",
        headers={"X-API-Key": test_api_key},
        json=customer_data
    )
    
    # Assert response
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New User"
    assert data["email"] == "new@example.com"
```

### 2. Model Tests

```python
# tests/test_models/test_customer.py

def test_customer_creation(db_session):
    """Test customer model creation."""
    customer = Customer(
        name="Test User",
        email="test@example.com",
        phone="1234567890"
    )
    
    db_session.add(customer)
    db_session.commit()
    
    # Query and verify
    saved_customer = db_session.query(Customer).first()
    assert saved_customer.name == "Test User"
    assert saved_customer.email == "test@example.com"
    assert saved_customer.phone == "1234567890"

def test_customer_validation(db_session):
    """Test customer model validation."""
    with pytest.raises(ValueError):
        Customer(
            name="",  # Empty name
            email="invalid-email",  # Invalid email
            phone="123"  # Invalid phone
        )
```

### 3. Security Tests

```python
# tests/test_security/test_auth.py

def test_api_key_validation(test_api_key):
    """Test API key validation."""
    from security.auth import APIKeyManager
    
    # Valid key
    assert APIKeyManager.validate_key(test_api_key)
    
    # Invalid key
    assert not APIKeyManager.validate_key("invalid-key")

def test_rate_limiting(test_client, test_api_key):
    """Test rate limiting."""
    from security.auth import rate_limiter
    
    # Make multiple requests
    for _ in range(100):
        response = test_client.get(
            "/api/customers",
            headers={"X-API-Key": test_api_key}
        )
        assert response.status_code == 200
    
    # Next request should be rate limited
    response = test_client.get(
        "/api/customers",
        headers={"X-API-Key": test_api_key}
    )
    assert response.status_code == 429
```

### 4. Integration Tests

```python
# tests/test_integration/test_billing.py

def test_bill_creation_and_payment(test_client, test_api_key, db_session):
    """Test complete billing workflow."""
    # Create customer
    customer = Customer(name="Test User", email="test@example.com")
    db_session.add(customer)
    db_session.commit()
    
    # Create bill
    bill_data = {
        "customer_id": customer.id,
        "amount": 100.00,
        "due_date": "2024-12-31"
    }
    
    response = test_client.post(
        "/api/bills",
        headers={"X-API-Key": test_api_key},
        json=bill_data
    )
    assert response.status_code == 201
    bill_id = response.get_json()["id"]
    
    # Record payment
    payment_data = {
        "bill_id": bill_id,
        "amount": 100.00,
        "payment_method": "credit_card",
        "transaction_id": "test-123"
    }
    
    response = test_client.post(
        "/api/payments",
        headers={"X-API-Key": test_api_key},
        json=payment_data
    )
    assert response.status_code == 201
    
    # Verify bill status
    response = test_client.get(
        f"/api/bills/{bill_id}",
        headers={"X-API-Key": test_api_key}
    )
    assert response.get_json()["status"] == "paid"
```

## Running Tests

### 1. Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api/test_customers.py

# Run specific test function
pytest tests/test_api/test_customers.py::test_get_customer

# Run tests with coverage
pytest --cov=telecomdb1 tests/
```

### 2. Test Options

```bash
# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Run tests and show print statements
pytest -s

# Run tests matching pattern
pytest -k "customer"
```

### 3. Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=telecomdb1 --cov-report=html tests/

# Generate XML coverage report
pytest --cov=telecomdb1 --cov-report=xml tests/
```

## Best Practices

### 1. Test Organization

1. **Test File Structure**
   - One test file per module
   - Group related tests in classes
   - Use descriptive test names

2. **Test Data Management**
   - Use fixtures for common setup
   - Create helper functions for data generation
   - Clean up test data after tests

3. **Test Isolation**
   - Each test should be independent
   - Use transactions for database tests
   - Mock external dependencies

### 2. Writing Good Tests

1. **Test Naming**
   - Use descriptive names
   - Follow pattern: test_<what>_<scenario>
   - Include expected outcome

2. **Test Structure**
   - Arrange: Set up test data
   - Act: Perform the action
   - Assert: Verify results

3. **Test Coverage**
   - Test happy path
   - Test error cases
   - Test edge cases

### 3. Performance

1. **Test Speed**
   - Use appropriate fixtures
   - Mock slow operations
   - Run tests in parallel

2. **Resource Management**
   - Clean up resources
   - Use context managers
   - Monitor memory usage

## Continuous Integration

### 1. GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:12
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=telecomdb1 tests/
```

### 2. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml

repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
```

## Troubleshooting

### Common Issues

1. **Database Connection**
   - Check database credentials
   - Verify database is running
   - Check network connectivity

2. **Test Failures**
   - Check test data setup
   - Verify assertions
   - Review error messages

3. **Performance Issues**
   - Check for slow tests
   - Review database queries
   - Monitor resource usage

### Getting Help

1. **Internal Resources**
   - Check test documentation
   - Review test logs
   - Consult team members

2. **External Resources**
   - pytest documentation
   - Stack Overflow
   - GitHub Issues 