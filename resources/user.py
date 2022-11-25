from flask import request, abort, jsonify
from flask_restx import Namespace, Resource, fields
from models.user import UserModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from passlib.hash import pbkdf2_sha256

api = Namespace('Users', description='User API operations')

user_input = api.model(
    'UserFields',
    {
        'name': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'roles': fields.List(fields.String, required=True),
    }
)

login_input = api.model(
    'LoginFields',
    {
        'email': fields.String(required=True),
        'password': fields.String(required=True)
    }
)

user_output = api.inherit(
    'User',
    user_input,
    {
        'id': fields.Integer()
    }

)

def check_admin_role():
    jwt = get_jwt()
    is_admin = jwt.get('is_admin')
    if not is_admin:
        abort(401, 'You do not have the permission to perform this action')

@api.route('/register')
@api.doc(
    responses={
        404: 'User not found',
        400: 'Bad request',
        500: 'An error occurred while registering user'
    }
)
class UserRegister(Resource):
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output)
    def post(self):
        user_data = request.get_json()
        existing_user = UserModel.find_by_email(user_data['email'])
        if existing_user:
            abort(400, 'The email already registered. Please log in')
        user = UserModel(
            name=user_data['name'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password']),
            roles=user_data['roles']
            )
        try:
            user.save()
        except SQLAlchemyError as e:
            abort(400, 'An error occurred while creating user')
        return user, 201



@api.route('/login')
@api.doc(
    responses={
        404: 'User not found',
        400: 'Bad request',
        500: 'An error occurred while logging in'
    }
)
class UserLogin(Resource):
    @api.expect(login_input, validate=True)
    def post(self):
        user_data = request.get_json()
        email = user_data['email']
        password = user_data['password']
        if not email or not password:
            abort(400, message='Please provide email or password')
        user = UserModel.find_by_email(email)
        if not user:
            abort(404, message=f'User not found with email {email}')
        is_password_match = pbkdf2_sha256.verify(password, user.password)
        if not is_password_match:
            abort(404, message='Invalid credentials')
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200


@api.route('/<user_id>')
@api.doc(
    responses={
        404: 'User not found',
        400: 'Bad request',
        500: 'An error occurred while registering user'
    }
)
class User(Resource):
    @jwt_required()
    @api.marshal_list_with(user_output)
    def get(self, user_id):
       user = UserModel.find_by_id(user_id)
       if not user:
          abort(404, f'User not found with id {user_id}')
       return user
         

    @jwt_required()
    @api.expect(user_input, validate=True)
    @api.marshal_with(user_output)
    def put(self, user_id):
        check_admin_role()
        user = UserModel.find_by_id(user_id)
        if not user:
          abort(404, f'User not found with id {user_id}')

        user_data = request.get_json()
        updated_user = UserModel(
            id=user_id,
            name=user_data['name'],
            email=user_data['email'],
            password=pbkdf2_sha256.hash(user_data['password']),
            roles=user_data['roles']
        )
        try:
            updated_user.update()
        except SQLAlchemyError as e:
            abort(400, 'An error occurred while creating user')
        return updated_user

    @jwt_required()
    def delete(self, user_id):
        check_admin_role()
        user = UserModel.find_by_id(user_id)
        if not user:
          abort(404, f'User not found with id {user_id}')
        try:
            user.delete()
        except SQLAlchemyError as e:
            abort(400, 'An error occurred while creating user')
        return {'message': 'User deleted successfully!'}


@api.route('')
@api.doc(
    responses={
        404: 'User not found',
        400: 'Bad request',
        500: 'An error occurred while retrieving users'
    }
)
class UserList(Resource):
    @jwt_required()
    @api.marshal_list_with(user_output)
    def get(self):
        return UserModel.find_all()
