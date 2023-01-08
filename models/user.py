from sqlalchemy.dialects.postgresql import ARRAY
from config.db_configs import db
from models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    roles = db.Column(ARRAY(db.String), nullable=False)


    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()