import re
from pathlib import Path

GITHUB_PATTERN = r"https:\/\/github\.com\/([\w-]+)\/(.+)\.git"
OWNER_REPO_GROUP = 1
REPO_NAME_GROUP = 2
RUN_LOG_FILE = "run.txt"
BUILD_LOG_FILE = "build.txt"


class PathManager:

    def __init__(self, url: str, branch: str = "master") -> None:
        self.url = url
        self.branch = branch
        self.info = re.search(GITHUB_PATTERN, url)

    @property
    def name(self) -> str:
        return self.info.group(OWNER_REPO_GROUP)

    @property
    def repo_name(self) -> str:
        return self.info.group(REPO_NAME_GROUP)

    def get_path(self) -> Path:
        return Path(f"/home/{self.name}/{self.repo_name}")

    def get_log_path(self) -> Path:
        path = Path(f"/home/logs/{self.name}/{self.repo_name}")
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def get_solution_run_file_path(self) -> Path:
        return Path.joinpath(self.get_log_path(), RUN_LOG_FILE)

    def get_solution_build_file_path(self) -> Path:
        return Path.joinpath(self.get_log_path(), BUILD_LOG_FILE)


if __name__ == '__main__':
    p = PathManager("https://github.com/OSLL/template-ros-core.git")
    print(p.name, p.repo_name, p.get_path())
