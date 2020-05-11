# src/views/UserpostView

from flask import request, json, Response, Blueprint, g
from ..models.UserpostModel import UserpostModel, UserpostSchema
from ..shared.Authentication import Auth
from ..models.RecipeModel import RecipeModel, RecipeSchema

user_api = Blueprint('user_api', __name__)
user_schema = UserpostSchema()
recipe_schema = RecipeSchema()


@user_api.route('/signup', methods=['POST'])
def create():
    """
    Create User Function
    """

    req_data = request.get_json()

    data = user_schema.load(req_data)

    user_in_db = UserpostModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 400)

    user = UserpostModel(data)
    user.save()
    user_data = user_schema.dump(user)

    token = Auth.generate_token(user_data.get('id'))

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/signin', methods=['POST'])
def signin():
    req_data = request.get_json()

    data = user_schema.load(req_data, partial=True)

    # if error:
    #     return custom_response(error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    user = UserpostModel.get_user_by_email(data.get('email'))

    if not user:
        return custom_response({'error': 'invalid credentials'}, 400)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid credentials'}, 400)

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)


@user_api.route('/<int:user_id>/recipes', methods=['GET'])
@Auth.auth_required
def get_all_user_recipes(user_id):
    current_user_id = g.user.get('id')
    if current_user_id != user_id:
        return custom_response({'error': 'Unauthorized request: User can only fetch personal recipes'}, 400)

    user_recipes = RecipeModel.get_user_recipes(user_id)
    user_data = recipe_schema.dump(user_recipes, many=True)
    return custom_response(user_data, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserpostModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)
    # if error:
    #     return custom_response(error, 400)

    user = UserpostModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserpostModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserpostModel.get_one_user(g.user.get('id'))
    print(user)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


def custom_error_response(res, status_code):
    """
    Custom Response Function
    """
    message = [str(x) for x in res.args]
    return Response(
        mimetype="application/json",
        response=json.dumps({'error': {'type': res.__class__.__name__, 'message': message}}),
        status=status_code
    )




# @user_api.route('/', methods=['GET'])
# @Auth.auth_required
# def get_all():
#    users = UserpostModel.get_all_users()
#    ser_users = user_schema.dump(users, many=True)
#    return custom_response(ser_users, 200)

