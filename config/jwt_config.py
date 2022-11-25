
from flask_jwt_extended import JWTManager
from models.user import UserModel
from flask import jsonify, abort
import os


def set_jwt_configs(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user_id = identity
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, 'User not found')

        if 'ROLE_ADMIN' in user.roles:
            return {'is_admin': True}
        return {'is_admin': False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({'message': 'The token has expired',
                    'error': 'token_expired'}), 401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({'message': 'Signature verification failed',
                    'error': 'invalid_token'}), 401
        )


    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({'message': 'Request does not have an access token',
                    'error': 'authorization_required'}), 401
        )


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return (
            jsonify({'message': 'The token is not fresh',
                    'error': 'fresh_token_required'}), 410
        )
