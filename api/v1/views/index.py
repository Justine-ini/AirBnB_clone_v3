#!/usr/bin/python3
'''View functions for the status route.'''
from flask import jsonify

from api.v1.views import app_views


@app_views.route('/status')
def get_status():
    '''Gets the status of the API.
    '''
    return jsonify({"status": "OK"})
