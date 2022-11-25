from flask import Flask, jsonify, abort
from flask_restx import Api
from db import db
from resources.user import api as user_namespace
from resources.patient import api as patient_namespace
from resources.patient_reports import api as patient_reports_namespace
from resources.health import api as health_namespace
from flask_jwt_extended import JWTManager
import os
import models
from models.user import UserModel
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)

api = Api(app,version='1.0',title='Patient Management APP', description='Patient API')

# JWT
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


with app.app_context():
    db.create_all()

api.add_namespace(patient_namespace, path='/patient')
api.add_namespace(patient_reports_namespace, path='/patient')
api.add_namespace(user_namespace, path='/user')
api.add_namespace(health_namespace, path='/health')


if __name__ == '__main__':
    app.run(debug=True)