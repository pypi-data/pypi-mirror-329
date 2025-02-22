import importlib.metadata
import json
import logging
from pathlib import Path
import rdkit

__all__ = ['core', 'engine','io','jobs','models','qm','reaction_sampling']

def _get_version() -> str:
    direct_url = (importlib.metadata.Distribution.from_name('chemtrayzer')
                  .read_text('direct_url.json'))
    direct_url = json.loads(direct_url)

    # direct_url must exists, if the package was installed from a url/path
    if direct_url is not None:
        # If the URL was a directory, dir_info must be present
        dir_info = direct_url.get('dir_info', {})
        is_editable = dir_info.get('editable', False)
    else:
        is_editable = False

    if not is_editable:
        return importlib.metadata.version('chemtrayzer')
    else:
        return _get_version_from_repo(direct_url['url'])

def _get_git_revision_hash(dir_path: str) -> str|None:
    import subprocess

    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                       encoding='utf-8',
                                       cwd=dir_path).strip()
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None     # git executable not found

def _get_version_from_repo(repo_path_uri: str) -> str:
    import sys
    if sys.version_info[:2] < (3, 11):
        import tomli as tomllib
    else:
        import tomllib  # added in 3.11
    from urllib.parse import unquote, urlparse

    repo_path = Path(unquote(urlparse(repo_path_uri).path))
    pyproject_toml = repo_path / 'pyproject.toml'

    with open(pyproject_toml, 'rb') as f:
        pyproject = tomllib.load(f)
        pyproject_version = pyproject['project']['version']

    git_hash =  _get_git_revision_hash(str(repo_path))

    if git_hash is not None:
        return f'{pyproject_version}+{git_hash}'
    else:
        return f'{pyproject_version}+dev'


__version__ =  _get_version()

logger = logging.getLogger("rdkit")
logger.propagate = True
# appending RDKit will help the user to distinguish what is coming from RDKit
logger.handlers[0].setFormatter(logging.Formatter('[RDKit]%(message)s'))
logger.setLevel(logging.DEBUG)  # everything will be forwarded by rdkit to
                                # the logger, and the logger can filter by
                                # setting loglevel
rdkit.rdBase.LogToPythonLogger()