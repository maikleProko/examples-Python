from flask_restful import Resource
from flask import request
from db.api import get_duckiebots, get_user_data_from_JWT


class DuckiebotsList(Resource):
    # get all exists duckiebots
    def get(self) -> [str]:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        return get_duckiebots()
