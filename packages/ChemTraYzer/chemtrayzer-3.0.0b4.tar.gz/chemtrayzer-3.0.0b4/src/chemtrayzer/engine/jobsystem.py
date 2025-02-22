from __future__ import annotations

import inspect
import json
import logging
import os
import pickle
import re
import shutil
import subprocess
import sys
from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Callable, Collection, Iterable, Mapping
from dataclasses import dataclass
from datetime import timedelta
from math import floor, log10
from pathlib import Path
from string import Template
from typing import ClassVar, Generic, Optional, Any

from chemtrayzer.engine.database import Database
from chemtrayzer.engine._event import Event, EventDispatcher
from chemtrayzer.engine._submittable import (
    FailedT,
    Failure,
    State,
    Submittable,
    Result,
    SuccessT,
)
from chemtrayzer.engine.config import JobSysConfig, JobSysType
from chemtrayzer.engine.database import DBOpenMode
from chemtrayzer.engine.errors import ProgrammingError


class NonzeroExitCodeFailure(Failure):
    """indicates that a job exited with a non-zero exit code"""

    def __init__(
        self,
        msg: Optional[str] = None,
        *,
        exit_code: int,
        causes=None,
        **kwargs,) -> None:
        self.exit_code = exit_code
        if msg is None:
            msg = f"Job exited with non-zero exit code {exit_code}"
        super().__init__(msg, causes=causes, **kwargs)


class JobAbortedFailure(Failure):
    """indicates that a job was aborted by the user or job system"""


class TimeoutFailure(JobAbortedFailure):
    """indicates that the job was aborted upon reaching its time limit"""


_JobState = State
"""deprecated. Provided for some backwards compatibility"""


class Version:
    """simple version class that allows comparisons

    format: <major>.<minor>.<patch>
    """

    def __init__(self, major: int, minor: int = 0, patch: int = 0) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def __gt__(self, other: Version) -> bool:
        if self.major > other.major:
            return True
        elif self.major == other.major:
            if self.minor > other.minor:
                return True
            elif self.minor == other.minor:
                if self.patch > other.patch:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __eq__(self, other: Version) -> bool:
        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch)

    def __ne__(self, other: Version) -> bool:
        return not self == other

    def __ge__(self, other: Version) -> bool:
        return self > other or self == other

    def __st__(self, other: Version) -> bool:
        return not (self > other or self == other)

    def __se__(self, other: Version) -> bool:
        return self < other or self == other


class Program(metaclass=ABCMeta):
    """
    Base class for representing external software. Objects of derived classes
    are typically passed to Job objects to provide additional information about
    platform specific configurations of each program.
    """

    def __init__(self, executable: str, version: Version = None) -> None:
        self.executable = executable
        self.version = version


@dataclass
class Memory:
    """memory needed for a computation job, i.e. submittable"""

    # provide string representations as interpreted by sbatch
    UNIT_KB: ClassVar[str] = "K"
    UNIT_MB: ClassVar[str] = "M"
    UNIT_GB: ClassVar[str] = "G"
    UNIT_TB: ClassVar[str] = "T"

    _coefficients: ClassVar[dict] = {
        UNIT_KB: 3,
        UNIT_MB: 6,
        UNIT_GB: 9,
        UNIT_TB: 12,
    }

    amount: int
    unit: str = UNIT_MB

    def __str__(self) -> str:
        return f"{self.amount}{self.unit}"

    def __eq__(self, other) -> bool:
        if type(other) is Memory:
            return self.amount_in_unit(Memory.UNIT_KB) == other.amount_in_unit(
                Memory.UNIT_KB)

    def amount_in_unit(self, unit) -> float:
        exponent = Memory._coefficients[self.unit] - Memory._coefficients[unit]

        # use size of self.amount as number of significant digits
        if self.amount != 0:
            n_significant = int(floor(log10(abs(self.amount)))) + 1
        else:
            n_significant = 0

            # undo rounding errors
        return round(self.amount * 10**exponent, n_significant - exponent)

    @classmethod
    def from_str(cls, val: str) -> Memory:
        """create a Memory object from a string representation
        :return: Memory object matching val
        :raise: ValueError, if the string is not a valid representation
        """

        m = re.match(r"^\s*(\d+)\s*(K|M|G|T)B?\s*$", val)

        if m is None:
            raise ValueError(
                'Memory string must have format <amount><unit>, where <amount>'
                ' is an integer and <unit> is one of "K", "M", "G", or "T", '
                'optionally followed by "B". E.g.: "10 GB"')

        return cls(amount=int(m.group(1)),
                   unit=m.group(2))


@dataclass
class Resources:
    """
    resources needed for a computation job

    :param cpu_time: Time used (Elapsed time * CPU count) by a job
                in cpu-seconds.
    :type cpu_time: int
    :param memory: Maximum resident set size of all tasks in job
                in MB
    :type memory: float
    :param n_cpus: Total number of CPUs allocated to the job
    :type n_cpus: int
    """

    memory: Memory|None = None
    cpu_time: timedelta|None = None
    n_cpus: int|None = None


