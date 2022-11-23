from db import db


class PatientDetailsModel(db.Model):
    __tablename__ = 'patient_details'

    id = db.Column(db.Integer, primary_key=True)
    insurance = db.Column(db.String(80),  nullable=False)
    notes = db.Column(db.String(80))
    provider = db.Column(db.String(80), nullable=False)
    total_cost = db.Column(db.Float(precision=2), nullable=False)
    copay = db.Column(db.Float(precision=2), nullable=False)
    complaint = db.Column(db.String(200), nullable=False)
    # date = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patients.id'), nullable=False)
    
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
