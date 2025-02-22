"""Defines the submittable base class used by jobs and investigations
"""
from __future__ import annotations

from dataclasses import field, dataclass
from enum import Enum
import logging
from string import Template
import textwrap
import traceback
from typing_extensions import TypeVar  # backwards compatibility
                                       # typing.TypeVar supports default for
                                       # Python >=3.13
from typing import Any, Generic, Optional, cast
from collections.abc import Iterable

from chemtrayzer.engine.errors import ProgrammingError

#####################################
# id related things
#####################################
class HasId:
    """Mixin class for classes that have an id"""

    def __init__(self):
        super().__init__()
        self.__id: int = None

    @property
    def id(self) -> int|None:
        """Get the id of the submittable"""
        return self.__id

    @id.setter
    def id(self, _id: int):
        """Set the id of the submittable"""
        if self.__id is not None:
            raise ValueError('id can only be set once')
        self.__id = _id
        self._set_id_hook(_id)

    def _set_id_hook(self, _id: int):
        """Hook function called when the id is set. Override to perform
        custom actions on id set.

        .. note:: When overriding, make sure to call the super method:
                  `super()._set_id_hook(id)`"""

#####################################
# state related functions & classes
#####################################
class State(Enum):
    """possible states of a submittable object"""
    PENDING = 10
    RUNNING = 20
    SUCCESSFUL = 30
    FAILED = 40

class IllegalTransitionError(Exception):
    """Raised when an illegal state transition is attempted"""

    def __init__(self, msg: str, old_state: State,new_state: State):
        msg = f'Tried to go from state {old_state} to {new_state}: {msg}'
        if old_state == State.FAILED:
            msg += ('\nThis error can occur, when self.succeed() is called '
                    'after'
                    ' self.fail(). Remember that self.fail() does not exit the'
                    ' function and you sometimes need to add `return` after '
                    '`self.fail()`')
        if old_state == State.SUCCESSFUL and new_state == State.FAILED:
            msg += ('\nThis error can occur, when self.fail() is called after'
                    ' self.succeed(). Remember that self.succeed() does not '
                    'exit the'
                    ' function and you sometimes need to add `return` after '
                    '`self.succeed()`')

        super().__init__(msg)

class HasState:
    """Mixin class for classes that have a state"""

    def __init__(self):
        super().__init__()
        self.__state: State = State.PENDING

    @property
    def _state(self) -> State:
        """Get the state of the submittable"""
        return self.__state

    @_state.setter
    def _state(self, new_state: State):
        """Set the state of the submittable"""

        self._check_state_transition(self.__state, new_state)
        self._set_state_hook(self.__state, new_state)

        self.__state = new_state

    def _check_state_transition(self, current_state: State, new_state: State):
        """:raise: IllegalTransitionError if the transition is not allowed"""
        if new_state == State.FAILED:
            if current_state != State.RUNNING:
                raise IllegalTransitionError("Cannot fail, when not in a "
                                             "running state.",
                                             current_state, new_state)
        elif new_state == State.SUCCESSFUL:
            if current_state != State.RUNNING:
                raise IllegalTransitionError("Cannot succeed, when not in "
                                             "a running state.",
                                             current_state, new_state)
        elif new_state == State.RUNNING:
            if current_state != State.PENDING:
                raise IllegalTransitionError("Already started.",
                                             current_state, new_state)

    def _set_state_hook(self, current: State, new: State):
        """Hook function called when the state is set. Override to perform
        custom actions on state set.

        .. note:: When overriding, make sure to call the super method:
                  `super()._set_state_hook(current_state, new_state)`"""

    @property
    def is_running(self) -> bool:
        """Check if the submittable is running"""
        return self._state == State.RUNNING

    @property
    def is_successful(self) -> bool:
        """Check if the submittable is successful"""
        return self._state == State.SUCCESSFUL

    @property
    def is_failed(self) -> bool:
        """Check if the submittable has failed"""
        return self._state == State.FAILED

    @property
    def is_finished(self) -> bool:
        """Check if the submittable has finished"""
        return self.is_successful or self.is_failed


#####################################
# logging
#####################################
class IdPrefixLogger(logging.LoggerAdapter):
    '''LoggerAdapter that prefixes the log message with the id of the
    object calling the logger. The caller has to be passed as the extra
    parameter and be of type HasLogger:

    .. code-block:: python

        logger = IdPrefixLogger(logging.getLogger(__name__),
                                {'logging_caller': self})
    '''

    def process(self, msg, kwargs):
        caller: HasLogger = self.extra['logging_caller']

        if caller.id is not None:
            return Template(caller._LOG_TEMPLATE).substitute(
                            id=caller.id,
                            msg=msg
                    ), kwargs
        else:
            return Template(caller._LOG_TEMPLATE_NO_ID).substitute(
                            msg=msg
                    ), kwargs