class Job(ABC, Submittable[SuccessT, FailedT], Generic[SuccessT, FailedT]):
    """
    Base Class from which simulation classes should inherit

    :param name: name of job (optional)
    :type name: str
    :param n_tasks: number of task to be scheduled
    :type n_tasks: int
    :param n_cpus: number of processors to be used
    :type n_cpus: int
    :param memory: maximum memory per cpu
    :type memory: Memory
    :param runtime: maximum runtime of job
    :type runtime: datetime.timedelta
    :param account: SLURM account
    :type account: string
    :param metadata: any metadata you may want to add to the job
    :param state: state of job
    :param id: id of the job given by the job system and set upon submission
    :type id: int
    :param result: contains result after parse_result has been called. This
                parameter is not a constructor argument.
    :type result: dict
    :param resources: used resources per job
    :type resources: Resources
    """

    name: str
    n_tasks: int
    n_cpus: int
    memory: Memory
    runtime: timedelta

    # used when calling self._logger
    _LOG_TEMPLATE = "job ${id}: ${msg}"
    _LOG_TEMPLATE_NO_ID = "job (no id):${msg}"

    def __init__(self, **kwargs) -> None:
        super().__init__()

        # use keyword arguments even for required arguments to avoid errors
        # with the order of this huge list of arguments

        # required arguments
        missing = set(["n_tasks", "n_cpus", "memory", "runtime"]).difference(
            set(kwargs.keys()))

        if len(missing) > 0:
            raise TypeError(
                f"__init__() missing required keyword "
                f"arguments: {missing}")

        self.name = (kwargs.get("name")
                     if "name" in kwargs
                     else self.__class__.__name__)
        self.n_tasks = kwargs.get("n_tasks")
        if not isinstance(self.n_tasks, int):
            raise TypeError("n_tasks must be an integer")
        self.n_cpus = kwargs.get("n_cpus")
        if not isinstance(self.n_cpus, int):
            raise TypeError("n_cpus must be an integer")
        self.memory = kwargs.get("memory")
        if not isinstance(self.memory, Memory):
            raise TypeError("memory must be a Memory object")
        self.runtime = kwargs.get("runtime")
        if not isinstance(self.runtime, timedelta):
            raise TypeError("runtime must be a timedelta object")
        self.resources = Resources()

        # optional arguments
        self.account = kwargs.get("account", None)
        self.metadata = kwargs.get("metadata", None)

    @abstractmethod
    def parse_result(self, path) -> None:
        """
        implemented by derived class; parses the output files of the job

        path: path to working directory for this job
        """

    @abstractmethod
    def gen_input(self, path) -> None:
        """
        implemented by derived class; generates the job's input file

        path: path to working directory for this job
        """

    @property
    @abstractmethod
    def command(self) -> str:
        """
        implemented by derived class;
        """

@dataclass
class PythonJobResult(Result):
    """result of a PythonJob

    :param return_value: return value of the callable
    :param reason: reason why the job failed, if it did
    """

    return_value: object = None

class PythonJob(Job[PythonJobResult]):
    """
    Job that executes a python callable via the job system.

    .. code:: python

        def my_function(a, b, mode='add'):
            if mode == 'add':
                return a + b
            elif mode == 'sub':
                return a - b
            else:
                raise ValueError('Unknown mode')

        # pass the callable as first argument followed by the arguments that
        # should be passed to it
        job = PythonJob(my_function, 1, 2, mode='add')

        jobsys.submit(job)

        # now the job is running and at some point jobsys.refresh() must be
        # called to check if the job is done
        ...

        # we can get the return value of the function from the job's result:
        result = job.result['return']   # = 3

    :param c: callable that should be executed
    :param args: any argumnets that should be passed to the callable
    :param kwargs: any keyword arguments that should be passed to the call, the
                   special keywords used by the parent job class such as name,
                   n_tasks, etc. keep their meaning and are also passed to the
                   callable
    """

    _CALLABLE_DEF_PATH = "callable_file.txt"
    """name of the file that contains the path to the file in which the
    callable is defined"""
    _CALLABLE_PICKLE = "callable.pickle"
    """name of the file that contains the pickled callable"""
    _ARGS_PICKLE = "args.pickle"
    """name of the file that contains the pickled args"""
    _LOG_TEMPLATE_NO_ID = "job (no id): ${msg}"
    _LOG_TEMPLATE = "job ${id}: ${msg}"


    def __init__(
        self,
        c: Callable,
        *args,
        n_tasks=1,
        memory=Memory(1, unit=Memory.UNIT_GB),
        n_cpus=1,
        runtime=timedelta(days=1),
        **kwargs,) -> None:
        super().__init__(
            **kwargs,
            n_tasks=n_tasks,
            memory=memory,
            n_cpus=n_cpus,
            runtime=runtime,)
        self.args = args
        self.kwargs = kwargs
        self.callable = c

        if not callable(c):
            raise TypeError("Callable must be callable")
        if inspect.isclass(c):
            raise ValueError("Callable may not be a class")
        if inspect.ismodule(c):
            raise ValueError("Callable may not be a module")

    def gen_input(self, path):
        path = Path(path)

        # Since the callable may be defined in a different file, we need to
        # store the path to that file in the job's folder so that the job
        # script can import it.
        try:
            callable_path = Path(
                inspect.getsourcefile(self.callable)).resolve()
        except TypeError as err:
            if inspect.isfunction(self.callable):
                raise TypeError(
                    "Cannot pickle the callable. It may be a lambda"
                    " function") from err
            elif hasattr(self.callable, "__class__"):
                # assume that the callable is an instance of a class that
                # defines the __call__ method
                callable_path = Path(
                    inspect.getsourcefile(self.callable.__class__)).resolve()
            else:
                raise TypeError(
                    "Cannot determine the file in which the "
                    "callable is defined. This may lead to problems"
                    " when unpickling it.") from err

        with open(
            path / self._CALLABLE_DEF_PATH, "w", encoding="utf-8") as file:
            file.write(str(callable_path))

        with open(path / self._CALLABLE_PICKLE, "wb") as file:
            pickle.dump(self.callable, file)

        with open(path / self._ARGS_PICKLE, "wb") as file:
            pickle.dump((self.args, self.kwargs), file)

        here = Path(__file__).parent
        #raise ValueError(here / "_pythonjob.py", path / "pythonjob.py")
        shutil.copy(here / "_pythonjob.py", path / "pythonjob.py")

    def parse_result(self, path):
        path = Path(path)

        try:
            with open(path / "result.pickle", "rb") as file:
                result_dict = pickle.load(file)

            if "return" in result_dict:
                self.result = PythonJobResult(
                    return_value=result_dict["return"])
                self.succeed()
            elif "reason" in result_dict:
                self.fail(result_dict["reason"])
            else:
                self.fail("Could not read output of Python job")

        except Exception as err:  # pylint: disable=broad-except
            self.fail(err)
        finally:
            # clean up
            if self.is_successful:
                os.remove(path / self._CALLABLE_DEF_PATH)
                os.remove(path / self._CALLABLE_PICKLE)
                os.remove(path / self._ARGS_PICKLE)

    @property
    def command(self):
        py_exec = sys.executable
        return f'{py_exec} {"pythonjob.py"}'


