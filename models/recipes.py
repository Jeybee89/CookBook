from db import db
import simplejson as json


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    # create recipe table
    id = db.Column(db.Integer, primary_key=True, )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuisine_id = db.Column(db.Integer, db.ForeignKey('cuisine.id'))
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

    allergens = db.relationship('AllergensModel', secondary='recipes_has_allergens')

    courses = db.relationship('CoursesModel', secondary='recipes_has_courses')

    cuisine = db.relationship('CuisineModel', backref='cuisine')

    upvotes = db.relationship('UpVotesModel', backref='upvotes')

    ingredients = db.relationship('IngredientsModel', backref='ingredients')

    def __init__(self, user_id, cuisine_id, name, description, image_path, total_time, prep_time, cook_time, level,
                 source, rating):
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

    # Return recipe as JSON object
    def json(self):
        return {
            'id': self.id,
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
            'allergens': [allergens.json() for allergens in self.allergens],
            'courses': [courses.json() for courses in self.courses],
            'cuisine': self.cuisine.json(),
            'upvotes': [upvotes.json() for upvotes in self.upvotes],
            'ingredients': [ingredients.json() for ingredients in self.ingredients],
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
    def save_recipe_to_db(self, category):
        self.recipes_has_categories.append(RecipeCategory(id=None, recipes_id=self.id, categories_id=category.id))
        db.session.add(self)
        db.session.commit()

    def save_allergen_to_db(self, allergens):
        self.recipes_has_allergens.append(RecipeAllergens(id=None, recipes_id=self.id, allergens_id=allergens.id))
        db.session.add(self)
        db.session.commit()

    def save_course_to_db(self, courses):
        self.recipes_has_courses.append(RecipeCourses(id=None, recipes_id=self.id, courses_id=courses.id))
        db.session.add(self)
        db.session.commit()

    # def save_to_db_category(self, category):
    #     db.session.add(self, category)
    #     db.session.commit()

    # Delete recipe from db
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


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


class RecipeAllergens(db.Model):
    __tablename__ = 'recipes_has_allergens'

    id = db.Column(db.Integer, primary_key=True, )
    recipes_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    allergens_id = db.Column(db.Integer, db.ForeignKey('allergens.id'))

    recipes = db.relationship("RecipeModel", backref=db.backref("recipes_has_allergens", cascade="all, delete-orphan"))
    allergens = db.relationship("AllergensModel",
                                backref=db.backref("recipes_has_allergens", cascade="all, delete-orphan"))

    def __init__(self, id, recipes_id, allergens_id):
        self.id = id
        self.recipes_id = recipes_id
        self.allergens_id = allergens_id


class RecipeCourses(db.Model):
    __tablename__ = 'recipes_has_courses'

    id = db.Column(db.Integer, primary_key=True, )
    recipes_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    recipes = db.relationship("RecipeModel", backref=db.backref("recipes_has_courses", cascade="all, delete-orphan"))
    courses = db.relationship("CoursesModel",
                              backref=db.backref("recipes_has_courses", cascade="all, delete-orphan"))

    def __init__(self, id, recipes_id, courses_id):
        self.id = id
        self.recipes_id = recipes_id
        self.courses_id = courses_id
