"""Tests for simple Pomodoro Timer application."""

import pytest
import json
import time
from simple_app import app, timer_state, timer_lock


@pytest.fixture
def client():
    """Create test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_timer_state():
    """Reset timer state before each test."""
    with timer_lock:
        timer_state['current_time'] = 1500
        timer_state['session_type'] = 'work'
        timer_state['status'] = 'stopped'
        timer_state['session_count'] = 0
        timer_state['total_time'] = 1500


def test_index_page(client):
    """Test that index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Pomodoro Timer' in response.data


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


def test_get_status(client):
    """Test getting timer status."""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['current_time'] == 1500
    assert data['session_type'] == 'work'
    assert data['status'] == 'stopped'
    assert data['session_count'] == 0


def test_start_timer(client):
    """Test starting the timer."""
    response = client.post('/api/start')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'running'


def test_pause_timer(client):
    """Test pausing the timer."""
    # Start timer first
    client.post('/api/start')
    
    # Then pause
    response = client.post('/api/pause')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'paused'


def test_reset_timer(client):
    """Test resetting the timer."""
    # Start timer and modify state
    client.post('/api/start')
    time.sleep(2)
    
    # Reset
    response = client.post('/api/reset')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'stopped'
    assert data['session_type'] == 'work'
    assert data['current_time'] == 1500


def test_skip_session_work_to_break(client):
    """Test skipping from work to break session."""
    response = client.post('/api/skip')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['session_type'] == 'break'
    assert data['current_time'] == 300  # Short break
    assert data['session_count'] == 1


def test_skip_session_break_to_work(client):
    """Test skipping from break to work session."""
    # First skip to break
    client.post('/api/skip')
    
    # Then skip back to work
    response = client.post('/api/skip')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['session_type'] == 'work'
    assert data['current_time'] == 1500


def test_long_break_after_four_sessions(client):
    """Test that long break occurs after 4 work sessions."""
    # Complete 3 work sessions
    for _ in range(3):
        client.post('/api/skip')  # work to break
        client.post('/api/skip')  # break to work
    
    # 4th work session should trigger long break
    response = client.post('/api/skip')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['session_type'] == 'break'
    assert data['current_time'] == 900  # Long break
    assert data['session_count'] == 4


def test_timer_countdown(client):
    """Test that timer counts down when running."""
    # Start timer
    client.post('/api/start')
    initial_time = timer_state['current_time']
    
    # Wait for timer to count down
    time.sleep(2)
    
    # Check status
    response = client.get('/api/status')
    data = json.loads(response.data)
    assert data['current_time'] < initial_time


def test_timer_does_not_countdown_when_paused(client):
    """Test that timer doesn't count down when paused."""
    # Start and pause timer
    client.post('/api/start')
    client.post('/api/pause')
    
    # Get current time
    response = client.get('/api/status')
    data = json.loads(response.data)
    paused_time = data['current_time']
    
    # Wait a bit
    time.sleep(2)
    
    # Time should not have changed
    response = client.get('/api/status')
    data = json.loads(response.data)
    assert data['current_time'] == paused_time
