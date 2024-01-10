#!/usr/bin/python3
"""Update Amenity"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", strict_slashes=False)
def get_state():
    """Method for state"""
    new_list = []
    for state in storage.all("State").values():
        new_list.append(state.to_dict())
    return jsonify(new_list)


@app_views.route("/states/<string:state_id>", strict_slashes=False)
def one_state(state_id):
    """Method for one state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<string:state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Method for delete state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """Method for post state"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<string:state_id>", methods=['PUT'],
                 strict_slashes=False)
def state_put(state_id):
    """Method that updates a state"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