class PythonScriptJob(Job):
    """Job for running a python script

    .. note::

        For security reasons, you should never pass user input directly as
        script or arguments!

    :param script: path to python script to be executed
    :param python: python executable/command. default: sys.executable
    :param arguments: command line arguments to pass to the script
    :param working_dir: directory in which the script should be executed. If
                        None, the job's directory assigned by the jobsystem is
                        used.
    """

    def __init__(
        self,
        *,
        script: os.PathLike,
        python=None,
        arguments=None,
        working_dir=None,
        **kwargs,) -> None:
        if python is None:
            python = sys.executable
        # only use defaults if not defined via kwargs
        job_metadata = {
            "n_cpus": 1,
            "n_tasks": 1,
            "memory": Memory(1, Memory.UNIT_GB),
        }
        job_metadata.update(kwargs)

        super().__init__(**job_metadata)

        self.arguments = arguments if arguments is not None else list()
        self.script = Path(script).resolve().absolute()
        self.python = python
        self.working_dir = Path(working_dir).resolve() if working_dir else None

    @property
    def command(self):
        arg_str = ""
        for arg in self.arguments:
            arg_str += f' "{arg}"'

        cmd = f'"{self.python}" "{str(self.script)}" {arg_str}'

        if self.working_dir is not None:
            # execute command in new working dir then switch back to old one
            cmd = (
                "OLD_WD=$(pwd)\n"
                f'cd "{str(self.working_dir)}"\n' + cmd + '\ncd "$OLD_WD"')

        return cmd

    def gen_input(self, path):
        pass

    def parse_result(self, path):
        self.result = Result()
        self.succeed()


class JobTemplate:
    """
    Job templates can be used to simplify the creation of new job classes. All
    you need to do is define a command template and an input template.
    Templates can contain identifiers of the form $my_attr or ${my_attr} will
    be replaced by str(job.my_attr). The identifiers can be any alphanumeric
    string (with underscores) that starts with an underscore or ASCII letter.
    identifiers in the template will be filled based on the jobs attributes.
    If the conversion of an attribute to a string should not happen via str(),
    simply define an additional property of the job.

    :param job: instance of a concrete job that should use the template
    :param cmd_tmpl: command template string.
    :param input_tmpls: template strings for input files. The file names are
                        given as keys, the templates for the input file content
                        as values.
    :type input_tmpls: Mapping[str, str]
    """

    def __init__(
        self, job: Job, cmd_tmpl: str, input_tmpls: Mapping[str, str]) -> None:
        self.job = job
        self.cmd_tmpl = cmd_tmpl
        self.input_tmpls = input_tmpls

    def gen_input(self, path):
        """
        Generates input files in path based on self.input_tmpls.

        :param path: Directory in which input files should be created
        """

        for filename in self.input_tmpls:
            with open(
                    os.path.join(path, filename),
                    encoding="utf-8",
                    mode="w") as file:
                file.write(
                    Template(self.input_tmpls[filename]).substitute(
                        self._get_job_properties()))

    @property
    def command(self):
        """
        Generates the command string based on self.cmd_tmpl
        """

        # use safe_substitute b/c there may be bash variables in the command
        return Template(self.cmd_tmpl).safe_substitute(
            self._get_job_properties())

    def _get_job_properties(self):
        """
        Python can be weird sometimes. This method is needed b/c __dict__ does
        not contain properties (e.g. defined via @property)

        :return: dictionary containing all properties and data attributes of
                 self.job
        """
        # just trust me, it works ;)

        # alright, if you really want to know how, here you go:
        # first collect properties
        data = {
            # get attribute of job object with name
            name: getattr(self.job, name)
            # loop through parent classes
            for cls in self.job.__class__.mro()
            # properties are class attributes
            for name, clsattr in cls.__dict__.items()
            # only add properties but skip command to avoid infinite recursion
            if isinstance(clsattr, property) and name != "command"
        }

        # now add attribtues
        data.update(
            {
                name: attr
                # loop through the attributes of the job instance
                for name, attr in self.job.__dict__.items()
                if not isinstance(attr, Callable)  # do not add methods
            })

        return data


class _JobFinishedEvent(Event):
    """This event is triggered by the job system, when a job finished or was
    aborted.

    :param spec: id of the job that finished as string
    :param job_id: id of the job
    """

    def __init__(self, job_id: int, job: Job = None) -> None:
        super().__init__(_JobFinishedEvent.gen_spec(job_id))

        self.job = job
        self.job_id = job_id

    @classmethod
    def gen_spec(cls, id):
        return str(id)


