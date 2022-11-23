from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.patient import PatientModel
from models.address import AddressModel
from models.patient_details import PatientDetailsModel
from sqlalchemy.exc import SQLAlchemyError

api = Namespace('Patients details', description='Patient details API operations')

patient_details_input = api.model(
    'PatientDetailsFields',
    {
        'insurance': fields.String(required=True),
        'notes': fields.String(),
        'provider': fields.String(required=True),
        'total_cost': fields.Float(required=True),
        'copay': fields.Float(required=True),
        'complaint': fields.String(required=True)
        # 'date': fields.String(required=True)
    }
)

patient_details_output = api.inherit(
    'PatientDetails',
    patient_details_input,
    {
        'id': fields.Integer()
    }

)

@api.route('/<patient_id>/details')
@api.doc(
    responses={
        404: 'Patient not found',
        400: 'Bad request',
        500: 'An error occurred while creating patient details'
    }
)
class PatientDetailsList(Resource):
    @api.marshal_list_with(patient_details_output)
    def get(self, patient_id):
        return PatientDetailsModel.find_by_patient_id(patient_id)
    
    @api.expect(patient_details_input, validate=True)
    @api.marshal_list_with(patient_details_output)
    def post(self, patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')
        pa_details = PatientDetailsModel(
            patient_id=patient_id, **request.get_json())
        patient.patient_details.append(pa_details)
        try:
            patient.save()
        except SQLAlchemyError:
            abort(500, 'An error occurred while creating patient details')
        return pa_details, 201
