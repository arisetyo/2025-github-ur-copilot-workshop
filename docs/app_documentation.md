# Pomodoro Timer Web Application Documentation

## Overview
This application is a modern Pomodoro timer built with Flask (Python) for the backend and HTML/CSS/JavaScript for the frontend. It features real-time updates, audio/visual notifications, and a clean, responsive UI. The project is designed for educational purposes and demonstrates best practices in web development and GitHub Copilot usage.

---

## User Flow Chart

```mermaid
flowchart TD
    A[User opens app] --> B[Timer UI loads]
    B --> C{User action}
    C -->|Start| D[Send /api/timer/start]
    C -->|Pause| E[Send /api/timer/pause]
    C -->|Reset| F[Send /api/timer/reset]
    C -->|Skip| G[Send /api/timer/skip]
    D --> H[Backend starts timer]
    H --> I[Socket.IO emits timer_update]
    I --> J[Frontend updates UI]
    J --> K{Session ends?}
    K -->|Yes| L[Show notification]
    K -->|No| C
    L --> M[Start next session]
    M --> D
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend
    participant BE as Backend
    participant SIO as Socket.IO

    U->>FE: Clicks Start
    FE->>BE: POST /api/timer/start
    BE->>SIO: Emit timer_update
    SIO->>FE: Receive timer_update
    FE->>FE: Update timer display
    BE->>SIO: Emit session_complete (if session ends)
    SIO->>FE: Receive session_complete
    FE->>FE: Show notification
    U->>FE: Clicks Pause/Reset/Skip
    FE->>BE: POST /api/timer/pause/reset/skip
    BE->>SIO: Emit timer_update
    SIO->>FE: Receive timer_update
    FE->>FE: Update timer display
```

---

## How the Application Works

### 1. User Interface
- The user interacts with a timer display, control buttons (start, pause, reset, skip), and session indicators.
- UI updates in real-time as the timer progresses or session changes.

### 2. Backend API
- Flask provides REST endpoints for timer control and configuration.
- Timer logic runs in a background thread, managing session transitions and timing.
- Socket.IO is used for real-time communication, broadcasting timer updates and session completions to all connected clients.

### 3. Frontend Logic
- JavaScript modules handle timer state, UI updates, notifications, and Socket.IO events.
- Audio and browser notifications alert the user when sessions start/end.
- LocalStorage is used for user preferences and session statistics.

### 4. Real-Time Updates
- When the timer starts, the backend emits `timer_update` events via Socket.IO.
- The frontend listens for these events and updates the timer display instantly.
- Session transitions trigger notifications and UI changes.

### 5. Customization & Persistence
- Users can adjust session durations and themes via the settings panel.
- Preferences are saved locally and can be loaded on subsequent visits.

---

## Key Features
 - Enhanced Visual Feedback: The application now provides improved visual cues and effects during timer transitions, session completions, and notifications. This includes dynamic animations, color changes, and more engaging feedback to help users track their progress and stay motivated.
- Modular codebase: `models/`, `routes/`, `services/`, `static/`, `templates/`
- RESTful API and Socket.IO for real-time features
- Unit tests for backend logic and API endpoints
- Easily extensible for new features

---

For more details, see `docs/architecture.md`.