class _JobDatabase(Database):
    """
    database to store job objects in
    """

    _VERSION = {"JobDatabase": "1.0", **Database._VERSION}
    _TABLES = {
        # meta data of the job (not its metadata member attribute though)
        "job_metadata": [
            ("job_id", "integer primary key autoincrement"),
            ("name", "text"),
            ("state", "text"),
        ],
        # the job object as pickled binary
        "job_blobs": [("job_id", "integer unique not null"), ("job", "blob")],
        **Database._TABLES,
    }

    def __init__(self, path: os.PathLike, mode=DBOpenMode.WRITE) -> None:
        super().__init__(path, mode)
        self._jobs = []
        self._last_job_id = None

    def list_jobs(
        self, name: str = None, state: State = None) -> Collection[int]:
        """
        :param name: name of the jobs to load (optional)
        :param state: state of the jobs to list
        :return: list with ids of all jobs that meet the specifications (name
                 and state); list may be empty
        """
        if name is not None and state is not None:
            cur = self._con.execute(
                "SELECT job_id FROM job_metadata "
                "WHERE name=(?) AND state=(?)",
                (name, str(state)),)
        elif name is None and state is not None:
            cur = self._con.execute(
                "SELECT job_id FROM job_metadata " "WHERE state=(?)",
                (str(state),),)
        elif name is not None and state is None:
            cur = self._con.execute(
                "SELECT job_id FROM job_metadata " "WHERE name=(?)", (name,))
        else:
            cur = self._con.execute("SELECT job_id FROM job_metadata")

        job_ids = [id for (id,) in cur]

        cur.close()

        return job_ids

    def load_job(self, job_id: int) -> Job:
        """
        :param job_id: id of job to load
        :return: job with id job_id or None if there is no job with that id
        """
        cur = self._con.execute(
            "SELECT job FROM job_blobs WHERE job_id=(?)", (job_id,))

        job_blob = cur.fetchone()
        if job_blob is not None:
            # unpack tuple
            job_blob = job_blob[0]

            job = pickle.loads(job_blob)
        else:
            job = None

        cur.close()

        return job

    def save_job(self, job: Job) -> int:
        """
        saves job to the database and sets its id

        :param job: job to save
        :return: id of the saved job
        """
        cur = self._con.cursor()

        try:
            # use None for id to let sqlite figure out the id
            cur.execute(
                "INSERT INTO job_metadata VALUES (?,?,?)",
                (None, job.name, str(job._state)),)

            job_id = cur.lastrowid
            job.id = job_id

            try:
                job_blob = pickle.dumps(job)
                cur.execute(
                    "INSERT INTO job_blobs VALUES (?, ?)", (job_id, job_blob))
            except Exception:
                # remove job metadata and reraise the exception
                cur.execute(
                    "DELETE FROM job_metadata WHERE job_id=(?)", (job_id,))
                raise

            self._con.commit()

            # when we reach here, the job was successfully saved
            self._last_job_id = job_id
        finally:
            cur.close()

        return job_id

    def update_job(self, job_id: int, job: Job):
        """
        :param job_id: id of the job to update/overwrite
        :param job: new job with that id
        """
        cur = self._con.cursor()

        job_blob = pickle.dumps(job)

        try:
            cur.execute(
                "UPDATE job_metadata SET name=(?), state=(?) "
                "WHERE job_id=(?)",
                (job.name, str(job._state), job_id),)
            cur.execute(
                "UPDATE job_blobs SET job=(?) WHERE job_id=(?)",
                (job_blob, job_id),)
            self._con.commit()
        finally:
            cur.close()

    def remove_last_job(self):
        """removes the last job that was written to the database"""
        cur = self._con.cursor()

        try:
            cur.execute(
                "DELETE FROM job_metadata WHERE job_id=(?)",
                (self._last_job_id,),)
            cur.execute(
                "DELETE FROM job_blobs WHERE job_id=(?)", (self._last_job_id,))
            self._con.commit()

            self._last_job_id = None
        finally:
            cur.close()


class JobSystem(ABC):
    """
    Base class for job systems. Job systems are used to submit jobs to a
    workload manager (e.g. SLURM) and to manage the jobs.

    The job system handles creation of job directories and triggers
    _JobFinishedEvents

    :param dir: directory for job files
    :param jobs: list of all jobs managed by the job system (may not be in the
                 order of their ids)
    """

    _DB_FILE = "job_db.sqlite"
    """name of the sqlite file in the job systems folder"""

    def __init__(self, dir: os.PathLike) -> None:
        super().__init__()
        self.dir = Path(dir)  # normalize path name
        db_path = self.dir / self._DB_FILE

        self._waiting_for: dict[int, list[int]] = {}

        # get the singleton instance of the event dispatcher
        self._dispatcher = EventDispatcher()

        if not self.dir.exists():
            os.makedirs(self.dir)
        else:
            if not self.dir.is_dir():
                raise FileExistsError(
                    "Job system path exists but is not a " "directory.")
            else:
                if (len(os.listdir(self.dir)) > 1
                    and (not db_path.exists()
                         or not (self.dir/_JobSysFactory._CONF_FILE).exists())
                        ):
                    raise FileExistsError('The job directory exists and is not'
                        ' empty but does not contain a job system.')

        self._job_db = _JobDatabase(path=self.dir / self._DB_FILE)

        self._in_context = False  # shows if JobSystem is used as context mgr


    def __enter__(self):
        self._in_context = True
        try:
            self._job_db.__enter__()
            return self
        except Exception:
            self._in_context = False
            raise

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._in_context = False
        return self._job_db.__exit__(exc_type, exc_value, exc_traceback)

    def submit(self, job: Job, wait_for: Iterable[int] = None) -> int:
        """
        used to submit jobs through the batch system.

        .. note::

            The job object may be copied internally at any point (especially
            when serializing and deserializing) which means that the object
            passed to this function and the object retrieved by
            jobsystem.get_job_by_id(id) where id is the id returned by this
            function may not be the same object although they represent the
            same job. In practice this means, that you should not call
            job.result on the original job object, but on the one that the job
            system gives back after the job is done.

        :param job: job to submit
        :param wait_for: list of jobs ids that need to finish before the actual
                         execution of this job starts. "Finish" does not refer
                         to the python job objects state (e.g. job.is_running),
                         but to the state of the process(es) that the job
                         object represents. In other words, if job A is
                         supposed to wait for job B, job A may already be
                         executed while job B is still shown as running
                         according to `job_b.is_running`.
        :return: id of the job
        """
        job_id = self._job_db.save_job(job)

        job_dir = self.get_job_dir(job_id)
        os.mkdir(job_dir)   # raises error if job_dir already exists

        try:
            job.gen_input(job_dir)

            self._waiting_for[job_id] = (list(wait_for)
                                         if wait_for is not None
                                         else list())
            self._submit(job, wait_for)
        except Exception as err:
            self._job_db.remove_last_job()

            shutil.rmtree(job_dir, ignore_errors=True)

            # simply reraise error for better debugging
            raise err

        # update the new state of the job etc
        job._state = State.RUNNING
        self._job_db.update_job(job_id=job_id, job=job)


        return job_id

    def refresh(self):
        """
        Checks if jobs finished running and parses the output of finished jobs
        and triggers a respective event.
        """
        running_ids = self._get_running_ids()
        finished = self._check_finished(running_ids)

        for job_id, (is_finished, failure) in zip(running_ids, finished):
            if not is_finished and failure is None:
                # no need to load job from DB
                continue

            job = self._job_db.load_job(job_id)

            if is_finished and failure is None:
                # TODO reload job on failure!
                # TODO how to exit call stack from here!?!-> special exception?
                job.parse_result(self.get_job_dir(job_id))
                self._save_resources(job)

                # sanity check on job implementation
                if job.is_running:
                    raise ProgrammingError(
                        f"Job {job.id}: parse_result() must set the job's"
                        " state to successful or failed.")
                if job.result is None:
                    raise ProgrammingError(
                        f"Job {job.id}: parse_result() must set the job's "
                        "result.")
            elif failure is not None:
                job.fail(failure)
                self._save_resources(job)

            # update database and trigger event only after no excep. was raised
            self._job_db.update_job(job_id=job_id, job=job)

            # TODO do not trigger yet
            self._dispatcher.trigger(_JobFinishedEvent(job_id=job_id, job=job))


    @abstractmethod
    def _submit(self, job: Job, wait_for: Optional[Iterable[int]] = None):
        """submit the job to the job system/execute it

        This function is called by submit() after the job id has been assigned
        and gen_input() has been called, but before the state of the job is set
        to RUNNING.
        Note that this function may be called with the same job (same id),
        multiple times, e.g., if a job is restarted manually.
        """

    @abstractmethod
    def _check_finished(
        self, ids: Iterable[int]) -> list[tuple[bool, Failure | None]]:
        """check if jobs with the given ids have finished.

        This function is called by refresh().

        :return: list of tuples where the first element is True if the job has
                    finished and the second element is a failure object, if the
                    job system already detected that the job did not finish
                    successfully, e.g., because it was aborted.
        """

    @abstractmethod
    def _save_resources(self, job: Job):
        """saves the resources used by a job in the job system"""

    @property
    def jobs(self):
        return [
            self._job_db.load_job(job_id)
            for job_id in self._job_db.list_jobs()
        ]

    def get_successful(self) -> Iterable[Job]:
        """:return: successfully finished jobs"""
        return [
            self._job_db.load_job(job_id)
            for job_id in self._job_db.list_jobs(state=State.SUCCESSFUL)
        ]

    def get_failed(self) -> Iterable[Job]:
        """:return: failed jobs"""
        return [
            self._job_db.load_job(job_id)
            for job_id in self._job_db.list_jobs(state=State.FAILED)
        ]

    def get_running(self) -> Iterable[Job]:
        """:return: jobs that are still running"""
        return [
            self._job_db.load_job(job_id) for job_id in self._get_running_ids()
        ]

    def _get_running_ids(self) -> Iterable[int]:
        """:return: job ids of jobs that are still running"""
        return self._job_db.list_jobs(state=State.RUNNING)

    def get_jobs_by_name(self, name: str) -> Iterable[Job]:
        """
        :param name:
        :return: jobs which have the name `name`
        """
        return [
            self._job_db.load_job(job_id)
            for job_id in self._job_db.list_jobs(name=name)
        ]

    def get_job_by_id(self, job_id: int) -> Job:
        """
        :param id:
        :return: the job with id `id`
        """
        return self._job_db.load_job(job_id)

    def get_job_dir(self, job_id: int) -> Path:
        """:return: directory name for job with id job_id"""
        return (self.dir / f'{job_id:05d}').resolve()

