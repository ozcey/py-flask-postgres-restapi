from db import db


class PatientReportsModel(db.Model):
    __tablename__ = 'patient_reports'

    id = db.Column(db.Integer, primary_key=True)
    diagnose = db.Column(db.String(200),  nullable=False)
    test_type = db.Column(db.String(80))
    test_result = db.Column(db.String(80))
    medicine = db.Column(db.String(80))
    doctor = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
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

    def update(self):
        db.session.merge(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
