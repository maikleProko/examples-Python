from flask import request
from flask_restful import Resource
from utils.path_manager import PathManager

RUN_LOG = 1
BUILD_LOG = 0


class Solutions(Resource):

    def get(self):
        # hostname: str = request.args.get("hostname")
        url: str = request.args.get("url")
        type_of_logs: int = request.args.get("category", 0, type=int)
        path_manager: PathManager = PathManager(url=url, branch="")
        print(type_of_logs == RUN_LOG)
        if type_of_logs == RUN_LOG:
            with open(path_manager.get_solution_run_file_path()) as file:
                return file.read()
        elif type_of_logs == BUILD_LOG:
            with open(path_manager.get_solution_build_file_path()) as file:
                return file.read()
        else:
            return ""
