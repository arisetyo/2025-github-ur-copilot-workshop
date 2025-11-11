/**
 * Notification system for Pomodoro Timer application
 * Handles audio notifications, browser notifications, and visual alerts
 */

class NotificationSystem {
    constructor() {
        this.audioContext = null;
        this.sounds = {};
        this.browserNotificationPermission = 'default';
        this.notificationArea = document.getElementById('notification-area');
        
        this.initialize();
    }

    /**
     * Initialize notification system
     */
    async initialize() {
        await this.requestNotificationPermission();
        this.loadAudioFiles();
        this.checkNotificationSupport();
    }

    /**
     * Request browser notification permission
     * @returns {Promise<string>} Permission status
     */
    async requestNotificationPermission() {
        if (!('Notification' in window)) {
            console.warn('Browser does not support notifications');
            return 'denied';
        }

        try {
            const permission = await Notification.requestPermission();
            this.browserNotificationPermission = permission;
            return permission;
        } catch (error) {
            console.error('Error requesting notification permission:', error);
            return 'denied';
        }
    }

    /**
     * Check browser notification support
     * @returns {boolean} True if notifications are supported
     */
    checkNotificationSupport() {
        const supported = 'Notification' in window;
        if (!supported) {
            console.warn('Browser notifications not supported');
        }
        return supported;
    }

    /**
     * Load audio files for notifications
     */
    loadAudioFiles() {
        try {
            // Create simple notification sounds using Web Audio API
            if ('AudioContext' in window || 'webkitAudioContext' in window) {
                this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                this.createNotificationSounds();
            } else {
                console.warn('Web Audio API not supported');
            }
        } catch (error) {
            console.error('Error loading audio files:', error);
        }
    }

    /**
     * Create notification sounds using Web Audio API
     */
    createNotificationSounds() {
        // Create a simple bell-like sound for session completion
        this.sounds.sessionComplete = this.createBellSound();
        
        // Create a gentle chime for session transitions
        this.sounds.sessionTransition = this.createChimeSound();
    }

