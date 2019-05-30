from db import db
import simplejson as json


class RecipeCategory(db.Model):
    __tablename__ = 'recipes_has_categories'

    id = db.Column(db.Integer, primary_key=True, )
    recipes_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    recipes = db.relationship("RecipeModel", backref=db.backref("recipes_has_categories", cascade="all, delete-orphan"))
    categories = db.relationship("CategoriesModel",
                                 backref=db.backref("recipes_has_categories", cascade="all, delete-orphan"))

    def __init__(self, id, recipes_id, categories_id):
        self.id = id
        self.recipes_id = recipes_id
        self.categories_id = categories_id


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    # create recipe table
    id = db.Column(db.Integer, primary_key=True, )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuisine_id = db.Column(db.Integer)
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    image_path = db.Column(db.String(100))
    total_time = db.Column(db.Integer)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    level = db.Column(db.String(45))
    source = db.Column(db.String(45))
    rating = db.Column(db.DECIMAL(3, 2))
    time_added = db.Column(db.Date)

    steps = db.relationship('StepsModel', backref='step',
                            cascade="all, delete-orphan",
                            lazy='dynamic',
                            passive_deletes=True)

    comments = db.relationship('CommentsModel', backref='comments',
                               cascade="all, delete-orphan",
                               lazy='dynamic',
                               passive_deletes=True)

    user = db.relationship('UserModel', backref='user')

    categories = db.relationship('CategoriesModel', secondary='recipes_has_categories')

    def __init__(self, user_id, cuisine_id, name, description, image_path, total_time, prep_time, cook_time, level,
                 source, rating, alergens):
        self.user_id = user_id
        self.cuisine_id = cuisine_id
        self.name = name
        self.description = description
        self.image_path = image_path
        self.total_time = total_time
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.level = level
        self.source = source
        self.rating = json.dumps(rating)
        self.alergens = alergens

    # Return recipe as JSON object
    def json(self):
        return {
            'name': self.name,
            'cuisine_id': self.cuisine_id,
            'description': self.description,
            'image_path': self.image_path,
            'total_time': self.total_time,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'level': self.level,
            'source': self.source,
            'rating': json.dumps(self.rating),  # JSON encoder and decoder for DECIMAL number
            'steps': [steps.json() for steps in self.steps.all()],
            'time_added': self.time_added.isoformat(),
            'comments': [comments.json() for comments in self.comments.all()],
            'user': self.user.json(),
        }

    # Find recipe by ID
    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Find all recipes
    @classmethod
    def find_all(cls):
        return cls.query.all()

    # Save recipe to db
    def save_to_db(self, category):
        print(self, category)

        self.recipes_has_categories.append(RecipeCategory(id=None, recipes_id=self.id, categories_id=category.id))
        db.session.add(self)
        db.session.commit()

    def save_to_db_category(self, category):
        db.session.add(self, category)
        db.session.commit()

    # Delete recipe from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()