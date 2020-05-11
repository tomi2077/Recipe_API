from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


from .RecipeModel import RecipeModel, RecipeSchema
from .UserpostModel import UserpostModel, UserpostSchema
from .VoteModel import VoteModel, VoteSchema
from .ReviewModel import ReviewModel, ReviewSchema

