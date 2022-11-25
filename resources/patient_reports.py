from flask import request, abort
from flask_restx import Namespace, Resource, fields
from models.patient import PatientModel
from models.patient_reports import PatientReportsModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required

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
    @jwt_required()
    @api.marshal_list_with(patient_reports_output)
    def get(self, patient_id):
        return PatientReportsModel.find_by_patient_id(patient_id)
    
    @jwt_required()
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
            abort(400, 'An error occurred while creating patient details')
        return reports, 201


@api.route('/<patient_id>/details/<patient_report_id>')
@api.doc(
    responses={
        404: 'Patient not found',
        400: 'Bad request',
        500: 'An error occurred while creating patient'
    }
)
class PatientReports(Resource):
    @jwt_required()
    @api.expect(patient_reports_input, validate=True)
    @api.marshal_with(patient_reports_output)
    def put(self, patient_id, patient_report_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')

        patient_report = PatientReportsModel.find_by_id(patient_report_id)
        if not patient_report:
            abort(404, f'Patient report not found with id {patient_report_id}')

        report_data = request.get_json()
        updated_report = {
            "diagnose": report_data['diagnose'],
            "test_type": report_data['test_type'],
            "test_result": report_data['test_result'],
            "medicine": report_data['medicine'],
            "doctor": report_data['doctor'],
            "date": report_data['date']
        }
        patient_report = PatientReportsModel(id=patient_report_id,**updated_report, patient_id=patient_id)
        try:
            patient_report.update()
        except SQLAlchemyError as e:
            abort(400, 'An error occurred while updating patient')
        return patient_report

    @jwt_required()
    def delete(self, patient_id, patient_report_id):
        patient = PatientModel.find_by_id(patient_id)
        if not patient:
            abort(404, f'Patient not found with id {patient_id}')
        patient_report = PatientReportsModel.find_by_id(patient_report_id)
        if not patient_report:
            abort(404, f'Patient report not found with id {patient_report_id}')
        try:
            patient_report.delete()
        except SQLAlchemyError:
            abort(400, 'An error occurred while deleting patient report')
        return {'message': 'Patient report deleted successfully!'}
