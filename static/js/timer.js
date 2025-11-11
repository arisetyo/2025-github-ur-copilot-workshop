/**
 * Timer-specific functionality for Pomodoro Timer application
 */

class Timer {
    constructor() {
        this.currentState = null;
        this.displayInterval = null;
        this.elements = this.initializeElements();
        this.setupEventListeners();
    }

    /**
     * Initialize DOM element references
     * @returns {Object} Object containing DOM element references
     */
    initializeElements() {
        return {
            timerMinutes: document.getElementById('timer-minutes'),
            timerSeconds: document.getElementById('timer-seconds'),
            sessionType: document.getElementById('session-type-text'),
            currentSession: document.getElementById('current-session'),
            startStopBtn: document.getElementById('start-stop-btn'),
            resetBtn: document.getElementById('reset-btn'),
            skipBtn: document.getElementById('skip-btn'),
            progressCircle: document.querySelector('.progress-ring-circle'),
            body: document.body
        };
    }

    /**
     * Set up event listeners for timer controls
     */
    setupEventListeners() {
        this.elements.startStopBtn.addEventListener('click', () => this.toggleTimer());
        this.elements.resetBtn.addEventListener('click', () => this.resetTimer());
        this.elements.skipBtn.addEventListener('click', () => this.skipSession());
    }

    /**
     * Initialize timer with current state
     * @param {Object} initialState - Initial timer state from server
     */
    initialize(initialState) {
        this.currentState = initialState;
        this.updateDisplay();
        this.updateProgressIndicator();
        this.updateSessionInfo();
        this.updateControlButtons();
    }

    /**
     * Toggle timer between start and pause
     */
    async toggleTimer() {
        try {
            this.showLoadingState();
            
            const endpoint = this.currentState?.status === 'running' ? '/api/timer/pause' : '/api/timer/start';
            const response = await fetch(endpoint, { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentState = data.data;
                this.updateDisplay();
                this.updateControlButtons();
                
                // Show success notification
                if (window.notifications) {
                    const message = this.currentState.status === 'running' ? 'Timer started!' : 'Timer paused!';
                    window.notifications.show(message, 'success');
                }
            } else {
                throw new Error(data.error || 'Failed to toggle timer');
            }
        } catch (error) {
            console.error('Error toggling timer:', error);
            if (window.notifications) {
                window.notifications.show(`Error: ${error.message}`, 'error');
            }
        } finally {
            this.hideLoadingState();
        }
    }

    /**
     * Reset timer to initial state
     */
    async resetTimer() {
        try {
            this.showLoadingState();
            
            const response = await fetch('/api/timer/reset', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentState = data.data;
                this.updateDisplay();
                this.updateProgressIndicator();
                this.updateControlButtons();
                
                if (window.notifications) {
                    window.notifications.show('Timer reset!', 'success');
                }
            } else {
                throw new Error(data.error || 'Failed to reset timer');
            }
        } catch (error) {
            console.error('Error resetting timer:', error);
            if (window.notifications) {
                window.notifications.show(`Error: ${error.message}`, 'error');
            }
        } finally {
            this.hideLoadingState();
        }
    }

    /**
     * Skip to next session
     */
    async skipSession() {
        try {
            this.showLoadingState();
            
            const response = await fetch('/api/timer/skip', { method: 'POST' });
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentState = data.data;
                this.updateDisplay();
                this.updateProgressIndicator();
                this.updateSessionInfo();
                this.updateControlButtons();
                
                if (window.notifications) {
                    window.notifications.show('Session skipped!', 'success');
                }
            } else {
                throw new Error(data.error || 'Failed to skip session');
            }
        } catch (error) {
            console.error('Error skipping session:', error);
            if (window.notifications) {
                window.notifications.show(`Error: ${error.message}`, 'error');
            }
        } finally {
            this.hideLoadingState();
        }
    }

    /**
     * Update timer display with current state
     */
    updateDisplay() {
        if (!this.currentState) return;

        const { minutes, seconds } = this.formatTime(this.currentState.current_time);
        
        this.elements.timerMinutes.textContent = minutes;
        this.elements.timerSeconds.textContent = seconds;
        
        // Update document title
        document.title = `${minutes}:${seconds} - ${this.currentState.session_type.charAt(0).toUpperCase() + this.currentState.session_type.slice(1)} - Pomodoro Timer`;
    }

