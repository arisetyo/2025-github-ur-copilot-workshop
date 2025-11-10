"""Timer data models for Pomodoro Timer application."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class SessionType(Enum):
    """Enumeration for different session types in Pomodoro technique."""
    WORK = "work"
    BREAK = "break"


class TimerStatus(Enum):
    """Enumeration for timer status states."""
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"


@dataclass
class TimerState:
    """Data class representing the current state of the Pomodoro timer.
    
    Attributes:
        current_time: Seconds remaining in current session
        session_type: Current session type (work or break)
        status: Current timer status (running, paused, or stopped)
        session_count: Number of completed work sessions
        total_time: Total duration of current session type in seconds
        start_time: Unix timestamp when current session started
    """
    current_time: int
    session_type: SessionType
    status: TimerStatus
    session_count: int = 0
    total_time: int = 1500  # Default 25 minutes for work session
    start_time: Optional[float] = None
    
    def __post_init__(self):
        """Validate timer state after initialization."""
        if self.current_time < 0:
            raise ValueError("Current time cannot be negative")
        if self.session_count < 0:
            raise ValueError("Session count cannot be negative")
        if self.total_time <= 0:
            raise ValueError("Total time must be positive")
    
    @property
    def progress_percentage(self) -> float:
        """Calculate the completion percentage of current session."""
        if self.total_time == 0:
            return 100.0
        return ((self.total_time - self.current_time) / self.total_time) * 100.0
    
    @property
    def is_complete(self) -> bool:
        """Check if the current session is complete."""
        return self.current_time <= 0
    
    def to_dict(self) -> dict:
        """Convert timer state to dictionary for JSON serialization."""
        return {
            "current_time": self.current_time,
            "session_type": self.session_type.value,
            "status": self.status.value,
            "session_count": self.session_count,
            "total_time": self.total_time,
            "progress_percentage": round(self.progress_percentage, 1),
            "is_complete": self.is_complete,
            "start_time": self.start_time
        }