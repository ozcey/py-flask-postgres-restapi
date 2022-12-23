import models
from flask import Flask
from flask_restx import Api
from resources.user import api as user_namespace
from resources.patient import api as patient_namespace
from resources.patient_reports import api as patient_reports_namespace
from resources.health import api as health_namespace
from config.jwt_config import set_jwt_configs
from config.db_configs import set_db_configs, create_tables
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# DB config
set_db_configs(app)
# Flask-restx config
api = Api(app,version='1.0',title='Patient Management APP', description='Patient API')
# JWT configs
set_jwt_configs(app)
# Create tables
create_tables(app)
# Namespaces
api.add_namespace(patient_namespace, path='/api/patient')
api.add_namespace(patient_reports_namespace, path='/api/patient')
api.add_namespace(user_namespace, path='/api/user')
api.add_namespace(health_namespace, path='/api/health')


if __name__ == '__main__':
    app.run(debug=True)