    /**
     * Update progress indicator
     */
    updateProgressIndicator() {
        if (!this.currentState) return;

        const progressPercentage = this.currentState.progress_percentage;
        const circumference = 2 * Math.PI * 120; // radius = 120
        const strokeDashoffset = circumference - (progressPercentage / 100) * circumference;
        
        this.elements.progressCircle.style.strokeDashoffset = strokeDashoffset;
        
        // Update progress ring color for session type
        const color = this.currentState.session_type === 'work' ? '#2563eb' : '#16a34a';
        this.elements.progressCircle.style.stroke = color;
    }

    /**
     * Update session information display
     */
    updateSessionInfo() {
        if (!this.currentState) return;

        // Update session type text
        const sessionText = this.currentState.session_type === 'work' ? 'Work Session' : 'Break Session';
        this.elements.sessionType.textContent = sessionText;
        
        // Update session counter
        this.elements.currentSession.textContent = this.currentState.session_count + 1;
        
        // Update body class for theme
        this.elements.body.className = `${this.currentState.session_type}-session`;
    }

    /**
     * Update control button states
     */
    updateControlButtons() {
        if (!this.currentState) return;

        const isRunning = this.currentState.status === 'running';
        const isPaused = this.currentState.status === 'paused';
        const isStopped = this.currentState.status === 'stopped';
        
        // Update start/stop button
        const startStopText = isRunning ? 'Pause' : 'Start';
        this.elements.startStopBtn.querySelector('.btn-text').textContent = startStopText;
        this.elements.startStopBtn.setAttribute('aria-label', isRunning ? 'Pause timer' : 'Start timer');
        
        // Enable/disable buttons based on state
        this.elements.resetBtn.disabled = false;
        this.elements.skipBtn.disabled = false;
    }

    /**
     * Handle timer state updates from Socket.IO
     * @param {Object} newState - Updated timer state
     */
    handleStateUpdate(newState) {
        this.currentState = newState;
        this.updateDisplay();
        this.updateProgressIndicator();
        this.updateSessionInfo();
        this.updateControlButtons();
    }

    /**
     * Handle session completion
     * @param {Object} completionData - Session completion data
     */
    handleSessionComplete(completionData) {
        // Play notification sound if available
        if (window.notifications) {
            window.notifications.playSound();
            window.notifications.showBrowser(
                'Session Complete!',
                completionData.message
            );
        }
        
        // Visual feedback
        this.showSessionTransition(completionData);
    }

    /**
     * Show session transition animation
     * @param {Object} completionData - Session completion data
     */
    showSessionTransition(completionData) {
        // Add transition class for animation
        this.elements.body.classList.add('session-transition');
        
        // Remove transition class after animation
        setTimeout(() => {
            this.elements.body.classList.remove('session-transition');
        }, 1000);
    }

    /**
     * Format time in seconds to MM:SS format
     * @param {number} seconds - Time in seconds
     * @returns {Object} Object with formatted minutes and seconds
     */
    formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        
        return {
            minutes: minutes.toString().padStart(2, '0'),
            seconds: remainingSeconds.toString().padStart(2, '0')
        };
    }

    /**
     * Calculate progress percentage
     * @param {number} currentTime - Current time remaining
     * @param {number} totalTime - Total session time
     * @returns {number} Progress percentage
     */
    calculateProgress(currentTime, totalTime) {
        if (totalTime === 0) return 100;
        return ((totalTime - currentTime) / totalTime) * 100;
    }

    /**
     * Check if timer is currently running
     * @returns {boolean} True if timer is running
     */
    isTimerRunning() {
        return this.currentState?.status === 'running';
    }

    /**
     * Show loading state
     */
    showLoadingState() {
        this.elements.startStopBtn.disabled = true;
        this.elements.resetBtn.disabled = true;
        this.elements.skipBtn.disabled = true;
        
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.remove('hidden');
        }
    }

    /**
     * Hide loading state
     */
    hideLoadingState() {
        this.elements.startStopBtn.disabled = false;
        this.elements.resetBtn.disabled = false;
        this.elements.skipBtn.disabled = false;
        
        const loadingOverlay = document.getElementById('loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
    }

    /**
     * Get current timer state
     * @returns {Object} Current timer state
     */
    getCurrentState() {
        return this.currentState;
    }
}

// Export for use in other modules
window.Timer = Timer;