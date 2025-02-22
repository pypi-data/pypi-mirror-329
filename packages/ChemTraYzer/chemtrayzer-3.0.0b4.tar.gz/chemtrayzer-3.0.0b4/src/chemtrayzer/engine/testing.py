"""
This module contains functionality for testing investigations and jobs.
"""

import argparse
import functools
import importlib
import logging
import os
import pathlib
import pickle
import shutil
import sys
from abc import ABC
from collections.abc import Callable, Iterable, Mapping
from contextlib import AbstractContextManager
from datetime import timedelta
from difflib import Differ
from shutil import copytree
from os import PathLike
from types import ModuleType
from typing import (
    Any,
    ClassVar,
    Generic,
    Optional,
    TypeVar,
    Union,
)
from unittest.mock import patch, MagicMock

import numpy as np
import pytest
from pydantic import field_validator

from chemtrayzer.engine._event import EventDispatcher
from chemtrayzer.engine._submittable import (
    Failure,
    Result,
    State,
    Submittable,
    _ResultBase,
)
from chemtrayzer.engine.cmdtools import (
    CommandLineInterface,
    IllegalConfigError,
    ConfigLoaderError,
    ConfigT,
)
from chemtrayzer.engine.config import CmdArgsBase, ConfigBase
from chemtrayzer.engine.investigation import (
    BatchInvestigation,
    Investigation,
    InvestigationContext,
    InvestigationError,
    InvestigationRunner,
)
from chemtrayzer.engine.jobsystem import (
    Job,
    JobSystem,
    Memory,
    _JobFinishedEvent,
)

__all__ = [
    "JobTester",
    "InvestigationTestCase",
    "DummyJob",
    "DummyInvestigation",
    "BatchCLI",
    "CLITestCase",
]


class DummyJob(Job):
    """a simple dummy job with some arbitrary default values

    :param parse_result_state: state to which the job is set upon
            calling parse_result()
    """

    def __init__(
        self,
        parse_result_state: State = None,
        failure: Optional[Failure | str | Exception] = None,
        name="job name",
        n_tasks=3,
        n_cpus=2,
        memory=Memory(140),
        account=None,
        runtime=timedelta(days=3, minutes=10),
        command="my_programm.exe",
        id=None,
        state=State.PENDING,
    ) -> None:
        super().__init__(
            name=name,
            n_tasks=n_tasks,
            n_cpus=n_cpus,
            memory=memory,
            runtime=runtime,
            account=account,
        )

        if failure is not None:
            if parse_result_state is not State.FAILED:
                raise ValueError(
                    "If a failure is provided, the "
                    "parse_result_state must be set to "
                    "State.FAILED."
                )

        self._id = id
        self._cmd = command
        self._state = state
        self._final_state = parse_result_state
        self._failure = failure
        self._parse_result_calls = []  #list of arguments passed to pass_result
        self._gen_input_calls = []

    @property
    def command(self):
        return self._cmd

    def gen_input(self, path):
        self._gen_input_calls.append(path)

    def parse_result(self, path):
        self._parse_result_calls.append(path)

        if self._final_state is not None:
            if self._final_state == State.FAILED:
                if self._failure is not None:
                    self.fail(self._failure)
                else:
                    self.fail(Failure("Default failure of DummyJob"))
            elif self._final_state == State.SUCCESSFUL:
                # allow setting a result beforehand for test purposes
                if self.result is None:
                    self.result = self.Result()
                self.succeed()
            else:
                self._state = self._final_state

    def assert_parse_result_not_called(self):
        assert len(self._parse_result_calls) == 0

    def assert_parse_result_called_once_with(self, args):
        n_calls = len(self._parse_result_calls)
        if n_calls != 1 or self._parse_result_calls[0] != args:
            raise AssertionError(
                f"parse_result called {n_calls} times with "
                f"arguments {self._parse_result_calls}"
            )

    def assert_gen_input_called_once_with(self, args):
        n_calls = len(self._gen_input_calls)
        if n_calls != 1 or self._gen_input_calls[0] != args:
            raise AssertionError(
                f"gen_input called {n_calls} times with "
                f"arguments {self._gen_input_calls}"
            )

    def finish_successfully(self):
        self.succeed()
        # usually the job system would to this, but we are not using it here
        EventDispatcher().trigger(_JobFinishedEvent(job_id=self.id, job=self))


