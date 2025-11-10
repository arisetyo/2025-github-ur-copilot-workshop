"""Timer API routes for Pomodoro Timer application."""

import time
from flask import Blueprint, jsonify, request
from typing import Dict, Any

from models.timer import TimerState
from models.session import PomodoroSession


# Global timer service instance (will be injected by app)
timer_service = None


def init_timer_routes(service):
    """Initialize timer routes with service dependency."""
    global timer_service
    timer_service = service


# Create blueprint for timer routes
timer_bp = Blueprint('timer', __name__, url_prefix='/api/timer')


@timer_bp.route('/status', methods=['GET'])
def get_timer_status() -> Dict[str, Any]:
    """Get current timer status.
    
    Returns:
        JSON response with current timer state
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        current_state = timer_service.get_current_state()
        
        return jsonify({
            'status': 'success',
            'data': current_state.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get timer status: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/start', methods=['POST'])
def start_timer() -> Dict[str, Any]:
    """Start the timer.
    
    Returns:
        JSON response with updated timer state
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        updated_state = timer_service.start_timer()
        
        return jsonify({
            'status': 'success',
            'message': 'Timer started successfully',
            'data': updated_state.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to start timer: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/pause', methods=['POST'])
def pause_timer() -> Dict[str, Any]:
    """Pause the timer.
    
    Returns:
        JSON response with updated timer state
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        updated_state = timer_service.pause_timer()
        
        return jsonify({
            'status': 'success',
            'message': 'Timer paused successfully',
            'data': updated_state.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to pause timer: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/reset', methods=['POST'])
def reset_timer() -> Dict[str, Any]:
    """Reset the timer.
    
    Returns:
        JSON response with reset timer state
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        reset_state = timer_service.reset_timer()
        
        return jsonify({
            'status': 'success',
            'message': 'Timer reset successfully',
            'data': reset_state.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to reset timer: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/skip', methods=['POST'])
def skip_session() -> Dict[str, Any]:
    """Skip to next session.
    
    Returns:
        JSON response with updated timer state
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        updated_state = timer_service.skip_session()
        
        return jsonify({
            'status': 'success',
            'message': 'Session skipped successfully',
            'data': updated_state.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to skip session: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/config', methods=['GET'])
def get_timer_config() -> Dict[str, Any]:
    """Get timer configuration.
    
    Returns:
        JSON response with current timer configuration
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        config = timer_service.get_session_config()
        
        return jsonify({
            'status': 'success',
            'data': config.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get timer config: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/config', methods=['PUT'])
def update_timer_config() -> Dict[str, Any]:
    """Update timer configuration.
    
    Expected JSON payload:
    {
        "work_duration": 1500,      // seconds
        "break_duration": 300,      // seconds
        "long_break_duration": 900, // seconds (optional)
        "sessions_until_long_break": 4 // optional
    }
    
    Returns:
        JSON response with updated configuration
    """
    try:
        if timer_service is None:
            return jsonify({
                'error': 'Timer service not initialized',
                'status': 'error'
            }), 500
        
        if not request.json:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400
        
        data = request.json
        
        # Validate required fields
        required_fields = ['work_duration', 'break_duration']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
            
            if not isinstance(data[field], int) or data[field] <= 0:
                return jsonify({
                    'error': f'{field} must be a positive integer',
                    'status': 'error'
                }), 400
        
        # Validate optional fields
        if 'long_break_duration' in data:
            if not isinstance(data['long_break_duration'], int) or data['long_break_duration'] <= 0:
                return jsonify({
                    'error': 'long_break_duration must be a positive integer',
                    'status': 'error'
                }), 400
        
        if 'sessions_until_long_break' in data:
            if not isinstance(data['sessions_until_long_break'], int) or data['sessions_until_long_break'] <= 0:
                return jsonify({
                    'error': 'sessions_until_long_break must be a positive integer',
                    'status': 'error'
                }), 400
        
        # Create new configuration
        try:
            new_config = PomodoroSession.from_dict(data)
            timer_service.update_session_config(new_config)
            
            return jsonify({
                'status': 'success',
                'message': 'Timer configuration updated successfully',
                'data': new_config.to_dict()
            }), 200
            
        except ValueError as ve:
            return jsonify({
                'error': f'Invalid configuration: {str(ve)}',
                'status': 'error'
            }), 400
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to update timer config: {str(e)}',
            'status': 'error'
        }), 500


@timer_bp.route('/health', methods=['GET'])
def health_check() -> Dict[str, Any]:
    """Health check endpoint for timer API.
    
    Returns:
        JSON response indicating API health status
    """
    try:
        service_status = 'healthy' if timer_service is not None else 'service_not_initialized'
        
        return jsonify({
            'status': 'success',
            'message': 'Timer API is healthy',
            'service_status': service_status,
            'timestamp': str(int(time.time()))
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Health check failed: {str(e)}',
            'status': 'error'
        }), 500


# Error handlers
@timer_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors for timer routes."""
    return jsonify({
        'error': 'Timer endpoint not found',
        'status': 'error'
    }), 404


@timer_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors for timer routes."""
    return jsonify({
        'error': 'Method not allowed for this timer endpoint',
        'status': 'error'
    }), 405


@timer_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for timer routes."""
    return jsonify({
        'error': 'Internal server error in timer service',
        'status': 'error'
    }), 500