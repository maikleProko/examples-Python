from dts.build import build_template_ros_core
from utils.path_manager import PathManager
from repos.download import download_repo
from flask_restful import Resource
from flask import request


class Build(Resource):
    def get(self) -> str:
        hostname = request.args.get('hostname', default='', type=str)
        repo_url = request.args.get('url', default='', type=str)
        branch = request.args.get('branch', default='master', type=str)
        path_manager = PathManager(repo_url, branch)
        download_repo(path_manager)
        build_template_ros_core(
            hostname=hostname,
            directory=path_manager.get_path(),
            log=path_manager.get_solution_build_file_path()
        )
        return "<h1>Solution was built!</h1>"
