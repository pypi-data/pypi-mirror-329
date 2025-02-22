from __future__ import annotations

import logging
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import (
    AliasChoices,
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    ValidationError,
    field_validator,
    model_validator,
)


class JobSysType(Enum):
    blocking = 'blocking'
    slurm = 'slurm'
    slurmclaix2023 = 'claix2023'


_LOG_LEVELS  = {
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }


class LogLevel(Enum):
    debug = 'debug'
    info = 'info'
    warning = 'warning'
    error = 'error'

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value

    def as_int(self) -> int:
        return _LOG_LEVELS[self.value]



class WarnOnExtraFields(BaseModel):
    """Mixin class that prints a warning if the model has extra fields.

    model_config['extra'] is set to 'allow', but the fields will be removed
    during validation.

    .. note::

        When inheriting this class and overriding the model_config, make sure
        to set `extra='allow'`
    """

    model_config = ConfigDict(extra='allow')

    @model_validator(mode='after')
    def __warn_on_extra_fields(self):
        logger = logging.getLogger(__name__)

        if self.model_extra:
            # create set to safely iterate over while deleting items
            extra = set(self.model_extra.keys())
            for e in extra:
                logger.warning(f'Additional field {e} will be ignored.')
                delattr(self, e)

        return self


# separate model for better separation of concerns -> JobSystem class only
# needs to know about the jobsystem and its options not ConfigBase
class JobSysConfig(BaseModel):
    """configuration for creating a job system"""

    jobsystem: JobSysType = JobSysType.slurm
    slurm_account: Optional[str] = None
    sbatch_cmd: str = 'sbatch'
    shell_exec: Path|None = None


class CmdArgsBase(WarnOnExtraFields, BaseModel):
    """combines all options that can be set via command line arguments"""

    workspace: Path
    wait: bool = False
    max_autosubmit: PositiveInt = 25
    config: Path|None = None
    log_level: LogLevel =  Field(default=LogLevel.info,
                                 validation_alias=AliasChoices('log_level',
                                                                'loglevel'))
    log_file: Path = Path('LOG')
    jobsystem: JobSysType = JobSysType.slurm
    slurm_account: Optional[str] = None
    sbatch_cmd: str = 'sbatch'

    @field_validator('workspace')
    @classmethod
    def check_workspace_is_dir_if_exists(cls, v: Path) -> Path:
        if v.exists() and not v.is_dir():
            raise ValidationError(f'Workspace "{str(v)}" must be a directory')

        return v.resolve()

class ConfigBase(WarnOnExtraFields, BaseModel):

    cmd: CmdArgsBase
    python_exec: Path = Path(sys.executable)
    shell_exec: Path|None = None

    @property
    def job_sys_config(self) -> JobSysConfig:
        return JobSysConfig(jobsystem=self.cmd.jobsystem,
                            slurm_account=self.cmd.slurm_account,
                            sbatch_cmd=self.cmd.sbatch_cmd,
                            shell_exec=self.shell_exec)

