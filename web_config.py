#!/usr/bin/env python3
"""
Web Configuration Interface for Tanzen Button Control System
Simple Flask web frontend to configure button settings
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import threading
import time

def create_app(button_controller, osc_manager, osc_client):
    """Create Flask app with initialized components"""
    app = Flask(__name__)

    @app.route('/')
    def index():
        """Main configuration page"""
        return render_template('index.html', 
                             current_path=osc_manager.get_button_path(),
                             current_delay=osc_manager.current_delay,
                             button_enabled=button_controller.button_enabled,
                             available_paths=osc_manager.button_paths,
                             available_delays=osc_manager.delay_presets)

    @app.route('/api/status')
    def api_status():
        """Get current system status"""
        return jsonify({
            "button_enabled": button_controller.button_enabled,
            "current_path": osc_manager.get_button_path(),
            "current_delay": osc_manager.current_delay,
            "available_paths": osc_manager.button_paths,
            "available_delays": osc_manager.delay_presets
        })

    @app.route('/api/button', methods=['POST'])
    def api_button():
        """Enable/disable button"""
        data = request.get_json()
        enabled = data.get('enabled', True)
        
        button_controller.set_button_enabled(enabled)
        
        return jsonify({
            "success": True,
            "button_enabled": button_controller.button_enabled
        })

    @app.route('/api/path', methods=['POST'])
    def api_path():
        """Set button path"""
        data = request.get_json()
        path_id = data.get('path_id')
        
        if path_id not in osc_manager.button_paths:
            return jsonify({"error": "Invalid path ID"}), 400
        
        osc_manager.set_button_path(path_id)
        
        return jsonify({
            "success": True,
            "current_path": osc_manager.get_button_path()
        })

    @app.route('/api/delay', methods=['POST'])
    def api_delay():
        """Set delay preset"""
        data = request.get_json()
        delay_id = data.get('delay_id')
        
        if delay_id not in osc_manager.delay_presets:
            return jsonify({"error": "Invalid delay ID"}), 400
        
        osc_manager.set_delay_preset(delay_id)
        
        return jsonify({
            "success": True,
            "current_delay": osc_manager.current_delay
        })

    @app.route('/api/led/<led_name>/<action>', methods=['POST'])
    def api_led(led_name, action):
        """Control LEDs"""
        if action == 'on':
            button_controller.turn_led(led_name, True)
        elif action == 'off':
            button_controller.turn_led(led_name, False)
        elif action == 'toggle':
            button_controller.toggle_led(led_name)
        else:
            return jsonify({"error": "Invalid action"}), 400
        
        return jsonify({"success": True})

    return app

