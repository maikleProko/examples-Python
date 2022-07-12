import pytest
from src.utils.path_manager import PathManager


@pytest.mark.parametrize(
    "owner, repo",
    [
        ('sttie', 'slang'),
        ('duckietown', 'template-ros-core'),
    ],
)
def test_path_manager(owner, repo):
    path_manager = PathManager(f"https://github.com/{owner}/{repo}.git")

    assert path_manager.name == owner
    assert path_manager.repo_name == repo
    assert str(path_manager.get_path()) == f"/home/{owner}/{repo}"

    # with pytest.raises(OSError):
    #     _ = path_manager.get_log_path()

    # with pytest.raises(OSError):
    #     _ = path_manager.get_solution_run_file_path()

    # with pytest.raises(OSError):
    #     _ = path_manager.get_solution_build_file_path()