class HasLogger(HasId):
    """Mixin class for classes that have a logger

    :param _logger: private logger that appends the submittable id. For use in
                    subclasses."""

    _LOG_TEMPLATE = '${id}: ${msg}'
    """Template used for logging. The template is formatted with the id and
    the message. Override to change the template."""
    _LOG_TEMPLATE_NO_ID = '${msg}'
    """Template used for logging when the id is not yet set."""

    def __init__(self):
        super().__init__()
        self._logger = IdPrefixLogger(logging.getLogger(__name__),
                                      {'logging_caller': self})

#####################################
# submittable class with result
#####################################
FailureT = TypeVar('FailureT', Exception, 'Failure')
"""Failure type. Used for type hinting"""

class Failure:
    r'''base class for all failure reasons. Any child classes'
    name should end with "Failure", e.g., DependentJobFailure.

    :param msg: message used in logging
    :param causes: list of failure that caused the current failure. Strings
                   will be converted to Failure objects.
    :ivar causes: list of causes for the failure
    :vartype causes: list[Reason\|Exception]
    '''

    def __init__(self, msg: Optional[str] = None, *,
                 causes: Optional[FailureT|str|Iterable[FailureT|str]] = None,
                 **kwargs)\
                 -> None:
        self.msg = msg

        def convert_to_failure(thing: Failure|str|Exception):
            if isinstance(thing, (Failure, Exception)):
                return thing
            elif isinstance(thing, str):
                return Failure(msg=thing)
            else:
                raise TypeError(f'invalid type for a cause: {type(thing)}')

        if causes is None:
            self.causes: list[Failure] = []
        elif isinstance(causes, (Failure, str, Exception)):
            self.causes = [convert_to_failure(causes)]
        else:   # assume its an iterable of causes otherwise
            self.causes = [convert_to_failure(cause) for cause in causes]

    def __str__(self) -> str:
        if not hasattr(self, 'msg'):
            raise ProgrammingError(
                'msg attribute for failure not set. This can'
                ' happen if the __init__ method of a '
                'Failure subclass is overridden and does not'
                ' call super().__init__().')
        return self.msg or self.__class__.__name__

    def __format__(self, __format_spec: str) -> str:
        return self.__str__()

    def traceback(self, level = 0) -> str:
        '''generate the failure traceback

        :param level: indentation level of message'''
        indent_size = 4
        initial_indent = ' '*(level*indent_size)
        subsequent_indent = ' '*((level+1)*indent_size)

        if self.msg is None:
            tb = initial_indent + type(self).__name__
        else:
            msg = type(self).__name__ + ': ' + self.msg
            tb = textwrap.fill(msg, width=80,
                                initial_indent=initial_indent,
                                subsequent_indent=subsequent_indent)
        if self.causes:
            tb += '\n' + subsequent_indent + 'Caused by:'
        for cause in self.causes:
            if isinstance(cause, Failure): # recursive call for traceback
                tb += '\n' + cause.traceback(level=level+1)
            elif isinstance(cause, Exception):
                tb += '\n' + self._format_exce(cause, level=level+1)

        return tb

    def _format_exce(self, exc, level=0) -> str:
        '''formats the exception traceback in a way compatible with the
        traceback function of this class.
        '''
        indent_size = 4
        indent = ' '*(level*indent_size)

        tb = ''

        for line in traceback.format_exception(
                exc,
                chain=False):
            tb += indent + line

        return tb

class ErrorCausedFailure(Failure):
    """indicates that an error occured while executing a submittable"""

    def __init__(self, msg: str = None, *,
                 causes: Failure|Exception|str|Iterable[Failure|Exception|str]
                        = None,
                **kwargs) -> None:

        if msg is None:
            msg = "An error occured while executing the submittable."

            if isinstance(causes, Exception):
                msg += f' The error was: {causes}'

        super().__init__(msg, causes=causes, **kwargs)

@dataclass(kw_only=True)
class _ResultBase:
    """result of a submittable object once it is finished"""

    reason: Failure|None = field(init=False, default=None)
    """reason for failure. Usually set by the `fail()` method of the
    submittable
    """
    submittable_id: int|None = field(init=False, default=None)
    """id of the submittable. Set automatically when result or id is
    assigned to the submittable
    """
    submittable_type: type|None = field(init=False, default=None)
    """type of the submittable. Set automatically when result is assigned
    to the submittable
    """

    def __getitem__(self, key: str):
        """Get the value of the result with the given key"""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)

class Result(_ResultBase):
    """base class for defining the "complete" result, i.e., the result of a
    successful submittable
    """
    reason: None

