"""Configuration settings for Pomodoro Timer application."""

import os
from typing import Dict, Any


class Config:
    """Base configuration class."""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Socket.IO Configuration
    SOCKETIO_ASYNC_MODE = 'threading'
    SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
    
    # Timer Configuration
    DEFAULT_WORK_DURATION = 1500      # 25 minutes in seconds
    DEFAULT_BREAK_DURATION = 300      # 5 minutes in seconds
    DEFAULT_LONG_BREAK_DURATION = 900 # 15 minutes in seconds
    DEFAULT_SESSIONS_UNTIL_LONG_BREAK = 4
    
    # API Configuration
    API_PREFIX = '/api'
    
    @staticmethod
    def get_timer_defaults() -> Dict[str, Any]:
        """Get default timer configuration."""
        return {
            'work_duration': Config.DEFAULT_WORK_DURATION,
            'break_duration': Config.DEFAULT_BREAK_DURATION,
            'long_break_duration': Config.DEFAULT_LONG_BREAK_DURATION,
            'sessions_until_long_break': Config.DEFAULT_SESSIONS_UNTIL_LONG_BREAK
        }


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    # Enable Flask-SocketIO debugging
    SOCKETIO_LOGGER = True
    SOCKETIO_ENGINEIO_LOGGER = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
    # Use secure secret key in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-me'
    
    # Production Socket.IO settings
    SOCKETIO_ASYNC_MODE = 'threading'
    SOCKETIO_CORS_ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '').split(',')
    
    def __init__(self):
        if self.SECRET_KEY == 'production-secret-key-change-me':
            import warnings
            warnings.warn("Using default SECRET_KEY in production. Please set SECRET_KEY environment variable.")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    
    # Test-specific timer durations (shorter for faster tests)
    DEFAULT_WORK_DURATION = 10       # 10 seconds for testing
    DEFAULT_BREAK_DURATION = 5       # 5 seconds for testing
    DEFAULT_LONG_BREAK_DURATION = 15 # 15 seconds for testing


# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """Get configuration class based on environment name.
    
    Args:
        config_name: Name of the configuration ('development', 'production', 'testing')
        
    Returns:
        Configuration class instance
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config_map.get(config_name, DevelopmentConfig)