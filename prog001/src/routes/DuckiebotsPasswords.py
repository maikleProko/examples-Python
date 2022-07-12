from flask import request
from flask_restful import Resource

from db.api import check_jwt

from utils.pass_generator import write_password_to_file, encode_password, create_primary_password
from pathlib import Path
from utils.docker_communicator import DockerCommunicator


class DuckiebotsPasswords(Resource):

    def post(self):
        if 'x-access-token' in request.headers:
            if check_jwt(request.headers['x-access-token']) != "admin":
                return None
        else:
            return None
        data: dict = request.get_json()
        hostname: str = data["hostname"]

        current_dir = Path.cwd()
        filename = current_dir / '..' / '..' / 'nginx' / '.htpasswd'
        write_password_to_file(filename, hostname, encode_password(hostname, create_primary_password()))

        dc = DockerCommunicator()
        flag_dc = dc.restart_nginx()

        if flag_dc == 0:
            return 201  # all is ok
        else:
            return 501  # cannot reload nginx
