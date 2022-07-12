import json
from collections import defaultdict

from flask import request
from flask_restful import Resource
from zeroconf import ServiceBrowser, Zeroconf


class DiscoverListener:
    services = defaultdict(dict)
    supported_services = [
        "DT::DASHBOARD",
    ]

    def __init__(self, args):
        self.args = args

    def process_service_name(self, name):
        name = name.replace("._duckietown._tcp.local.", "")
        service_parts = name.split("::")
        if len(service_parts) != 3 or service_parts[0] != "DT":
            return None, None
        name = "{}::{}".format(service_parts[0], service_parts[1])
        server = service_parts[2]
        return name, server

    def remove_service(self, zeroconf, type, name):
        name, server = self.process_service_name(name)
        if not name:
            return
        del self.services[name][server]

    def add_service(self, zeroconf, type, sname):
        name, server = self.process_service_name(sname)
        if not name:
            return
        try:
            info = zeroconf.get_service_info(type, sname)
        except RuntimeError:
            return
        if not info:
            return
        txt = json.loads(list(info.properties.keys())[0].decode("utf-8")) if len(info.properties) else dict()
        self.services[name][server] = {"port": info.port, "txt": txt}

    def update_service(self, *args, **kwargs):
        pass


class RobotStatus(Resource):

    def get(self):
        zeroconf = Zeroconf()
        listener = DiscoverListener(args=[])
        ServiceBrowser(zeroconf, "_duckietown._tcp.local.", listener)
        status = False
        hostname = request.args['name']
        if hostname in listener.services["DT::DASHBOARD"]:
            status = True
        return status
