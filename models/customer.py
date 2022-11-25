from db import db


class CustomerModel(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

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