class JobTester:
    """Provides some utility functions to test Job classes"""

    def __init__(self, tmp_path_factory):
        # do not use the tmp_path fixture, because it may be used by tests for
        # other purposes
        self.tmp_path_factory = tmp_path_factory

    def test_gen_input_writes_files(
        self,
        job: Job,
        contents: dict[str, str] = None,
        expected_files: Union[dict[str, str], os.PathLike, str] = None,
    ):
        """
        Calls job.gen_input(tmp_path) and asserts that all files defined in
        contents have been written.

        :param job: job object to test
        :param contents: dictionary whose keys are file names and whose values
                         are the expected contents of the file after
                         gen_input() has been called
        :param expected_files: alternative/addition to "contents".
                               If this is a dictionary, the keys are the names
                               of files that ``gen_input()`` is supposed to
                               generate in the job folder and the values are
                               paths to files that contain the expected input
                               of those files.
                               If it is a path or string, it should point to a
                               folder containing all the files that are
                               supposed to be generated with the correct name.
        """
        # gen_input can be called multiple times (e.g., if the job should be
        # restarted due to an error) -> test two executions
        for i in range(2):
            # ARANGE
            path = pathlib.Path(
                self.tmp_path_factory.mktemp("JobTester_dir", numbered=True)
            )

            # ACT
            job.gen_input(path)

            # ASSERT
            self.assert_job_dir_contains_expected_files(
                path, contents, expected_files
            )

    @classmethod
    def assert_job_dir_contains_expected_files(
        cls,
        job_dir: os.PathLike,
        contents: dict[str, str] = None,
        expected_files: Union[dict[str, os.PathLike], os.PathLike] = None,
    ):
        """
        :job_dir: directory in which ``gen_input()`` was supposed to generate
                  the files whose contents and file names will be checked
        :param contents: dictionary whose keys are file names and whose values
                         are the expected contents of the file after
                         gen_input() has been called
        :param expected_files: alternative/addition to "contents".
                               If this is a dictionary, the keys are the names
                               of files, that ``gen_input()`` is supposed to
                               generate in the job folder and the values are
                               paths to files that contain the expected input
                               of those files.
                               If it is a path or string, it should point to a
                               folder containing all the files that are
                               supposed to be generated with the correct name.
        """
        job_dir = pathlib.Path(job_dir)

        # add stuff from expected files to contents
        if contents is None:
            contents = {}
        else:
            # make a copy to not modify the original (this part of the test is
            # executed twice)
            contents = contents.copy()

        if expected_files is not None:
            if isinstance(expected_files, dict):
                for name, in_path in expected_files.items():
                    if name in contents:
                        raise ValueError(
                            f'File "{name}" is defined in both '
                            '"contents" and via "expected_files".'
                        )

                    with open(in_path, "r", encoding="utf-8") as file:
                        contents[name] = file.read()
            elif pathlib.Path(expected_files).is_dir():
                files = os.listdir(expected_files)
                if len(files) == 0:
                    logging.warning(
                        f'Path for expected files "{expected_files}" '
                        "is empty."
                    )

                for fname in files:
                    if fname in contents:
                        raise ValueError(
                            f'File "{fname}" is defined in '
                            'both "contents" and via "expected_files".'
                        )
                    # when an empty folder should be commited to git, you
                    # typically create an empty file ".gitkeep" in it. We want
                    # to ignore those files
                    if fname == ".gitkeep":
                        continue

                    with open(
                        pathlib.Path(expected_files) / fname,
                        "r",
                        encoding="utf-8",
                    ) as file:
                        contents[fname] = file.read()
            else:
                raise ValueError(
                    "expected_files must be a dictionary or an "
                    "existing directory"
                )

        # do assertion for the whole content of each expected file
        for f_name, expected_content in contents.items():
            f_path = job_dir / f_name

            if not f_path.is_file():
                raise AssertionError(
                    f"File {f_path} was not generated"
                    " by the job"
                )

            with open(f_path, encoding="utf-8", mode="r") as f:
                actual_content = f.read()

            if expected_content != actual_content:
                d = Differ()
                diff = list(
                    d.compare(
                        expected_content.splitlines(),
                        actual_content.splitlines(),
                    )
                )

                raise AssertionError(
                    f"Contents of {f_path} not as "
                    "expected:\n" + "\n".join(diff)
                )

    def _write_fake_job_output(
        self,
        tmp_path: str,
        contents: dict[str, str],
        out_files: dict[str, Union[str, os.PathLike]],
    ):
        tmp_path = pathlib.Path(tmp_path)

        for f_name, content in contents.items():
            path = tmp_path / f_name

            with open(path, "w", encoding="utf-8") as file:
                file.write(content)

        for f_name, path in out_files.items():
            shutil.copy(path, tmp_path / f_name)

    def test_parse_result(
        self,
        job: Job,
        contents: dict[str, str],
        out_files: dict[str, Union[str, os.PathLike]],
        expected_result: dict,
        atol=0.0,
        rtol=1e-8,
        checkers: dict[str, Callable] = None,
    ):
        """used to check if the output is parsed correctly

        :param job: job object to test
        :param tmp_path: temporary path, usually tmp_path fixture
        :param contents: dictionary, where the keys are file names of the
                         output files which should be parsed and the values are
                         their contents
        :param out_files: output files which are too large to provide as string
                          in `contents`, can be copied from the source path
                          defined by the values of this dictionary. The keys
                          are the file names, that the job expects.
        :param expected_result: expected contents of job.result after
                                job.parse_result() has been called.
        :param atol: absolute tolerance for numerical values (incl. ndarrays)
        :param rtol: relative tolerance for numerical values (incl. ndarrays)
        :param checkers: If values in job.results should be checked with
                         something other than an equality assertion, one may
                         provide a function to perform the check via this dict.
                         Using the same key as the to-be-tested value in
                         job.results has, one can provide a callable which
                         returns True if the value passes the test and false if
                         it does not.
                         E.g. if job.results['message'] is expected to contain
                         a string starting with 'Hello', this dictionary could
                         look like this: `checkers = {'message': lambda val :
                         val.startswith('Hello)}`
        """
        # arrange
        tmp_path = self.tmp_path_factory.mktemp("JobTester_dir", numbered=True)
        self._write_fake_job_output(tmp_path, contents, out_files)
        job.id = 1
        job._state = State.RUNNING

        # act
        job.parse_result(tmp_path)

        # assert
        assert isinstance(
            job.result, _ResultBase
        ), "job.result is not a Job.Result object"
        for key, expected_data in expected_result.items():
            if not hasattr(job.result, key):
                raise AssertionError(
                    f'job.result does not contain key "{key}"'
                )

            data = job.result[key]

            if isinstance(data, (np.ndarray, np.dtype, int, float, complex)):
                if data != pytest.approx(expected_data, rel=rtol, abs=atol):
                    raise AssertionError(
                        f'job.result["{key}"] != '
                        f'pytest.approx(expected_result["{key}"], rel={rtol}, '
                        f'abs={atol})\n where job.result["{key}"]='
                        f'\n{job.result[key]}\n and expected_result["{key}"]='
                        f"\n{expected_data}"
                    )
            else:
                if data != expected_data:
                    raise AssertionError(
                        f'job.result["{key}"] != '
                        f'expected_result["{key}"]\n where job.result["{key}"]'
                        f'=\n{job.result[key]}\n and expected_result["{key}"]='
                        f"\n{expected_data}"
                    )

        # complex check for single attribute using 'checkers' functions
        if checkers is not None:
            for key, checker in checkers.items():
                if not checker(job.result[key]):
                    raise AssertionError(
                        f'Result with key "{key}" failed '
                        f"check. Current value: {job.result[key]}"
                    )

        # test the job result object:
        result = job.result

        # the result of any job should be a job.Result object
        assert isinstance(
            result, _ResultBase
        ), f"Invalid type: Expected job.Result, got {type(result).__name__}."

        # check if the result object is picklable
        try:
            _ = pickle.dumps(result)
        except pickle.PickleError as e:
            raise AssertionError(
                "The result object of the job is not picklable"
            ) from e


class _DummyJobSystem(JobSystem):
    """Very basic job system where every job finishes immediately

    You can provide a hook that is called on submission after the id is set.

    :param on_submit: function that is called with job and wait_for on
                      submission
    """

    def __init__(
        self,
        dir: os.PathLike,
        on_submit: Optional[
            Callable[[JobSystem, Job, Optional[Iterable[int]]], Any]
        ],
    ) -> None:
        super().__init__(dir)

        self.on_submit = on_submit

    def _submit(self, job: Job, wait_for: Optional[Iterable[int]] = None):
        if self.on_submit is not None:
            self.on_submit(self, job, wait_for)

        return job.id

    def _check_finished(
        self, ids: Iterable[int]
    ) -> list[tuple[bool, Failure | None]]:
        # all jobs are already done, so always return True
        return [(True, None) for job_id in ids]

    def _save_resources(self, job: Job):
        job.resources.cpu_time = None
        job.resources.memory = None
        job.resources.n_cpus = None


# define T as general type that can be any subtype of Investigation
T = TypeVar("T", bound=Investigation)


