"""
Import
---
``` python
import (
    get_git_repos,
    get_repo_contents,
    get_repo_content,
    get_git_repo
)
```
---

Description
---
A Python package to interact with GitHub API and get repository contents.

"""


from github import Github
from github.Repository import Repository
from github.ContentFile import ContentFile
from github.GithubObject import NotSet

from typing import List, Dict, Optional


def get_git_repos(app: Github, user_id: Optional[str] = NotSet) -> Dict[str, Repository]:
    """
    If your app is logged in, use it without user_id to keep the authority.
    """
    user = app.get_user(user_id)

    repos = {}

    for repo in user.get_repos():
        repos[repo.name] = repo

    return repos

def get_git_repo(repo_name:str, git_token:str=None)->Repository:
    """
    Args:
        repo_name: full name of the repository, e.g., "username/repo_name"
        git_token: github token. It is required if the repository is private
        
    Returns:
		Repository: github repository object
    """

    g = Github(
        login_or_token=git_token,
	)

    git_repo = g.get_repo(repo_name)
    return git_repo

def get_repo_contents(repo: Repository, dir: str) -> List[ContentFile]:

    contents: List[ContentFile] = repo.get_contents(dir)
    file_contents: List[ContentFile] = []

    while contents:
        file_content: ContentFile = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file_contents.append(file_content)

    return file_contents


def get_repo_content(repo: Repository, path: str) -> ContentFile:
    content: List[ContentFile] = repo.get_contents(path)

    return content
