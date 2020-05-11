from . import db
import datetime
from marshmallow import fields, Schema
from .UserpostModel import UserpostSchema
from .RecipeModel import RecipeSchema


class ReviewModel(db.Model):
    """
    Review Model
    """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review_content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    reviewed_at = db.Column(db.DateTime)
    recipes = db.relationship("RecipeModel", backref="reviews", lazy=True)

    def __init__(self, data):
        self.review_content = data.get('review_content')
        self.user_id = data.get('user_id')
        self.recipe_id = data.get('recipe_id')
        self.reviewed_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_review_for_recipe(recipe_id, review_content):
        return ReviewModel.query.filter_by(recipe_id, review_content).first()

    def review(self, user_id, recipe_id, review_content):
        return self.review(user_id, recipe_id, review_content)

    def get_one_review(id):
        return ReviewModel.query.get(id)

class ReviewSchema(Schema):
    """
    Review Schema
    """

    id = fields.Int(dumb_only=True)
    user_id = fields.Int(required=True)
    recipe_id = fields.Int(required=True)
    reviewed_at = fields.DateTime(dump_only=True)
    review_content = fields.Str(required=True)
    # recipes = fields.Nested(RecipeSchema, many=True)