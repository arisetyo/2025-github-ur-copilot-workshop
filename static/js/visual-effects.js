/**
 * Visual Effects System for Pomodoro Timer
 * Handles particle effects, ripple animations, and color transitions
 */

class VisualEffects {
    constructor() {
        this.canvas = document.getElementById('particles-canvas');
        this.rippleContainer = document.getElementById('ripple-container');
        this.ctx = null;
        this.particles = [];
        this.animationFrame = null;
        this.isActive = false;
        this.currentColor = '#3b82f6';
        this.rippleInterval = null;
        
        this.initCanvas();
    }

    /**
     * Initialize canvas for particle effects
     */
    initCanvas() {
        if (!this.canvas) {
            console.warn('Particles canvas not found');
            return;
        }

        this.ctx = this.canvas.getContext('2d');
        this.resizeCanvas();
        
        // Resize canvas on window resize
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    /**
     * Resize canvas to match window size
     */
    resizeCanvas() {
        if (!this.canvas) return;
        
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    /**
     * Start visual effects
     * @param {string} sessionType - 'work' or 'break'
     */
    start(sessionType = 'work') {
        this.isActive = true;
        this.canvas?.classList.add('active');
        
        // Initialize particles
        this.initializeParticles(sessionType);
        
        // Start animation loop
        this.animate();
        
        // Start periodic ripples during work sessions
        if (sessionType === 'work') {
            this.startRipples();
        }
    }

    /**
     * Stop visual effects
     */
    stop() {
        this.isActive = false;
        this.canvas?.classList.remove('active');
        
        // Stop animation
        if (this.animationFrame) {
            cancelAnimationFrame(this.animationFrame);
            this.animationFrame = null;
        }
        
        // Stop ripples
        this.stopRipples();
        
        // Clear particles
        this.particles = [];
        this.clearCanvas();
    }

    /**
     * Initialize particles
     * @param {string} sessionType - 'work' or 'break'
     */
    initializeParticles(sessionType) {
        const particleCount = 50;
        this.particles = [];
        
        const baseColor = sessionType === 'work' ? 
            { r: 102, g: 126, b: 234 } : // Blue for work
            { r: 72, g: 187, b: 120 };   // Green for break
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                alpha: Math.random() * 0.5 + 0.3,
                color: baseColor
            });
        }
    }

    /**
     * Animate particles
     */
    animate() {
        if (!this.isActive || !this.ctx) return;
        
        this.clearCanvas();
        this.updateParticles();
        this.drawParticles();
        
        this.animationFrame = requestAnimationFrame(() => this.animate());
    }

    /**
     * Update particle positions
     */
    updateParticles() {
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around screen edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
        });
    }

    /**
     * Draw particles on canvas
     */
    drawParticles() {
        if (!this.ctx) return;
        
        this.particles.forEach(particle => {
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${particle.alpha})`;
            this.ctx.fill();
            
            // Draw connections between nearby particles
            this.particles.forEach(other => {
                const dx = particle.x - other.x;
                const dy = particle.y - other.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 100) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle.x, particle.y);
                    this.ctx.lineTo(other.x, other.y);
                    this.ctx.strokeStyle = `rgba(${particle.color.r}, ${particle.color.g}, ${particle.color.b}, ${0.1 * (1 - distance / 100)})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            });
        });
    }

    /**
     * Clear canvas
     */
    clearCanvas() {
        if (!this.ctx) return;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    }

    /**
     * Start periodic ripple effects
     */
    startRipples() {
        this.stopRipples(); // Clear any existing interval
        
        // Create ripple every 8 seconds
        this.rippleInterval = setInterval(() => {
            if (this.isActive) {
                this.createRipple();
            }
        }, 8000);
        
        // Create initial ripple
        this.createRipple();
    }

    /**
     * Stop ripple effects
     */
    stopRipples() {
        if (this.rippleInterval) {
            clearInterval(this.rippleInterval);
            this.rippleInterval = null;
        }
    }

    /**
     * Create a ripple effect
     */
    createRipple() {
        if (!this.rippleContainer) return;
        
        const ripple = document.createElement('div');
        ripple.className = 'ripple';
        
        // Random position
        const x = Math.random() * window.innerWidth;
        const y = Math.random() * window.innerHeight;
        const size = Math.random() * 200 + 100;
        
        ripple.style.left = `${x - size / 2}px`;
        ripple.style.top = `${y - size / 2}px`;
        ripple.style.width = `${size}px`;
        ripple.style.height = `${size}px`;
        
        this.rippleContainer.appendChild(ripple);
        
        // Remove ripple after animation completes
        setTimeout(() => {
            ripple.remove();
        }, 3000);
    }

    /**
     * Update particle colors based on time percentage
     * @param {number} percentage - Progress percentage (0-100)
     */
    updateParticleColors(percentage) {
        if (!this.isActive || this.particles.length === 0) return;
        
        // Interpolate between blue, yellow, and red
        let r, g, b;
        
        if (percentage < 50) {
            // Blue to Yellow (0-50%)
            const t = percentage / 50;
            r = Math.floor(59 + (234 - 59) * t);   // 59 -> 234
            g = Math.floor(130 + (179 - 130) * t); // 130 -> 179
            b = Math.floor(246 - 246 * t);         // 246 -> 0
        } else {
            // Yellow to Red (50-100%)
            const t = (percentage - 50) / 50;
            r = Math.floor(234 + (239 - 234) * t); // 234 -> 239
            g = Math.floor(179 - (111) * t);       // 179 -> 68
            b = Math.floor(8 + (60) * t);          // 8 -> 68
        }
        
        // Update all particles
        this.particles.forEach(particle => {
            particle.color = { r, g, b };
        });
    }

    /**
     * Get color for progress bar based on percentage
     * @param {number} percentage - Progress percentage (0-100)
     * @returns {string} Color in hex format
     */
    getProgressColor(percentage) {
        let r, g, b;
        
        if (percentage < 50) {
            // Blue to Yellow (0-50%)
            const t = percentage / 50;
            r = Math.floor(59 + (234 - 59) * t);
            g = Math.floor(130 + (179 - 130) * t);
            b = Math.floor(246 - 246 * t);
        } else {
            // Yellow to Red (50-100%)
            const t = (percentage - 50) / 50;
            r = Math.floor(234 + (239 - 234) * t);
            g = Math.floor(179 - (111) * t);
            b = Math.floor(8 + (60) * t);
        }
        
        // Convert to hex
        const toHex = (n) => {
            const hex = n.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        };
        
        return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
    }

    /**
     * Check if effects are active
     * @returns {boolean}
     */
    isEffectsActive() {
        return this.isActive;
    }
}

// Export for use in other modules
window.VisualEffects = VisualEffects;