class BlockingJobSystem(JobSystem):
    """Simple job system that waits on jobs to finish on submission

    This job system submits jobs via Python's subprocess module and waits for
    them to finish, i.e., the call to `submit()` will not return until the job
    is done. It does not use an external scheduler such as SLURM.

    .. note::

        This job system is not suitable for long running jobs as it will block
        the main thread until the job is done.
    """

    def __init__(self, dir: os.PathLike, shell_exec: Path|None = None) -> None:
        super().__init__(dir)

        # since we are blocking, we need to keep track of the jobs that are
        # currently running until
        self.__running: dict[int, Failure | None] = {}
        self.shell_exec = str(shell_exec) if shell_exec is not None else None

    def _submit(self, job: Job, wait_for: Optional[Iterable[int]] = None):
        if job.n_tasks > 1:
            # multiple tasks/distributed memory parallelization would require
            # MPI
            raise ValueError('BlockingJobSystem does not support jobs with '
                             f'multiple tasks. Requested {job.n_tasks} tasks.')

        # since this job system is blocking, we can ignore wait_for
        cmd = job.command
        job_id: int = job.id   # job.id is set by the job system # type:ignore
        job_dir = self.get_job_dir(job_id)

        logging.debug("Executing command: %s", cmd)
        try:
            process = subprocess.run(cmd, shell=True, capture_output=True,
                                cwd=str(job_dir), check=True,
                                executable=self.shell_exec,
                                timeout=job.runtime.total_seconds())

            self.__running[job_id] = None

            stdout = str(process.stdout, encoding="utf-8")
            stderr = str(process.stderr, encoding="utf-8")

            with open(job_dir / "stdout.txt", "w", encoding="utf-8") as file:
                file.write(stdout)

            with open(job_dir / "stderr.txt", "w", encoding="utf-8") as file:
                file.write(stderr)
        except subprocess.CalledProcessError as err:
            stderr = str(err.stderr, encoding="utf-8")

            # state is officially changed only in refresh() -> store it
            self.__running[job_id] = NonzeroExitCodeFailure(
                msg="Job failed with exit code " f"{err.returncode}: {stderr}",
                exit_code=err.returncode,)
        except subprocess.TimeoutExpired:
            self.__running[job_id] = TimeoutFailure(
                f"Job timed out after {job.runtime}")

    def _check_finished(self, ids: Iterable[int])\
            -> list[tuple[bool, Failure | None]]:
        # all jobs are already done, so always return True
        return [(True, self.__running[job_id]) for job_id in ids]

    def _save_resources(self, job: Job):
        job.resources.cpu_time = None
        job.resources.memory = None
        job.resources.n_cpus = None

