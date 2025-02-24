import pytest
from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from crimson.github_app.getter import get_git_repos, get_repo_contents, get_repo_content
import os

try:
    from secret import set_env
    set_env()
except Exception as error:
    error
    pass


@pytest.fixture
def github_app() -> Github:
    token = os.environ.get('GIT_APP_TOKEN')
    if token:
        return Github(token)
    else:
        raise ValueError("GIT_APP_TOKEN not found in environment variables")


@pytest.fixture
def test_repo(github_app):
    repos = get_git_repos(github_app)
    return repos["github-app-lab"]


def test_get_git_repos(github_app):
    repos = get_git_repos(github_app)
    assert isinstance(repos, dict)
    assert len(repos.keys()) != 0
    assert "github-app-lab" in repos
    assert isinstance(repos["github-app-lab"], Repository)


def test_get_git_repos_with_user_id(github_app):
    repos = get_git_repos(github_app, "crimson206")
    assert isinstance(repos, dict)
    assert len(repos.keys()) != 0
    # github-app-lab is a private repo
    assert "github-app-lab" not in repos.keys()


def test_get_repo_contents(test_repo):
    contents = get_repo_contents(test_repo, "/")
    assert isinstance(contents, list)
    assert all(isinstance(content, ContentFile) for content in contents)


def test_get_repo_content(test_repo):
    contents = get_repo_contents(test_repo, "/")
    if contents:
        first_file = contents[0]
        assert isinstance(first_file.path, str)
        content = get_repo_content(test_repo, first_file.path)
        assert isinstance(content, ContentFile)
        assert content.path == first_file.path
