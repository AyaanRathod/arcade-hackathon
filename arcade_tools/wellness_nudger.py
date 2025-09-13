"""
Wellness nudges using Arcade.dev Gmail toolkit
Sends personalized reminders to promote healthy study habits
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

class WellnessNudger:
    """Sends wellness reminders using Gmail"""
    
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.client = None
        self.initialized = False
        
    def initialize(self):
        """Initialize Arcade.dev Gmail toolkit"""
        try:
            from arcadepy import Arcade
            self.client = Arcade(api_key=self.api_key)
            self.initialized = True
            print("✅ Gmail toolkit client initialized")
            return True
            
        except ImportError:
            print("⚠️ arcadepy not available, using simulation mode")
            return False
        except Exception as e:
            print(f"❌ Gmail toolkit initialization error: {e}")
            return False
    
    def send_wellness_reminder(self, reminder_type: str, user_email: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send a wellness reminder via email"""
        if not self.initialized:
            if not self.initialize():
                return self._simulate_reminder(reminder_type, context)
        
        try:
            return self._send_with_arcade_toolkit(reminder_type, user_email, context)
        except Exception as e:
            print(f"Error sending reminder: {e}")
            return self._simulate_reminder(reminder_type, context)
    
    def _send_with_arcade_toolkit(self, reminder_type: str, user_email: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Send reminder using real Arcade.dev Gmail toolkit"""
        
        try:
            if not self.client:
                return self._simulate_reminder(reminder_type, context)
            
            # Generate reminder content
            reminder_content = self._generate_reminder_content(reminder_type, context)
            
            # Send email using Arcade.dev Gmail toolkit
            email_response = self.client.tools.execute(
                tool_name="Gmail.SendEmail",
                input={
                    "to": user_email,
                    "subject": reminder_content['subject'],
                    "body": reminder_content['body'],
                    "body_format": "text"
                },
                user_id=self.user_id
            )
            
            success = False
            message_id = None
            
            if email_response and hasattr(email_response, 'output') and email_response.output:
                if hasattr(email_response.output, 'value') and email_response.output.value:
                    response_value = email_response.output.value
                    if isinstance(response_value, dict):
                        success = True
                        message_id = response_value.get('id', 'unknown')
            
            return {
                'status': 'sent' if success else 'failed',
                'reminder_type': reminder_type,
                'subject': reminder_content['subject'],
                'message_id': message_id,
                'timestamp': datetime.now().isoformat(),
                'method': 'arcade_toolkit'
            }
            
        except Exception as e:
            print(f"Error using Arcade Gmail toolkit: {e}")
            print("💡 Authorization may be needed. Visit https://api.arcade.dev/dashboard")
            return self._simulate_reminder(reminder_type, context)
    
    def _generate_reminder_content(self, reminder_type: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate personalized reminder content"""
        
        context = context or {}
        
        templates = {
            'break_reminder': {
                'subject': '🌟 Time for a Study Break!',
                'body': f'''Hey there! 👋

You've been studying hard for {context.get('study_duration', 'a while')} - time for a well-deserved break!

Quick break suggestions:
• 🚶‍♀️ Take a 5-10 minute walk
• 🧘‍♀️ Do some stretching or light yoga  
• 💧 Hydrate with water
• 🌬️ Practice deep breathing exercises
• 👀 Rest your eyes by looking at something far away

Remember: Regular breaks improve focus and prevent burnout!

Best wishes,
StudyBalance AI 📚✨'''
            },
            
            'hydration': {
                'subject': '💧 Hydration Reminder',
                'body': '''Hi! 💙

Don't forget to stay hydrated! Your brain needs water to function optimally.

Quick hydration tips:
• Drink a full glass of water now
• Keep a water bottle at your study space
• Set hourly hydration reminders
• Try herbal tea for variety

Stay healthy and keep learning! 🌊

StudyBalance AI'''
            },
            
            'posture_check': {
                'subject': '🪑 Posture Check-In',
                'body': '''Hello! 🙋‍♀️

Time for a quick posture check! Good posture reduces fatigue and improves concentration.

Quick adjustments:
• Sit up straight with shoulders back
• Keep feet flat on the floor
• Position screen at eye level
• Take micro-breaks to stretch
• Roll your shoulders and neck

Your future self will thank you! 💪

StudyBalance AI'''
            },
            
            'eye_rest': {
                'subject': '👁️ Eye Rest Reminder', 
                'body': '''Hi there! 👀

Following the 20-20-20 rule: Every 20 minutes, look at something 20 feet away for 20 seconds.

Eye care tips:
• Blink frequently to moisten eyes
• Adjust screen brightness
• Use good lighting
• Consider blue light filters
• Close eyes and rest for 30 seconds

Protect your vision for lifelong learning! 🌟

StudyBalance AI'''
            },
            
            'stress_relief': {
                'subject': '😌 Stress Relief Moment',
                'body': f'''Hey! 🌸

Feeling stressed? That's completely normal! Here's a quick stress-buster routine:

Try this 2-minute reset:
• Take 5 deep breaths (4 counts in, 6 counts out)
• Do 10 gentle neck rolls
• Smile (yes, really!) for 10 seconds
• Think of one thing you're grateful for
• Remind yourself: "I'm doing my best"

{context.get('encouragement', 'You\'ve got this!')} 💪

StudyBalance AI'''
            },
            
            'achievement': {
                'subject': '🎉 Great Progress!',
                'body': f'''Congratulations! 🎊

You've completed {context.get('completed_sessions', 'several')} study sessions today - that's fantastic progress!

Your achievements:
• Study time: {context.get('total_study_time', 'Good amount')}
• Subjects covered: {context.get('subjects_studied', 'Multiple areas')}
• Breaks taken: {context.get('breaks_taken', 'Regular intervals')}

Keep up the excellent work! Remember to celebrate small wins along the way. 🌟

Proud of you,
StudyBalance AI'''
            }
        }
        
        # Get template or use default
        template = templates.get(reminder_type, templates['break_reminder'])
        
        # Add current time context
        current_hour = datetime.now().hour
        if current_hour < 12:
            time_greeting = "Good morning"
        elif current_hour < 17:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Personalize based on time
        if reminder_type == 'break_reminder' and current_hour >= 18:
            template['body'] += "\n\n🌙 Since it's evening, consider lighter activities to wind down."
        
        return template
    
    def _simulate_reminder(self, reminder_type: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Simulate reminder sending when Arcade toolkit is not available"""
        
        content = self._generate_reminder_content(reminder_type, context)
        
        return {
            'status': 'simulated',
            'reminder_type': reminder_type,
            'subject': content['subject'],
            'message_id': f'sim_{random.randint(10000, 99999)}',
            'timestamp': datetime.now().isoformat(),
            'method': 'simulation',
            'note': 'Real email would be sent with proper Arcade.dev authentication'
        }
    
    def schedule_wellness_reminders(self, user_email: str, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule multiple wellness reminders based on study schedule"""
        
        study_blocks = schedule.get('study_blocks', [])
        if not study_blocks:
            return {'scheduled_reminders': []}
        
        scheduled_reminders = []
        
        for i, block in enumerate(study_blocks):
            if block.get('type') == 'study' and block.get('duration', 0) >= 45:
                
                # Schedule break reminder at 75% through study block
                break_time_offset = int(block['duration'] * 0.75)
                reminder_time = self._add_minutes_to_time(block['start_time'], break_time_offset)
                
                reminder = {
                    'type': 'break_reminder',
                    'scheduled_time': reminder_time,
                    'context': {
                        'study_duration': f"{break_time_offset} minutes",
                        'subject': block.get('subject', 'your subject')
                    }
                }
                scheduled_reminders.append(reminder)
        
        # Add hydration reminders every 2 hours
        hydration_times = self._generate_hydration_schedule(study_blocks)
        for time in hydration_times:
            scheduled_reminders.append({
                'type': 'hydration',
                'scheduled_time': time,
                'context': {}
            })
        
        # Add posture check every 90 minutes
        posture_times = self._generate_posture_schedule(study_blocks)
        for time in posture_times:
            scheduled_reminders.append({
                'type': 'posture_check', 
                'scheduled_time': time,
                'context': {}
            })
        
        return {
            'scheduled_reminders': scheduled_reminders,
            'total_reminders': len(scheduled_reminders),
            'reminder_types': list(set(r['type'] for r in scheduled_reminders))
        }
    
    def _add_minutes_to_time(self, time_str: str, minutes: int) -> str:
        """Add minutes to a time string (HH:MM format)"""
        try:
            time_obj = datetime.strptime(time_str, '%H:%M')
            new_time = time_obj + timedelta(minutes=minutes)
            return new_time.strftime('%H:%M')
        except Exception:
            return time_str
    
    def _generate_hydration_schedule(self, study_blocks: List[Dict]) -> List[str]:
        """Generate hydration reminder times every 2 hours"""
        if not study_blocks:
            return []
        
        study_start = study_blocks[0].get('start_time', '09:00')
        study_end = study_blocks[-1].get('end_time', '17:00')
        
        times = []
        current_time = datetime.strptime(study_start, '%H:%M')
        end_time = datetime.strptime(study_end, '%H:%M')
        
        while current_time < end_time:
            current_time += timedelta(hours=2)
            if current_time <= end_time:
                times.append(current_time.strftime('%H:%M'))
        
        return times
    
    def _generate_posture_schedule(self, study_blocks: List[Dict]) -> List[str]:
        """Generate posture check times every 90 minutes"""
        if not study_blocks:
            return []
        
        study_start = study_blocks[0].get('start_time', '09:00')
        study_end = study_blocks[-1].get('end_time', '17:00')
        
        times = []
        current_time = datetime.strptime(study_start, '%H:%M')
        end_time = datetime.strptime(study_end, '%H:%M')
        
        while current_time < end_time:
            current_time += timedelta(minutes=90)
            if current_time <= end_time:
                times.append(current_time.strftime('%H:%M'))
        
        return times
    
    def send_motivational_message(self, user_email: str, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send motivational message based on achievements"""
        
        context = {
            'completed_sessions': achievement_data.get('sessions_completed', 0),
            'total_study_time': achievement_data.get('total_minutes', 0),
            'subjects_studied': ', '.join(achievement_data.get('subjects', [])),
            'breaks_taken': achievement_data.get('breaks_taken', 0)
        }
        
        # Choose encouragement based on performance
        if context['completed_sessions'] >= 5:
            context['encouragement'] = "You're absolutely crushing it today!"
        elif context['completed_sessions'] >= 3:
            context['encouragement'] = "Fantastic progress - keep the momentum going!"
        else:
            context['encouragement'] = "Every step forward counts - you're doing great!"
        
        return self.send_wellness_reminder('achievement', user_email, context)
    
    def get_wellness_stats(self) -> Dict[str, Any]:
        """Get wellness reminder statistics"""
        
        # This would track actual sending in a real implementation
        return {
            'reminders_sent_today': random.randint(3, 8),
            'most_effective_time': '14:30',
            'popular_reminder_types': ['break_reminder', 'hydration', 'posture_check'],
            'user_engagement_score': round(random.uniform(7.5, 9.5), 1),
            'wellness_improvement': '15%'
        }
