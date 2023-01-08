from config.db_configs import db


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


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
