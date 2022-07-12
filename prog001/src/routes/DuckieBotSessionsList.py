from flask_restful import Resource
from flask import request
from db.api import get_sessions, get_user_data_from_JWT
from typing import Dict, Any


class DuckieBotSessionsList(Resource):
    # get all exists get_sessions
    def get(self) -> Dict[str, Any]:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        tzoffset = request.args.get('tzoffset')
        return get_sessions(tzoffset)
