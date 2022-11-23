from flask import Flask, jsonify
from flask_restx import Api
from db import db
from resources.patient import api as patient_namespace
from resources.patient_details import api as patient_details_namespace

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
api = Api(app, version='1.0', title='Patient Management APP', description='Patient API')

with app.app_context():
    db.create_all()

api.add_namespace(patient_namespace, path='/patient')
api.add_namespace(patient_details_namespace, path='/patient')

@app.get('/')
def health_info():
    return {'status': 'UP'}


if __name__ == '__main__':
    app.run(debug=True)