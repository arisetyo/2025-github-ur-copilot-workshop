"""Simple Pomodoro Timer Web Application - Single File Version."""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-pomodoro-timer'

# Global timer state
timer_state = {
    'current_time': 1500,  # 25 minutes in seconds
    'session_type': 'work',  # 'work' or 'break'
    'status': 'stopped',  # 'running', 'paused', 'stopped'
    'session_count': 0,
    'total_time': 1500,
    'work_duration': 1500,
    'break_duration': 300,
    'long_break_duration': 900,
    'sessions_until_long_break': 4
}

# Timer lock for thread safety
timer_lock = threading.Lock()
timer_thread = None
stop_timer_flag = threading.Event()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Pomodoro Timer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }
        
        .session-type {
            color: #666;
            font-size: 1.2em;
            margin-bottom: 30px;
            text-transform: capitalize;
        }
        
        .timer-display {
            font-size: 5em;
            font-weight: bold;
            color: #667eea;
            margin: 30px 0;
            font-variant-numeric: tabular-nums;
        }
        
        .session-count {
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }
        
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
        }
        
        button {
            padding: 15px 30px;
            font-size: 1em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: 600;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
            transform: translateY(-2px);
        }
        
        .status {
            color: #888;
            font-size: 0.9em;
            margin-top: 20px;
        }
        
        @media (max-width: 600px) {
            .timer-display {
                font-size: 3.5em;
            }
            
            .controls {
                flex-direction: column;
            }
            
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍅 Pomodoro Timer</h1>
        <div class="session-type" id="session-type">Work Session</div>
        <div class="timer-display" id="timer-display">25:00</div>
        <div class="session-count" id="session-count">Sessions completed: 0</div>
        
        <div class="controls">
            <button class="btn-primary" id="start-btn" onclick="startTimer()">Start</button>
            <button class="btn-primary" id="pause-btn" onclick="pauseTimer()" style="display:none;">Pause</button>
            <button class="btn-secondary" onclick="resetTimer()">Reset</button>
            <button class="btn-secondary" onclick="skipSession()">Skip</button>
        </div>
        
        <div class="status" id="status">Ready to focus!</div>
    </div>
    
    <script>
        let updateInterval = null;
        
        function formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
        
        function updateDisplay(state) {
            document.getElementById('timer-display').textContent = formatTime(state.current_time);
            document.getElementById('session-type').textContent = 
                state.session_type === 'work' ? 'Work Session' : 'Break Time';
            document.getElementById('session-count').textContent = 
                `Sessions completed: ${state.session_count}`;
            
            const startBtn = document.getElementById('start-btn');
            const pauseBtn = document.getElementById('pause-btn');
            
            if (state.status === 'running') {
                startBtn.style.display = 'none';
                pauseBtn.style.display = 'inline-block';
                document.getElementById('status').textContent = 
                    state.session_type === 'work' ? '⏰ Focus time!' : '☕ Take a break!';
            } else if (state.status === 'paused') {
                startBtn.style.display = 'inline-block';
                startBtn.textContent = 'Resume';
                pauseBtn.style.display = 'none';
                document.getElementById('status').textContent = '⏸️ Paused';
            } else {
                startBtn.style.display = 'inline-block';
                startBtn.textContent = 'Start';
                pauseBtn.style.display = 'none';
                document.getElementById('status').textContent = '✨ Ready to focus!';
            }
            
            // Change timer color based on session type
            const timerDisplay = document.getElementById('timer-display');
            timerDisplay.style.color = state.session_type === 'work' ? '#667eea' : '#48bb78';
        }
        
        function fetchStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                    
                    // Show notification when session completes
                    if (data.current_time === 0 && data.status === 'running') {
                        showNotification(data.session_type);
                    }
                })
                .catch(error => console.error('Error:', error));
        }
        
        function showNotification(sessionType) {
            const message = sessionType === 'work' 
                ? '🎉 Work session completed! Time for a break!' 
                : '✅ Break finished! Ready for another session?';
            
            document.getElementById('status').textContent = message;
            
            // Browser notification if supported
            if ('Notification' in window && Notification.permission === 'granted') {
                new Notification('Pomodoro Timer', { body: message });
            }
        }
        
        function startTimer() {
            fetch('/api/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                    startPolling();
                })
                .catch(error => console.error('Error:', error));
        }
        
        function pauseTimer() {
            fetch('/api/pause', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                    stopPolling();
                })
                .catch(error => console.error('Error:', error));
        }
        
        function resetTimer() {
            fetch('/api/reset', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                    stopPolling();
                })
                .catch(error => console.error('Error:', error));
        }
        
        function skipSession() {
            fetch('/api/skip', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    updateDisplay(data);
                })
                .catch(error => console.error('Error:', error));
        }
        
        function startPolling() {
            if (!updateInterval) {
                updateInterval = setInterval(fetchStatus, 1000);
            }
        }
        
        function stopPolling() {
            if (updateInterval) {
                clearInterval(updateInterval);
                updateInterval = null;
            }
        }
        
        // Request notification permission on load
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
        
        // Initial status fetch
        fetchStatus();
    </script>
