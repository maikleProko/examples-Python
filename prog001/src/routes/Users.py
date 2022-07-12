from flask import request
from flask_restful import Resource
from typing import Dict, Any
from db.api import get_user, del_user, add_user, get_user_data_from_JWT
from db.classes import User as DB_User


class Users(Resource):

    def get(self) -> Dict[str, Any]:
        name = request.args.get('name')
        user = get_user(DB_User(name))
        if user:
            return user.dict()
        return None

    def post(self) -> [Dict[str, Any], int]:
        # need header: Content-type: application/json
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        name: str = data["name"]
        role: str = data["role"]
        user_jwt: str = ""
        added_user: dict = add_user(DB_User(name, role, user_jwt))
        if added_user:
            del added_user["_id"]
        return added_user, 201

    def delete(self) -> Dict[str, Any]:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        name = request.args.get('name')
        user = get_user(DB_User(name))
        if not user:
            return None
        del_user(user)
        return user.dict()
