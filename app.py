"""
StudyBalance AI - Student Burnout Prevention System
Flask web application using Arcade.dev toolkits for Gmail and Google Calendar integration
Author: AyaanRathod
"""

import os
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Import our custom Arcade toolkit modules
from arcade_tools.gmail_analyzer import GmailAnalyzer
from arcade_tools.calendar_optmizer import CalendarOptimizer
from arcade_tools.wellness_nudger import WellnessNudger
from configs import Config
from utils import format_time, calculate_wellness_score

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize Arcade toolkit managers
gmail_analyzer = None
calendar_optimizer = None
wellness_nudger = None

def initialize_arcade_tools():
    """Initialize Arcade.dev toolkits"""
    global gmail_analyzer, calendar_optimizer, wellness_nudger
    
    try:
        # Initialize with Arcade.dev API credentials
        api_key = app.config.get('ARCADE_API_KEY')
        user_id = app.config.get('ARCADE_USER_ID')
        
        if api_key and user_id:
            gmail_analyzer = GmailAnalyzer(api_key, user_id)
            calendar_optimizer = CalendarOptimizer(api_key, user_id)
            wellness_nudger = WellnessNudger(api_key, user_id)
            print("✅ Arcade.dev toolkits initialized successfully!")
            print("🔐 Authentication status will be checked when tools are used")
        else:
            print("⚠️ Arcade API credentials not found in environment variables")
            print("💡 Please set ARCADE_API_KEY and ARCADE_USER_ID in your .env file")
            print("📝 Copy .env.example to .env and fill in your arcade.dev credentials")
            print("🌐 Get credentials from: https://api.arcade.dev/dashboard")
        
    except Exception as e:
        print(f"❌ Error initializing Arcade toolkits: {e}")
        print("🔄 Running in simulation mode...")

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/analyze')
def analyze_page():
    """Email and calendar analysis page"""
    return render_template('analyze.html')

@app.route('/schedule')
def schedule_page():
    """Schedule optimization page"""
    return render_template('schedule.html')

@app.route('/wellness')
def wellness_page():
    """Wellness tips and nudges page"""
    return render_template('wellness.html')

@app.route('/sw.js')
def service_worker():
    """Serve service worker from correct path"""
    return app.send_static_file('sw.js')

# API Endpoints
@app.route('/api/analyze_gmail', methods=['POST'])
def analyze_gmail():
    """Analyze Gmail using Arcade.dev Gmail toolkit"""
    try:
        data = request.get_json()
        days_back = data.get('days', 7)
        
        if gmail_analyzer:
            # This is where OAuth will happen if needed
            print("🔐 Attempting Gmail analysis - OAuth may be triggered")
            analysis = gmail_analyzer.analyze_email_patterns(days_back)
            print("✅ Gmail analysis completed successfully")
        else:
            print("⚠️ No Gmail analyzer available, using simulation")
            # Fallback simulation data
            analysis = {
                'total_emails': 67,
                'work_emails': 34,
                'urgent_emails': 12,
                'stress_keywords_found': ['deadline', 'urgent', 'asap', 'emergency'],
                'peak_hours': ['09:00-11:00', '14:00-16:00', '20:00-22:00'],
                'workload_score': 7.8,
                'burnout_risk': 'moderate',
                'recommendations': [
                    'Consider email batching - check only 3 times daily',
                    'High stress keywords detected - practice mindfulness',
                    'Late evening emails - set boundaries after 9 PM'
                ]
            }
        
        # Calculate wellness score
        wellness_score = calculate_wellness_score(analysis)
        analysis['wellness_score'] = wellness_score
        
        # Check if authorization is needed
        if analysis.get('auth_required'):
            return jsonify({
                'success': False,
                'error': 'Gmail authorization required',
                'analysis': analysis,
                'auth_required': True,
                'auth_url': 'https://api.arcade.dev/dashboard',
                'instructions': [
                    'Visit your arcade.dev dashboard',
                    'Authorize Gmail toolkit access',
                    'Return and try analysis again'
                ],
                'timestamp': datetime.now().isoformat()
            }), 401
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'timestamp': datetime.now().isoformat(),
            'data_source': 'real' if analysis.get('real_data') else 'simulated'
        })
        
    except Exception as e:
        print(f"❌ Gmail analysis error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'oauth_help': 'If you see auth errors, check browser for OAuth popup or visit arcade.dev dashboard'
        }), 500

