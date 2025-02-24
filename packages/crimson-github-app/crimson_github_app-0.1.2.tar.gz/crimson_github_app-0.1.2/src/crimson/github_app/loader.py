"""
Import
---
``` python
import (
    save_contents_to_folder,
    download_repo_contents
)
```

Description
---
A Python package to interact with GitHub API and download repository contents.
"""


from github.ContentFile import ContentFile
import os
import base64
from typing import List
from crimson.github_app.getter import get_repo_contents, get_git_repo

def save_contents_to_folder(contents: List[ContentFile], output_dir: str):
    """
    Saves file contents retrieved from GitHub API to a local folder while preserving directory structure.
    
    Args:
        contents: List of ContentFile objects retrieved from GitHub API
        output_dir: Base directory path where files will be saved
        
    Example:
        >>> contents = get_repo_contents(repo, "src")
        >>> save_contents_to_folder(contents, "local_copy")
        
    Note:
        - Creates output directory and subdirectories if they don't exist
        - Handles base64 decoding of file contents from GitHub API
        - Prints success/failure messages for each file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for content in contents:
        file_path = os.path.join(output_dir, content.path)
        
        # Check and create directory where file will be saved
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        
        # Decode and save file contents
        try:
            # GitHub API provides base64 encoded content
            file_content = base64.b64decode(content.content)
            
            # Save file in binary mode
            with open(file_path, 'wb') as f:
                f.write(file_content)
                
            print(f"File saved successfully: {file_path}")
        except Exception as e:
            print(f"Failed to save file ({content.path}): {str(e)}")


def download_repo_contents(repo_name: str, dir_in_repo: str, output_dir: str="output", git_token: str=None):
    """
    Downloads files from a specific directory in a GitHub repository to a local folder.
    
    Args:
        repo_name: Repository name in format "username/repo_name"
        dir_in_repo: Path to the directory in the repository to download files from
        output_dir: Base directory path where files will be saved (default: "output")
        git_token: GitHub token required for private repositories
        
    Example:
        >>> download_repo_contents("octocat/Hello-World", "src", "local_copy")
        >>> download_repo_contents("org/private-repo", "docs", "local_docs", "gh_token")
        
    Note:
        - Downloads all files recursively from the specified directory
        - Maintains original directory structure
        - Creates output directories if they don't exist

    """
    # Create GitHub repository object
    repo = get_git_repo(repo_name, git_token)

    # Get list of files in the repository
    contents = get_repo_contents(repo, dir_in_repo)

    # Save files
    save_contents_to_folder(contents, output_dir)
