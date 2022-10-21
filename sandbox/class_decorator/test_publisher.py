class DuplicateError(Exception):
    pass

class Publisher:
    """Publish notifications to subscribers"""

    _subscribers: list

    def __init__(self):
        self._subscribers = []

    @property
    def subscribers(self):
        """Returns a list of registered subscribers."""
        return (*self._subscribers,)

    def subscribe(self, observer):
        """Create observer subscription.
        
        Raises
        ------

        DuplicateError:
           Raised if observer is not subscribed."""
        if observer in self._subscribers:
            raise DuplicateError("Observer already subsribed.")
        self._subscribers.append(observer)

    def unsubscribe(self, observer):
        """Remove existing observer subscription.
        
        Raises
        ------

        ValueError:
           Raised if observer is not subscribed."""
        self._subscribers.remove(observer)

    def notify(self, *args, **kwargs):
        """Invoke subscribers with given arguments."""

        for observer in self._subscribers:
            observer(*args, **kwargs)

from typing import Callable, cast
from unittest.mock import Mock
import pytest


class TestPublisherClass:
    @pytest.fixture(name="publisher")
    def given_publisher(self):
        return Publisher()

    @pytest.fixture(name="observer")
    def given_observer(self):
        return Mock()

    @pytest.fixture(name="subscribed_observer")
    def given_subscribed_observer(self, publisher, observer):
        publisher.subscribe(observer)
        return observer

    def test_given_new_publisher_then_subscribers_list_is_empty(self, publisher: Publisher):
        assert publisher.subscribers == tuple()

    def test_given_new_publisher_then_subscribers_is_tuple(self, publisher: Publisher):
        assert isinstance(publisher.subscribers, tuple)

    def test_given_new_publisher_and_observer_when_subscribe_observer_then_observer_is_in_subscribers(self, publisher: Publisher, observer: Callable):
        publisher.subscribe(observer)
        assert observer in publisher.subscribers

    def test_given_new_publisher_and_subscribed_observer_when_subscribe_same_observer_then_raises_duplicateerror(self, publisher: Publisher, subscribed_observer: Callable):
        with pytest.raises(DuplicateError):
            publisher.subscribe(subscribed_observer)

    def test_given_publisher_and_subscribed_observer_when_unsubscribe_same_observer_than_observer_not_in_subscribers(self, publisher: Publisher, subscribed_observer: Callable):
        publisher.unsubscribe(subscribed_observer)
        assert subscribed_observer not in publisher.subscribers

    def test_given_publisher_and_observer_when_unsubscribe_observer_then_raises_valueerror(self, publisher: Publisher, observer: Callable):
        with pytest.raises(ValueError):
            publisher.unsubscribe(observer)

    def test_given_publisher_and_subscribed_observer_when_notify_is_called_observer_is_called(self, publisher: Publisher, subscribed_observer: Callable):
        args = [Mock()]
        kwargs = {"kwarg":Mock()}
        publisher.notify(*args, **kwargs)
        observer = cast(Mock, subscribed_observer)
        observer.assert_called_once_with(*args, **kwargs)


