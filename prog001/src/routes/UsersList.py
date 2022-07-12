from flask_restful import Resource
from flask import request
from db.api import get_list_of_users, get_user_data_from_JWT
from typing import Dict, Any


class UsersList(Resource):
    def get(self) -> [Dict[str, Any]]:
        if 'x-access-token' in request.headers:
            try:
                if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                    return None
            except:
                return None
        else:
            return None
        return get_list_of_users()
