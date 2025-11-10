# Pomodoro Timer Application - Step-by-Step Implementation Plan

## Implementation Overview

This document outlines a granular, step-by-step plan for implementing the Pomodoro timer web application using FastAPI and HTML/CSS/JavaScript. The plan is structured to maximize learning opportunities with GitHub Copilot while building incrementally.

## Necessary Functions to Implement

### Backend Functions (FastAPI)

#### Data Models & Types
- `SessionType` enum (work, break)
- `TimerStatus` enum (running, paused, stopped)
- `TimerState` class with validation
- `PomodoroSession` configuration class

#### Timer Service Functions
- `create_timer_state()` - Initialize new timer state
- `start_timer()` - Begin timer countdown
- `pause_timer()` - Pause current timer
- `reset_timer()` - Reset to initial state
- `get_timer_status()` - Get current timer state
- `update_timer()` - Decrement timer by 1 second
- `switch_session()` - Toggle between work/break
- `calculate_progress()` - Calculate completion percentage
- `is_session_complete()` - Check if timer reached 00:00

#### API Endpoint Functions
- `get_timer_status_endpoint()` - GET /api/timer/status
- `start_timer_endpoint()` - POST /api/timer/start
- `pause_timer_endpoint()` - POST /api/timer/pause
- `reset_timer_endpoint()` - POST /api/timer/reset
- `skip_session_endpoint()` - POST /api/timer/skip

#### WebSocket Functions
- `websocket_endpoint()` - Handle WebSocket connections
- `broadcast_timer_update()` - Send updates to connected clients
- `handle_client_connection()` - Manage client connections
- `handle_client_disconnection()` - Clean up disconnected clients

#### Background Task Functions
- `timer_background_task()` - Main timer loop
- `schedule_timer_updates()` - Regular update scheduler
- `handle_session_completion()` - Process session transitions

### Frontend Functions (JavaScript)

#### Core Timer Functions
- `initializeTimer()` - Set up initial timer state
- `startTimer()` - Start timer countdown
- `pauseTimer()` - Pause timer
- `resetTimer()` - Reset timer to initial state
- `skipSession()` - Move to next session
- `updateTimerDisplay()` - Update MM:SS display
- `formatTime()` - Convert seconds to MM:SS format

#### UI Update Functions
- `updateProgressIndicator()` - Update progress bar/circle
- `updateSessionInfo()` - Update session type display
- `updateControlButtons()` - Update button states
- `updateSessionCounter()` - Update completed sessions count
- `toggleSessionStyle()` - Switch between work/break styling

#### WebSocket Communication Functions
- `connectWebSocket()` - Establish WebSocket connection
- `handleWebSocketMessage()` - Process incoming messages
- `handleWebSocketError()` - Handle connection errors
- `handleWebSocketClose()` - Handle connection closure
- `reconnectWebSocket()` - Reconnect on failure

#### Notification Functions
- `requestNotificationPermission()` - Ask for browser notifications
- `showNotification()` - Display browser notification
- `playAudioNotification()` - Play completion sound
- `showVisualAlert()` - Display visual notification

#### Utility Functions
- `calculateProgress()` - Calculate completion percentage
- `getSessionTypeColor()` - Get color for current session
- `isTimerRunning()` - Check if timer is active
- `saveTimerState()` - Save to localStorage (optional)
- `loadTimerState()` - Load from localStorage (optional)

### CSS Functions/Classes
- `.timer-display` - Main timer styling
- `.progress-indicator` - Progress bar/circle styling
- `.work-session` - Work session theme
- `.break-session` - Break session theme
- `.control-buttons` - Button styling
- `.session-info` - Session information styling
- Media queries for responsive design

## Step-by-Step Implementation Plan

### Phase 1: Project Foundation (Steps 1-5)

#### Step 1: Project Structure Setup
**Objective**: Create basic project structure and environment
**Files to Create**:
- Create directory structure (`backend/`, `frontend/`, `tests/`)
- Set up virtual environment with `uv`
- Create `requirements.txt` with FastAPI dependencies
- Initialize `__init__.py` files

