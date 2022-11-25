import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def set_db_configs(app):
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)


def create_tables(app):
    with app.app_context():
        db.create_all()
