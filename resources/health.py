from flask_restx import Resource, Namespace


api = Namespace('Health Status', description='APPs health status')

@api.route('/health')
class HealthInfo(Resource):
    def get(self):
      return {'status': 'UP'}
