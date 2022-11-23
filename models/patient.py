from db import db


class PatientModel(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),  nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    ssn = db.Column(db.String(9), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.String(7), nullable=False)
    address = db.relationship(
        'AddressModel', backref='patients', uselist=False)
    patient_details = db.relationship(
        'PatientDetailsModel', backref='patients')

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_ssn(cls, ssn):
        return cls.query.filter_by(ssn=ssn).first()
    
    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

