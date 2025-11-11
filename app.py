"""Main Flask application for Pomodoro Timer."""

import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

from config.settings import get_config
from services.timer_service import TimerService
from routes.timer import timer_bp, init_timer_routes
from models.session import PomodoroSession


# Global instances
socketio = SocketIO()
timer_service = None


def create_app(config_name: str = None) -> Flask:
    """Create and configure Flask application.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Initialize extensions
    socketio.init_app(
        app,
        async_mode=app.config['SOCKETIO_ASYNC_MODE'],
        cors_allowed_origins=app.config['SOCKETIO_CORS_ALLOWED_ORIGINS']
    )
    
    # Initialize timer service
    global timer_service
    session_config = PomodoroSession(
        work_duration=config.DEFAULT_WORK_DURATION,
        break_duration=config.DEFAULT_BREAK_DURATION,
        long_break_duration=config.DEFAULT_LONG_BREAK_DURATION,
        sessions_until_long_break=config.DEFAULT_SESSIONS_UNTIL_LONG_BREAK
    )
    timer_service = TimerService(session_config)
    
    # Set up timer callbacks for Socket.IO events
    timer_service.set_update_callback(handle_timer_update)
    timer_service.set_session_complete_callback(handle_session_complete)
    
    # Initialize routes
    init_timer_routes(timer_service)
    
    # Register blueprints
    app.register_blueprint(timer_bp)
    
    # Register main routes
    register_main_routes(app)
    
    # Register Socket.IO events
    register_socket_events()
    
    return app


def register_main_routes(app: Flask) -> None:
    """Register main application routes.
    
    Args:
        app: Flask application instance
    """
    @app.route('/')
    def index():
        """Serve main application page."""
        return render_template('index.html')
    
    @app.route('/health')
    def health_check():
        """Application health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'message': 'Pomodoro Timer API is running',
            'timer_service': 'initialized' if timer_service else 'not_initialized'
        }), 200
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return jsonify({
            'error': 'Page not found',
            'status': 'error'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500


def register_socket_events() -> None:
    """Register Socket.IO event handlers."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        print('Client connected')
        
        # Send current timer state to newly connected client
        if timer_service:
            current_state = timer_service.get_current_state()
            emit('timer_update', current_state.to_dict())
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        print('Client disconnected')
    
    @socketio.on('request_timer_status')
    def handle_timer_status_request():
        """Handle request for current timer status."""
        if timer_service:
            current_state = timer_service.get_current_state()
            emit('timer_update', current_state.to_dict())


def handle_timer_update(timer_state) -> None:
    """Handle timer update events from timer service.
    
    Args:
        timer_state: Updated TimerState object
    """
    socketio.emit('timer_update', timer_state.to_dict())


def handle_session_complete(timer_state) -> None:
    """Handle session completion events from timer service.
    
    Args:
        timer_state: TimerState object at completion
    """
    socketio.emit('session_complete', {
        'message': f'{timer_state.session_type.value.title()} session completed!',
        'session_type': timer_state.session_type.value,
        'session_count': timer_state.session_count,
        'next_session': 'break' if timer_state.session_type.value == 'work' else 'work'
    })


def main():
    """Main entry point for development server."""
    app = create_app('development')
    
    # Run with Socket.IO support
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )


if __name__ == '__main__':
    main()