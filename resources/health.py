from flask_restx import Resource, Namespace


api = Namespace('Health Status', description='APPs health status')

@api.route('')
class HealthInfo(Resource):
    def get(self):
      return {'status': 'UP'}
