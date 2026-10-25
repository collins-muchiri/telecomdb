# Telecom Billing System

*Telecom database management system with analytics, reporting and data pipelines; Python.*

![category](https://img.shields.io/badge/category-data-engineering-10B981?style=flat-square) ![language](https://img.shields.io/badge/language-Python-2563EB?style=flat-square) ![license](https://img.shields.io/badge/license-MIT-16A34A?style=flat-square) ![maintenance](https://img.shields.io/badge/maintenance-dormant-D97706?style=flat-square) ![repo](https://img.shields.io/badge/repo-telecomdb-111827?style=flat-square)

---

A secure and efficient API for managing telecom billing data, including customer management, bill generation, payment processing, and usage tracking.

## Features

### Core Functionality
- Customer Management
  - Customer registration and profile management
  - Account status tracking
  - Customer information validation

- Billing Management
  - Automated bill generation
  - Usage-based billing
  - Multiple plan support
  - Overage charge calculation

- Payment Processing
  - Multiple payment method support
  - Payment status tracking
  - Payment history
  - Automated payment reminders

- Usage Tracking
  - Data usage monitoring
  - Voice minutes tracking
  - SMS usage tracking
  - Usage limits enforcement

### Security Features
- API Key Authentication
- Rate Limiting
- Audit Logging
- Data Encryption
- Secure Payment Processing

### Database Management
- PostgreSQL Database
- Database Migrations (Alembic)
- Automated Backups
- Connection Pooling

### Development Tools
- Code Quality Checks
- Type Checking
- Automated Testing
- Documentation Generation

## Prerequisites

- Python 3.9 or higher
- PostgreSQL 15 or higher
- Redis (for rate limiting and caching)
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/collins-muchiri/telecomdb.git
cd telecomdb
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Project Structure

```
telecomdb1/
├── api/
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   └── __init__.py
├── security/
│   ├── auth.py         # Authentication
│   └── audit.py        # Audit logging
├── scripts/
│   └── migrations/     # Database migrations
├── tests/
│   ├── unit/          # Unit tests
│   └── integration/   # Integration tests
├── docs/              # Documentation
├── exports/           # Data export directory
├── alembic.ini        # Alembic configuration
├── config.py          # Application configuration
├── requirements.txt   # Dependencies
└── setup.py          # Setup script
```

## API Endpoints

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer details
- `POST /api/customers` - Create new customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Deactivate customer

### Bills
- `GET /api/bills` - List all bills
- `GET /api/bills/{id}` - Get bill details
- `POST /api/bills` - Generate new bill
- `PUT /api/bills/{id}` - Update bill
- `GET /api/bills/{id}/payments` - List bill payments

### Payments
- `POST /api/payments` - Process payment
- `GET /api/payments/{id}` - Get payment details
- `GET /api/payments/customer/{customer_id}` - List customer payments

### Usage
- `GET /api/usage/{customer_id}` - Get customer usage
- `POST /api/usage` - Record usage
- `GET /api/usage/limits/{customer_id}` - Get usage limits

## Development

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=telecomdb1

# Run specific test file
python -m pytest tests/test.py
```

### Code Quality
```bash
# Run linters
flake8
black .
isort .
mypy .

# Run security checks
bandit -r telecomdb1
```

### Database Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Deployment

### Using Docker
```bash
# Build and start services
docker-compose up --build

# Stop services
docker-compose down
```

### Manual Deployment
1. Set up PostgreSQL database
2. Configure Redis
3. Set environment variables
4. Run database migrations
5. Start the application:
```bash
gunicorn --bind 0.0.0.0:5000 telecomdb1.api.app:app
```

## Security

- All API endpoints require authentication
- Rate limiting is enforced
- Sensitive data is encrypted
- Audit logging tracks all operations
- Regular security updates and patches

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the development team. 