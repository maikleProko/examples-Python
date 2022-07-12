import base64
import os
from pathlib import Path
import subprocess
import shutil
from typing import List

import github.ContentFile
from github import Github
from github import GithubException
from github.Repository import Repository

from utils.path_manager import PathManager


def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha


def download_directory(repository: Repository, sha: str, folder: Path, path_in_repo=""):
    folder: str = str(folder.absolute())
    os.makedirs(folder, exist_ok=True)
    contents: List[github.ContentFile.ContentFile] = repository.get_dir_contents(path_in_repo, ref=sha)

    for content in contents:
        path_obj = os.path.join(folder, content.path)
        if content.type == 'dir':
            os.makedirs(path_obj, exist_ok=True)
            download_directory(repository, sha, Path(folder), content.path)
        else:
            try:
                path = content.path
                print(path)
                file_content = repository.get_contents(path, ref=sha)
                file_data = base64.b64decode(file_content.content)
                path = os.path.join(folder, *content.path.split("//")[:-1])
                if not os.path.exists(path):
                    os.makedirs(path)
                file_out = open(path_obj, "wb+")
                file_out.write(file_data)
                file_out.close()
            except (GithubException, IOError) as exc:
                print('Error processing %s: %s', content.path, exc)


def _download_repo(repo: str = "light5551/template-ros-core", branch: str = "v1", folder: Path = Path("./test")):
    g = Github(os.getenv('REACT_APP_GITHUB_REPO_TOKEN'))
    repository = g.get_repo(repo)
    sha = get_sha_for_tag(repository, branch)
    download_directory(repository, sha, folder)


def download_repo(path_manager: PathManager):
    print(f"Path: {path_manager.get_path().absolute()}")
    if os.path.exists(path_manager.get_path().absolute()):
        shutil.rmtree(path_manager.get_path().absolute())
    ret = subprocess.call("git clone -q -b {branch} --single-branch {repo} {local_path}".format(
        branch=path_manager.branch,
        repo=f"https://github.com/{path_manager.name}/{path_manager.repo_name}.git",
        local_path=path_manager.get_path().absolute()
    ).split())
    print(f"Status for repo {ret}")
    # _download_repo(repo=f"{path_manager.name}/{path_manager.repo_name}", https://github.com/OSLL/template-ros-core.git
    #               branch=path_manager.branch,
    #               folder=path_manager.get_path())


if __name__ == "__main__":
    url = "https://github.com/light5551/template-ros-core.git"
    # path, (name, repo_name) = path_solution_by_url(url)
    # _download_repo(folder=Path(f"/home/{os.getlogin()}/{name}/{repo_name}"))