class _SlurmJobSystem(JobSystem):
    """
    Used to control the SLURM batch system and give folders to each job that
    runs

    :param dir: directory for job files
    :param account: SLURM account
    :param sbatch_cmd: SLURM's sbatch command
    :param jobs: list of all jobs managed by the job system (may not be in the
                 order of their ids)
    """

    _SBATCH_TEMPLATE = """\
${shebang}
#SBATCH --job-name="${job_name}"
#SBATCH --error=stderr.txt
#SBATCH --output=stdout.txt
#SBATCH --time=${time}
#SBATCH --cpus-per-task=${n_cpus}
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=${n_tasks}
#SBATCH --mem-per-cpu=${memory}
${optional}

trap 'touch "job.${job_id}.aborted"' SIGTERM SIGKILL SIGQUIT SIGINT

${command}

touch "job.${job_id}.finished"
"""

    _SBATCH_ACCOUNT = "#SBATCH --account=${account}"

    _SLURM_IDS_FILE = "slurm_ids.json"

    def __init__(
        self,
        dir: os.PathLike,
        account: Optional[str] = None,
        sbatch_cmd: str = "sbatch",
        shebang="#!/bin/bash",) -> None:
        super().__init__(dir)
        self.account = account

        self.sbatch_cmd = sbatch_cmd
        self.shebang = shebang

        self._slurm_ids: dict[int, str] = {}

    def __enter__(self):
        super().__enter__()
        json_file = self.dir / self._SLURM_IDS_FILE
        if json_file.exists():
            with open(json_file, encoding="utf-8") as fp:
                self._slurm_ids = {
                    job_id: slurm_id for job_id, slurm_id in json.load(fp)
                }
        else:
            self._slurm_ids = {}

        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        json_file = self.dir / self._SLURM_IDS_FILE
        with open(json_file, "w", encoding="utf-8") as fp:
            # JSON keys are always strings so we store the items instead to
            # keep the job ids as integers
            json.dump([el for el in self._slurm_ids.items()], fp)

        return super().__exit__(exc_type, exc_value, exc_traceback)

    def _create_template_dict(self, job: Job) -> dict[str, Any]:
        """Creates the dictionary that is used to fill the template for the
        job file
        """
        # set up template for job file
        if job.account is not None:
            account = Template(self._SBATCH_ACCOUNT).substitute(
                {'account': job.account})
        elif self.account is not None:
            account = Template(self._SBATCH_ACCOUNT).substitute(
                {'account': self.account})
        else:
            account = ''

        tmp_mapping = {
            'job_name': job.name,
            'job_id': job.id,
            'time': self._timedelta2str(job.runtime),
            'n_cpus': job.n_cpus,
            'n_tasks': job.n_tasks,
            'memory': job.memory,
            'optional': account,
            'command': job.command,
            'shebang': self.shebang
        }
        return tmp_mapping

    def _submit(self, job: Job, wait_for: Iterable[int] = None):
        """
        used to submit jobs through the SLURM system.

        .. note::

            The job object may be copied internally at any point
            (especially when serializing and deserializing) which means that
            the object passed to this function and the object retrieved by
            jobsystem.get_job_by_id(id) where id is the id returned by this
            function may not be the same object although they represent the
            same job. In practice this means, that you should not call
            job.result on the original job object, but on the one that the job
            system gives back after the job is done.

        :param job: job to submit
        :param wait_for: list of jobs ids that need to finish before the actual
                         execution of this job starts
        """
        job_dir = self.get_job_dir(job.id)
        # set up template for job file
        tmp_mapping = self._create_template_dict(job)
        # write job file and generate input files
        sh_name = 'job_' + job.name + '.sh'
        sh_path = os.path.join(job_dir, sh_name)
        with open(sh_path, 'x') as sh_file:
            # don't use safe_substitute so that there can be bash variables
            # in the template
            sh_file.write(Template(self._SBATCH_TEMPLATE).substitute(
                tmp_mapping))

        # submit job
        if not wait_for:
            cmd = f'{self.sbatch_cmd} --parsable "{sh_name}"' #
        else:
            wait_slurm_ids = [self._slurm_ids[job_id]
                                for job_id in wait_for]
            cmd = (f'{self.sbatch_cmd} --parsable --dependency=afterburst'
                    f'buffer:{",".join(wait_slurm_ids)} "{sh_name}"')

        logging.debug('Executing command: %s', cmd)
        try:
            process = subprocess.run(cmd, shell=True, capture_output=True,
                                cwd=job_dir, check=True)
        except subprocess.CalledProcessError as err:
            logging.error(str(err.stderr, encoding='utf-8'))

            # reraise to abort submission
            raise err

        output = str(process.stdout, encoding='utf-8').splitlines()

        # --parsable usually outputs just the slurm id, but sometimes,
        # it prepends errors/warnings which we want to log
        for line in output[:-1]:
            logging.warning(line)

        slurm_id = output[-1]
        logging.debug(f'Job {job.id} has SLURM id {slurm_id}.')

        if slurm_id.isnumeric():
            self._slurm_ids[job.id] = slurm_id # type: ignore
        else:
            raise RuntimeError(f'Unexpected SLURM id: {slurm_id}')


    def _timedelta2str(self, td: timedelta):
        """helper function to get string representation of format dd-hh:mm:ss
        """

        days = td.days
        seconds = td.seconds
        hours = seconds // 3600
        seconds = seconds % 3600
        minutes = seconds // 60
        seconds = seconds % 60

        return f"{days:02d}-{hours:02d}:{minutes:02d}:{seconds:02d}"

    def _get_sacct(
        self,
        fields: list[str],
        slurm_ids: list[str],
        additional_flags: Optional[str] = None,) -> dict[str, list[str]]:
        """
        Get the sacct output for one or more jobs.

        :param fields: list of fields to get
        :param job_ids: list of SLURM ids to get data for
        :param additional_flags: additional flags to pass to sacct such as
                                 --units=M (be careful with this one, it
                                 changes the output format and may lead to
                                 wrong results during parsing the output)
        :return: dictionary with job ids as keys and list of values as values
                 in the order of the fields. Note, that the returned dictionary
                 contains more job ids than requested, because sacct may return
                 rows for substeps of the job.
        """
        if not slurm_ids:  # empty list
            return {}

        # always add JobID, it may be printed twice but it is not a problem
        fields = ["JobID"] + fields

        fields_str = ",".join(fields)
        ids_str = ",".join(slurm_ids)

        cmd = f"sacct --format={fields_str} -j {ids_str} -P"
        if additional_flags:
            cmd += f" {additional_flags}"

        process = subprocess.run(cmd, shell=True, capture_output=True)
        try:
            process.check_returncode()
        except subprocess.CalledProcessError as err:
            logging.error(str(err.stderr, encoding="utf-8"))
            raise err

        output = str(process.stdout, "utf-8")

        lines = output.splitlines()

        data = {}

        for line in lines[1:]:
            words = line.split("|")

            data[words[0]] = words[1:]

        return data

    def _check_finished(self, ids: Iterable[int])\
            -> list[tuple[bool, Failure|None]]:
        ret = [] # return value

        # SLURM states corresponding to finished jobs
        FINISHED_STATES = ["BOOT_FAIL", "COMPLETED", "FAILED"]
        ABORTED_STATES = [
            "CANCELLED",
            "DEADLINE",
            "NODE_FAIL",
            "PREEMPTED",
            "TIMEOUT",
        ]
        # get SLURM states of all jobs registered as running in DB via sacct:
        sacct_data = self._get_sacct(
            ["State"], [self._slurm_ids[job_id] for job_id in ids])

        for job_id in ids:
            slurm_id = self._slurm_ids[job_id]

            try:
                slurm_state = sacct_data[slurm_id][0]
            except KeyError:
                logging.warning(
                    "Job %d with SLURM id %s not "
                    "found in sacct output. This job will not be "
                    "recognized as finished.",
                    job_id,
                    slurm_id,)
                continue

            # slurm_state may be "CANCELLED by 12345" -> use startswith
            if any(slurm_state.startswith(state)
                   for state in ABORTED_STATES + FINISHED_STATES):
                # Never return Failure so that Job parser still has chance to
                #  get some data (even from aborted jobs)
                ret.append((True, None))
            else:
                ret.append((False, None))  # job still running

        # return in correct order
        return ret

    def _save_resources(self, job: Job):
        """
        saves resources used by job to the job.resources object
        """
        slurm_id = self._slurm_ids[job.id]
        cmd = f"seff {slurm_id}"

        process = subprocess.run(cmd, shell=True, capture_output=True)
        process.check_returncode()

        lines = str(process.stdout, encoding="utf-8").splitlines()

        cpu_time = None
        ncpus = None
        nodes = 1
        cores_per_node = None

        # parsing the seff output
        # this could change with different versions of seff
        for line in lines:
            if "CPU Utilized" in line:
                cpu_utilized = line.split(":", 1)[1].strip()
                parts = cpu_utilized.split("-")
                h, m, s = map(int, parts[-1].split(":"))
                if len(parts) == 1:
                    cpu_time = timedelta(
                        days=0,
                        seconds=s,
                        microseconds=0,
                        milliseconds=0,
                        minutes=m,
                        hours=h,
                        weeks=0,)
                else:
                    cpu_time = timedelta(
                        days=int(parts[0]),
                        seconds=s,
                        microseconds=0,
                        milliseconds=0,
                        minutes=m,
                        hours=h,
                        weeks=0,)
            elif "Nodes" in line:
                nodes = int(line.split(":", 1)[1].strip())
            elif "Cores per node" in line:
                cores_per_node = int(line.split(":", 1)[1].strip())
            elif "Memory Utilized" in line:
                memory_str = line.split(":", 1)[1].split("(", 1)[0]
                # memory can have a variety of units, this needs to be caught
                memory_value, memory_unit = memory_str.split()
                memory_value = float(memory_value)
                if memory_unit != "MB":
                    if memory_unit == "GB":
                        memory_value = float(memory_value) * 1024.0
                    elif memory_unit == "KB":
                        memory_value = float(memory_value) / 1024.0
                    else:
                        raise ValueError(
                            f"Unknown memory unit: {memory_unit}. Please add "
                            "a conversion formula.")

        if cores_per_node is not None:
            ncpus = nodes * cores_per_node

        job.resources.cpu_time = cpu_time
        job.resources.memory = Memory(memory_value, unit=Memory.UNIT_MB)
        job.resources.n_cpus = ncpus


