from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.patient import PatientModel
from models.address import AddressModel
from sqlalchemy.exc import SQLAlchemyError

api = Namespace('Patients', description='Patient API operations')

address_input = api.model(
    'AddressFields',
    {
        'street': fields.String(required=True),
        'city': fields.String(required=True),
        'state': fields.String(required=True),
        'zipcode': fields.String(required=True)
    }
)

patient_input = api.model(
    'PatientFields',
    {
        'name': fields.String(required=True),
        'ssn': fields.String(required=True),
        'email': fields.String(required=True),
        'phone': fields.String(required=True),
        'age': fields.Integer(required=True),
        'gender': fields.String(required=True),
        'address': fields.Nested(address_input)
    }
)

patient_output = api.inherit(
    'Patient',
    patient_input,
    {
        'id': fields.Integer()
    }

)

@api.route('')
@api.doc(
    responses={
        404: 'Patient not found',
        400: 'Bad request',
        500: 'An error occurred while creating patient'
    }
)
class PatientList(Resource):
    @api.marshal_list_with(patient_output)
    def get(self):
        return PatientModel.find_all()
    
    @api.expect(patient_input, validate=True)
    @api.marshal_with(patient_output)
    def post(self):
        patient_data = request.get_json()
        new_address = AddressModel(**patient_data['address'])
        new_patient = {
            "name": patient_data['name'],
            "ssn": patient_data['ssn'],
            "email": patient_data['email'],
            "phone": patient_data['phone'],
            "age": patient_data['age'],
            "gender": patient_data['gender']
        }
        patient = PatientModel(**new_patient)
        patient.address = new_address
        try:
            patient.save()
        except SQLAlchemyError:
            abort(500, 'An error occurred while creating patient')
        return patient, 201


@api.route('/<patient_id>')
@api.doc(
    responses={
        404: 'Patient not found',
        400: 'Bad request',
        500: 'An error occurred while creating patient'
    }
)
class Patient(Resource):
    @api.marshal_with(patient_output)
    def get(self, patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')
        return patient
    
    # TODO: Set uo postgres then try using delete 
    def delete(self, patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')
        try:
            patient.delete()
        except SQLAlchemyError:
            abort(500, 'An error occurred while deleting patient')
        return {'message': 'Patient deleted successfully!'}