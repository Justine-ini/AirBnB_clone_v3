#!/usr/bin/python3
"""Update states"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", strict_slashes=False)
def get_places(city_id):
    """Method for list all places from city"""
    new_list = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route("/places/<string:place_id>", strict_slashes=False)
def one_place(place_id):
    """Method for list one place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<string:place_id>", methods=["DELETE"],
                 strict_slashes=False)
def place_delete(place_id):
    """Method that deletes a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route("/cities/<string:city_id>/places", methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """Method that creates a place"""
    city = storage.get(City, city_id)
    data = request.get_json()
    if not city:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data['city_id'] = city_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/places/<string:place_id>", methods=['PUT'],
                 strict_slashes=False)
def place_put(place_id):
    """Method that updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)

def find_places():
    '''Finds places based on a list of State, City, or Amenity ids.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    all_places = storage.all(Place).values()
    places = []
    places_id = []
    keys_status = (
        all([
            'states' in data and type(data['states']) is list,
            'states' in data and len(data['states'])
        ]),
        all([
            'cities' in data and type(data['cities']) is list,
            'cities' in data and len(data['cities'])
        ]),
        all([
            'amenities' in data and type(data['amenities']) is list,
            'amenities' in data and len(data['amenities'])
        ])
    )
    if keys_status[0]:
        for state_id in data['states']:
            if not state_id:
                continue
            state = storage.get(State, state_id)
            if not state:
                continue
            for city in state.cities:
                new_places = []
                if storage_t == 'db':
                    new_places = list(
                        filter(lambda x: x.id not in places_id, city.places)
                    )
                else:
                    new_places = []
                    for place in all_places:
                        if place.id in places_id:
                            continue
                        if place.city_id == city.id:
                            new_places.append(place)
                places.extend(new_places)
                places_id.extend(list(map(lambda x: x.id, new_places)))
    if keys_status[1]:
        for city_id in data['cities']:
            if not city_id:
                continue
            city = storage.get(City, city_id)
            if city:
                new_places = []
                if storage_t == 'db':
                    new_places = list(
                        filter(lambda x: x.id not in places_id, city.places)
                    )
                else:
                    new_places = []
                    for place in all_places:
                        if place.id in places_id:
                            continue
                        if place.city_id == city.id:
                            new_places.append(place)
                places.extend(new_places)