@dataclass
class _ClaixPartition:
    """Represents a compute partition"""
    name: str
    memory_per_core: int  # in MiB
    cores_per_node: int
    total_nodes: int


"""Contains the specific Compute Partitions for current Claix-2023
system"""
_CLAIX_PARTITIONS_2023 = [
    _ClaixPartition(  # small
        name="c23ms",
        memory_per_core=2540,
        total_nodes=625,
        cores_per_node=96,
    ),
    _ClaixPartition(  # medium
        name="c23mm",
        memory_per_core=5210,
        total_nodes=166,
        cores_per_node=96,
    ),
    _ClaixPartition(  # large
        name="c23ml",
        memory_per_core=10560,
        total_nodes=2,
        cores_per_node=96,
    ),

]


class _Claix2023JobSystem(_SlurmJobSystem):
    """
    Slurm Job system with finer control for the current claix 2023 compute
    partitions
    """

    @staticmethod
    def _select_partition(memory_per_cpu: Memory) -> _ClaixPartition:
        """Selects the most suitable partition base on the needed memory
        consumption
        """
        memory_per_cpu_in_mib = memory_per_cpu.amount_in_unit(
            Memory.UNIT_MB  # is in MiB not in MB
        )
        # Requested Memory is smaller than max of large partition
        for partition in _CLAIX_PARTITIONS_2023:
            if memory_per_cpu_in_mib <= partition.memory_per_core:
                return partition
        # Memory is larger than the largest partition
        sorted_claix_partitions = sorted(
            _CLAIX_PARTITIONS_2023,
            key=lambda part: part.memory_per_core,
        )
        largest_claix_partition = sorted_claix_partitions[-1]
        return largest_claix_partition

    @staticmethod
    def _upgrade_memory(
            partition: _ClaixPartition,
            original_memory_per_cpu: Memory
    ) -> Memory:
        """Creates a new memory object whose amount is set to the amount
        of memory in partition or original_memory_per_cpu, whichever is
        greater.
        """
        original_memory_per_cpu_in_mib = (
            original_memory_per_cpu.amount_in_unit(Memory.UNIT_MB)  # MiB
        )
        return Memory(  # in MiB
            amount=max(
                partition.memory_per_core,
                int(original_memory_per_cpu_in_mib),
            ),
            unit=Memory.UNIT_MB,
        )

    def _create_template_dict(self, job: Job) -> dict[str, Any]:
        """Adds the partition flag to the original slurm job template
        dictionary
        """
        original_tmp_mapping = (
            super()._create_template_dict(job)
        )
        partition = self._select_partition(job.memory)
        partition_flag = f"#SBATCH --partition={partition.name}"
        if original_tmp_mapping["optional"]:
            original_tmp_mapping["optional"] = (  # account is optional
                f'{original_tmp_mapping["optional"]}\n{partition_flag}'
            )
        else:
            original_tmp_mapping["optional"] = partition_flag
        return original_tmp_mapping

    def submit(self, job: Job, wait_for: Iterable[int] = None) -> int:
        """Alters the Memory of the job before submitting the job through
        the job system
        """
        original_memory = job.memory
        partition = self._select_partition(job.memory)
        new_memory = self._upgrade_memory(partition, original_memory)
        job.memory = new_memory

        job_id = super().submit(job, wait_for)
        logging.info(
            "Selected partition %s with memory %s for job %d",
            partition.name, new_memory, job.id,
        )
        return job_id