**Expected Outcome**: Clean project structure ready for development

#### Step 2: Basic FastAPI Server
**Objective**: Set up working FastAPI server
**Files to Create/Modify**:
- `backend/main.py` - Basic FastAPI app with health check
- `backend/config/settings.py` - Basic configuration

**Functions to Implement**:
```python
# main.py
def create_app() -> FastAPI
def health_check() -> dict
```

**Expected Outcome**: Running FastAPI server on localhost:8000

#### Step 3: Data Models
**Objective**: Define core data structures
**Files to Create**:
- `backend/models/timer.py` - Timer state models
- `backend/models/session.py` - Session configuration models

**Functions to Implement**:
```python
# timer.py
class SessionType(Enum)
class TimerStatus(Enum)
class TimerState(BaseModel)

# session.py
class PomodoroSession(BaseModel)
```

**Expected Outcome**: Well-defined data models with validation

#### Step 4: Basic HTML Template
**Objective**: Create foundation HTML structure
**Files to Create**:
- `frontend/templates/index.html` - Basic HTML structure
- `frontend/static/css/style.css` - Basic CSS styling

**Expected Outcome**: Simple HTML page with timer layout

#### Step 5: Static File Serving
**Objective**: Serve HTML/CSS/JS from FastAPI
**Files to Modify**:
- `backend/main.py` - Add static file mounting

**Functions to Implement**:
```python
def setup_static_files(app: FastAPI)
```

**Expected Outcome**: HTML page served from FastAPI server

### Phase 2: Core Timer Logic (Steps 6-10)

#### Step 6: Timer Service Foundation
**Objective**: Create core timer business logic
**Files to Create**:
- `backend/services/timer_service.py` - Core timer operations

**Functions to Implement**:
```python
class TimerService:
    def __init__(self)
    def create_timer_state(self) -> TimerState
    def get_current_state(self) -> TimerState
    def reset_timer(self) -> TimerState
```

**Expected Outcome**: Basic timer service with state management

#### Step 7: Timer REST API Endpoints
**Objective**: Create API endpoints for timer operations
**Files to Create**:
- `backend/routers/timer.py` - Timer API endpoints

**Functions to Implement**:
```python
def get_timer_status() -> TimerState
def start_timer() -> TimerState
def pause_timer() -> TimerState
def reset_timer() -> TimerState
```

**Expected Outcome**: Working REST API for timer operations

#### Step 8: Frontend Timer JavaScript
**Objective**: Create client-side timer logic
**Files to Create**:
- `frontend/static/js/app.js` - Main application logic
- `frontend/static/js/timer.js` - Timer-specific functions

**Functions to Implement**:
```javascript
// app.js
function initializeApp()
function setupEventListeners()

// timer.js
function startTimer()
function pauseTimer()
function resetTimer()
function updateTimerDisplay()
function formatTime(seconds)
```

**Expected Outcome**: Interactive timer with start/pause/reset functionality

#### Step 9: Timer Display Updates
**Objective**: Real-time timer display updates
**Files to Modify**:
- `frontend/static/js/timer.js` - Add display update logic
- `frontend/static/css/style.css` - Timer display styling

**Functions to Implement**:
```javascript
function updateDisplay(timerState)
function scheduleDisplayUpdate()
setInterval(updateDisplay, 1000)
```

**Expected Outcome**: Timer display updates every second

#### Step 10: Session Management
**Objective**: Handle work/break session transitions
**Files to Modify**:
- `backend/services/timer_service.py` - Add session logic
- `frontend/static/js/timer.js` - Add session handling

**Functions to Implement**:
```python
# Backend
def switch_session(self) -> TimerState
def is_session_complete(self) -> bool

# Frontend
function handleSessionTransition()
function updateSessionInfo()
```

**Expected Outcome**: Automatic transitions between work and break sessions

### Phase 3: Real-time Features (Steps 11-15)

#### Step 11: WebSocket Backend
**Objective**: Implement real-time communication
**Files to Modify**:
- `backend/main.py` - Add WebSocket endpoint
- `backend/services/timer_service.py` - Add WebSocket broadcasting

