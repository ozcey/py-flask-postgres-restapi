from db import db


class AddressModel(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(80),  nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(9), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey(
        'patients.id'), nullable=False)
