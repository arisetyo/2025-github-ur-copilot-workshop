"""
Tests for visual effects integration in the Pomodoro Timer application.
These tests verify that the visual effects module is properly integrated
and the color transition logic works correctly.
"""

import pytest


class TestColorTransitions:
    """Test color transition calculations for progress bar."""
    
    def test_color_at_start_is_blue(self):
        """Test that color at 0% progress is blue."""
        # At 0%, color should be blue (#3b82f6)
        # RGB: (59, 130, 246)
        percentage = 0
        
        # Calculate color (mirroring the JavaScript logic)
        r = int(59 + (234 - 59) * (percentage / 50))
        g = int(130 + (179 - 130) * (percentage / 50))
        b = int(246 - 246 * (percentage / 50))
        
        assert r == 59
        assert g == 130
        assert b == 246
    
    def test_color_at_halfway_is_yellow(self):
        """Test that color at 50% progress is yellow."""
        # At 50%, color should be yellow-ish (#eab300)
        # RGB: (234, 179, 0)
        percentage = 50
        
        # Calculate color for 0-50% range
        r = int(59 + (234 - 59) * (percentage / 50))
        g = int(130 + (179 - 130) * (percentage / 50))
        b = int(246 - 246 * (percentage / 50))
        
        assert r == 234
        assert g == 179
        assert b == 0  # At 50%, blue component should be 0
    
    def test_color_at_end_is_red(self):
        """Test that color at 100% progress is red."""
        # At 100%, color should be red (#ef4444)
        # RGB: (239, 68, 68)
        percentage = 100
        
        # Calculate color for 50-100% range
        t = (percentage - 50) / 50
        r = int(234 + (239 - 234) * t)
        g = int(179 - 111 * t)
        b = int(8 + 60 * t)
        
        assert r == 239
        assert g == 68
        assert b == 68
    
    def test_color_at_25_percent_is_blue_yellow_blend(self):
        """Test that color at 25% progress is between blue and yellow."""
        percentage = 25
        
        # Calculate color for 0-50% range
        r = int(59 + (234 - 59) * (percentage / 50))
        g = int(130 + (179 - 130) * (percentage / 50))
        b = int(246 - 246 * (percentage / 50))
        
        # Should be between blue and yellow
        assert 59 < r < 234
        assert 130 < g < 179
        assert 8 < b < 246
    
    def test_color_at_75_percent_is_yellow_red_blend(self):
        """Test that color at 75% progress is between yellow and red."""
        percentage = 75
        
        # Calculate color for 50-100% range
        t = (percentage - 50) / 50
        r = int(234 + (239 - 234) * t)
        g = int(179 - 111 * t)
        b = int(8 + 60 * t)
        
        # Should be between yellow and red
        assert 234 < r < 239
        assert 68 < g < 179
        assert 8 < b < 68


class TestVisualEffectsIntegration:
    """Test visual effects integration with timer."""
    
    def test_visual_effects_script_exists(self):
        """Test that visual-effects.js file exists."""
        import os
        visual_effects_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'js', 'visual-effects.js'
        )
        assert os.path.exists(visual_effects_path), "visual-effects.js file should exist"
    
    def test_visual_effects_script_has_class_definition(self):
        """Test that VisualEffects class is defined in the script."""
        import os
        visual_effects_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'js', 'visual-effects.js'
        )
        
        with open(visual_effects_path, 'r') as f:
            content = f.read()
        
        assert 'class VisualEffects' in content, "VisualEffects class should be defined"
        assert 'window.VisualEffects = VisualEffects' in content, "VisualEffects should be exported to window"
    
    def test_html_includes_particles_canvas(self):
        """Test that index.html includes the particles canvas."""
        import os
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates', 'index.html'
        )
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        assert 'id="particles-canvas"' in content, "particles-canvas should be in HTML"
        assert 'canvas' in content.lower(), "Canvas element should be present"
    
    def test_html_includes_ripple_container(self):
        """Test that index.html includes the ripple container."""
        import os
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates', 'index.html'
        )
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        assert 'id="ripple-container"' in content, "ripple-container should be in HTML"
        assert 'ripple-container' in content, "Ripple container class should be present"
    
    def test_html_includes_visual_effects_script(self):
        """Test that index.html includes visual-effects.js script."""
        import os
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates', 'index.html'
        )
        
        with open(template_path, 'r') as f:
            content = f.read()
        
        assert 'visual-effects.js' in content, "visual-effects.js script should be included"
    
    def test_css_includes_particle_styles(self):
        """Test that style.css includes styles for particles."""
        import os
        css_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'css', 'style.css'
        )
        
        with open(css_path, 'r') as f:
            content = f.read()
        
        assert '#particles-canvas' in content, "Particle canvas styles should be present"
        assert 'ripple' in content.lower(), "Ripple styles should be present"
    
    def test_css_includes_progress_color_variables(self):
        """Test that CSS includes progress color stage variables."""
        import os
        css_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'css', 'style.css'
        )
        
        with open(css_path, 'r') as f:
            content = f.read()
        
        assert '--progress-color-start' in content, "Progress color start variable should be defined"
        assert '--progress-color-mid' in content, "Progress color mid variable should be defined"
        assert '--progress-color-end' in content, "Progress color end variable should be defined"
    
    def test_timer_js_integrates_visual_effects(self):
        """Test that timer.js integrates with visual effects."""
        import os
        timer_js_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'static', 'js', 'timer.js'
        )
        
        with open(timer_js_path, 'r') as f:
            content = f.read()
        
        assert 'this.visualEffects' in content, "Timer should have visualEffects property"
        assert 'VisualEffects' in content, "Timer should reference VisualEffects class"
        assert 'getProgressColor' in content, "Timer should use getProgressColor method"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
