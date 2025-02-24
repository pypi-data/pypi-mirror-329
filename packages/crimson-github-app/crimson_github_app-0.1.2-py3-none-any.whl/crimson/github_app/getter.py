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
    Get all repositories for a given user or the authenticated user.
    
    Args:
        app: Github instance with authentication
        user_id: Optional GitHub username. If not provided, gets repos for authenticated user
        
    Returns:
        Dict[str, Repository]: Dictionary mapping repository names to Repository objects
        
    Example:
        >>> g = Github(token)
        >>> repos = get_git_repos(g)  # Get authenticated user's repos
        >>> repos = get_git_repos(g, "octocat")  # Get specific user's repos
    """
    user = app.get_user(user_id)

    repos = {}

    for repo in user.get_repos():
        repos[repo.name] = repo

    return repos

def get_git_repo(repo_name:str, git_token:str=None)->Repository:
    """
    Get a GitHub repository object by its full name.
    
    Args:
        repo_name: Full name of the repository in format "username/repo_name"
        git_token: GitHub personal access token. Required for private repositories
        
    Returns:
        Repository: GitHub repository object
        
    Example:
        >>> repo = get_git_repo("octocat/Hello-World")
        >>> repo = get_git_repo("org/private-repo", "gh_token")
    """

    g = Github(
        login_or_token=git_token,
	)

    git_repo = g.get_repo(repo_name)
    return git_repo

def get_repo_contents(repo: Repository, dir: str) -> List[ContentFile]:
    """
    Recursively get all file contents from a directory in a repository.
    
    Args:
        repo: GitHub repository object
        dir: Directory path within the repository (e.g., "src" or "docs/api")
        
    Returns:
        List[ContentFile]: List of ContentFile objects representing all files in directory
        
    Example:
        >>> repo = get_git_repo("user/repo")
        >>> contents = get_repo_contents(repo, "src")
    """
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
    """
    Get content of a single file from a repository.
    
    Args:
        repo: GitHub repository object
        path: Path to the file within the repository
        
    Returns:
        ContentFile: ContentFile object representing the file
        
    Example:
        >>> repo = get_git_repo("user/repo")
        >>> content = get_repo_content(repo, "README.md")
        
    Raises:
        github.GithubException: If file doesn't exist
    """
    content: List[ContentFile] = repo.get_contents(path)

    return content
