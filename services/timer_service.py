"""Timer service for Pomodoro Timer application business logic."""

import threading
import time
from typing import Optional, Callable
from datetime import datetime

from models.timer import TimerState, SessionType, TimerStatus
from models.session import PomodoroSession


class TimerService:
    """Service class for managing Pomodoro timer state and operations."""
    
    def __init__(self, session_config: Optional[PomodoroSession] = None):
        """Initialize timer service with optional custom configuration.
        
        Args:
            session_config: Custom session configuration, uses defaults if None
        """
        self._session_config = session_config or PomodoroSession()
        self._current_state: Optional[TimerState] = None
        self._timer_thread: Optional[threading.Thread] = None
        self._timer_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._update_callback: Optional[Callable[[TimerState], None]] = None
        self._session_complete_callback: Optional[Callable[[TimerState], None]] = None
        
        # Initialize with default work session
        self.reset_timer()
    
    def set_update_callback(self, callback: Callable[[TimerState], None]) -> None:
        """Set callback function for timer updates.
        
        Args:
            callback: Function to call on each timer update
        """
        self._update_callback = callback
    
    def set_session_complete_callback(self, callback: Callable[[TimerState], None]) -> None:
        """Set callback function for session completions.
        
        Args:
            callback: Function to call when a session completes
        """
        self._session_complete_callback = callback
    
    def create_timer_state(self, session_type: SessionType = SessionType.WORK) -> TimerState:
        """Create a new timer state with specified session type.
        
        Args:
            session_type: Type of session to create
            
        Returns:
            New TimerState instance
        """
        duration = self._session_config.get_session_duration(
            session_type.value,
            self._current_state.session_count if self._current_state else 0
        )
        
        return TimerState(
            current_time=duration,
            session_type=session_type,
            status=TimerStatus.STOPPED,
            session_count=self._current_state.session_count if self._current_state else 0,
            total_time=duration,
            start_time=None
        )
    
    def get_current_state(self) -> TimerState:
        """Get the current timer state.
        
        Returns:
            Current TimerState
        """
        with self._timer_lock:
            if self._current_state is None:
                self._current_state = self.create_timer_state()
            return self._current_state
    
    def start_timer(self) -> TimerState:
        """Start the timer countdown.
        
        Returns:
            Updated TimerState after starting
        """
        with self._timer_lock:
            if self._current_state is None:
                self._current_state = self.create_timer_state()
            
            if self._current_state.status != TimerStatus.RUNNING:
                self._current_state.status = TimerStatus.RUNNING
                self._current_state.start_time = time.time()
                
                # Start background timer thread if not already running
                if self._timer_thread is None or not self._timer_thread.is_alive():
                    self._stop_event.clear()
                    self._timer_thread = threading.Thread(target=self._timer_background_task, daemon=True)
                    self._timer_thread.start()
        
        return self.get_current_state()
    
    def pause_timer(self) -> TimerState:
        """Pause the timer countdown.
        
        Returns:
            Updated TimerState after pausing
        """
        with self._timer_lock:
            if self._current_state and self._current_state.status == TimerStatus.RUNNING:
                self._current_state.status = TimerStatus.PAUSED
        
        return self.get_current_state()
    
    def reset_timer(self) -> TimerState:
        """Reset the timer to initial state.
        
        Returns:
            Reset TimerState
        """
        with self._timer_lock:
            # Stop background timer
            self._stop_event.set()
            
            # Create new timer state, preserving session type if exists
            session_type = SessionType.WORK
            session_count = 0
            
            if self._current_state:
                session_type = self._current_state.session_type
                session_count = self._current_state.session_count
            
            self._current_state = self.create_timer_state(session_type)
            self._current_state.session_count = session_count
        
        return self.get_current_state()
    
    def skip_session(self) -> TimerState:
        """Skip to the next session type.
        
        Returns:
            Updated TimerState with next session
        """
        with self._timer_lock:
            if self._current_state is None:
                self._current_state = self.create_timer_state()
            
            # Stop current timer
            self._stop_event.set()
            
            current_session_count = self._current_state.session_count
            
            # Determine next session type
            if self._current_state.session_type == SessionType.WORK:
                # Increment session count when completing work session
                current_session_count += 1
                next_session = SessionType.BREAK
            else:
                # No increment for break sessions
                next_session = SessionType.WORK
            
            # Create new state for next session
            self._current_state = self.create_timer_state(next_session)
            self._current_state.session_count = current_session_count
            self._current_state.status = TimerStatus.STOPPED
        
        return self.get_current_state()
    
    def update_timer_tick(self) -> bool:
        """Update timer by one second (internal method).
        
        Returns:
            True if session is complete, False otherwise
        """
        with self._timer_lock:
            if (self._current_state and 
                self._current_state.status == TimerStatus.RUNNING and 
                self._current_state.current_time > 0):
                
                self._current_state.current_time -= 1
                
                # Check if session is complete
                if self._current_state.current_time <= 0:
                    return True
        
        return False
    
    def switch_session(self) -> TimerState:
        """Switch to the next session type automatically.
        
        Returns:
            Updated TimerState with new session
        """
        with self._timer_lock:
            if self._current_state is None:
                return self.create_timer_state()
            
            current_session_count = self._current_state.session_count
            
            # Determine next session and update session count
            if self._current_state.session_type == SessionType.WORK:
                current_session_count += 1
                next_session = SessionType.BREAK
            else:
                next_session = SessionType.WORK
            
            # Create new session
            self._current_state = self.create_timer_state(next_session)
            self._current_state.session_count = current_session_count
            self._current_state.status = TimerStatus.RUNNING
            self._current_state.start_time = time.time()
        
        return self.get_current_state()
    
    def is_session_complete(self) -> bool:
        """Check if the current session is complete.
        
        Returns:
            True if session is complete, False otherwise
        """
        with self._timer_lock:
            return (self._current_state is not None and 
                   self._current_state.current_time <= 0)
    
    def update_session_config(self, new_config: PomodoroSession) -> None:
        """Update session configuration.
        
        Args:
            new_config: New session configuration
        """
        with self._timer_lock:
            self._session_config = new_config
            
            # If timer is stopped, update current session duration
            if (self._current_state and 
                self._current_state.status == TimerStatus.STOPPED):
                
                new_duration = self._session_config.get_session_duration(
                    self._current_state.session_type.value,
                    self._current_state.session_count
                )
                
                self._current_state.current_time = new_duration
                self._current_state.total_time = new_duration
    
    def get_session_config(self) -> PomodoroSession:
        """Get current session configuration.
        
        Returns:
            Current PomodoroSession configuration
        """
        return self._session_config
    
    def stop_timer_service(self) -> None:
        """Stop the timer service and cleanup background thread."""
        self._stop_event.set()
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_thread.join(timeout=1.0)
    
    def _timer_background_task(self) -> None:
        """Background task that handles timer countdown."""
        while not self._stop_event.is_set():
            try:
                # Update timer every second
                session_complete = self.update_timer_tick()
                
                # Notify callback of timer update
                if self._update_callback:
                    self._update_callback(self.get_current_state())
                
                # Handle session completion
                if session_complete:
                    # Notify callback of session completion
                    if self._session_complete_callback:
                        self._session_complete_callback(self.get_current_state())
                    
                    # Auto-switch to next session
                    self.switch_session()
                    
                    # Continue running the new session
                    continue
                
                # Sleep for 1 second
                time.sleep(1.0)
                
            except Exception as e:
                # Log error and continue
                print(f"Timer background task error: {e}")
                time.sleep(1.0)