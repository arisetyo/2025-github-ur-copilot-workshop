import pytest
from models.timer import TimerState, SessionType, TimerStatus
from models.session import PomodoroSession
from services.timer_service import TimerService

def test_timer_service_initialization():
    service = TimerService()
    state = service.get_current_state()
    assert isinstance(state, TimerState)
    assert state.session_type == SessionType.WORK
    assert state.status == TimerStatus.STOPPED


def test_timer_service_start_pause_reset():
    service = TimerService()
    state = service.start_timer()
    assert state.status == TimerStatus.RUNNING
    state = service.pause_timer()
    assert state.status == TimerStatus.PAUSED
    state = service.reset_timer()
    assert state.status == TimerStatus.STOPPED


def test_timer_service_skip_session():
    service = TimerService()
    service.start_timer()
    state = service.skip_session()
    assert state.session_type == SessionType.BREAK or state.session_type == SessionType.WORK


def test_timer_service_update_session_config():
    service = TimerService()
    new_config = PomodoroSession(work_duration=1200, break_duration=200, long_break_duration=600, sessions_until_long_break=3)
    service.update_session_config(new_config)
    config = service.get_session_config()
    assert config.work_duration == 1200
    assert config.break_duration == 200
    assert config.long_break_duration == 600
    assert config.sessions_until_long_break == 3


def test_timer_service_is_session_complete():
    service = TimerService()
    state = service.get_current_state()
    state.current_time = 0
    assert service.is_session_complete() is True
