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
    every_minute = Mock(return_value=None)
    afterwards = Mock(return_value=None)

    subject.run_for(3, every_minute=lambda x: every_minute(x), afterwards=afterwards)
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    every_minute.assert_called_once_with(2)
    time_travel.fast_forward(1).minutes()
    every_minute.assert_called_with(1)
    time_travel.fast_forward(1).minutes()
    afterwards.assert_called_once()


@pytest.mark.asyncio
def test_run_for_same_running_group(given_that, subject: App, assert_that, time_travel):
    every_minute_1 = Mock(return_value=None)
    every_minute_2 = Mock(return_value=None)
    running_group = uuid.uuid4()

    subject.run_for(3, every_minute=lambda x: every_minute_1(x), running_group=running_group)
    subject.run_for(10, every_minute=lambda x: every_minute_2(x), running_group=running_group)
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    every_minute_2.assert_called_once_with(9)
    every_minute_1.assert_not_called()


@pytest.mark.asyncio
def test_run_for_different_running_group(given_that, subject: App, assert_that, time_travel):
    every_minute_1 = Mock(return_value=None)
    every_minute_2 = Mock(return_value=None)

    subject.run_for(3, every_minute=lambda x: every_minute_1(x), running_group=uuid.uuid4())
    subject.run_for(10, every_minute=lambda x: every_minute_2(x), running_group=uuid.uuid4())
    time_travel.fast_forward(10).seconds()
    time_travel.fast_forward(1).minutes()
    every_minute_2.assert_called_once_with(9)
    every_minute_1.assert_called_once_with(2)



@pytest.mark.asyncio
def test_run_for_aborts_when_callback_exception(given_that, subject: App, assert_that, time_travel):
    every_minute = Mock(side_effect=Exception("boom"))
    afterwards = Mock(return_value=None)

    subject.run_for(3, every_minute=lambda x: every_minute(x), afterwards=afterwards)
    time_travel.fast_forward(4).minutes()
    every_minute.assert_called_once_with(2)
    afterwards.assert_not_called()
