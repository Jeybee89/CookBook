from db import db


class CoursesModel(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # recipes = db.relationship('RecipeModel', secondary='recipes_has_courses')

    def __init__(self, id, name):
        self.id = id,
        self.name = name

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
