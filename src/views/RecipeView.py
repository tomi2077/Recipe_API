from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.RecipeModel import RecipeModel, RecipeSchema
from ..models.VoteModel import VoteModel, VoteSchema
from ..models.ReviewModel import ReviewModel, ReviewSchema

recipe_api = Blueprint('recipe', __name__)
recipe_schema = RecipeSchema()
vote_schema = VoteSchema()
review_schema = ReviewSchema()


@recipe_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Blogpost Function
    """

    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    recipe_data = recipe_schema.load(req_data)
    recipe = RecipeModel(recipe_data)
    print(recipe)
    recipe.save()
    recipe_data = recipe_schema.dump(recipe)
    return custom_response(recipe_data, 201)


@recipe_api.route('/<int:recipe_id>', methods=['PUT'])
@Auth.auth_required
def update(recipe_id):
    recipe_data = request.get_json()
    recipe = RecipeModel.get_one_recipe(recipe_id)
    # if not recipe:
    #     return custom_response({'error': 'recipe not found'}, 404)
    # recipe_correct = recipe_schema.dump(recipe)
    # if recipe_correct('owner_id') != g.user.get('id'):
    #     return custom_response({'error': 'permission denied'}, 400)

    recipe_correct = recipe_schema.load(recipe_data, partial=True)
    print(recipe_correct)
    # if error:
    #     return custom_response(error, 400)
    recipe.update(recipe_correct)

    recipe_correct = recipe_schema.dump(recipe)
    return custom_response(recipe_correct, 200)


@recipe_api.route('/<int:recipe_id>', methods=['DELETE'])
@Auth.auth_required
def delete(recipe_id):
    """
    Delete A Recipe
    """

    recipe_data = RecipeModel.get_one_recipe(recipe_id)
    if not recipe_data:
        return custom_response({'error': 'recipe not found'}, 404)
    recipe = recipe_schema.dump(recipe_data)
    if recipe.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    recipe_data.delete()
    return custom_response({'message': 'deleted'}, 204)


# @recipe_api.route('/', methods=['GET'])
# def get_all():
#     query_params = request.args
#     print(query_params, 'queryparams')
#
#     recipe_all = RecipeModel.get_and_filter_recipe()
#     # recipe_all = RecipeModel.get_all_recipes()
#     recipe = recipe_schema.dump(recipe_all, many=True)
#     return custom_response(recipe, 200)


@recipe_api.route('<int:recipe_id>', methods=['GET'])
@Auth.auth_required
def get_one(recipe_id):
    recipe_data = RecipeModel.get_one_recipe(recipe_id)
    if not recipe_data:
        return custom_response({'error': 'recipe not found'}, 404)
    recipe = recipe_schema.dump(recipe_data)
    return custom_response(recipe, 200)


@recipe_api.route('/vote', methods=['POST'])
@Auth.auth_required
def vote():
    req_data = request.get_json()
    req_data['user_id'] = g.user.get('id')
    action = req_data.pop('action')


    if action == 'upvote':
        print('upvoting')
        vote_data = VoteModel.get_recipe_vote_for_user(req_data['user_id'], req_data['recipe_id'])
        if vote_data:
            return custom_response({'error': 'User already voted for this recipe'}, 400)

        vote_data = vote_schema.load(req_data)
        vote = VoteModel(vote_data)
        print(vote, "Newly created vote")
        vote.save()
        return custom_response({'message': 'recipe successfully upvoted'}, 200)

    elif action == 'downvote':
        print('downvoting')
        vote_data = VoteModel.get_recipe_vote_for_user(req_data['user_id'], req_data['recipe_id'])
        print(vote_data, 'vote data for current user for this recipe')
        if vote_data:
            vote_data.delete()
            return custom_response({'message': 'recipe successfully downvoted'}, 200)
        return custom_response({'error': 'No vote recorded fo this recipe by this user'}, 400)
    else:
        return custom_response({'error': 'Invalid action passed'}, 400)


@recipe_api.route('/<int:recipe_id>/reviews', methods=['POST'])
@Auth.auth_required
def reviews(recipe_id):
    # id = request.args['id']
    req_data = request.get_json()
    req_data['user_id'] = g.user.get('id')
    req_data['recipe_id'] = recipe_id

    if not req_data.get('review_content'):
        return custom_response({'error': 'No review passed'}, 400)

    if req_data['user_id'] and req_data['recipe_id']:
        review_data = review_schema.load(req_data)
        review_data2 = ReviewModel(review_data)
        review_data2.save()
        return custom_response({'Message': 'Your review has been added!'}, 200)
    else:
        return custom_response({'error': 'Invalid request'}, 400)


@recipe_api.route('/', methods=['GET'])
def get_all():
    recipe_all = RecipeModel.query
    if request.args:
        sort = request.args['sort']
        order = request.args['order']

        if order == 'desc':
            if sort == 'upvotes':
                recipe_all = recipe_all.order_by(RecipeModel.id.desc())
            elif sort == 'downvotes':
                recipe_all = recipe_all.order_by(RecipeModel.id.desc())
        elif order == 'asc':
            if sort == 'upvotes':
                recipe_all = recipe_all.order_by(RecipeModel.id.asc())
            elif sort == 'downvotes':
                recipe_all = recipe_all.order_by(RecipeModel.id.asc())

    recipe_all = recipe_all.all()
    # recipe_all = RecipeModel.get_all_recipes()
    # recipe_all = RecipeModel.query.join(VoteModel).group_by(RecipeModel.id).order_by(func.count().desc()).all()
    recipe = recipe_schema.dump(recipe_all, many=True)
    return custom_response(recipe, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