**Functions to Implement**:
```python
async def websocket_endpoint(websocket: WebSocket)
async def broadcast_timer_update(state: TimerState)
class ConnectionManager:
    def connect(websocket)
    def disconnect(websocket)
    def broadcast(message)
```

**Expected Outcome**: WebSocket server broadcasting timer updates

#### Step 12: WebSocket Frontend
**Objective**: Connect frontend to real-time updates
**Files to Create**:
- `frontend/static/js/websocket.js` - WebSocket client logic

**Functions to Implement**:
```javascript
function connectWebSocket()
function handleWebSocketMessage(event)
function handleWebSocketError(event)
function reconnectWebSocket()
```

**Expected Outcome**: Real-time timer synchronization

#### Step 13: Background Timer Task
**Objective**: Server-side timer countdown
**Files to Modify**:
- `backend/services/timer_service.py` - Add background task

**Functions to Implement**:
```python
async def timer_background_task()
async def update_timer_tick()
def start_background_timer()
def stop_background_timer()
```

**Expected Outcome**: Server maintains timer state, broadcasts updates

#### Step 14: Progress Indicator
**Objective**: Visual progress representation
**Files to Modify**:
- `frontend/static/css/style.css` - Progress bar styling
- `frontend/static/js/timer.js` - Progress calculation

**Functions to Implement**:
```javascript
function updateProgressIndicator(percentage)
function calculateProgress(currentTime, totalTime)
```

**Functions to Style**:
```css
.progress-circle
.progress-bar
.progress-fill
```

**Expected Outcome**: Visual progress indicator showing session completion

#### Step 15: Session Type Styling
**Objective**: Different visual themes for work/break
**Files to Modify**:
- `frontend/static/css/style.css` - Session-specific styling
- `frontend/static/js/timer.js` - Style switching logic

**Functions to Implement**:
```javascript
function updateSessionStyling(sessionType)
function getSessionTheme(sessionType)
```

**CSS Classes to Create**:
```css
.work-session
.break-session
.session-transition
```

**Expected Outcome**: Distinct visual themes for different session types

### Phase 4: Enhanced User Experience (Steps 16-20)

#### Step 16: Audio Notifications
**Objective**: Sound alerts for session transitions
**Files to Create**:
- `frontend/static/js/notifications.js` - Notification handling
- Add audio files to `frontend/static/assets/sounds/`

**Functions to Implement**:
```javascript
function playAudioNotification(type)
function loadAudioFiles()
function setVolume(level)
```

**Expected Outcome**: Audio alerts when sessions complete

#### Step 17: Browser Notifications
**Objective**: Desktop notifications for session changes
**Files to Modify**:
- `frontend/static/js/notifications.js` - Add browser notifications

**Functions to Implement**:
```javascript
function requestNotificationPermission()
function showBrowserNotification(title, message)
function checkNotificationSupport()
```

**Expected Outcome**: Desktop notifications with user permission

#### Step 18: Responsive Design
**Objective**: Mobile-friendly interface
**Files to Modify**:
- `frontend/static/css/style.css` - Responsive styling
- Add `frontend/static/css/responsive.css`

**CSS Features to Implement**:
```css
@media (max-width: 768px)
@media (max-width: 480px)
.mobile-layout
.touch-friendly
```

**Expected Outcome**: Fully responsive design across devices

#### Step 19: Keyboard Shortcuts
**Objective**: Keyboard accessibility
**Files to Modify**:
- `frontend/static/js/app.js` - Keyboard event handling

**Functions to Implement**:
```javascript
function setupKeyboardShortcuts()
function handleKeyPress(event)
function toggleTimer() // Space bar
function resetTimer() // 'R' key
```

**Expected Outcome**: Keyboard shortcuts for main actions

#### Step 20: Session Counter & Statistics
**Objective**: Track completed sessions
**Files to Modify**:
- `backend/services/timer_service.py` - Session tracking
- `frontend/static/js/timer.js` - Counter display

**Functions to Implement**:
```python
# Backend
def increment_session_count()
def get_session_statistics()

# Frontend
function updateSessionCounter()
function displayStatistics()
```

