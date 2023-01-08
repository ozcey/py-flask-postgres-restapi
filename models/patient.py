from config.db_configs import db
from models.base import BaseModel


class PatientModel(BaseModel):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  nullable=False)
    ssn = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(7), nullable=False)
    address = db.relationship(
        'AddressModel', backref='patients', cascade='all, delete-orphan', uselist=False)
    patient_reports = db.relationship(
        'PatientReportsModel', backref='patients', cascade='all, delete-orphan')

    @classmethod
    def find_by_ssn(cls, ssn):
        return cls.query.filter_by(ssn=ssn).first()
