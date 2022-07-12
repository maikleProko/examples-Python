from flask import request
from flask_restful import Resource


class Joystick(Resource):

    def get(self) -> str:
        hostname: str = request.args.get("hostname")
        print("GET JOYSTICK")
        return hostname

    def post(self) -> str:
        # need header: Content-type: application/json
        data: dict = request.get_json()
        hostname: str = data["hostname"]
        state: dict = data["state"]
        print(state)
        return f"duck {hostname} state {state}"

    def delete(self) -> str:
        data: dict = request.get_json()
        hostname: str = data["hostname"]
        print("DELETE JOYSTICK")
        return hostname  # add close joystick