**Expected Outcome**: Session counter and basic statistics

### Phase 5: Polish & Testing (Steps 21-25)

#### Step 21: Error Handling
**Objective**: Robust error handling
**Files to Modify**:
- All JavaScript files - Add try/catch blocks
- All Python files - Add error handling

**Functions to Implement**:
```javascript
function handleAPIError(error)
function showErrorMessage(message)

# Python
def handle_timer_error(error)
def log_error(error)
```

**Expected Outcome**: Graceful error handling throughout app

#### Step 22: Loading States
**Objective**: User feedback during operations
**Files to Modify**:
- `frontend/static/js/app.js` - Loading indicators
- `frontend/static/css/style.css` - Loading animations

**Functions to Implement**:
```javascript
function showLoadingState()
function hideLoadingState()
function disableButtons()
function enableButtons()
```

**Expected Outcome**: Clear feedback during API calls

#### Step 23: Configuration Options
**Objective**: Customizable timer durations
**Files to Modify**:
- `backend/routers/timer.py` - Configuration endpoints
- `frontend/templates/index.html` - Settings UI

**Functions to Implement**:
```python
def get_timer_config()
def update_timer_config(config)

# Frontend
function showSettingsModal()
function saveSettings()
function loadSettings()
```

**Expected Outcome**: User-customizable timer settings

#### Step 24: Testing Setup
**Objective**: Automated testing infrastructure
**Files to Create**:
- `tests/test_timer_service.py` - Service tests
- `tests/test_api.py` - API endpoint tests
- `tests/conftest.py` - Test configuration

**Test Functions to Implement**:
```python
def test_timer_creation()
def test_timer_start_stop()
def test_session_transitions()
def test_api_endpoints()
```

**Expected Outcome**: Comprehensive test suite

#### Step 25: Documentation & Deployment
**Objective**: Production readiness
**Files to Create/Modify**:
- Update `README.md` - Usage instructions
- Create `docker/Dockerfile` - Containerization
- Create `deployment/` - Deployment scripts

**Documentation to Create**:
- API documentation
- User guide
- Deployment guide
- Contributing guidelines

**Expected Outcome**: Production-ready application with documentation

## Implementation Guidelines

### GitHub Copilot Optimization
- Use descriptive function names and type hints
- Write clear docstrings for complex functions
- Add comments explaining business logic
- Use consistent naming conventions
- Structure code in small, focused functions

### Testing Strategy
- Write tests immediately after implementing each function
- Test both happy path and edge cases
- Mock external dependencies
- Test responsive design on multiple devices

### Code Quality
- Follow PEP 8 for Python code
- Use ESLint configuration for JavaScript
- Implement proper error handling
- Add logging for debugging
- Use semantic HTML elements

### Development Workflow
1. Implement backend function
2. Write tests for the function
3. Implement corresponding frontend function
4. Test integration
5. Update documentation
6. Commit changes with descriptive messages

## Success Criteria

### Phase 1 Success
- ✅ FastAPI server running
- ✅ Basic HTML page displayed
- ✅ Project structure established

### Phase 2 Success
- ✅ Timer starts, pauses, resets
- ✅ Display updates every second
- ✅ Session transitions work

### Phase 3 Success
- ✅ Real-time updates via WebSocket
- ✅ Multiple clients synchronized
- ✅ Visual progress indicator

### Phase 4 Success
- ✅ Audio and browser notifications
- ✅ Responsive on all devices
- ✅ Keyboard shortcuts functional

### Phase 5 Success
- ✅ Error handling robust
- ✅ User settings configurable
- ✅ Tests passing
- ✅ Documentation complete

## Estimated Timeline

- **Phase 1**: 2-3 hours (Foundation)
- **Phase 2**: 4-5 hours (Core Features)
- **Phase 3**: 3-4 hours (Real-time)
- **Phase 4**: 3-4 hours (Enhanced UX)
- **Phase 5**: 2-3 hours (Polish)

**Total Estimated Time**: 14-19 hours

This plan provides granular steps that are perfect for learning GitHub Copilot while building a complete, production-ready Pomodoro timer application.