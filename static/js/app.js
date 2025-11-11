/**
 * Main application controller for Pomodoro Timer
 * Coordinates between Timer, NotificationSystem, and Socket.IO
 */

class PomodoroApp {
    constructor() {
        this.timer = null;
        this.notifications = null;
        this.socket = null;
        this.settings = this.loadSettings();
        this.isInitialized = false;
        
        // Bind methods to preserve context
        this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
        this.handleKeyPress = this.handleKeyPress.bind(this);
        this.handleBeforeUnload = this.handleBeforeUnload.bind(this);
    }

    /**
     * Initialize the application
     */
    async initialize() {
        try {
            // Initialize components
            this.timer = new Timer();
            this.notifications = new NotificationSystem();
            
            // Make notifications globally available
            window.notifications = {
                show: (message, type) => this.notifications.showVisualNotification(message, type),
                playSound: () => this.notifications.playAudioNotification('sessionComplete'),
                showBrowser: (title, message) => this.notifications.showBrowserNotification(title, message)
            };
            
            // Initialize Socket.IO connection
            this.initializeSocket();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Set up settings panel
            this.setupSettingsPanel();
            
            // Load initial timer state
            await this.loadInitialState();
            
            this.isInitialized = true;
            console.log('Pomodoro Timer initialized successfully');
            
        } catch (error) {
            console.error('Error initializing application:', error);
            this.notifications?.showError('Failed to initialize application');
        }
    }

    /**
     * Initialize Socket.IO connection and event handlers
     */
    initializeSocket() {
        try {
            this.socket = io();
            
            // Connection events
            this.socket.on('connect', () => {
                console.log('Connected to server');
                this.socket.emit('request_timer_status');
            });
            
            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.notifications?.showWarning('Connection lost. Attempting to reconnect...');
            });
            
            this.socket.on('connect_error', (error) => {
                console.error('Connection error:', error);
                this.notifications?.showError('Connection error. Please refresh the page.');
            });
            
            // Timer events
            this.socket.on('timer_update', (timerState) => {
                this.handleTimerUpdate(timerState);
            });
            
