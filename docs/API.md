# API Documentation

## Authentication

All API endpoints require authentication using an API key. Include the API key in the request header:

```
X-API-Key: your_api_key_here
```

### API Key Management

#### Generate API Key
```http
POST /api/keys
Content-Type: application/json

{
    "client_name": "string",
    "permissions": ["read:customers", "write:bills"]
}
```

#### Revoke API Key
```http
DELETE /api/keys/{api_key}
```

### Rate Limiting

- 100 requests per minute per API key
- Rate limit headers included in responses:
  - `X-RateLimit-Limit`
  - `X-RateLimit-Remaining`
  - `X-RateLimit-Reset`

## Endpoints

### Customers

#### Get Customer
```http
GET /api/customers/{customer_id}
```

Response:
```json
{
    "id": "string",
    "name": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

#### Create Customer
```http
POST /api/customers
Content-Type: application/json

{
    "name": "string",
    "email": "string",
    "phone": "string",
    "address": "string"
}
```

#### Update Customer
```http
PUT /api/customers/{customer_id}
Content-Type: application/json

{
    "name": "string",
    "email": "string",
    "phone": "string",
    "address": "string"
}
```

#### Delete Customer
```http
DELETE /api/customers/{customer_id}
```

### Bills

#### Get Bill
```http
GET /api/bills/{bill_id}
```

Response:
```json
{
    "id": "string",
    "customer_id": "string",
    "amount": "decimal",
    "due_date": "date",
    "status": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

#### Create Bill
```http
POST /api/bills
Content-Type: application/json

{
    "customer_id": "string",
    "amount": "decimal",
    "due_date": "date"
}
```

#### Update Bill
```http
PUT /api/bills/{bill_id}
Content-Type: application/json

{
    "amount": "decimal",
    "due_date": "date",
    "status": "string"
}
```

#### Delete Bill
```http
DELETE /api/bills/{bill_id}
```

### Payments

#### Get Payment
```http
GET /api/payments/{payment_id}
```

Response:
```json
{
    "id": "string",
    "bill_id": "string",
    "amount": "decimal",
    "payment_date": "datetime",
    "payment_method": "string",
    "transaction_id": "string"
}
```

#### Record Payment
```http
POST /api/payments
Content-Type: application/json

{
    "bill_id": "string",
    "amount": "decimal",
    "payment_method": "string",
    "transaction_id": "string"
}
```

#### Get Bill Payments
```http
GET /api/bills/{bill_id}/payments
```

Response:
```json
{
    "bill_id": "string",
    "payments": [
        {
            "id": "string",
            "amount": "decimal",
            "payment_date": "datetime",
            "payment_method": "string",
            "transaction_id": "string"
        }
    ]
}
```

### Reports

#### Generate Billing Report
```http
POST /api/reports/billing
Content-Type: application/json

{
    "start_date": "date",
    "end_date": "date",
    "customer_id": "string",
    "format": "csv|pdf"
}
```

#### Export Data
```http
POST /api/export
Content-Type: application/json

{
    "data_type": "customers|bills|payments",
    "start_date": "date",
    "end_date": "date",
    "format": "csv|pdf"
}
```

## Error Responses

### 400 Bad Request
```json
{
    "error": "string",
    "details": "object"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid API key"
}
```

### 403 Forbidden
```json
{
    "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

### 429 Too Many Requests
```json
{
    "error": "Rate limit exceeded",
    "retry_after": "seconds"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "request_id": "string"
}
```

## Best Practices

1. **Error Handling**
   - Always check response status codes
   - Handle rate limiting gracefully
   - Implement exponential backoff

2. **Security**
   - Keep API keys secure
   - Use HTTPS for all requests
   - Rotate API keys regularly

3. **Performance**
   - Cache responses when appropriate
   - Use pagination for large datasets
   - Implement request compression

4. **Monitoring**
   - Log all API calls
   - Monitor rate limits
   - Track error rates

## Rate Limits

| Endpoint | Rate Limit | Window |
|----------|------------|---------|
| All | 100 requests | 60 seconds |
| Reports | 10 requests | 60 seconds |
| Export | 5 requests | 60 seconds |

## Versioning

The API is versioned through the URL path:
```
/api/v1/customers
/api/v1/bills
```

Current version: v1 