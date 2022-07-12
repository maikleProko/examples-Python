import os
from importlib import import_module
from inspect import isclass

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from flask_socketio import SocketIO
from db.api import prepare_for_first_start

# FOR DEV - for http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
api = Api(app)

# find .py modules for import
file_names = []
for root, dirs, files in os.walk("./routes"):
    file_names += [os.path.join(root, name) for name in files if
                   name.find(".py") != -1 and
                   root.find("__pycache__") == -1 and
                   name.find("__init__.py") == -1]

# prepare module names for import
module_names = []
for mod in file_names:
    mod = mod.replace("/", ".")
    mod = mod.replace(".py", "")
    mod = mod.replace("..", "")
    module_names.append(mod)

# dynamic modules import
for name in module_names:
    module = import_module(name)
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)
        if isclass(attribute):
            # add the class to this package's variables
            globals()[attribute_name] = attribute

# connect resources
connect_list = []
for mod in file_names:
    mod = mod.replace("./routes", "")
    mod = mod.replace(".py", "")
    connect_list.append(mod)

for mod in connect_list:
    class_name = mod.split("/")[-1]
    path = mod.lower()
    api.add_resource(globals()[class_name], path)

# sockets part


@socketio.on('connected')
def handle_session_on(json):
    print(f"Client connected. Session id {request.sid}")


@socketio.on('disconnect')
def test_disconnect():
    print(f"Client disconnected. Session id {request.sid}")


@socketio.on('user on')
def handle_user_on(json):
    print(f"User {json['name']} on the site now. Session id {request.sid}")


@socketio.on('user off')
def handle_user_off(json):
    print(f"User {json['name']} left the site")


if __name__ == '__main__':
    prepare_for_first_start()
    socketio.run(app, debug=True, port=5000)