    /**
     * Create a bell-like notification sound
     * @returns {Function} Function to play the bell sound
     */
    createBellSound() {
        return () => {
            if (!this.audioContext) return;
            
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            // Bell-like frequencies
            oscillator.frequency.setValueAtTime(800, this.audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, this.audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 1);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 1);
        };
    }

    /**
     * Create a chime notification sound
     * @returns {Function} Function to play the chime sound
     */
    createChimeSound() {
        return () => {
            if (!this.audioContext) return;
            
            const oscillator = this.audioContext.createOscillator();
            const gainNode = this.audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(this.audioContext.destination);
            
            // Gentle chime frequencies
            oscillator.frequency.setValueAtTime(523.25, this.audioContext.currentTime); // C5
            oscillator.frequency.setValueAtTime(659.25, this.audioContext.currentTime + 0.2); // E5
            oscillator.frequency.setValueAtTime(783.99, this.audioContext.currentTime + 0.4); // G5
            
            gainNode.gain.setValueAtTime(0.2, this.audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.8);
            
            oscillator.start(this.audioContext.currentTime);
            oscillator.stop(this.audioContext.currentTime + 0.8);
        };
    }

    /**
     * Play audio notification
     * @param {string} type - Type of notification sound ('sessionComplete', 'sessionTransition')
     */
    playAudioNotification(type = 'sessionComplete') {
        try {
            if (this.sounds[type]) {
                this.sounds[type]();
            } else {
                console.warn(`Unknown notification sound type: ${type}`);
            }
        } catch (error) {
            console.error('Error playing audio notification:', error);
        }
    }

    /**
     * Show browser notification
     * @param {string} title - Notification title
     * @param {string} message - Notification message
     * @param {Object} options - Additional notification options
     */
    showBrowserNotification(title, message, options = {}) {
        if (!this.checkNotificationSupport() || this.browserNotificationPermission !== 'granted') {
            console.warn('Browser notifications not available');
            return;
        }

        try {
            const defaultOptions = {
                body: message,
                icon: '/static/favicon.ico', // Add favicon if available
                badge: '/static/favicon.ico',
                tag: 'pomodoro-timer',
                requireInteraction: false,
                silent: false
            };

            const notificationOptions = { ...defaultOptions, ...options };
            
            const notification = new Notification(title, notificationOptions);

            // Auto-close notification after 5 seconds
            setTimeout(() => {
                notification.close();
            }, 5000);

            // Handle notification click
            notification.onclick = () => {
                window.focus();
                notification.close();
            };

        } catch (error) {
            console.error('Error showing browser notification:', error);
        }
    }

    /**
     * Show visual notification in the app
     * @param {string} message - Notification message
     * @param {string} type - Notification type ('success', 'error', 'warning', 'info')
     * @param {number} duration - Duration in milliseconds (default: 3000)
     */
    showVisualNotification(message, type = 'info', duration = 3000) {
        if (!this.notificationArea) {
            console.warn('Notification area not found');
            return;
        }

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" aria-label="Close notification">&times;</button>
            </div>
        `;

        // Add close functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            this.removeNotification(notification);
        });

        // Add to notification area
        this.notificationArea.appendChild(notification);

        // Auto-remove after duration
        setTimeout(() => {
            this.removeNotification(notification);
        }, duration);

        return notification;
    }

    /**
     * Remove a visual notification
     * @param {HTMLElement} notification - Notification element to remove
     */
    removeNotification(notification) {
        if (notification && notification.parentNode) {
            notification.style.animation = 'slideOut 300ms ease-in-out forwards';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }

    /**
     * Show success notification
     * @param {string} message - Success message
     * @param {number} duration - Duration in milliseconds
     */
    showSuccess(message, duration = 3000) {
        this.showVisualNotification(message, 'success', duration);
    }

    /**
     * Show error notification
     * @param {string} message - Error message
     * @param {number} duration - Duration in milliseconds
     */
    showError(message, duration = 5000) {
        this.showVisualNotification(message, 'error', duration);
    }

    /**
     * Show warning notification
     * @param {string} message - Warning message
     * @param {number} duration - Duration in milliseconds
     */
    showWarning(message, duration = 4000) {
        this.showVisualNotification(message, 'warning', duration);
    }

    /**
     * Show info notification
     * @param {string} message - Info message
     * @param {number} duration - Duration in milliseconds
     */
    showInfo(message, duration = 3000) {
        this.showVisualNotification(message, 'info', duration);
    }

    /**
     * Handle session completion with full notification suite
     * @param {Object} sessionData - Session completion data
     */
    handleSessionComplete(sessionData) {
        const { session_type, message, next_session } = sessionData;
        
        // Play audio notification
        this.playAudioNotification('sessionComplete');
        
        // Show browser notification
        this.showBrowserNotification(
            'Pomodoro Timer',
            message,
            {
                body: `Time to ${next_session === 'work' ? 'get back to work' : 'take a break'}!`,
                requireInteraction: true
            }
        );
        
        // Show visual notification
        this.showSuccess(message, 5000);
    }

    /**
     * Set volume level for audio notifications
     * @param {number} level - Volume level (0-1)
     */
    setVolume(level) {
        this.volumeLevel = Math.max(0, Math.min(1, level));
        // Note: Web Audio API volume would be implemented in the sound creation functions
    }

    /**
     * Enable or disable audio notifications
     * @param {boolean} enabled - Whether audio notifications are enabled
     */
    setAudioEnabled(enabled) {
        this.audioEnabled = enabled;
    }

    /**
     * Enable or disable browser notifications
     * @param {boolean} enabled - Whether browser notifications are enabled
     */
    setBrowserNotificationsEnabled(enabled) {
        this.browserNotificationsEnabled = enabled;
        
        if (enabled && this.browserNotificationPermission === 'default') {
            this.requestNotificationPermission();
        }
    }

    /**
     * Get current notification settings
     * @returns {Object} Current notification settings
     */
    getSettings() {
        return {
            audioEnabled: this.audioEnabled !== false,
            browserNotificationsEnabled: this.browserNotificationsEnabled !== false,
            browserPermission: this.browserNotificationPermission,
            volumeLevel: this.volumeLevel || 0.3
        };
    }
}

// Add slideOut animation to CSS (if not already present)
if (!document.querySelector('#notification-animations')) {
    const style = document.createElement('style');
    style.id = 'notification-animations';
    style.textContent = `
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
        
        .notification-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .notification-close {
            background: none;
            border: none;
            font-size: 1.2rem;
            cursor: pointer;
            padding: 0 0.25rem;
            margin-left: 0.5rem;
            opacity: 0.7;
            transition: opacity 150ms ease;
        }
        
        .notification-close:hover {
            opacity: 1;
        }
    `;
    document.head.appendChild(style);
}

// Export for use in other modules
window.NotificationSystem = NotificationSystem;