class FailedResult(_ResultBase):
    """base class for defining an "incomplete" result, i.e., the result of a
    submittable, that failed but computed partial results
    """
    reason: Failure


class _FailedResultDefault(FailedResult):
    """special child class for failed results only used for type hinting"""

    # override make the type checker not complain when accessing fields
    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

SuccessT = TypeVar("SuccessT", bound=Result)
"""type var used to describe complete result type"""
FailedT = TypeVar("FailedT", bound=FailedResult,
                  default=_FailedResultDefault)
"""type var used to describe incomplete result type."""

class Submittable(HasLogger, HasState, HasId, Generic[SuccessT, FailedT]):
    """Base class for jobs and investigations

    :ivar id: unique identifier of the submittable set on submission
    :ivar result: result of the submittable set on completion
    :ivar _logger: private logger that appends the submittable id. For use in
                   subclasses.
    """

    class Result(_ResultBase):
        """**Deprecated**. Specialize the generic class when inheriting

        result of a submittable object once it is finished"""

    def __init__(self):
        super().__init__()
        self.__result = None

    @property
    def result(self) -> Submittable.Result|FailedT|SuccessT|None:
        """result of the submittable, if finished. If the submittable is
        successful, the result is of type SuccessT. If the submittable has
        failed, the type is probably FailedT, but may still be SuccessT (if
        some data was already computed). If the submittable is not finished,
        the result is None.
        """
        return self.__result

    @property
    def success_result(self) -> SuccessT:
        """`result`, but with a more specific type hint. May be used after
        having checked if the submittable is successful.
        """
        return cast(SuccessT, self.result)

    @property
    def failed_result(self) -> FailedT:
        """`result`, but with a more specific type hint. May be used after
        having checked if the submittable has failed.

        .. note:: The actual type may be SuccessT, if the submittable has
                  already computed some data before failing, but reason will
                  always be set, if failed. The type hint is compatible with
                  any Result dataclass.
        """
        return cast(FailedT, self.result)

    @result.setter
    def result(self, result: SuccessT|FailedT):
        # Allow users to reset the result while running and preparation
        if result is None:
            if not self.is_finished:
                self.__result = None
            else:
                # we want to guarantee that there is a result object if the
                # investigation has finished
                raise ValueError('Cannot set result to None after '
                                 'submittable has finished.')
        else:
            if not isinstance(result, _ResultBase):
                raise TypeError(f'Unexpected type of job.result: '
                                f'{type(result)}')

            result.submittable_id = self.id # may be None
            result.submittable_type = type(self)
            self.__result = result

    @classmethod
    def _create_failed_result_obj(cls) -> FailedResult:
        """Factory method to create a FailedResult object. Override to create
        a custom FailedResult object.
        """
        return FailedResult()

    def _set_id_hook(self, _id: int):
        super()._set_id_hook(_id)
        # If the result is already initialized in __init__ before submission,
        # there may already be a result, but submittable_id is None
        if self.result is not None:
            self.result.submittable_id = _id

    def __set_failure_reason(self, reason: str|Failure|Exception):
        """Set the failure reason of the submittable"""
        if isinstance(reason, str):
            reason = Failure(msg=reason)
        elif isinstance(reason, Exception):
            reason = ErrorCausedFailure(causes=reason)
        elif not isinstance(reason, Failure):
            raise TypeError('reason must be a string, an Exception or a '
                            'Failure object')

        # check if the investigation has already create a result object
        # containing partial data
        if self.result is None:
            self.result = FailedResult()
        else:
            if self.result.reason is not None:
                self._logger.warning('fail() was called although result.reason'
                                     ' is not None. Current reason will be '
                                     'overridden.')

        self.result.reason = reason

    def _check_state_transition(self, current_state: State, new_state: State):
        super()._check_state_transition(current_state, new_state)

        # while fail() and run() do this, it is possible to set the state
        # manually -> catch errors when doing this wrong
        if new_state == State.RUNNING and self.id is None:
            raise IllegalTransitionError('Cannot start without an id.',
                                         current_state, new_state)

        if new_state == State.FAILED and (self.result is None
                                          or self.result.reason is None):
            raise IllegalTransitionError('Cannot fail without a reason. Use '
                                         'fail() to set a reason.',
                                         current_state, new_state)

    def start(self, _id: int):
        """Starts the submittable and sets the id.

        :raise: IllegalStateTransition if not pending"""
        self.id = _id
        self._state = State.RUNNING

    def fail(self, reason: str|Failure|Exception):
        """Fail the submittable and set the failure reason.

        :raise: IllegalStateTransition if not running"""
        self.__set_failure_reason(reason)

        self._logger.info('failed: %s', reason)

        self._state = State.FAILED

    def succeed(self):
        """Finish the submittable successfully"""
        self._state = State.SUCCESSFUL