class _JobSysFactory:
    """class to collect all job system creation methods

    never needs to be instantiated
    """

    _CONF_FILE = 'conf.json'
    """name of the file that contains the job system type"""

    @classmethod
    def _create_slurm_jobsystem(cls, job_dir: os.PathLike,
                            account: str|None, sbatch_cmd: str,
                            shell_exec: Path|None = None
                            ) -> _SlurmJobSystem:
        if shell_exec is None:
            return _SlurmJobSystem(dir=job_dir,
                         account=account,
                         sbatch_cmd=sbatch_cmd,)

        return _SlurmJobSystem(dir=job_dir,
                         account=account,
                         sbatch_cmd=sbatch_cmd,
                         shebang=f"#!{str(shell_exec)}")

    @classmethod
    def _create_claix2023_jobsystem(cls, job_dir: os.PathLike,
                                account: str|None, sbatch_cmd: str,
                                shell_exec: Path|None = None
                                ) -> _Claix2023JobSystem:
        if shell_exec is None:
            return _Claix2023JobSystem(dir=job_dir,
                            account=account,
                            sbatch_cmd=sbatch_cmd,)

        return _Claix2023JobSystem(dir=job_dir,
                            account=account,
                            sbatch_cmd=sbatch_cmd,
                            shebang=f"#!{str(shell_exec)}")

    @classmethod
    def _create_blocking_jobsystem(cls, job_dir: os.PathLike, shell_exec)\
            -> BlockingJobSystem:
        logging.info('With the blocking job system jobs will be run directly '
                     'as subprocesses. This means that the program '
                     'will wait for each job to finish before starting the '
                     'next one.\nOnly waiting mode is possible now, --restart/'
                     '--no-wait will be ignored.')
        return BlockingJobSystem(dir=job_dir, shell_exec=shell_exec)


    @classmethod
    def _load_config(cls, job_dir: Path) -> JobSysConfig|None:
        """load the configuration from the job directory"""
        job_dir = Path(job_dir)
        try:
            with open(job_dir/cls._CONF_FILE, 'r', encoding='utf-8') as file:
                conf = json.load(file)
        except FileNotFoundError:
            return None

        return JobSysConfig(**conf)

    @classmethod
    def _store_config(cls, job_dir: Path, conf: JobSysConfig):
        """store the configuration in the job directory"""
        job_dir = Path(job_dir)

        job_dir.mkdir(exist_ok=True, parents=True)

        with open(job_dir/cls._CONF_FILE, 'w', encoding='utf-8') as file:
            file.write(conf.model_dump_json())

    @classmethod
    def create(cls, job_dir: Path, conf: JobSysConfig|None = None
               ) -> JobSystem:
        """returns the job system that should be used
        """
        old_conf = cls._load_config(job_dir)
        if conf is None:
            if old_conf is None:
                raise ValueError('No job system configuration found in the '
                                 'job directory and none provided.')
            else:
                conf = old_conf
        else:
            if old_conf is not None and old_conf.jobsystem != conf.jobsystem:
                raise ValueError(
                    'The job system type in the job directory is'
                    ' not consistent with the given job system type')

            cls._store_config(job_dir, conf)

        if conf.jobsystem == JobSysType.blocking:
            return cls._create_blocking_jobsystem(job_dir, conf.shell_exec)

        elif (os.name == 'nt' and
              (conf.jobsystem in [
                  JobSysType.slurm, JobSysType.slurmclaix2023
              ])):
            logging.info('SLURM not supported on Windows. Using blocking job.')
            conf.jobsystem = JobSysType.blocking
            return cls._create_blocking_jobsystem(job_dir, conf.shell_exec)
        elif (os.name == 'posix' and
              (conf.jobsystem in [
                  JobSysType.slurm, JobSysType.slurmclaix2023
              ])):
            # to determine if SLURM is installed/available, we just check,
            # if the sbatch command is available
            if shutil.which(conf.sbatch_cmd) is not None:
                if conf.jobsystem == JobSysType.slurm:
                    return cls._create_slurm_jobsystem(job_dir,
                                                       conf.slurm_account,
                                                       conf.sbatch_cmd,
                                                       conf.shell_exec)
                elif conf.jobsystem == JobSysType.slurmclaix2023:
                    return cls._create_claix2023_jobsystem(job_dir,
                                                           conf.slurm_account,
                                                           conf.sbatch_cmd,
                                                           conf.shell_exec)
            else:
                logging.info('sbatch not found. Using blocking job system.')
                return cls._create_blocking_jobsystem(job_dir, conf.shell_exec)
        elif conf.jobsystem not in [
            'slurm', 'claix2023', 'blocking'
        ]:
            raise ValueError(f'Unknown job system "{conf.jobsystem}"')
        else:
            raise NotImplementedError('Unsupported operating system '
                                      f'"{os.name}"')

def create_jobsystem(job_dir: Path, conf: JobSysConfig|None = None
                     ) -> JobSystem:
    """creates a job system based on the configuration

    :param job_dir: directory for job files
    :param conf: configuration for the job system (may be changed, if the
                 requested job system is not available)
    :return: job system
    """
    return _JobSysFactory.create(job_dir, conf)
