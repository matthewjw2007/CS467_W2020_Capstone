from flask import Flask, Blueprint, jsonify, make_response, request
import constants

# Define the blueprint for Users
bp = Blueprint('recipes', __name__, url_prefix='/recipes')

# Setup route for /recipes
# methods variable defines accepted methods to this route
# using full list of HTTP verbs from constants.py to allow
# for error handling if an invalid verb is submitted to this route
@bp.route('', methods=constants.http_verbs)
def get_users():
    # GET
    if request.method == 'GET':

        # Make a response object with a JSON body
        res = make_response(jsonify(content="This is the Recipes page"))
        res.status_code = 200
        return res
        
    # All other verbs
    else:

        # Make a response object with a JSON body
        res = make_response(jsonify(error='Invalid HTTP method used for request'))
        res.status_code = 405
        return res