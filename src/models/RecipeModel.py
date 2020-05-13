from . import db
import datetime
from marshmallow import fields, Schema
#from ..models.VoteModel import VoteModel


class RecipeModel(db.Model):

    """
    Recipe model
    """

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    votes = db.relationship("VoteModel", backref="recipes", lazy=True)

    def __init__(self, data):
        self.title = data.get('title')
        self.contents = data.get('contents')
        self.owner_id = data.get('owner_id')
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_recipes():
        return RecipeModel.query.all()

    @staticmethod
    def get_one_recipe(id):
        return RecipeModel.query.get(id)

    @staticmethod
    def get_user_recipes(user_id):
        return RecipeModel.query.filter_by(owner_id=user_id)

    @staticmethod
    def get_recipe_of_user(owner_id, recipe_id):
        return RecipeModel.query.filter_by(owner_id=owner_id, recipe_id=recipe_id)

    @staticmethod
    def get_and_filter_recipe():
        return RecipeModel.query.join(VoteModel).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class RecipeSchema(Schema):
    """
    Recipe Schema
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    contents = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)