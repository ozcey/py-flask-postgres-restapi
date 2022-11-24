from db import db


class PatientModel(db.Model):
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
    
    def update(self):
        db.session.merge(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

