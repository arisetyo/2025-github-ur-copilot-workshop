import pytest
from routes.timer import timer_service
from services.timer_service import TimerService
from models.timer import TimerState, SessionType, TimerStatus
from models.session import PomodoroSession

# Setup a test timer service for route tests
test_service = TimerService()
timer_service = test_service


def test_get_timer_status():
    state = timer_service.get_current_state()
    assert isinstance(state, TimerState)
    assert state.session_type == SessionType.WORK


def test_start_timer():
    state = timer_service.start_timer()
    assert state.status == TimerStatus.RUNNING


def test_pause_timer():
    timer_service.start_timer()
    state = timer_service.pause_timer()
    assert state.status == TimerStatus.PAUSED


def test_reset_timer():
    timer_service.start_timer()
    state = timer_service.reset_timer()
    assert state.status == TimerStatus.STOPPED


def test_skip_session():
    timer_service.start_timer()
    state = timer_service.skip_session()
    assert state.session_type in [SessionType.WORK, SessionType.BREAK]


def test_update_timer_config():
    new_config = PomodoroSession(work_duration=1200, break_duration=200, long_break_duration=600, sessions_until_long_break=3)
    timer_service.update_session_config(new_config)
    config = timer_service.get_session_config()
    assert config.work_duration == 1200
    assert config.break_duration == 200
    assert config.long_break_duration == 600
    assert config.sessions_until_long_break == 3
