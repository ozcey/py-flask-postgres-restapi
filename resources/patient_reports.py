from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.patient import PatientModel
from models.address import AddressModel
from models.patient_reports import PatientReportsModel
from sqlalchemy.exc import SQLAlchemyError

api = Namespace('Patients reports', description='Patient reports API operations')

patient_reports_input = api.model(
    'PatientReportsFields',
    {
        'diagnose': fields.String(required=True),
        'test_type': fields.String(),
        'test_result': fields.String(),
        'medicine': fields.String(),
        'doctor': fields.String(required=True),
        'date': fields.String(required=True)
    }
)

patient_reports_output = api.inherit(
    'PatientReports',
    patient_reports_input,
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
class PatientReportsList(Resource):
    @api.marshal_list_with(patient_reports_output)
    def get(self, patient_id):
        return PatientReportsModel.find_by_patient_id(patient_id)
    
    @api.expect(patient_reports_input, validate=True)
    @api.marshal_list_with(patient_reports_output)
    def post(self, patient_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')
        reports = PatientReportsModel(
            patient_id=patient_id, **request.get_json())
        patient.patient_reports.append(reports)
        try:
            patient.save()
        except SQLAlchemyError:
            abort(500, 'An error occurred while creating patient details')
        return reports, 201
