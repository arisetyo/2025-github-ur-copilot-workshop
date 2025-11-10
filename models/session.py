"""Session configuration models for Pomodoro Timer application."""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PomodoroSession:
    """Configuration class for Pomodoro session durations and settings.
    
    Attributes:
        work_duration: Duration of work sessions in seconds (default: 25 minutes)
        break_duration: Duration of short break sessions in seconds (default: 5 minutes)
        long_break_duration: Duration of long break sessions in seconds (default: 15 minutes)
        sessions_until_long_break: Number of work sessions before long break (default: 4)
    """
    work_duration: int = 1500      # 25 minutes in seconds
    break_duration: int = 300      # 5 minutes in seconds
    long_break_duration: int = 900 # 15 minutes in seconds
    sessions_until_long_break: int = 4
    
    def __post_init__(self):
        """Validate session configuration after initialization."""
        if self.work_duration <= 0:
            raise ValueError("Work duration must be positive")
        if self.break_duration <= 0:
            raise ValueError("Break duration must be positive")
        if self.long_break_duration <= 0:
            raise ValueError("Long break duration must be positive")
        if self.sessions_until_long_break <= 0:
            raise ValueError("Sessions until long break must be positive")
    
    def get_session_duration(self, session_type: str, session_count: int = 0) -> int:
        """Get the duration for a specific session type.
        
        Args:
            session_type: Type of session ('work', 'break')
            session_count: Current completed work session count
            
        Returns:
            Duration in seconds for the specified session type
        """
        if session_type == "work":
            return self.work_duration
        elif session_type == "break":
            # Check if it's time for a long break
            if session_count > 0 and session_count % self.sessions_until_long_break == 0:
                return self.long_break_duration
            return self.break_duration
        else:
            raise ValueError(f"Unknown session type: {session_type}")
    
    def is_long_break_due(self, session_count: int) -> bool:
        """Check if a long break is due based on session count.
        
        Args:
            session_count: Number of completed work sessions
            
        Returns:
            True if long break is due, False otherwise
        """
        return session_count > 0 and session_count % self.sessions_until_long_break == 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session configuration to dictionary for JSON serialization."""
        return {
            "work_duration": self.work_duration,
            "break_duration": self.break_duration,
            "long_break_duration": self.long_break_duration,
            "sessions_until_long_break": self.sessions_until_long_break
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PomodoroSession':
        """Create PomodoroSession instance from dictionary.
        
        Args:
            data: Dictionary containing session configuration
            
        Returns:
            PomodoroSession instance
        """
        return cls(
            work_duration=data.get('work_duration', 1500),
            break_duration=data.get('break_duration', 300),
            long_break_duration=data.get('long_break_duration', 900),
            sessions_until_long_break=data.get('sessions_until_long_break', 4)
        )