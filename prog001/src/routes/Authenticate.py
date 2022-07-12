from flask_restful import Resource
from flask import request
import requests
from db.classes import User as DB_User
from db.api import delete_jwt_for_user, get_jwt_and_store_it_in_db, get_user
from typing import Dict, Any


class Authenticate(Resource):
    def get(self) -> Dict[str, Any]:
        data = {
            "client_id": request.args.get('client_id'),
            "client_secret": request.args.get('client_secret'),
            "code": request.args.get('code'),
            "redirect_uri": request.args.get('redirect_uri')
        }
        return self.get_access_token_from_github(data)

    def post(self) -> str:
        # need header: Content-type: application/json
        data: dict = request.get_json()
        name: str = data["name"]
        new_jwt = get_jwt_and_store_it_in_db(DB_User(name))
        return new_jwt

    def delete(self) -> None:
        data: dict = request.get_json()
        try:
            name = data["name"]
            user = get_user(DB_User(name))
            delete_jwt_for_user(user)
        except:
            pass

    def get_access_token_from_github(self, data) -> Dict[str, Any]:
        res = requests.get("https://github.com/login/oauth/access_token", data=data).text
        access_token = res.split("&")[0].split("=")[1]
        res = requests.get("https://api.github.com/user", headers={"Authorization": f"token {access_token}"})
        return res.json()
