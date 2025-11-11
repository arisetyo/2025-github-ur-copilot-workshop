import pytest
from models.session import PomodoroSession

def test_pomodoro_session_defaults():
    session = PomodoroSession()
    assert session.work_duration == 1500
    assert session.break_duration == 300
    assert session.long_break_duration == 900
    assert session.sessions_until_long_break == 4


def test_pomodoro_session_custom_values():
    session = PomodoroSession(work_duration=1200, break_duration=200, long_break_duration=600, sessions_until_long_break=3)
    assert session.work_duration == 1200
    assert session.break_duration == 200
    assert session.long_break_duration == 600
    assert session.sessions_until_long_break == 3


def test_pomodoro_session_validation():
    with pytest.raises(ValueError):
        PomodoroSession(work_duration=0)
    with pytest.raises(ValueError):
        PomodoroSession(break_duration=0)
    with pytest.raises(ValueError):
        PomodoroSession(long_break_duration=0)
    with pytest.raises(ValueError):
        PomodoroSession(sessions_until_long_break=0)


def test_get_session_duration():
    session = PomodoroSession()
    assert session.get_session_duration('work') == 1500
    assert session.get_session_duration('break', session_count=1) == 300
    assert session.get_session_duration('break', session_count=4) == 900
    with pytest.raises(ValueError):
        session.get_session_duration('invalid')


def test_is_long_break_due():
    session = PomodoroSession()
    assert session.is_long_break_due(4) is True
    assert session.is_long_break_due(3) is False


def test_to_dict_and_from_dict():
    session = PomodoroSession(work_duration=1200, break_duration=200, long_break_duration=600, sessions_until_long_break=3)
    d = session.to_dict()
    assert d['work_duration'] == 1200
    assert d['break_duration'] == 200
    assert d['long_break_duration'] == 600
    assert d['sessions_until_long_break'] == 3
    session2 = PomodoroSession.from_dict(d)
    assert session2.work_duration == 1200
    assert session2.break_duration == 200
    assert session2.long_break_duration == 600
    assert session2.sessions_until_long_break == 3
