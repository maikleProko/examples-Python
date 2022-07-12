from flask import request
from flask_restful import Resource
from db.api import tg_add_user, tg_get_user_from_chat_id, tg_delete_user


class TGUsers(Resource):

    # get name from chat id
    def get(self):
        chat_id = request.args.get('tg_chat_id')
        user = tg_get_user_from_chat_id(int(chat_id))
        if user:
            return user['tg_github_name']
        return None

    # set name from chat id
    def post(self):
        # need header: Content-type: application/json
        data = request.get_json()
        tg_add_user({"tg_chat_id": data["tg_chat_id"], "tg_github_name": data["tg_github_name"]})

    # delete user from chat id
    def delete(self):
        # need header: Content-type: application/json
        data: dict = request.get_json()
        chat_id: str = data["tg_chat_id"]
        tg_delete_user(chat_id)
