import pytest
from models.timer import TimerState, SessionType, TimerStatus


def test_timer_state_initialization():
    state = TimerState(current_time=1500, session_type=SessionType.WORK, status=TimerStatus.STOPPED)
    assert state.current_time == 1500
    assert state.session_type == SessionType.WORK
    assert state.status == TimerStatus.STOPPED
    assert state.session_count == 0
    assert state.total_time == 1500
    assert state.is_complete is False
    assert 0.0 <= state.progress_percentage <= 100.0


def test_timer_state_progress_percentage():
    state = TimerState(current_time=750, session_type=SessionType.WORK, status=TimerStatus.RUNNING, total_time=1500)
    assert state.progress_percentage == 50.0


def test_timer_state_is_complete():
    state = TimerState(current_time=0, session_type=SessionType.WORK, status=TimerStatus.STOPPED)
    assert state.is_complete is True


def test_timer_state_to_dict():
    state = TimerState(current_time=1500, session_type=SessionType.WORK, status=TimerStatus.STOPPED)
    d = state.to_dict()
    assert d['current_time'] == 1500
    assert d['session_type'] == 'work'
    assert d['status'] == 'stopped'
    assert d['progress_percentage'] == 0.0
    assert d['is_complete'] is False


def test_timer_state_negative_values():
    with pytest.raises(ValueError):
        TimerState(current_time=-1, session_type=SessionType.WORK, status=TimerStatus.STOPPED)
    with pytest.raises(ValueError):
        TimerState(current_time=10, session_type=SessionType.WORK, status=TimerStatus.STOPPED, session_count=-1)
    with pytest.raises(ValueError):
        TimerState(current_time=10, session_type=SessionType.WORK, status=TimerStatus.STOPPED, total_time=0)