class InvestigationTestCase(ABC, Generic[T]):
    """
    Utility class to simplify testing investigations. This function adds
    additional functionality into certain methods in the investigation and job
    mechanism to insert tests automatically.

    To create a test case for your investigation, simply create a Test... class
    and inherit from InvestigationTestCase. Then you need to set the class
    variables ``JOB_INPUT_PATH``, ``JOB_OUTPUT_PATH`` and ``STEPS``. In
    addition, you need to provide the fixture ``investigation``.
    ``investigation`` creates and returns the investigation that should be
    tested. A fixture called
    ``inves_context`` is provided by InvestigationTestCase and returns the
    InvestigationContext instance.
    The fixture ``context_managers`` is optional and can be overridden if the
    specific test case requires it. By default, it returns an empty dictionary.

    .. code::

        class TestMyInvestigation(InvestigationTestCase[MyInvestigation]):
            JOB_INPUT_PATH =  'path/to/job/input/files'
            JOB_OUTPUT_PATH = 'path/to/job/output/files'
            STEPS = ['do_some_thing', 'do_next_thing']

            @pytest.fixture
            def context_managers(self, tmp_path) -> Mapping[ContextManager]:
                return {'species_db': SpeciesDB(tmp_path/'db.sqlite')}

            @pytest.fixture
            def investigation(self, inves_context: InvestigationContext)\\
                    -> MyInvestigation:
                return MyInvestigation(initial_data=42)


    The investigation is run almost like in a real system, only that no jobs
    are submitted. Instead, the job input files that are created can be
    compared to
    expected input files and the output files that are provided are copied into
    the right folder for the investigation to work.
    All you need to do is to supply the expected job input files and the needed
    output generated by the jobs.
    The investigation will be started automatically and it is checked whether
    the steps in ``STEPS`` are executed in the given order. Furthermore, you
    can add functions following the naming scheme:
    ``step_X(self, investigation)``. If such a function exists, it is executed
    after step number X (starting at zero)
    and can be used to assert that the member variables of the tested
    investigation were set correctly.

    .. code::

        class TestMyInvestigation(InvestigationTestCase[MyInvestigation]):
            ...

            def step_1(self, inves: MyInvestigation):
                \'\'\'will be run after the second step is run.\'\'\'
                assert inves.some_property == 10.0

    """

    JOB_INPUT_PATH: ClassVar[os.PathLike | None] = None
    """Path to the directory containing the expected input files.

    "expected files" means that the investigation is expected to create
    those files by submitting jobs. The content of the expected files is
    checked against the actual files that are created by the investigation.
    The directory must be structured as follows:

        JOB_INPUT_PATH/
            step_0/
                job_0/
                job_1/
            step_1/
                job_0/
                ...

    Here, step_X/job_Y contains the expected files for the Y-th job that is
    submitted during the X-th step of the investigation test case.
    """

    JOB_OUTPUT_PATH: ClassVar[os.PathLike | None] = None
    """Path to the directory containing the job output files.

    Since the jobs are not actually executed during testing, the output
    files are not generated. Hence they have to be supplied via this
    directory. They will be parsed by the respective job objects s.t. the
    investigation being tested can simply access the job objects result
    member variable to get the correct data for the test case.
    The directory must be structured as follows:

        JOB_OUTPUT_PATH/
            step_0/
                job_0/
                job_1/
            step_1/
                job_0/
                ...

    Here, step_X/job_Y contains the output files for the Y-th job that is
    submitted during the X-th step of the investigation test case.
    """

    WORKSPACE: Union[str, os.PathLike] = "__tmp__"
    """Directory in which the investigations and jobs are stored and executed,
    when this test case is run. By default, a temporary directory is created
    and will be deleted after testing. But when
    this variable points to a path, that path will be used allowing the
    developer to inspect the files creating during the test."""

    STEPS: ClassVar[list[str]]
    """list of function names of the tested investigations in the order
    they are executed for this test case
    """

    _MAX_JOBSYS_REFRESH: int = 50
    """When executing the test case, jobsystem.refresh() will be called in a
    loop that does at most this many interations. This number should be big
    enough for most investigations. For very large investigations, this number
    can be increased.
    """

    TMP_PATH_FACTORY = None
    """variable that is set by pytest to a function that creates a temporary
    directory once the test session begins
    """

    @pytest.fixture(autouse=True)
    def set_sleep_timer_to_zero(self):
        """do not wait several seconds between each call to refresh()"""
        with patch.object(InvestigationRunner, "SLEEP_TIMER", new=0):
            yield

    @pytest.fixture(autouse=True)
    def remove_save_checkpoint(self):
        """do not pickle the investigation in run()"""
        with patch.object(InvestigationContext, "save_checkpoint"):
            yield

    def run_next_step_decorator(self, run_next_step_func):
        @functools.wraps(run_next_step_func)
        def wrapper(*args, **kwargs):
            try:
                expected_name, assertion = self._steps[self._current_step+1]

            # the current step counter is increased after each step, so a
            # value error will be raised when executing more steps than
            # defined in self._steps (or STEPS, respectively)
            except ValueError:
                raise AssertionError(
                    "The investigation is trying to execute step "
                    f"{self._current_step}, but only {len(self._steps)} steps "
                    "were defined for this test case in self.STEPS."
                )

            # steps should be methods of the investigations that use them
            investigation: Investigation = run_next_step_func.__self__

            # check name
            actual_next_step = investigation.tell_next_step()
            if actual_next_step != expected_name:
                raise AssertionError(
                    "Unexpected next step.\nExpected: "
                    f"{expected_name}\nActual: {actual_next_step}"
                )

            # increase current step counter before execution such that jobs
            # submitted in the current step and those submitted by other
            # investigations submitted in the current step get the same current
            # step number
            self._current_step += 1
            self._current_job = 0

            # run the actual _run_next_step()
            run_next_step_func(*args)

            if assertion is not None:
                assertion(investigation)
                investigation._logger.debug(
                    "No assertion failed for step" ' %d "%s"',
                    self._current_step,
                    expected_name,
                )


        return wrapper

    def jobsystem_on_submit(
        self, jobsys: JobSystem, job: Job, *args, **kwargs
    ):
        """used to decorate JobSystem.submit() to add testing functionality."""

        logging.debug(
            "Submitted %s with job id = %d", type(job).__name__, job.id
        )

        # check that it created the input files as expected
        job_dir = pathlib.Path(jobsys.get_job_dir(job.id))
        expected_files = pathlib.Path(
            self.JOB_INPUT_PATH,
            f"step_{self._current_step}",
            f"job_{self._current_job}",
        )

        if expected_files.exists():
            JobTester.assert_job_dir_contains_expected_files(
                job_dir, expected_files=expected_files
            )
        else:
            logging.info(
                "No expected input files for job %d. Directory "
                "%s/step_%d/job_%d not found.",
                job.id,
                str(self.JOB_INPUT_PATH),
                self._current_step,
                self._current_job,
            )

        # create the output as if the job did it:
        output_files = pathlib.Path(
            self.JOB_OUTPUT_PATH,
            f"step_{self._current_step}",
            f"job_{self._current_job}",
        )

        if output_files.exists():
            copytree(str(output_files), str(job_dir), dirs_exist_ok=True)
        else:
            logging.info(
                "No output files for job %d supplied. Directory "
                "%s/step_%d/job_%d not found.",
                job.id,
                str(self.JOB_OUTPUT_PATH),
                self._current_step,
                self._current_job,
            )

        self._current_job += 1

    @pytest.fixture
    def _set_up(self, tmp_path_factory):
        self._current_job = 0  # counts jobs submitted during the current step
        self._current_step = -1 # will be increased before executing step
        self._steps: list[tuple[str, Callable[[T], None]]] = []
        # store this as attribute, so that others can access it more easily:
        self.tmp_path_factory = tmp_path_factory

        self.JOB_OUTPUT_PATH = (
            tmp_path_factory.mktemp("job_output")
            if self.JOB_OUTPUT_PATH is None
            else self.JOB_OUTPUT_PATH
        )

        self.JOB_INPUT_PATH = (
            tmp_path_factory.mktemp("job_input")
            if self.JOB_INPUT_PATH is None
            else self.JOB_INPUT_PATH
        )

        user_defined_assertions = {
            attr
            for attr in dir(self)
            if attr.startswith("step_") and callable(getattr(self, attr))
        }

        # fill _steps with tuples containing the name of the method of the
        # investigation object and an assertion function (that can be defined
        # by the user)
        for i, step in enumerate(self.STEPS):
            if f"step_{i}" in user_defined_assertions:
                self._steps.append((step, getattr(self, f"step_{i}")))
            else:
                self._steps.append((step, None))

    @pytest.fixture()
    def inves_context(
        self, context_managers, tmp_path_factory
    ) -> InvestigationContext:
        if self.WORKSPACE == "__tmp__":
            path: pathlib.Path = tmp_path_factory.mktemp("tmp")
        else:
            path = pathlib.Path(self.WORKSPACE)
            if [_ for _ in path.iterdir()]:
                raise FileExistsError(
                    "The test case workspace directory is not empty: "
                    + str(path)
                )

        with InvestigationContext(
            path=path / "investigations.pickle",
            jobsystem=_DummyJobSystem(
                path / "jobs", on_submit=self.jobsystem_on_submit
            ),
            context_mgrs=context_managers,
            # let all exceptions pass through instead of just failing
            # failing the investigation
            fail_deadly=True,
        ) as context:
            yield context

    def test_investigation(
        self,
        _set_up,
        inves_context: InvestigationContext,
        investigation: Investigation,
        request,
    ):
        """this is the test function that will be executed by pytest"""
        context = inves_context

        # decorate the investigations _run_next_step method
        original_run_func = investigation.run_next_step
        investigation.run_next_step = self.run_next_step_decorator(
            original_run_func
        )

        try:
            context.inves_mgr.submit(investigation)

            counter = 0

            def is_finished_or_max_refresh_reached(*args, **kwargs):
                nonlocal counter, investigation
                counter += 1
                return (
                    counter >= self._MAX_JOBSYS_REFRESH
                    or investigation.is_finished
                )

            context.runner.run(until=is_finished_or_max_refresh_reached)

            if counter >= self._MAX_JOBSYS_REFRESH:
                raise AssertionError(
                    "Maximum number of iterations reached: "
                    f"{self._MAX_JOBSYS_REFRESH}.\nIf this error is raised, "
                    "because your investigation contains a lot of steps, you "
                    "could increase _MAX_JOBSYS_REFRESH, but you should also "
                    "consider splitting the investigation into several smaller"
                    " ones."
                )

            if self._current_step+1 < len(self.STEPS):
                raise AssertionError(
                    f"Investigation finished, but not all steps have been "
                    "executed. The next expected step "
                    f'is "{self.STEPS[self._current_step+1]}". '
                    "This may be due to an error. Try using --log-level debug "
                    "to get more information."
                )

        # undo everything to the context can be closed witout problems
        finally:
            investigation.run_next_step = original_run_func

    @pytest.fixture
    def context_managers(self) -> dict[str, Any]:
        """returns a dictionary with the context managers that the
        investigation needs"""
        return {}

