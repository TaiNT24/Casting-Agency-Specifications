import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()

    # add one demo row
    mov = Movies()
    mov.title = 'Fast and furious 8'
    mov.release_date = datetime.strptime('2017-04-14', '%Y-%m-%d')

    mov.insert()

    act = Actors()
    act.name = 'Dwayne Johnson'
    act.age = 50
    act.gender = 0

    act.insert()


class Movies(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    release_date = Column(Date, nullable=False)

    def description(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("")
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.description())


class Actors(db.Model):
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=True)
    age = Column(Integer, nullable=False)
    # 0: man, 1: women
    gender = Column(Integer, nullable=True)

    def description(self):
        gender = ""
        if self.gender == 0:
            gender = "Man"
        elif self.gender == 1:
            gender = "Women"

        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.description())
