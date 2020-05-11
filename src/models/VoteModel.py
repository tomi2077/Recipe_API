from . import db
import datetime
from marshmallow import fields, Schema
from .UserpostModel import UserpostSchema
from .RecipeModel import RecipeSchema


class VoteModel(db.Model):
    """
    Vote Model
    """
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    voted_at = db.Column(db.DateTime)
    user = db.relationship("UserpostModel", backref="users", lazy=True)

    def __init__(self, data):
        self.user_id = data.get('user_id')
        self.recipe_id = data.get('recipe_id')
        self.voted_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # @staticmethod
    # def count_recipe_votes(value_id):
    #     return VoteModel.query.filter_by(recipe_id=value_id).count()
    #
    @staticmethod
    def get_user_votes(recipe_id):
        return VoteModel.query.filter_by(recipe_id).count()

    @staticmethod
    def get_recipe_vote_for_user(user_id, recipe_id):
        return VoteModel.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()

    @staticmethod
    def get_all_votes():
        return VoteModel.query.all()


class VoteSchema(Schema):
    """
    Vote Schema
    """

    id = fields.Int(dumb_only=True)
    user_id = fields.Int(required=True)
    recipe_id = fields.Int(required=True)
    voted_at = fields.DateTime(dump_only=True)
    # user = fields.Nested(UserpostSchema, many=True)
    # recipe = fields.Nested(RecipeSchema, many=True)