class CLITestCase(ABC, Generic[T]):
    """Base class for testing command line interfaces.

    This class provides a testing framework for checking command line
    interfaces, including argument parsing, configuration handling,
    investigation creation, and result processing.

    To use this class, inherit from it and implement required methods and
    attributes.

    Required Class Attributes:
        :attr:`CLI_CONFIG_PATH`:
            Path to test configuration file
        :attr:`CLI_ARGS`:
            Command line arguments
        :attr:`INVESTIGATION_RESULT`:
            Expected investigation result
        :attr:`INVESTIGATION_DEPENDENCIES`:
            Dependencies of investigation (optional)

    Required Methods:
        :attr:`cli_class`:
            Property that must return CLI class to test
        :meth:`test_investigation`:
            Test investigation instance after creation
        :meth:`test_postprocessing`:
            Test results after postprocessing
        :meth:`pre_postprocessing`:
            Set up test data for postprocessing

    .. note::

        The :attr:`cli_class` property must return the non instantiated
        CLI class.

    .. code::

        class TestMyInvestigationCLI(CLITestCase[MyInvestigationCLI]):

            CLI_CONFIG_PATH = Path('test_data/config.toml')
            CLI_ARGS = ['input.xyz', '--charge', '0']
            INVESTIGATION_RESULT = MyInvestigation.Result(energy=-76.34)
            INVESTIGATION_DEPENDENCIES = {'species_db': SpeciesDB}

            @property
            def cli_class(self):
                return MyInvestigationCLI

            @pytest.fixture
            def pre_postprocessing(
                self, investigation, investigation_context
            ):
                # Add test data to database for postprocessing test
                db = investigation_context["my_db"]
                geometry = Geometry.from_xyz_file("my_molecule.xyz")
                geo_id = db.save_geometry(
                                        None,
                                        geometry,
                                        lot=LevelOfTheory(...),
                                        ...
                )

            def test_investigation(self, investigation):
                assert isinstance(investigation, MyInvestigation)
                assert investigation.my_property == 0

            def test_postprocessing(self, postprocessing):
                (
                investigation,
                investigation_context,
                investigation_config
                ) = postprocessing

                output_file = investigation_config.cmd.workspace
                / 'output.json'
                assert output_file.exists()
                with open(output_file) as f:
                    data = json.load(f)
                assert data['my_result'] == expected_value
    """

    CLI_CONFIG_PATH: ClassVar[pathlib.Path] = None
    """Path to config file for CLI"""

    CLI_ARGS: ClassVar[list[str]] = []
    """List of command line arguments to pass to CLI"""

    INVESTIGATION_DEPENDENCIES: ClassVar[dict] = {}
    """Expected dependencies of investigation"""

    INVESTIGATION_RESULT: ClassVar[Investigation.Result | None] = None
    """Expected result of investigation"""

    # -----------------------------------------
    # Helpers
    # -----------------------------------------

    @staticmethod
    def assert_configs_equal(
        original: ConfigBase | CmdArgsBase | Any,
        loaded: ConfigBase | CmdArgsBase | Any,
    ) -> None:
        """
        Asserts two pydantic config models are equal. Removes the cmd args
        since those can change on resume (serialization /
        desserializtation).
        """

        # Remove cmd args since they change on resume
        original.cmd = None
        loaded.cmd = None

        # Dump to string since arrays and other objects are not comarable
        # (ambigious error message)
        original_dict = original.model_dump(mode="json")
        original_dict_str = {f"{k}": f"{v}"
                             for k, v in original_dict.items()}

        loaded_dict = loaded.model_dump(mode="json")
        loaded_dict_str = {f"{k}": f"{v}"
                             for k, v in loaded_dict.items()}

        assert original_dict_str == loaded_dict_str, ("Config models are"
                                                      "not equal after"
                                                      "resuming.")

    @staticmethod
    def __create_patched_start(
            cli: CommandLineInterface,
            postprocessing: bool = False,
            predefined_investigation: Investigation = None,
    ) -> Callable[[list[str] | None], tuple[
        Investigation, InvestigationContext, ConfigT]]:
        """Creates a patched CLI start method for testing.

        :param cli: CLI instance to patch
        :param postprocessing: Enable postprocessing mode, defaults to False
        :param predefined_investigation: Mock investigation for postprocessing
            tests, defaults to None
        :return: Patched start method that returns (investigation, context,
            config) tuple
        :raises ValueError: If postprocessing=True without
            predefined_investigation
        """
        if postprocessing and predefined_investigation is None:
            raise ValueError(
                "Investigation must be provided for postprocessing")

        original_start_method = cli._CommandLineInterface__start
        original_load_config_method =(
            cli._CommandLineInterface__load_and_validate_config
        )

        extracted = {
            'investigation': None,
            'context': None,
            'config': None,
        }

        def submit_inves_side_effect(ctx: InvestigationContext, cfg):
            extracted.update({
                'investigation': cli.create_investigation(ctx, cfg),
                'context': ctx,
                'config': cfg
            })

            ctx.inves_mgr._investigations = [extracted['investigation']]

        def load_config_side_effect(args):
            if (cfg := original_load_config_method(args)[0]):
                extracted.update({'config': cfg})
                return cfg, postprocessing
            else:
                return None, postprocessing

        def postprocessing_side_effect(ctx, cfg):
            return cli.postprocessing(predefined_investigation, cfg)

        def patched_start(
                argv: list[str] | None
        ) -> tuple[Investigation, InvestigationContext, ConfigT]:
            """Patched start method for testing."""
            with (patch.multiple(  # Patch CLI methods
                    cli,
                    _CommandLineInterface__submit_inves=MagicMock(
                        side_effect=submit_inves_side_effect,
                    ),
                    _CommandLineInterface__schedule_restart=MagicMock(
                    ),
                    _CommandLineInterface__postprocessing=MagicMock(
                        side_effect=postprocessing_side_effect,
                    ),
                    _CommandLineInterface__load_and_validate_config=MagicMock(
                        side_effect=load_config_side_effect,
                    ),
            ),
            patch.multiple(  # Patch zero finished engine level
                'chemtrayzer.engine.cmdtools',
                investigation_zero_finished=MagicMock(
                    return_value=postprocessing),
            ),
            patch(  # Patch zero finished investigation level
                'chemtrayzer.engine.investigation.investigation_zero_finished',
                return_value=postprocessing
            ),
            patch(
                'chemtrayzer.engine.investigation.InvestigationRunner.run',
                new_callable=MagicMock
            )):
                original_start_method(argv)  # Run start with patches

            return (extracted['investigation'],
                    extracted['context'],
                    extracted['config'])

        return patched_start

    # -----------------------------------------
    # Fixtures
    # -----------------------------------------

    @pytest.fixture
    def cli(self):
        """Creates CLI instance with patched start method"""
        cli = self.cli_class(script="__test__.py", debug_mode=True)
        cli._CommandLineInterface__start = CLITestCase.__create_patched_start(
            cli, postprocessing=False, predefined_investigation=None
        )
        return cli

    @pytest.fixture
    def run_cli(
        self, tmp_path_factory, cli: CommandLineInterface,
        workspace_path
    ) -> tuple[Investigation, InvestigationContext, ConfigT]:
        """Runs a patched CLI instance up to investigation creation"""
        # Construct full command
        full_args = [
            "__test__.py",  # Script name
            str(workspace_path),  # Workspace path
            *self.CLI_ARGS,  # Additional CLI-specific args defined by user
            "--config",  # Config file
            str(self.CLI_CONFIG_PATH.resolve()),
            "--loglevel",  # Log level
            "debug",
            "--jobsystem",  # Use blocking jobsystem
            "blocking",
        ]
        # Run CLI up to investigation creation
        inves, context, config = cli.start(full_args)
        return inves, context, config

    @pytest.fixture
    def investigation(
        self, run_cli: tuple[Investigation, InvestigationContext, ConfigT]
    ) -> Investigation:
        """
        :return: Investigation instance created by patched CLI
        """
        investigation, _, _ = run_cli
        return investigation

    @pytest.fixture
    def investigation_context(
        self, run_cli: tuple[Investigation, InvestigationContext, ConfigT]
    ) -> InvestigationContext:
        """
        :return: investigation context created by patched CLI
        """
        _, investigation_context, _ = run_cli
        with investigation_context:
            yield investigation_context


    @pytest.fixture
    def investigation_config(
        self, run_cli: tuple[Investigation, InvestigationContext, ConfigT]
    ) -> ConfigT:
        """
        :return: investigation config created by patched CLI
        """
        _, _, config = run_cli
        return config

    @pytest.fixture
    def workspace_path(self, tmp_path_factory):
        """Path to workspace directory"""
        return tmp_path_factory.mktemp("workspace")

    @pytest.fixture
    def postprocessing(
        self,
        tmp_path_factory,
        investigation_config: ConfigT,
        workspace_path,
        pre_postprocessing: tuple[Investigation, InvestigationContext],
    ) -> tuple[Investigation, InvestigationContext, ConfigT]:
        """Sets up and executes CLI postprocessing with mock
        investigation result.

        :raises ValueError: If `INVESTIGATION_RESULT` is not defined
        """
        if not hasattr(self, "INVESTIGATION_RESULT"):
            raise ValueError(
                "Test class must define INVESTIGATION_RESULT with expected"
                "investigation result"
            )

        if not pre_postprocessing or len(pre_postprocessing) != 2:
            raise ValueError(
                "The Pre-Postprocessing Fixture has to return Investigation"
                " and the InvestigationContext."
            )
        # Set Result, context and state
        (
            pre_postprocessed_investigation,
            pre_postprocessed_investigation_context
        ) = pre_postprocessing

        # no investigation is actually submitted, but the CLI checks this
        pre_postprocessed_investigation_context.inves_mgr._investigations = [
            pre_postprocessed_investigation
        ]

        pre_postprocessed_investigation.result = self.INVESTIGATION_RESULT
        pre_postprocessed_investigation.context = (
            pre_postprocessed_investigation_context
        )
        pre_postprocessed_investigation.id = 0
        pre_postprocessed_investigation._state = State.RUNNING
        pre_postprocessed_investigation._state = State.SUCCESSFUL
        # Patched Start
        cli = self.cli_class(script="__test__.py", debug_mode=True)
        cli._CommandLineInterface__start = self.__create_patched_start(
            cli,
            postprocessing=True,
            predefined_investigation=pre_postprocessed_investigation
        )
        # Construct full command
        full_args = [
            "__test__.py",  # Script name
            str(workspace_path),  # Workspace path
            *self.CLI_ARGS,  # Additional CLI-specific args defined by user
            "--config",  # Config file
            str(self.CLI_CONFIG_PATH.resolve()),
            "--loglevel",  # Log level
            "debug",
            "--jobsystem",  # Use blocking jobsystem
            "blocking",
        ]
        # Run patched CLI for prostprocessing
        inves, context, config = cli.start(full_args)
        return inves, context, config

    # -----------------------------------------
    # User Properties / Fixtures / Test methods
    # -----------------------------------------

    @property
    def cli_class(self) -> type[CommandLineInterface]:
        """Returns CLI class to test. Must be implemented by child classes.

        :return: CLI class to instantiate and test (not instance)

        .. code::

            class TestMyInvestigationCLI(CLITestCase[MyInvestigationCLI]):
                @property
                def cli_class(self):
                    return MyInvestigationCLI
        """

        raise NotImplementedError(
            "The test case for the command line interface must implement "
            "cli_class property"
        )

    @pytest.fixture
    def pre_postprocessing(
            self,
            investigation: Investigation,
            investigation_context: InvestigationContext
    ) -> tuple[Investigation, InvestigationContext]:
        """Set up test data before postprocessing. Must be implemented by
        child classes.

        Sets up databases and context managers with mock data that would
        normally be created during investigation execution.
        Additionally the Investigation with the already set result and
        ran successful state is provided for further adaption if needed.
        The Fixture must return at least the unaltered investgiation and
        investigation context.

        :param investigation: Successful Investigation with set Result
        :param investigation_context: Opened Investigation context

        :return investigation, investigation_context: Tuple with the updated
            investigation and context

        .. code::

            @pytest.fixture
            def pre_postprocessing(self, investigation_context):
                db = investigation_context['my_db']
                geometry = Geometry.from_xyz_file('test.xyz')
                geo_id = db.save_geometry(None, geometry, lot=geo_lot)
        """

        return investigation, investigation_context

    def test_investigation(self, investigation: Investigation):
        """Validate investigation after creation but before submission.
        Can be implemented by child classes.

        :param investigation: Investigation instance created by CLI

        .. code::

            def test_investigation(self, investigation: MyInvestigation):
                assert isinstance(investigation, MyInvestigation)
                assert investigation.my_property is not None
                assert investigation.options.option_1 == expected
        """

        pass

    def test_investigation_context(
        self, investigation_context: InvestigationContext
    ):
        """Test investigation context after creation. Can be implemented by
        child classes

        :param investigation_context: Opened Investigation Context

        .. code::

            def test_investigation_context(self, investigation_context):
                assert 'my_db' in investigation_context
                db = investigation_context['my_db']
                assert isinstance(db, DatabaseInstance)
    """

        pass

    def test_postprocessing(self, postprocessing):
        """Validate results after postprocessing has completed. Can be
        implemented by child classes

        :param postprocessing:
            Fixture with investigation, context, and config after
            postprocessing

        .. code::

            def test_postprocessing(self, postprocessing):
                investigation, context, config = postprocessing
                output_file = config.cmd.workspace / 'output.log'
                assert output_file.exists()
                assert 'Optimization complete' in output_file.read_text()
        """

        pass

    # -----------------------------------------
    # Built in Tests
    # -----------------------------------------

    def test_dependencies(self, investigation_context: InvestigationContext):
        """Tests that CLI properly creates investigation dependencies."""
        if not hasattr(self, "INVESTIGATION_DEPENDENCIES"):
            return
        investigation_context.check_dependencies(
            self.INVESTIGATION_DEPENDENCIES
        )

    def test_missing_config(self, tmp_path_factory, cli: CommandLineInterface):
        """Tests that CLI properly handles missing config argument"""
        workspace = tmp_path_factory.mktemp("workspace")
        # command without config
        args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        with pytest.raises((IllegalConfigError, ConfigLoaderError)):
            cli.start(args)

    def test_invalid_config_path(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles invalid config path"""
        workspace = tmp_path_factory.mktemp("workspace")
        # command with nonexistent config file
        args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            "nonexistent_config.toml",
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        with pytest.raises(
            ConfigLoaderError, match="Could not find config file"
        ):
            cli.start(args)

    def test_missing_required_args(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles missing required
        investigation-specific arguments
        """
        workspace = tmp_path_factory.mktemp("workspace")
        # command without CLI specific cmd args
        args = [
            "__test__.py",
            str(workspace),
            "--config",
            str(self.CLI_CONFIG_PATH),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        # Missing Arguments lead to different exceptions
        # depending on the CLI implementation
        with pytest.raises((SystemExit, IllegalConfigError)) as excinfo:
            cli.start(args)
            if isinstance(excinfo.value, SystemExit):
                assert excinfo.value.code == 2

    def test_invalid_command(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles invalid start/resume command"""
        workspace = tmp_path_factory.mktemp("workspace")
        # invalid command
        args = [
            "__test__.py",
            "invalid_command",  # Invalid command
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(self.CLI_CONFIG_PATH),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        # Should raise SystemExit with exit code 2
        # (indicating incorrect usage)
        with pytest.raises(SystemExit) as excinfo:
            cli.start(args)
        assert excinfo.value.code == 2

    def test_empty_config(self, tmp_path_factory, cli: CommandLineInterface):
        """Tests that CLI properly handles an empty config file"""
        workspace = tmp_path_factory.mktemp("workspace")
        # empty config file
        empty_config = workspace / "empty.toml"
        empty_config.write_text("")
        args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(empty_config),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        with pytest.raises(IllegalConfigError):
            cli.start(args)

    def test_malformed_config(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles an invalid config file"""
        workspace = tmp_path_factory.mktemp("workspace")
        # invalid config file
        invalid_config = workspace / "invalid.toml"
        invalid_config.write_text("invalid")
        args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(invalid_config),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        with pytest.raises(ConfigLoaderError):
            cli.start(args)

    def test_invalid_config_fields(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles an invalid config file"""
        workspace = tmp_path_factory.mktemp("workspace")
        # invalid config file
        invalid_config = workspace / "invalid.toml"
        invalid_config.write_text("""
            [some_section]
            some_option = "seom_value"
            """)
        args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(invalid_config),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        with pytest.raises(IllegalConfigError):
            cli.start(args)

    def test_resume(self, tmp_path_factory, cli: CommandLineInterface):
        """Tests that configuration is properly serialized and loaded when
        resuming an investigation
        """
        workspace = tmp_path_factory.mktemp("workspace")
        # initial command with initial config
        first_args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(self.CLI_CONFIG_PATH.resolve()),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        # create cli -> serialize config
        investigation, context, initial_config = cli.start(first_args)
        # Verify config was serialized
        CONFIG_POS = "chemtrayzer.engine.cmdtools"
        _CONFIG_DIR = "config"
        config_file = workspace / _CONFIG_DIR / CONFIG_POS
        assert config_file.exists(), "Config file was not created"
        # resume arguments are the same as the start arguments
        resume_args = first_args
        # resume cli
        resumed_investigation, resumed_context, loaded_config = cli.start(
            resume_args
        )
        # Compare inital and loaded configs
        self.assert_configs_equal(initial_config, loaded_config)

    def test_invalid_resume_args(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that CLI properly handles invalid resume arguments"""
        workspace = tmp_path_factory.mktemp("workspace")
        # resume with config argument
        invalid_resume_args = [
            "__test__.py",
            str(workspace),
            "--config",
            str(self.CLI_CONFIG_PATH),
            "--loglevel",
            "debug",
        ]
        # Depending on the CLI implementation, this should raise
        # either SystemExit or IllegalConfigError
        with pytest.raises((SystemExit, IllegalConfigError)) as excinfo:
            cli.start(invalid_resume_args)
            if isinstance(excinfo.value, SystemExit):
                assert excinfo.value.code == 2

    def test_resume_with_modified_config_file(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """Tests that modifications to original config file don't affect
        resume"""

        workspace = tmp_path_factory.mktemp("workspace")
        # initial config
        first_args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(self.CLI_CONFIG_PATH.resolve()),
            "--loglevel",
            "debug",
            "--jobsystem",
            "blocking",
        ]
        investigation, context, initial_config = cli.start(first_args)
        modified_config = workspace / "modified_config.toml"
        with open(self.CLI_CONFIG_PATH, "r") as f:
            config_content = f.read()
        modified_content = config_content + "\n# Modified content\n"
        modified_config.write_text(modified_content)
        resume_args = first_args
        resumed_investigation, resumed_context, loaded_config = cli.start(
            resume_args
        )
        self.assert_configs_equal(initial_config, loaded_config)

    def test_resume_with_modified_cmd_args(
        self, tmp_path_factory, cli: CommandLineInterface
    ):
        """
        Tests that command line arguments can be changed during resume
        """
        workspace = tmp_path_factory.mktemp("workspace")
        # original arguments
        first_args = [
            "__test__.py",
            str(workspace),
            *self.CLI_ARGS,
            "--config",
            str(self.CLI_CONFIG_PATH.resolve()),
            "--loglevel",
            "info",  # Original log level
            "--jobsystem",
            "blocking",
        ]
        investigation, context, initial_config = cli.start(first_args)
        # resume arguments are the same as the start arguments
        resume_args = first_args
        # change couple of args
        resume_args[resume_args.index("--loglevel") + 1] = "debug"
        resume_args.extend(["--max_autosubmit", "50"])

        resumed_investigation, resumed_context, loaded_config = cli.start(
            resume_args
        )
        assert loaded_config.cmd.log_level.value == "debug"
        assert loaded_config.cmd.max_autosubmit == 50
        self.assert_configs_equal(initial_config, loaded_config)


class DummyResult(Investigation.Result):
    """dummy result class"""

    answer: str = "42"
    """answer to life, the universe and everything"""


class DummyInvestigation(Investigation[DummyResult]):
    """
    Helper class for testing the investigation mechanism.

    Provides a basic implementation of the Investigation class that can be
    customized for each test case by adding the predefined steps. All steps
    log their arguments to the history attribute.

    .. code::python
        def test_my_investigation():
            mock_job = MockJob()
            inves= DummyInvestigation(waitables=[mock_job])

            # an investigation with three teps
            inves.add_step(inves.do_nothing)
            inves.add_step(inves.submit_waitables)
            inves.add_step(inves.finish_by_failing)

            # now you can use inves in your tests
            ...

            # after the test, you can check the history of the investigation
            assert inves.history == [('do_nothing', ()),
                                     ('submit_waitables', ()),
                                     ('finish_by_failing', (mock_job,))]

    :param waitables: jobs or investigations that will be submitted by
                      submit_waitables()
    :param mock_job_factory: mock_job_factory fixture
    :param provided_result: result that will be set by the set_result() step,
                            If not set, DummyInvestigation.Result will be
                            initialized with default values
    :ivar history: stores the steps that were called and the arguments
    :type history: tuple[str, tuple(Any)]
    """


    def __init__(
        self,
        waitables: Iterable[Union[Job, Investigation]] = None,
        provided_result: Result = None,
        target: str = None,
    ) -> None:
        super().__init__(target=target)

        self.provided_result = provided_result
        if provided_result is None:
            self.provided_result = DummyResult()

        # stores the steps that were called and the arguments
        self.history: tuple[str, tuple(Any)] = []

        if waitables is not None:
            self.waitables = waitables
        else:
            self.waitables = []

    def update(self, event):
        """just used for logging incoming events"""
        self._logger.debug(f"Update called with event: {event}")
        return super().update(event)

    def set_result(self, *args):
        """sets the result to the provided result"""
        self.history.append(("set_result", args))

        self.result = self.provided_result

    def finish_successfully(self, *args):
        """finishes the investigation successfully"""
        self.history.append(("finish_successfully", args))

        self._state = State.SUCCESSFUL

    def finish_by_failing(self, *args):
        """finishes the investigation by failing"""
        self.history.append(("finish_by_failing", args))

        self.fail("Test failure")

    def do_nothing(self, *args):
        """just an empty step that logs its arguments"""
        self.history.append(("do_nothing", args))

    def submit_waitables(self, *args):
        """submits all waitables passed to the constructor"""
        self.history.append(("submit_waitables", args))

        for obs in self.waitables:
            self.wait_for_and_submit(obs)

    def raise_error(self, *args):
        """raises an error"""
        self.history.append(("raise_error", args))

        raise InvestigationError("Hi, I am an error :)")

    def submit_waitables_but_finish(self, *args):
        """
        Submits all waitables passed to the constructor and then finishes.
        Only used to test that this behavior is not allowed."""
        self.history.append(("submit_waitables_but_finish", args))

        for obs in self.waitables:
            self.wait_for_and_submit(obs)

        self.succeed()

    def wait_forever(self, *args):
        """appends"""
        self.history.append(("wait_forever", args))

        # submit a mock job, that never finishes
        self.wait_for_and_submit(DummyJob())


@pytest.fixture(scope="session")
def prepare_test_inves_class(tmp_path_factory):
    InvestigationTestCase.TMP_PATH_FACTORY = tmp_path_factory


class BatchCmdOptions(CmdArgsBase):
    submittables_file: pathlib.Path
    pickle_path: pathlib.Path | None = None

    @field_validator("submittables_file")
    @classmethod
    def _validate_submittables_file(cls, submittables_file: pathlib.Path):
        if not submittables_file.exists():
            raise ValueError(f'"{submittables_file}" not found')
        if not submittables_file.is_file():
            raise ValueError(f'"{submittables_file}" is not a file.')

        return submittables_file


class BatchOptions(ConfigBase):
    cmd: BatchCmdOptions


class BatchCLI(CommandLineInterface[BatchInvestigation, BatchOptions]):
    """Executes one or more jobs or investigations.

    This class is meant to be used for testing purposes. The user needs to
    provide job or investigation objects in a Python file (here called
    `my_file.py`):

    .. code::python

        job1 = MyJob(some_arg=42)
        job2 = MyJob(some_arg=43)
        inves = MyInvestigation()

        SUBMITTABLES = [job1, job2, inves]
        ...

    All jobs and investigations in the SUBMITTABLES variable will be submitted
    and executed. The user can optionally provide a POSTPROCESSORS variable
    that contains a list of executables that will be executed after all
    submittables have finished.

    .. code::python

        ...
        # very simple example functions to print all of the results
        def print_job_output(is_successful, job_result):
            if is_successful:
                print('Job finished successfully')
            else:
                print('Job failed')
            print(job_result)

        def print_inves_output(is_successful: bool, inves_result):
            print(inves_result)

        # We need to supply three postprocessors for the three submittables
        POSTPROCESSORS = [print_job_output, print_job_output,
                          print_inves_output]
        ...

    Now, we can execute the two jobs and the investigation by calling
    ``chemtrayzer test my_file.py``. In addition, we can supply
    context_managers to the investigation, e.g., databases by adding the
    ``CONTEXT_MGRS``
    variable:

    .. code::python

        # if an investigation expects a SpeciesDB under the name "species_db"
        # we could supply it like this:
        CONTEXT_MGRS = {'species_db': SpeciesDB('path/to/dbfile')}
    """

    CONFIG_MODEL = BatchOptions

    def __init__(
        self,
        script: PathLike | str,
        debug_mode: bool = False,
        prog: str | None = None,
    ) -> None:
        self.__imported: Mapping[str, ModuleType] = dict()
        super().__init__(script, debug_mode, prog)

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        parser.add_argument(
            "submittables_file",
            help="*.py file containing a SUBMITTABLES variable which is an "
            "iterable of jobs or investigations that should be submitted."
            "Optionally, it can contain an iterable POSTPROCESSORS of "
            "executables  that do the postprocessing of jobs and "
            "investigaiton results.",
            action="store",
            metavar="SUBMITTABLES_FILE",
            type=pathlib.Path,
        )
        parser.add_argument(
            "--pickle-path",
            help="Path to the pickle file that stores the results of the "
            "submittables. If not given, the results will not be stored.",
            action="store",
            type=pathlib.Path,
            default=None,
            dest="pickle_path",
        )

    def get_context_managers(
        self, config: BatchOptions
    ) -> Mapping[str, AbstractContextManager]:
        f = pathlib.Path(config.cmd.submittables_file)
        sys.path.append(str(f.parent))
        module = self.__import_module(f, f.stem)

        # check if the postprocessors are defined
        if not hasattr(module, "CONTEXT_MGRS"):
            return {}
        else:
            return module.CONTEXT_MGRS

    def __import_module(
        self, module_path: pathlib.Path, name: str
    ) -> ModuleType:
        """imports the module at the given path and returns it"""
        module_path = pathlib.Path(module_path)
        if not module_path.exists():
            raise ValueError(f'Could not find file "{module_path}".')

        # all imported modules are stored by their name to not load them twice
        if name in self.__imported:
            return self.__imported[name]

        spec = importlib.util.spec_from_file_location(name, module_path)
        if spec is None:
            raise ValueError('Could not determine module info for '
                             f'{module_path}".')

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[name] = module

        self.__imported[name] = module
        return module

    def __import_submittables(
        self, submittables_file: pathlib.Path
    ) -> list[Job | Investigation]:
        """imports the submittables from the given file and returns them as a
        list

        :return: list of submittables"""
        submittables_file = pathlib.Path(submittables_file)
        sys.path.append(str(submittables_file.parent))
        module = self.__import_module(
            submittables_file, submittables_file.stem
        )

        # check if the submittables are defined
        if not hasattr(module, "SUBMITTABLES"):
            raise AttributeError(
                f"Module '{submittables_file.name}' has no "
                "attribute 'SUBMITTABLES'"
            )
        submittables = list(module.SUBMITTABLES)

        # check if the submittables are valid
        for submittable in submittables:
            if not isinstance(submittable, Submittable):
                raise AttributeError(
                    "The SUBMITTABLES variable must contain "
                    "instances of Job or Investigation."
                )

        return submittables

    def __import_postprocessors(
        self, submittables_file: pathlib.Path
    ) -> list[Callable] | None:
        """
        :return: list of postprocessors or None, if no postprocessors are
                    defined
        """
        submittables_file = pathlib.Path(submittables_file)
        sys.path.append(str(submittables_file.parent))
        module = self.__import_module(
            submittables_file, submittables_file.stem
        )

        # check if the postprocessors are defined
        if not hasattr(module, "POSTPROCESSORS"):
            return None
        else:
            return list(module.POSTPROCESSORS)

    def __check_postprocessors(
        self, submittables_file: pathlib.Path, n_submittables: int
    ):
        """checks if the postprocessors are valid"""
        postprocessors = self.__import_postprocessors(submittables_file)
        if postprocessors is not None:
            if len(postprocessors) != n_submittables:
                raise ValueError(
                    "If defined, the POSTPROCESSORS variable must "
                    "contain as many elements as the SUBMITTABLES "
                    "variable."
                )

            # check if the postprocessor takes two arguemnts and the first one
            # is a bool
            for postprocessor in postprocessors:
                if not callable(postprocessor):
                    raise ValueError(
                        "The POSTPROCESSORS variable must contain"
                        " callable objects."
                    )
                if not callable(postprocessor):
                    raise ValueError(
                        "The POSTPROCESSORS variable must contain"
                        " callable objects that take two arguments "
                        "of type bool and a job or investigation."
                    )

    def create_investigation(
        self, context: InvestigationContext, config: BatchOptions
    ) -> Any:
        submittables = self.__import_submittables(config.cmd.submittables_file)

        # fail early (before submitting)
        self.__check_postprocessors(
            config.cmd.submittables_file, len(submittables)
        )

        inves = BatchInvestigation(
            inves_and_job_list=submittables,
            pickle_path=config.cmd.pickle_path,
            pickle_results=config.cmd.pickle_path is not None,
        )

        return inves

    def postprocessing(self, inves: BatchInvestigation, config: BatchOptions):
        postprocessors = self.__import_postprocessors(
            config.cmd.submittables_file
        )

        if postprocessors:
            for postprocessor, is_successful, result in zip(
                postprocessors,
                inves.result.success_list,
                inves.result.results_list,
            ):
                postprocessor(is_successful, result)