            this.socket.on('session_complete', (completionData) => {
                this.handleSessionComplete(completionData);
            });
            
        } catch (error) {
            console.error('Error initializing Socket.IO:', error);
        }
    }

    /**
     * Set up global event listeners
     */
    setupEventListeners() {
        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyPress);
        
        // Page visibility changes
        document.addEventListener('visibilitychange', this.handleVisibilityChange);
        
        // Before page unload
        window.addEventListener('beforeunload', this.handleBeforeUnload);
        
        // Error handling
        window.addEventListener('error', (event) => {
            console.error('Global error:', event.error);
            this.notifications?.showError('An unexpected error occurred');
        });
        
        // Unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.notifications?.showError('An unexpected error occurred');
        });
    }

    /**
     * Set up settings panel functionality
     */
    setupSettingsPanel() {
        const settingsToggle = document.getElementById('settings-toggle-btn');
        const settingsPanel = document.getElementById('settings-panel');
        const saveSettingsBtn = document.getElementById('save-settings-btn');
        const cancelSettingsBtn = document.getElementById('cancel-settings-btn');
        const workDurationInput = document.getElementById('work-duration');
        const breakDurationInput = document.getElementById('break-duration');
        
        if (!settingsToggle || !settingsPanel) {
            console.warn('Settings elements not found');
            return;
        }
        
        // Toggle settings panel
        settingsToggle.addEventListener('click', () => {
            const isVisible = settingsPanel.classList.contains('visible');
            if (isVisible) {
                this.hideSettings();
            } else {
                this.showSettings();
            }
        });
        
        // Save settings
        saveSettingsBtn?.addEventListener('click', async () => {
            await this.saveSettings();
        });
        
        // Cancel settings
        cancelSettingsBtn?.addEventListener('click', () => {
            this.hideSettings();
        });
        
        // Close settings when clicking outside
        document.addEventListener('click', (event) => {
            if (settingsPanel.classList.contains('visible') && 
                !settingsPanel.contains(event.target) && 
                !settingsToggle.contains(event.target)) {
                this.hideSettings();
            }
        });
        
        // Load current settings into form
        this.loadSettingsForm();
    }

    /**
     * Load initial timer state from server
     */
    async loadInitialState() {
        try {
            const response = await fetch('/api/timer/status');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.timer.initialize(data.data);
            } else {
                throw new Error(data.error || 'Failed to load initial state');
            }
        } catch (error) {
            console.error('Error loading initial state:', error);
            this.notifications?.showError('Failed to load timer state');
        }
    }

    /**
     * Handle timer state updates from Socket.IO
     * @param {Object} timerState - Updated timer state
     */
    handleTimerUpdate(timerState) {
        if (this.timer) {
            this.timer.handleStateUpdate(timerState);
        }
    }

    /**
     * Handle session completion events
     * @param {Object} completionData - Session completion data
     */
    handleSessionComplete(completionData) {
        // Handle timer-specific completion logic
        if (this.timer) {
            this.timer.handleSessionComplete(completionData);
        }
        
        // Handle notifications
        if (this.notifications) {
            this.notifications.handleSessionComplete(completionData);
        }
    }

    /**
     * Handle keyboard shortcuts
     * @param {KeyboardEvent} event - Keyboard event
     */
    handleKeyPress(event) {
        // Only handle shortcuts when settings panel is not visible
        const settingsPanel = document.getElementById('settings-panel');
        if (settingsPanel?.classList.contains('visible')) {
            return;
        }
        
        // Don't handle shortcuts if user is typing in an input
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.timer?.toggleTimer();
                break;
            case 'KeyR':
                event.preventDefault();
                this.timer?.resetTimer();
                break;
            case 'KeyS':
                event.preventDefault();
                this.timer?.skipSession();
                break;
            case 'Escape':
                event.preventDefault();
                this.hideSettings();
                break;
        }
    }

    /**
     * Handle page visibility changes
     */
    handleVisibilityChange() {
        if (document.hidden) {
            // Page is hidden, timer continues in background
            console.log('Page hidden, timer continues in background');
        } else {
            // Page is visible, request current state
            console.log('Page visible, requesting current state');
            if (this.socket) {
                this.socket.emit('request_timer_status');
            }
        }
    }

    /**
     * Handle before page unload
     * @param {BeforeUnloadEvent} event - Before unload event
     */
    handleBeforeUnload(event) {
        // Only show confirmation if timer is running
        if (this.timer?.isTimerRunning()) {
            event.preventDefault();
            event.returnValue = 'Timer is running. Are you sure you want to leave?';
            return event.returnValue;
        }
    }

    /**
     * Show settings panel
     */
    showSettings() {
        const settingsPanel = document.getElementById('settings-panel');
        if (settingsPanel) {
            settingsPanel.classList.add('visible');
        }
    }

    /**
     * Hide settings panel
     */
    hideSettings() {
        const settingsPanel = document.getElementById('settings-panel');
        if (settingsPanel) {
            settingsPanel.classList.remove('visible');
        }
    }

    /**
     * Load current settings into form
     */
    async loadSettingsForm() {
        try {
            const response = await fetch('/api/timer/config');
            const data = await response.json();
            
            if (data.status === 'success') {
                const config = data.data;
                
                const workDurationInput = document.getElementById('work-duration');
                const breakDurationInput = document.getElementById('break-duration');
                
                if (workDurationInput) {
                    workDurationInput.value = Math.floor(config.work_duration / 60);
                }
                if (breakDurationInput) {
                    breakDurationInput.value = Math.floor(config.break_duration / 60);
                }
            }
        } catch (error) {
            console.error('Error loading settings form:', error);
        }
    }

    /**
     * Save settings to server
     */
    async saveSettings() {
        try {
            const workDurationInput = document.getElementById('work-duration');
            const breakDurationInput = document.getElementById('break-duration');
            
            const workMinutes = parseInt(workDurationInput?.value || 25);
            const breakMinutes = parseInt(breakDurationInput?.value || 5);
            
            // Validate input
            if (workMinutes < 1 || workMinutes > 60) {
                this.notifications?.showError('Work duration must be between 1 and 60 minutes');
                return;
            }
            
            if (breakMinutes < 1 || breakMinutes > 30) {
                this.notifications?.showError('Break duration must be between 1 and 30 minutes');
                return;
            }
            
            const config = {
                work_duration: workMinutes * 60,
                break_duration: breakMinutes * 60,
                long_break_duration: 900, // Keep default 15 minutes
                sessions_until_long_break: 4 // Keep default 4 sessions
            };
            
            const response = await fetch('/api/timer/config', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(config)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.notifications?.showSuccess('Settings saved successfully!');
                this.hideSettings();
                
                // Save to local storage
                this.settings = { ...this.settings, ...config };
                this.saveSettings();
                
                // Refresh timer state if stopped
                if (this.timer?.getCurrentState()?.status === 'stopped') {
                    this.socket?.emit('request_timer_status');
                }
            } else {
                throw new Error(data.error || 'Failed to save settings');
            }
        } catch (error) {
            console.error('Error saving settings:', error);
            this.notifications?.showError(`Failed to save settings: ${error.message}`);
        }
    }

    /**
     * Load settings from localStorage
     * @returns {Object} Loaded settings
     */
    loadSettings() {
        try {
            const saved = localStorage.getItem('pomodoroSettings');
            return saved ? JSON.parse(saved) : {};
        } catch (error) {
            console.error('Error loading settings:', error);
            return {};
        }
    }

    /**
     * Save settings to localStorage
     */
    saveSettingsToStorage() {
        try {
            localStorage.setItem('pomodoroSettings', JSON.stringify(this.settings));
        } catch (error) {
            console.error('Error saving settings to storage:', error);
        }
    }

    /**
     * Get application status
     * @returns {Object} Application status information
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            timerState: this.timer?.getCurrentState(),
            socketConnected: this.socket?.connected || false,
            settings: this.settings
        };
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const app = new PomodoroApp();
        window.pomodoroApp = app; // Make globally available for debugging
        await app.initialize();
    } catch (error) {
        console.error('Failed to initialize Pomodoro Timer:', error);
        
        // Show error message to user
        const errorElement = document.createElement('div');
        errorElement.innerHTML = `
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: #fee2e2;
                border: 1px solid #fecaca;
                border-radius: 0.5rem;
                padding: 1rem;
                max-width: 20rem;
                text-align: center;
                z-index: 9999;
            ">
                <h3 style="color: #dc2626; margin: 0 0 0.5rem 0;">
                    Failed to Initialize
                </h3>
                <p style="color: #7f1d1d; margin: 0 0 1rem 0;">
                    There was an error starting the Pomodoro Timer. Please refresh the page to try again.
                </p>
                <button onclick="window.location.reload()" style="
                    background: #dc2626;
                    color: white;
                    border: none;
                    border-radius: 0.25rem;
                    padding: 0.5rem 1rem;
                    cursor: pointer;
                ">
                    Refresh Page
                </button>
            </div>
        `;
        document.body.appendChild(errorElement);
    }
});