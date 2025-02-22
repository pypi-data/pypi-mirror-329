"""
This module contains the event system used internally to notify investigations
about finished jobs or other investigations.
"""

from collections import defaultdict
import logging
import traceback
from typing import Optional
from collections.abc import Iterable
from abc import ABCMeta, abstractmethod

###############################################################################
# classes relevant to implement the observer pattern
###############################################################################

class EventError(Exception):
    ''' base class for all exceptions related with the event system'''

class UnexpectedEventError(Exception):
    '''raised when a listener receives an event it did not expect'''

class MultipleExceptionsWhileNotifyingError(EventError):
    ''' raised when more than one exceptions are thrown while an listeners are
    notified

    :param causes: Exceptions that were raised while notifying listeners'''

    def __init__(self, *args, causes: Iterable[Exception] = None) -> None:
        super().__init__(*args)

        self.causes = causes

    def print_strack_traces(self):
        '''prints the stack traces of all exceptions that caused this one'''

        for e in self.causes:
            traceback.print_exc(e)


class Event:
    '''
    Event that Listeners can subscribe to. An event is defined by its type and
    its specification string.

    Child classes may add additional member variables to provide more data,
    but whether or not a listeners gets notified depends soley on the type
    and specification string.

    :param spec: a string providing further specification of the event.
    '''

    def __init__(self, spec: str) -> None:
        self.spec = spec

    def __hash__(self) -> int:
        return hash(type(self)) ^ hash(self.spec)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Event):
            return type(self) is type(__o) and self.spec == __o.spec
        else:
            return False

    def __repr__(self) -> str:
        return f'<{type(self).__name__} spec="{self.spec}">'


class Listener(metaclass=ABCMeta):
    '''A Listener can subscribe to events with an EventHandler. When the event
    happens, its update method is called.
    '''

    @abstractmethod
    def update(self, event: Event) -> None:
        '''called by the event handler when a subscribed event happens '''
        pass


class EventDispatcher:
    '''
    Used to register listeners and trigger events.

    This class is a singleton. That means that EventDispatcher() will alway
    return the same instance.
    '''

    # using the Singleton pattern here. That means that there will always be
    # only one instance of the event dispatcher
    _instance = None
    _listeners: dict[tuple[type, str], list[Listener]]
    _rev_listeners: dict[Listener, list[tuple[type, str]]]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # dictionary with event definition as key and listeners as value
            cls._instance._listeners = defaultdict(list)
            # dictionary with listeners as key and event definition as value
            # i.e. the reverse of _listeners
            cls._instance._rev_listeners =  defaultdict(list)

        return cls._instance

    def register_listener(self, listener: Listener,
                          event: Optional[Event] = None,
                          event_type: Optional[type] = None,
                          spec: Optional[str] = None):
        ''' subscribes a listener to an event. The event can either be defined
        by an event object or by passing the type and specification string
        separately.

        :param listener: listener that should be notified when the event
                         happens
        :type listener: Listener
        :param event: event to subscribe to
        :param event_type: subclass of event the listener wants to subscibe to
        :param spec:    specification string of the event
        '''
        if event is None and not (event_type is None and spec is None):
            event_def = (event_type, spec)  # definition
        elif event is not None and (event_type is None and spec is None):
            event_def = (type(event), event.spec)  # definition
        else:
            raise EventError('The event needs to be defined by either suppling'
                             ' an event object or by supplying its type and'
                             ' specification.')

        if listener in self._listeners[event_def]:
            # the listner is already registered to this event
            return

        self._listeners[event_def].append(listener)
        self._rev_listeners[listener].append(event_def)

    def deregister_listener(self, listener: Listener, event_type: type = None,
                            spec: str = None) -> list[tuple[type, str]]:
        '''
        Removes all events registered to listener.

        Call this function at the end of the lifetime of the listener object to
        avoid memory leaks.

        :param listener: listener to unregister
        :param event_type: type of the events from which to unregister the
                           listener
        :param spec: specification string of the events from which to
                     unregister the listener
        :return: list of tuples that define all the events from which the
                 listener has been unsubscribed. The first item in the tuple is
                 the type of the event, and the second is the specification
                 string.
        '''
        removed = []

        if listener in self._rev_listeners:
            for event_def in self._rev_listeners[listener]:
                # only remove events of correct type and with correct spec
                if (event_type is None or event_def[0] == event_type) \
                        and (spec is None or event_def[1] == spec):
                    self._remove_entry_in_dict_of_lists(self._listeners,
                                                        event_def, listener)

                    removed.append(event_def)

            for event_def in removed:
                self._remove_entry_in_dict_of_lists(self._rev_listeners,
                                                    listener, event_def)

        return removed

    def get_events(self, listener: Listener) -> list[tuple[type, str]]:
        '''returns all events the listener is subscribed to

        :param listener: listener to get the events for
        :return: list of tuples that define all the events from which the
                 listener has been unsubscribed. The first item in the tuple is
                 the type of the event, and the second is the specification
                 string.
        '''
        return self._rev_listeners.get(listener, [])

    def _remove_entry_in_dict_of_lists(self, d_of_l, key, entry):
        '''
        Checks if entry is in d_of_l[key] and removes it. If d_of_l[key] is
        empty afterwards, it also removes the entry d_of_l[key]

        :param d_of_l: dictionary where the values are lists
        '''
        if key in d_of_l:
            try:
                d_of_l[key].remove(entry)
            except ValueError:
                pass  # entry wasn't in the list

            if len(d_of_l[key]) == 0:
                del d_of_l[key]

    def trigger(self, event: Event):
        ''' Tells the event handler to notify all subscribers of the event

        :param event: event that just happened
        :type event: Event
        '''
        excs = []  # collects all exceptions until everyone is notified

        event_def = (type(event), event.spec)

        if event_def in self._listeners:
            for listener in self._listeners[event_def]:
                try:
                    listener.update(event)
                except Exception as err:
                    excs.append(err)

                    logging.getLogger(__name__).debug(
                        'An exception occured while updating "%s" '
                        'about the event "%s"', listener, event)

            if len(excs) == 1:
                raise excs[0]  # reraise if just a single exception
            elif len(excs) > 1:
                raise MultipleExceptionsWhileNotifyingError(causes=excs)
