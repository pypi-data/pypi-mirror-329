from contextlib import AbstractContextManager
import json
from chemtrayzer.engine.config import JobSysConfig
from chemtrayzer.engine.investigation import InvestigationContext
from chemtrayzer.engine.jobsystem import create_jobsystem


from pathlib import Path
from typing import Any


class Workspace:
    """ChemTraYzer workspace containing investigations, job directory, etc.

    This class is responsible for setting up the workspace, creating the
    necessary directories, and providing access to the investigations and jobs
    via the InvestigationContext
    """

    _INVESTIGATIONS_FILE = 'investigations.pickle'
    '''name of the file that is created in the workspace which contains
    the serialized investigations'''
    _JOB_DIR = 'jobs'
    '''subdirectory of workspace containing all jobs submitted by the
    investigations'''
    _CONFIG_DIR = 'config'

    def __init__(self, path: Path|str) -> None:
        self._path = Path(path)

        self._ensure_exits(self._path)
        self._ensure_exits(self._path/self._CONFIG_DIR)

    @property
    def path(self) -> Path:
        '''path to the workspace directory'''
        return self._path

    @staticmethod
    def _ensure_exits(path: Path):
        '''create a directory, if it does not exist

        :raise: ValueError if path exists, but is not a directory
        '''
        if path.exists():
            if not path.is_dir():
                raise ValueError(f'{path} is not a directory')
        else:
            path.mkdir(parents=True, exist_ok=True)

    def save_config(self, name, config: dict[str, Any]):
        """
        store a set of configuration values in the workspace under "name"

        :param name: recommended to use __name__ of the module
        :param config: configuration values to store (must be JSON
                       serializable)
        """
        with open(self._path/self._CONFIG_DIR/name, 'w',
                  encoding='utf-8') as f:
            json.dump(config, f, default=str)

    def load_config(self, name) -> dict[str, Any]:
        """
        load a set of configuration values from the workspace under "name"

        :param name: recommended to use __name__ of the module
        :return: configuration values or an empty dictionary, if no
                 configuration is stored
        """
        try:
            with open(self._path/self._CONFIG_DIR/name, 'r',
                      encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def is_empty(self) -> bool:
        '''check if the workspace is empty

        :return: True, if the workspace is empty, False otherwise
        :raise: NotADirectoryError if the workspace is not a directory
        '''

        try:
            next(self.path.iterdir())

            return False
        except StopIteration:
            return True    # empty directory
        except OSError as err:
            raise NotADirectoryError('Workspace is not a directory'
                                     ) from err

    def contains_inves_file(self) -> bool:
        '''
        :return: True, if the workspace contains a pickle investigation file
        :raise: NotADirectoryError, if the workspace is not a directory
        '''
        ws = self.path

        if self.is_empty():
            return False
        else:
            return (ws/self._INVESTIGATIONS_FILE).exists()

    def create_inves_context(
            self,
            context_mgrs: dict[str, AbstractContextManager]|None = None,
            job_sys_config: JobSysConfig|None = None
        ) -> InvestigationContext:
        '''create an investigation context for the workspace'''
        if context_mgrs is None:
            context_mgrs = {}

        jobsys = create_jobsystem(self._path/self._JOB_DIR,
                                  job_sys_config)
        return InvestigationContext(
                    path=self._path/self._INVESTIGATIONS_FILE,
                    jobsystem=jobsys,
                    context_mgrs=context_mgrs)