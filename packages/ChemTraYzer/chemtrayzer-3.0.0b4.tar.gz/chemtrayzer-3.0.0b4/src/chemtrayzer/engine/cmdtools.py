"""
Contains classes/functions used with the command line interface of this
package.
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable
from contextlib import AbstractContextManager
import dataclasses
import logging
import os
import sys
import traceback
import typing
import enum
from abc import ABC, abstractmethod
from argparse import ArgumentError, ArgumentParser, Namespace
from datetime import timedelta
from pathlib import Path
from types import UnionType
from typing import (
    Any,
    Generic,
    Optional,
    TypeVar,
    Union,
    get_origin,
)
from collections.abc import Mapping

import chemtrayzer
from chemtrayzer.engine._workspace import Workspace
from chemtrayzer.engine.config import CmdArgsBase, ConfigBase, LogLevel
import numpy as np
from numpy.typing import ArrayLike
from pydantic import RootModel, ValidationError

if sys.version_info[:2] < (3, 11):
    import tomli as tomllib
else:
    import tomllib  # added in 3.11

from chemtrayzer.engine.errors import ProgrammingError
from chemtrayzer.engine.investigation import (
    all_investigations_waiting,
    investigation_zero_finished,
    Investigation,
    InvestigationContext,
)
from chemtrayzer.engine.jobsystem import BlockingJobSystem, PythonScriptJob


class UserError(Exception):
    """base exception meant to be used, when the user can fix the error

    Inherit from this class to indicate that the exception should be considered
    a message to the user and not, e.g., a programming error/bug. The message
    should be a bit more verbose and aimed at the user."""


class IllegalCmdArgsError(UserError):
    """raised when the check of the command line arguments fails."""


class IllegalConfigError(UserError):
    """raised when the config file is not valid"""


class ConfigLoaderError(UserError):
    """raised when the config file could not be loaded"""


class WorkspaceNotEmptyError(UserError):
    """raised when the workspace is not empty, but does not contain an
    investigation file either"""


def _load_toml(path: Path | str) -> dict:
    path = Path(path)

    try:
        with open(path, "rb") as fp:
            config = tomllib.load(fp)
    except FileNotFoundError as err:
        raise ConfigLoaderError(f'Could not find config file "{path}"'
                                ) from err
    except tomllib.TOMLDecodeError as err:
        raise ConfigLoaderError("Error reading toml file: " f'"{path}": {err}'
                                ) from err

    return config


InvesT = TypeVar("InvesT", bound=Investigation)
"""investigation type"""
ConfigT = TypeVar("ConfigT", bound=ConfigBase)
"""type of the configuration that is passed to create_investigation(), etc."""


class CommandLineInterface(Generic[InvesT, ConfigT], ABC):
    """
    Helper class to create a command line interface that starts a main
    investigation. This class defines what the "main" investigation looks like.
    It is used by the main.py script.

    It is supposed to be run in a directory called workspace where it first
    checks if there are already investigations in this workspace. If not, a new
    main investigation is created and submitted. If there are already
    investigations in this workspace, the jobsystem is checked for new jobs.

    :param script: script to execute when all jobs are done in the "restart
                   strategy"
    :param debug_mode: if False, exceptions will be caught, logged, and a
                       user-friendly error message is shown. If True, uncaught
                       exceptions will be passed up the callstack.
    :param prog: prog argument passed to the argument parser (used in help
                 messages shown to user)
    :param start_cmd: Command that should be used to create the main
                      investigation and submit it. Has to be called once, then,
                      "resume" should be used to continue.
    """

    DESCRIPTION = ""
    """Text shown before the help texts of the arguments & options"""

    # since evaluating generic types at runtime is not fully worked out yet,
    # we have to go the old way of storing the class in a variable
    CONFIG_MODEL: type[ConfigT] = ConfigBase
    """data model for configuration"""

    _CHANGEABLE_ARGS = {'workspace', 'wait', 'max_autosubmit', 'log_level',
                        'log_file', 'config'}
    """command line arguments that can be changed between calls"""

    def __init__(
        self,
        script: Union[os.PathLike, str],
        debug_mode: bool = False,
        prog: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.script = script
        self.__debug_mode = debug_mode
        # used for raising error in start():
        self.__init_called = True

        self.__parser = self.__create_parser(prog=prog)

    def get_context_managers(self,
                             config: ConfigT
                             ) -> dict[str, AbstractContextManager]:
        """can be overridden to supply context managers for the investigation

        .. note::

            This method will be called on every execution of the program, thus,
            it may be called multiple times, if the program is resumed after
            waiting for a job to finish. The contents of the config file and
            the command line arguments may change between calls, if the user
            passes different arguments or changes the config file.

        :param config: Contents of the loaded configuration file. If the config
                        file is a python file, this is the module object. If
                        the config file is a TOML file, this is a dictionary.
        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        """
        return {}

    @abstractmethod
    def create_investigation(
        self, context: InvestigationContext, config: ConfigT
    ) -> InvesT:
        """This method is called, when no investigation has been submitted yet.
        It should create and return the main investigation object.

        .. note::

            This method is called only once per workspace. If the program is
            resumed after waiting for jobs to finish, this method is not
            called.

        :param config: Contents of the loaded configuration file. If the config
                        file is a python file, this is the module object. If
                        the config file is a TOML file, this is a dictionary.
        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        """

    def postprocessing(self, inves: InvesT, config: ConfigT):
        """can be overridden to deal with the investion after it is finished,
        e.g. for printing results, etc.

        .. note::

            The program may be restarted after waiting on a job to finish. If
            the user changes the configuration file or command line arguments,
            they may be different from what was used when setting up the
            investigation!

        :param cmd_args: command line arguments including the first
                         argument which contains the workspace
        """

    def __add_default_cmd_args(self, parser: ArgumentParser):
        """
        Add arguments that are allowed to change between calls

        .. note::

            This method will be called on every execution of the program, thus,
            it may be called multiple times, if the program is resumed after
            waiting for a job to finish.
        """
        parser.add_argument(
            "workspace",
            help="workspace directory in which the data is stored.",
            metavar="WORKSPACE",)
        wait_group = parser.add_mutually_exclusive_group()
        wait_group.add_argument(
            "--restart",
            "--no-wait",
            action="store_false",
            dest="wait",
            default=None,
            help="do not keep the Python process alive and restart this script"
            " once all jobs are finished. [default]",)
        wait_group.add_argument(
            "--wait",
            "--no-restart",
            action="store_true",
            default=None,  # store_true sets default value False. Since we want
                           # to use the default value from config.CmdArgsBase,
                           # we need to set it to None
            dest="wait",
            help="keep the Python process alive and check for finished jobs",)
        parser.add_argument(
            "--max_autosubmit",
            dest="max_autosubmit",
            type=int,
            help='number of times this script should be restarted, if --wait '
                 'is not set. [default: '
                f'{CmdArgsBase.model_fields["max_autosubmit"].default}]',
            metavar="N_CALLS",)
        parser.add_argument(
            "--loglevel",
            "--log-level",
            dest="log_level",
            help='Set the logging level. Choices are: "'
            + '", "'.join(str(lvl) for lvl in LogLevel)
            + '". '
            f'[default: {CmdArgsBase.model_fields["log_level"].default}]',
            choices=tuple(str(lvl) for lvl in LogLevel),)
        parser.add_argument(
            "-l",
            "--log",
            dest="log_file",
            help=f'path to the LOG_FILE. [default: '
                 f'{CmdArgsBase.model_fields["log_file"].default}]',)

        parser.add_argument(
            "--jobsystem",
            # default is set in engine.config.JobSysConfig class
            help="Name of the job system to use. [default: slurm]",
            action="store",
            type=str,
            choices=("blocking", "slurm", "claix2023"),
            dest="jobsystem",)
        slurm_args = parser.add_argument_group(
            title="SLURM options", description="Options for SLURM Workload"
                                               " Manager")
        parser.add_argument(
            "--config",
            dest="config",
            help="configuration file, e.g., config.toml" "[default: "
                 "%(default)s]",
            metavar="CONFIG_FILE",)
        slurm_args.add_argument(
            "--sbatch",
            dest="sbatch_cmd",
            help="SLURM's sbatch command. [default: %(default)s]",
            metavar="CMD",
            default="sbatch",)
        slurm_args.add_argument(
            "--account",
            dest="slurm_account",
            help="SLURM account that should be used",
            metavar="ACCOUNT",)

    def add_cmd_args(self, parser: ArgumentParser):
        """can be overridden to add additional command line arguments

        .. note::

            Do not add any default values here. They should be added in the
            ConfigBase class. Otherwise, default values defined here will
            always override values read from the config file.
        """

    def start(self, argv: Optional[list[str]] = None):
        """set up the command line interface and run the investigations

        :param argv: alternative command line arguments. If None, the arguments
                     from sys.argv are used. This is only used for testing.
        """
        if not self.__debug_mode:
            self.__handle_errors(self.__start, argv)
        else:
            return self.__start(argv)

    def __start(self, argv: list[str] | None):
        if hasattr(self, "__init_called"):
            # simplify debugging by printing error message for this common
            # error
            raise ProgrammingError(
                "super().__init__() was not called in the "
                "CommandLineInterface child class")

        argv = sys.argv if argv is None else argv
        args = self.__parse_args(argv[1:])

        config, is_resuming = self.__load_and_validate_config(args)

        # set up logging as early as possible (errors before this can
        # unfortunately not be redirected to the correct file)
        logging.basicConfig(
            filename=config.cmd.log_file,
            format="%(levelname)s:%(message)s",
            level=config.cmd.log_level.as_int(),
            # if in debug mode, we may not want to create a log file but allow
            # logging to console only; during normal run -> force this config
            force=not self.__debug_mode)

        workspace = Workspace(config.cmd.workspace)
        context = workspace.create_inves_context(
            self.get_context_managers(config), config.job_sys_config)

        with context:
            if context.inves_mgr.n_investigations == 0 and is_resuming:
                raise UserError(
                    "An existing workspace directory was found, but it does "
                    "not contain any investigations. The workspace could "
                    "be corrupted."
                )


            if context.inves_mgr.n_investigations == 0 and is_resuming:
                raise UserError(
                    "An existing workspace directory was found, but it does "
                    "not contain any investigations. The workspace could "
                    "be corrupted."
                )

            if not is_resuming:  # create investigation only once
                logging.info('ChemTraYzer %s',
                             chemtrayzer.__version__)
                # create and submit the main investigation (with id 0)
                self.__submit_inves(context, config)

            if config.cmd.wait or isinstance(context.jobsystem,
                                             BlockingJobSystem):
                context.runner.run(until=investigation_zero_finished)

            else:
                context.runner.run(until=all_investigations_waiting)

                if not investigation_zero_finished(context):
                    self.__schedule_restart(context, config, argv)

            if investigation_zero_finished(context):
                logging.info("Main investigation is finished.")
                self.__postprocessing(context, config)

    def __parse_args(self, argv) -> Namespace:
        """parse the command line, check the arguments and return them

        :raise: IllegalCmdArgsError if the check fails"""
        parser = self.__parser

        try:
            args = parser.parse_args(argv)
        except argparse.ArgumentError as err:
            raise IllegalCmdArgsError(
                f"Could not parse command line arguments: " f"{str(err)}"
            ) from err

        return args

    def __create_parser(self, prog) -> ArgumentParser:
        parser = ArgumentParser(prog=prog, description=self.DESCRIPTION)
        try:
            self.__add_default_cmd_args(parser)
            self.add_cmd_args(parser)
        except argparse.ArgumentError as err:
            raise ProgrammingError(
                "Could not add command line argument: " f"{str(err)}"
            ) from err

        return parser

    def __load_and_validate_config(self, args: Namespace
                                   ) -> tuple[ConfigT, bool]:
        CONFIG_POS = "chemtrayzer.engine.cmdtools"
        args_dict = vars(args)
        # remove values that were not passed to the command line
        args_dict = {k: v for k, v in args_dict.items() if v is not None}

        ### load config toml file ###
        if 'config' in args_dict:
            config_dict = _load_toml(args_dict['config'])
        else:
            config_path = Path('config.toml')

            if config_path.exists():
                config_dict = _load_toml(config_path)
            else:
                logging.warning('No config file supplied. "%s" Could'
                                ' not be found.',
                                str(config_path))
                config_dict = {}

        if "cmd" not in config_dict:
            config_dict["cmd"] = {}

        # command line arguments have higher precendence than config file
        try:
            config_dict["cmd"].update(args_dict)
        except AttributeError:  # happens, e.g., if cmd = 1 in config file
            raise IllegalConfigError('"cmd" must be a section in the config '
                                      "file")

        ### update values from workspace ###
        workspace = Workspace(args_dict["workspace"])
        ws_config_dict = workspace.load_config(CONFIG_POS)

        is_resuming = False
        if ws_config_dict != {}:
            is_resuming = True
            update = set(config_dict['cmd'].keys()) & self._CHANGEABLE_ARGS
            ignore = set(config_dict['cmd'].keys()) - self._CHANGEABLE_ARGS
            ignore = {f"cmd.{key}" for key in ignore}
            ignore |= set(config_dict.keys()) - {'cmd'}

            if ignore:
                logging.warning(
                    "Existing configuration found in workspace. The following"
                    " settings will be ignored: %s", ', '.join(ignore))

            ws_config_dict['cmd'].update({k: v
                                        for k, v in config_dict['cmd'].items()
                                        if k in update})

            config_dict = ws_config_dict

        ### validate ###
        try:
            config = self.CONFIG_MODEL(**config_dict)

            if isinstance(config, RootModel):
                config = config.root

            # save configuration for resuming
            workspace.save_config(CONFIG_POS, config_dict)

        except ValidationError as err:
            err_msg = self._format_pydantic_error(err)

            raise IllegalConfigError(err_msg)

        return config, is_resuming

    @classmethod
    def _format_pydantic_error(cls, err: ValidationError) -> str:
        """Format a pydantic ValidationError into a string that can be shown
        to the user"""
        err_msg = ""
        for pyderr in err.errors():
            # Since loc also includes discriminator names, providing the
            # full path could lead to more confusion than help -> only last
            #  entry
            if pyderr['loc']:
                if (isinstance(pyderr['loc'][-1], int)
                        and len(pyderr['loc'])>=2): # most likely list entry
                    err_msg += (f"{pyderr['loc'][-2]}[{pyderr['loc'][-1]}]:"
                               f" {pyderr['msg']}\n")
                else:
                    err_msg += f"{pyderr['loc'][-1]}: {pyderr['msg']}\n"
            else:  # root of model
                err_msg += f"{pyderr['msg']}\n"

        return err_msg

    def __handle_errors(self, func, *args, **kwargs):
        """decorator that catches all exceptions

        :param func: function to decorate
        :param args: arguments for the function
        :param kwargs: keyword arguments for the function"""
        try:
            return func(*args, **kwargs)
        except (ArgumentError, UserError) as err:
            # For the kind of errors that are meant to be shown to the
            # user  we usually do not need the stacktrace
            logging.debug("User error:\n"
                          + "".join(traceback.format_exception(err)))

            self.__error(msg=str(err), exit_code=1)
        except Exception as err:  # pylint: disable=broad-except
            # All non-user errors should have been caught before, so
            # these errors are unexpected and should be logged properly
            logging.error(
                "A fatal error occurred:\n"
                + "".join(traceback.format_exception(err)))
            self.__error(
                msg=f"A fatal error occurred: {str(err)}\nCheck the log"
                " for more information.",
                exit_code=1,)

    def __error(self, msg: str, print_usage: bool = True, exit_code: int = 1):
        """print an error message and exit the program"""
        if print_usage:
            msg = self.__parser.format_usage() + "\n" + msg

        sys.stderr.write(msg + "\n")
        sys.exit(exit_code)

    def __submit_inves(self, opened_context: InvestigationContext,
                       config: ConfigT):
        """create and submit the main investigation

        :raise: ProgrammingError if no investigation is found in the context
        """
        inves = self.create_investigation(opened_context, config)

        inves_id = opened_context.inves_mgr.submit(inves)

        # save the main investigation, so that it can be resumed on error
        opened_context.save_checkpoint()

        logging.info("Submitted main investigation with id %d", inves_id)
        assert inves_id == 0

    def __schedule_restart(
        self,
        opened_context: InvestigationContext,
        config: ConfigT,
        argv: list[str]):
        jobsystem = opened_context.jobsystem
        workspace = config.cmd.workspace

        if self.__count_calls(workspace) < config.cmd.max_autosubmit:
            cwd = Path(os.getcwd()).resolve()

            logging.debug(
                "The program is scheduled for restart with the "
                "following script cmd: %s %s in %s",
                self.script,
                " ".join(argv),
                str(cwd),)

            job = PythonScriptJob(
                script=self.script,
                arguments=argv,
                working_dir=cwd,
                python=config.python_exec,
                runtime=timedelta(hours=5),)

            running_job_ids = jobsystem._get_running_ids()

            # submit this script as a job and execute it after all current
            # jobs are done
            jobsystem.submit(job, wait_for=running_job_ids)
        else:
            logging.info(
                "The investigation is not finished, but the limit"
                " of automatic restarts (%d) was "
                "reached. If you would like to continue, increase "
                "the limit with the --max_autosubmit option.",
                config.cmd.max_autosubmit,)

    def __count_calls(self, workspace: Path) -> int:
        """keeps track how often this function was called by using a counter in
        a file in the workspace. If this function is called once per execution
        of this script, it can be used to count how often the script is
        executed with the workspace."""

        counter_file = workspace / "__counter__"

        if counter_file.exists():
            with open(counter_file, encoding="utf-8") as fp:
                counter = int(fp.read())

        else:
            counter = 0

        with open(counter_file, "w", encoding="utf-8") as fp:
            fp.write(str(counter + 1))

        return counter

    def __postprocessing(self, opened_context: InvestigationContext,
                         config: ConfigT):
        inves: InvesT = opened_context.inves_mgr.get_investigation_by_id(0)
        self.postprocessing(inves, config)



class TypeConversionError(Exception):
    """raised when a value could not be converted to the expected type"""


_T = TypeVar("_T", contravariant=True)


def dict2dataclass(
    dict_obj: dict,
    cls: type[_T],
    aliases: Mapping[str, str | Mapping[str, Any]] | None = None,
) -> _T:
    """Converts a dictionary to a dataclass instance.

    The keys of dict_obj must match the field names of cls. Additional values
    whose keys do not match any field of cls are ignored. If a mandatory field
    is not found in dict_obj, a KeyError is raised. Non-init fields are set
    after the initialization of the object, if they are present in dict_obj,
    otherwise, they are not set, but could still be set by __post_init__() of
    the dataclass.
    If the type of a field is another dataclass and the corresponding value in
    dict_obj is not already of that type, the function will recurse and
    expect the corresponding value in the dict to be another dict.

    This function expects each field to have a single type. Union types are not
    supported.

    .. code::python

        @dataclass
        class A:
            a: int
            b: int

        @dataclass
        class B:
            d: A
            c: int

        @dataclass
        class APlus(B):
            '''A with an additional field'''
            e: int

        dict_obj = {'z': 1, 'd': {'a': 2, 'B': 3}}

        b = dict2dataclass(
                dict_obj,
                B,
                # z -> c, d.B -> d.b, type(B.d) -> APlus
                aliases={'z':'c', 'd':{'B': 'b', '__type__': APlus}})

    :raise: TypeError if cls is not a dataclass
    :raise: TypeConversionError if a value in dict_obj does not match the type
            of the corresponding field in cls and cannot be cast. args will
            be (field_name, expected_type, actual_type)
    :raise: KeyError if a field is not found in dict_obj. args[0] will be the
            missing field name
    :raise: NotImplementedError, if a field has a Union type
    :param cls: dataclass, an instance of which is to be created
    :param dict_obj: dictionary with the same keys as the fields of cls
    :param aliases: mapping of aliases to field names. Aliases for nested
                    classes can be supplied as nested dict using the field name
                    as key.
    :return: instance of cls with data from dict_obj"""
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f"cls ({cls}) must be a dataclass")

    if aliases is not None:
        field_names = {f.name for f in dataclasses.fields(cls)}

        # copy dict before replacing aliases with field names to keep the
        # original dict unchanged
        new_dict = {}
        for k, v in dict_obj.items():
            # if k is a field name, aliases could contain an entry for it,
            # i.e., in the case that k refers to a nested field
            if k not in field_names:
                new_dict[aliases.get(k, k)] = v
            else:
                new_dict[k] = v
        # aliases for nested dicts (i.e. where key in alias is also a
        # field name and the value is an alias dict) are stored separately
        nested_aliases = {k: v for k, v in aliases.items() if k in field_names}

        dict_obj = new_dict
    else:
        nested_aliases = {}

    values = {}
    non_init_values = {}

    # field.type will be a string in the future (or with from __future__ import
    # annotations). So we use get_type_hints to resolve the types
    types = typing.get_type_hints(cls)

    for field in dataclasses.fields(cls):
        field: dataclasses.Field

        if field.name not in dict_obj:
            if (
                field.default != dataclasses.MISSING
                or field.default_factory != dataclasses.MISSING
                or not field.init):
                # field has a default value
                continue
            else:
                raise KeyError(field.name)

        val = dict_obj[field.name]
        field_type = types[field.name]

        # since np.typing.ArrayLike is a Union, it needs special treatment
        field_type = np.ndarray if field_type == ArrayLike else field_type

        if isinstance(field_type, UnionType):
            raise NotImplementedError("Union types are not supported")

        # isinstance not supported for `list[int]`, so we convert it to `list`
        origin = get_origin(field_type)
        if origin is not None:  # no square brackets also means no origin
            field_type = origin

        # allow conversion of iterables (necessary, if the type hints are
        # very strict)
        if isinstance(val, Iterable) and not isinstance(val, str):
            if field_type in (list, tuple, set):
                val = field_type(val)
            if field_type == np.ndarray:
                val = np.array(val)  # returns np.ndarray
        # also allow conversion of numeric types
        elif isinstance(val, (int, float)) and field_type is complex:
            val = complex(val)
        elif isinstance(val, int) and field_type is float:
            val = float(val)
        elif isinstance(val, float) and field_type is int:
            if val.is_integer():
                val = int(val)
        elif isinstance(val, str) and issubclass(field_type, enum.Enum):
            val = getattr(field_type, val)

        # and convert strings to Path objects
        elif isinstance(val, str) and field_type == Path:
            val = Path(val)

        if not isinstance(val, field_type):
            # recursion
            if isinstance(val, dict) and dataclasses.is_dataclass(field_type):
                inner_aliases = nested_aliases.get(field.name, None)
                if inner_aliases is not None:
                    field_type = inner_aliases.get("__type__", field_type)

                val = dict2dataclass(val, field_type, aliases=inner_aliases)
            else:
                # choose ValueError instead of type error to distinguish from
                # case above which is most likely a programming error whereas
                # this can also be a user error.
                raise TypeConversionError(field.name, field_type, type(val))

        if field.init:
            values[field.name] = val
        else:
            non_init_values[field.name] = val

    # create dataclass object
    obj = cls(**values)

    # fields where init=False need to be set after initialization
    for name, value in non_init_values.items():
        setattr(obj, name, value)

    return obj
