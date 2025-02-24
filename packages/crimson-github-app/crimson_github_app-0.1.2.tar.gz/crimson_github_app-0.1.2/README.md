# Crimson GitHub App

A Python package to easily download contents from GitHub repositories.

## Installation

```bash
pip install crimson-github-app
```

## Main Function

The package exposes one main function for downloading repository contents:

```python
from crimson.github_app import download_repo_contents

# Download repository contents
download_repo_contents(
    repo_name="username/repository",
    dir_in_repo="path/to/directory",
    output_dir="output",
    git_token=None
)
```

### Parameters

- `repo_name` (str): Full repository name in the format "username/repository"
- `dir_in_repo` (str): Directory path within the repository to download from
- `output_dir` (str, optional): Local directory to save files to. Defaults to "output"
- `git_token` (str, optional): GitHub token for private repositories. Required for private repos

### Example

```python
# Download public repository contents
download_repo_contents(
    "crimson206/my-project",
    "src/examples",
    output_dir="downloaded_files"
)

# Download private repository contents
download_repo_contents(
    "crimson206/private-repo",
    "docs",
    output_dir="local_docs",
    git_token="your_github_token"
)
```

## Requirements

- Python ≥ 3.9
- PyGithub

## License

MIT License