</body>
</html>
"""


def timer_worker():
    """Background timer worker thread."""
    global timer_state
    
    while not stop_timer_flag.is_set():
        with timer_lock:
            if timer_state['status'] == 'running' and timer_state['current_time'] > 0:
                timer_state['current_time'] -= 1
                
                # Handle session completion
                if timer_state['current_time'] == 0:
                    if timer_state['session_type'] == 'work':
                        timer_state['session_count'] += 1
                        # Determine next session type
                        if timer_state['session_count'] % timer_state['sessions_until_long_break'] == 0:
                            timer_state['session_type'] = 'break'
                            timer_state['current_time'] = timer_state['long_break_duration']
                            timer_state['total_time'] = timer_state['long_break_duration']
                        else:
                            timer_state['session_type'] = 'break'
                            timer_state['current_time'] = timer_state['break_duration']
                            timer_state['total_time'] = timer_state['break_duration']
                    else:
                        timer_state['session_type'] = 'work'
                        timer_state['current_time'] = timer_state['work_duration']
                        timer_state['total_time'] = timer_state['work_duration']
        
        time.sleep(1)


def start_timer_thread():
    """Start the background timer thread."""
    global timer_thread, stop_timer_flag
    
    if timer_thread is None or not timer_thread.is_alive():
        stop_timer_flag.clear()
        timer_thread = threading.Thread(target=timer_worker, daemon=True)
        timer_thread.start()


@app.route('/')
def index():
    """Serve the main page."""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status')
def get_status():
    """Get current timer status."""
    with timer_lock:
        return jsonify(timer_state)


@app.route('/api/start', methods=['POST'])
def start():
    """Start the timer."""
    with timer_lock:
        timer_state['status'] = 'running'
        start_timer_thread()
        return jsonify(timer_state)


@app.route('/api/pause', methods=['POST'])
def pause():
    """Pause the timer."""
    with timer_lock:
        timer_state['status'] = 'paused'
        return jsonify(timer_state)


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset the timer."""
    with timer_lock:
        timer_state['status'] = 'stopped'
        timer_state['session_type'] = 'work'
        timer_state['current_time'] = timer_state['work_duration']
        timer_state['total_time'] = timer_state['work_duration']
        return jsonify(timer_state)


@app.route('/api/skip', methods=['POST'])
def skip():
    """Skip to next session."""
    with timer_lock:
        if timer_state['session_type'] == 'work':
            timer_state['session_count'] += 1
            # Determine next session type
            if timer_state['session_count'] % timer_state['sessions_until_long_break'] == 0:
                timer_state['session_type'] = 'break'
                timer_state['current_time'] = timer_state['long_break_duration']
                timer_state['total_time'] = timer_state['long_break_duration']
            else:
                timer_state['session_type'] = 'break'
                timer_state['current_time'] = timer_state['break_duration']
                timer_state['total_time'] = timer_state['break_duration']
        else:
            timer_state['session_type'] = 'work'
            timer_state['current_time'] = timer_state['work_duration']
            timer_state['total_time'] = timer_state['work_duration']
        
        return jsonify(timer_state)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    start_timer_thread()
    app.run(host='0.0.0.0', port=5000, debug=True)