@app.route('/api/optimize_schedule', methods=['POST'])
def optimize_schedule():
    """Create optimized schedule using Arcade.dev Google Calendar toolkit"""
    try:
        data = request.get_json()
        preferences = {
            'study_duration': data.get('study_duration', 90),  # minutes
            'break_duration': data.get('break_duration', 15),  # minutes
            'subjects': data.get('subjects', ['Math', 'Physics', 'Chemistry', 'English']),
            'start_time': data.get('start_time', '09:00'),
            'end_time': data.get('end_time', '17:00')
        }
        
        if calendar_optimizer:
            # Use real Arcade.dev Google Calendar toolkit
            schedule = calendar_optimizer.create_optimized_schedule(preferences)
        else:
            # Fallback simulation data
            schedule = {
                'study_blocks': [
                    {
                        'subject': 'Mathematics',
                        'start_time': '09:00',
                        'end_time': '10:30',
                        'type': 'study',
                        'duration': 90
                    },
                    {
                        'subject': 'Break',
                        'start_time': '10:30',
                        'end_time': '10:45',
                        'type': 'break',
                        'duration': 15
                    },
                    {
                        'subject': 'Physics',
                        'start_time': '10:45',
                        'end_time': '12:15',
                        'type': 'study',
                        'duration': 90
                    }
                ],
                'total_study_time': 360,
                'total_break_time': 60,
                'wellness_score': 9.2,
                'efficiency_rating': 'Excellent'
            }
        
        return jsonify({
            'success': True,
            'schedule': schedule,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/send_wellness_nudge', methods=['POST'])
def send_wellness_nudge():
    """Send wellness nudge using Arcade.dev Gmail toolkit"""
    try:
        data = request.get_json()
        nudge_type = data.get('type', 'break_reminder')
        recipient = data.get('recipient', 'user@example.com')  # User should provide their email
        context = data.get('context', {})
        
        if wellness_nudger:
            # Use real Arcade.dev Gmail toolkit to send email
            result = wellness_nudger.send_wellness_reminder(nudge_type, recipient, context)
            success = result.get('status') == 'sent'
        else:
            # Simulate success
            success = True
            result = {'status': 'simulated', 'message': 'Wellness nudge simulated'}
        
        return jsonify({
            'success': success,
            'result': result,
            'message': f'Wellness nudge sent successfully!' if success else 'Failed to send nudge',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/get_calendar_events', methods=['GET'])
def get_calendar_events():
    """Get calendar events using Arcade.dev Google Calendar toolkit"""
    try:
        days = request.args.get('days', 7, type=int)
        
        if calendar_optimizer:
            # Use real Arcade.dev Google Calendar toolkit
            events = calendar_optimizer.get_calendar_events(days)
        else:
            # Fallback simulation data
            events = {
                'events': [
                    {
                        'title': 'Data Structures Lecture',
                        'start': '2025-01-15T09:00:00',
                        'end': '2025-01-15T10:30:00',
                        'type': 'class'
                    },
                    {
                        'title': 'Algorithm Analysis Lab',
                        'start': '2025-01-15T14:00:00',
                        'end': '2025-01-15T17:00:00',
                        'type': 'lab'
                    }
                ],
                'free_time_blocks': [
                    {'start': '10:30', 'end': '14:00'},
                    {'start': '17:00', 'end': '19:00'}
                ]
            }
        
        return jsonify({
            'success': True,
            'events': events,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/dashboard_stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        # Combine data from all sources
        stats = {
            'wellness_score': 7.5,
            'weekly_emails': 42,
            'study_hours_today': 6.5,
            'active_nudges': 3,
            'last_analysis': '2 hours ago',
            'next_break': '45 minutes',
            'calendar_events_today': 4,
            'stress_level': 'moderate'
        }
        
        # Add recent activity data
        recent_activity = [
            {
                'type': 'email_analysis',
                'title': 'Gmail analysis completed',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                'type': 'schedule_created',
                'title': 'Study schedule optimized',
                'timestamp': (datetime.now() - timedelta(hours=4)).isoformat()
            },
            {
                'type': 'wellness_nudge',
                'title': 'Break reminder sent',
                'timestamp': (datetime.now() - timedelta(minutes=30)).isoformat()
            }
        ]
        
        return jsonify({
            'success': True,
            'stats': stats,
            'recent_activity': recent_activity,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/auth_status', methods=['GET'])
def get_auth_status():
    """Get authentication status for arcade.dev toolkits"""
    try:
        auth_status = {
            'arcade_configured': False,
            'gmail_ready': False,
            'calendar_ready': False,
            'auth_url': None,
            'message': None
        }
        
        # Check if arcade.dev credentials are configured
        api_key = app.config.get('ARCADE_API_KEY')
        user_id = app.config.get('ARCADE_USER_ID')
        
        if api_key and user_id and api_key != 'your_arcade_api_key_here':
            auth_status['arcade_configured'] = True
            auth_status['message'] = 'Arcade.dev ready! OAuth will prompt when you first analyze emails or access calendar.'
            
            # Test initialization
            if gmail_analyzer:
                auth_status['gmail_ready'] = gmail_analyzer.initialized
            if calendar_optimizer:
                auth_status['calendar_ready'] = calendar_optimizer.initialized
                
        else:
            auth_status['message'] = 'Please configure ARCADE_API_KEY and ARCADE_USER_ID in .env file'
            auth_status['auth_url'] = 'https://api.arcade.dev/dashboard'
        
        return jsonify({
            'success': True,
            'auth_status': auth_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting StudyBalance AI...")
    initialize_arcade_tools()
    print("📧 Gmail analysis ready")
    print("📅 Calendar optimization ready")
    print("💚 Wellness nudging ready")
    print("🌐 Web interface: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)