from typing import Any, Dict
from flask import request
from flask_restful import Resource
from db.api import add_session, del_session, get_next_id, update_session_from_id, \
    get_session_from_id, get_user_data_from_JWT
from db.classes import DuckieBotSession


class DuckieBotSessions(Resource):
    # get session
    def get(self) -> Dict[str, Any]:
        session_id: int = request.args.get("id")
        session: Dict[str, Any] = get_session_from_id(session_id)
        if session:
            return session
        return None

    # add new session
    def post(self) -> [Dict[str, Any], int]:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        session_id: int = get_next_id()
        owner: str = data["owner"]
        hostname: str = data["hostname"]
        start_time: dict = data["start_time"]
        end_time: dict = data["end_time"]
        added_session: dict = add_session(DuckieBotSession(session_id, owner, hostname, start_time, end_time))
        if added_session:
            del added_session["_id"]
        return added_session, 201

    # edit session
    def put(self) -> int:
        # id and owner will not change
        print("entry")
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        session_id: int = data["id"]
        owner: str = data["owner"]
        hostname: str = data["hostname"]
        start_time: dict = data["start_time"]
        end_time: dict = data["end_time"]
        update_session_from_id(session_id, owner, hostname, start_time, end_time)
        return 201

    # delete session
    def delete(self) -> int:
        if 'x-access-token' in request.headers:
            if get_user_data_from_JWT(request.headers['x-access-token'])['role'] != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        session_id: int = data["id"]
        session = get_session_from_id(session_id)
        del_session(session)
        return 201
