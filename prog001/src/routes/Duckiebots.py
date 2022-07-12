from flask import request
from flask_restful import Resource
from typing import Dict, Any

from db.api import get_duckiebot, add_duckiebot, del_duckiebot, update_duckiebot_from_id, get_user_data_from_JWT
from db.classes import DuckieBot


class Duckiebots(Resource):

    def get(self) -> Dict[str, Any]:
        hostname: str = request.args.get("hostname")
        bot: DuckieBot = get_duckiebot(DuckieBot(hostname))
        if bot:
            return bot.dict()
        return None

    def post(self) -> [Dict[str, Any], int]:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        hostname: str = data["hostname"]
        added_duckiebot: dict = add_duckiebot(DuckieBot(hostname))
        if added_duckiebot:
            del added_duckiebot["_id"]
        return added_duckiebot, 201

    # edit duckiebot
    def put(self):
        # id and owner will not change
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        hostname: str = data["hostname"]
        hostnameId: str = data["hostnameId"]
        duckiebot = get_duckiebot(DuckieBot(hostnameId))
        update_duckiebot_from_id(duckiebot, hostname)
        return 201

    def delete(self):
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        hostname: str = data["hostname"]
        duckiebot = get_duckiebot(DuckieBot(hostname))
        if not duckiebot:
            return None
        del_duckiebot(duckiebot)
        return duckiebot.dict()
