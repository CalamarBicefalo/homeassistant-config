import uuid
from unittest.mock import Mock

import pytest
from appdaemontestframework import automation_fixture

import matchers
from app import App


class GenericApp(App):
    def initialize(self) -> None:
        pass


@automation_fixture(GenericApp)
def subject() -> None:
    matchers.init()
    pass


@pytest.mark.asyncio
def test_run_for_runs_every_minute_and_afterwards(given_that, subject: App, assert_that, time_travel):
    callback = Mock(return_value=None)
    afterwards = Mock(return_value=None)

    subject.run_for(3, callback=lambda x: callback(x), afterwards=afterwards)
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    callback.assert_called_once_with(2)
    time_travel.fast_forward(1).minutes()
    callback.assert_called_with(1)
    time_travel.fast_forward(1).minutes()
    afterwards.assert_called_once()


@pytest.mark.asyncio
def test_run_for_same_running_group(given_that, subject: App, assert_that, time_travel):
    callback_1 = Mock(return_value=None)
    callback_2 = Mock(return_value=None)
    running_group = uuid.uuid4()

    subject.run_for(3, callback=lambda x: callback_1(x), running_group=running_group)
    subject.run_for(10, callback=lambda x: callback_2(x), running_group=running_group)
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    callback_2.assert_called_once_with(9)
    callback_1.assert_not_called()


@pytest.mark.asyncio
def test_run_for_different_running_group(given_that, subject: App, assert_that, time_travel):
    callback_1 = Mock(return_value=None)
    callback_2 = Mock(return_value=None)

    subject.run_for(3, callback=lambda x: callback_1(x), running_group=uuid.uuid4())
    subject.run_for(10, callback=lambda x: callback_2(x), running_group=uuid.uuid4())
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    callback_2.assert_called_once_with(9)
    callback_1.assert_called_once_with(2)



@pytest.mark.asyncio
def test_run_for_aborts_when_callback_exception(given_that, subject: App, assert_that, time_travel):
    callback = Mock(side_effect=Exception("boom"))
    afterwards = Mock(return_value=None)

    subject.run_for(3, callback=lambda x: callback(x), afterwards=afterwards)
    time_travel.fast_forward(4).minutes()
    callback.assert_called_once_with(2)
    afterwards.assert_not_called()


@pytest.mark.asyncio
def test_run_for_with_custom_interval(given_that, subject: App, assert_that, time_travel):
    callback = Mock(return_value=None)
    afterwards = Mock(return_value=None)

    subject.run_for(15, callback=lambda x: callback(x), afterwards=afterwards, interval_minutes=5)
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(5).minutes()
    callback.assert_called_once_with(10)
    time_travel.fast_forward(5).minutes()
    callback.assert_called_with(5)
    time_travel.fast_forward(5).minutes()
    afterwards.assert_called_once()
