#!/usr/bin/python3
"""Create a new view for User object that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def get_users():
    """Retrieves the list of all User objects"""
    users = storage.get(User)
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', stict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes an User object"""
    users = storage.get(User, user_id)
    if users is None:
        abort(404)
    users.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def post_user():
    """Creates a User"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    user = User(**data)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False, methods=['PUT'])
def put_user(user_id):
    """Updates User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


if __name__ == "__main__":
    app_views.run(host='0.0.0.0')