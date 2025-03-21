from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from security.auth import require_api_key
from security.audit import audit_logger
from typing import Dict, Any

app = Flask(__name__)
api = Api(app)

class CustomerAPI(Resource):
    @require_api_key(['read:customers'])
    def get(self, customer_id: str) -> Dict[str, Any]:
        """Get customer details."""
        try:
            # TODO: Implement customer retrieval
            customer = {'id': customer_id, 'name': 'Test Customer'}
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='customer',
                resource_id=customer_id,
                action='read'
            )
            return customer
        except Exception as e:
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='customer',
                resource_id=customer_id,
                action='read',
                status='error',
                error=str(e)
            )
            return {'error': str(e)}, 500

    @require_api_key(['write:customers'])
    def post(self) -> Dict[str, Any]:
        """Create a new customer."""
        try:
            data = request.get_json()
            # TODO: Implement customer creation
            customer_id = '123'  # Replace with actual creation
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='customer',
                resource_id=customer_id,
                action='create'
            )
            return {'id': customer_id, 'message': 'Customer created'}, 201
        except Exception as e:
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='customer',
                resource_id='new',
                action='create',
                status='error',
                error=str(e)
            )
            return {'error': str(e)}, 500

class BillAPI(Resource):
    @require_api_key(['read:bills'])
    def get(self, bill_id: str) -> Dict[str, Any]:
        """Get bill details."""
        try:
            # TODO: Implement bill retrieval
            bill = {'id': bill_id, 'amount': 100.00}
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='bill',
                resource_id=bill_id,
                action='read'
            )
            return bill
        except Exception as e:
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='bill',
                resource_id=bill_id,
                action='read',
                status='error',
                error=str(e)
            )
            return {'error': str(e)}, 500

    @require_api_key(['write:bills'])
    def post(self) -> Dict[str, Any]:
        """Create a new bill."""
        try:
            data = request.get_json()
            # TODO: Implement bill creation
            bill_id = '456'  # Replace with actual creation
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='bill',
                resource_id=bill_id,
                action='create'
            )
            return {'id': bill_id, 'message': 'Bill created'}, 201
        except Exception as e:
            audit_logger.log_data_access(
                user_id=request.headers.get('X-API-Key'),
                resource_type='bill',
                resource_id='new',
                action='create',
                status='error',
                error=str(e)
            )
            return {'error': str(e)}, 500

# Register API routes
api.add_resource(CustomerAPI, '/api/customers/<string:customer_id>', '/api/customers')
api.add_resource(BillAPI, '/api/bills/<string:bill_id>', '/api/bills')

if __name__ == '__main__':
    app.run(debug=True) 