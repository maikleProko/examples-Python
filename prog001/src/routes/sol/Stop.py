from dts.stop import hard_stop, soft_stop
from utils.constants import HARD_STOP, SOFT_STOP
from flask_restful import Resource
from flask import request


class Stop(Resource):
    def get(self) -> str:
        hostname = request.args.get('hostname', default='', type=str)
        category = request.args.get('category', 0, type=int)
        if category == SOFT_STOP:
            soft_stop(hostname)
        elif category == HARD_STOP:
            hard_stop(hostname)
        return "stopped"
