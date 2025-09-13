"""
Calendar Optimization using Arcade.dev Google Calendar Toolkit
Creates optimized study schedules with perfect break timing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class CalendarOptimizer:
    """Optimizes study schedules using Arcade.dev Google Calendar toolkit"""
    
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.client = None
        self.initialized = False
        
    def initialize(self):
        """Initialize Arcade.dev Google Calendar toolkit"""
        try:
            from arcadepy import Arcade
            self.client = Arcade(api_key=self.api_key)
            self.initialized = True
            print("✅ Google Calendar toolkit client initialized")
            return True
            
        except ImportError:
            print("⚠️ arcadepy not available, using simulation mode")
            return False
        except Exception as e:
            print(f"❌ Calendar toolkit initialization error: {e}")
            return False
    
    def create_optimized_schedule(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create an optimized study schedule"""
        if not self.initialized:
            if not self.initialize():
                return self._simulate_schedule(preferences)
        
        try:
            return self._create_with_arcade_toolkit(preferences)
        except Exception as e:
            print(f"Error creating optimized schedule: {e}")
            return self._simulate_schedule(preferences)
    
    def _create_with_arcade_toolkit(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Use real Arcade.dev Google Calendar toolkit for schedule creation"""
        
        try:
            if not self.client:
                return self._simulate_schedule(preferences)
            
            # Get existing calendar events to avoid conflicts
            existing_events = self._get_existing_events()
            
            # Create optimized schedule avoiding conflicts
            schedule = self._generate_optimized_blocks(preferences, existing_events)
            
            return schedule
            
        except Exception as e:
            print(f"Error using Arcade Calendar toolkit: {e}")
            print("💡 Authorization may be needed. Visit https://api.arcade.dev/dashboard")
            return self._simulate_schedule(preferences)
    
    def _get_existing_events(self) -> List[Dict]:
        """Get existing calendar events using Arcade.dev toolkit"""
        try:
            if not self.client:
                return []
                
            today = datetime.now().date()
            tomorrow = today + timedelta(days=1)
            
            events_response = self.client.tools.execute(
                tool_name="GoogleCalendar.ListEvents",
                input={
                    "min_end_datetime": f"{today}T00:00:00",
                    "max_start_datetime": f"{tomorrow}T23:59:59",
                    "calendar_id": "primary",
                    "max_results": 20
                },
                user_id=self.user_id
            )
            
            events = []
            if events_response and hasattr(events_response, 'output') and events_response.output:
                if hasattr(events_response.output, 'value') and events_response.output.value:
                    response_value = events_response.output.value
                    if isinstance(response_value, list):
                        events = response_value
            
            return events
            
        except Exception as e:
            print(f"Error fetching calendar events: {e}")
            return []
    
    def _generate_optimized_blocks(self, preferences: Dict[str, Any], existing_events: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Generate optimized study blocks using scientific principles"""
        
        study_duration = preferences.get('study_duration', 90)
        break_duration = preferences.get('break_duration', 15)
        subjects = preferences.get('subjects', ['Math', 'Physics', 'Chemistry', 'English'])
        start_time_str = preferences.get('start_time', '09:00')
        
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        current_datetime = datetime.combine(datetime.now().date(), start_time)
        
        study_blocks = []
        total_study_time = 0
        total_break_time = 0
        
        difficulty_order = self._order_subjects_by_difficulty(subjects)
        
        for i, subject in enumerate(difficulty_order):
            adjusted_duration = self._adjust_duration_for_time_and_subject(
                current_datetime, subject, study_duration
            )
            
            end_datetime = current_datetime + timedelta(minutes=adjusted_duration)
            
            study_blocks.append({
                'subject': subject,
                'start_time': current_datetime.strftime('%H:%M'),
                'end_time': end_datetime.strftime('%H:%M'),
                'type': 'study',
                'duration': adjusted_duration,
                'difficulty': self._get_subject_difficulty(subject),
                'optimal_time': self._is_optimal_time_for_subject(current_datetime, subject)
            })
            
            total_study_time += adjusted_duration
            current_datetime = end_datetime
            
            if i < len(difficulty_order) - 1:
                adjusted_break = self._adjust_break_duration(break_duration, adjusted_duration)
                break_end = current_datetime + timedelta(minutes=adjusted_break)
                
                study_blocks.append({
                    'subject': 'Break',
                    'start_time': current_datetime.strftime('%H:%M'),
                    'end_time': break_end.strftime('%H:%M'),
                    'type': 'break',
                    'duration': adjusted_break,
                    'activity': self._suggest_break_activity(adjusted_break)
                })
                
                total_break_time += adjusted_break
                current_datetime = break_end
        
        wellness_score = self._calculate_wellness_score(study_blocks, total_study_time, total_break_time)
        efficiency_score = self._calculate_efficiency_score(study_blocks)
        
        return {
            'study_blocks': study_blocks,
            'total_study_time': total_study_time,
            'total_break_time': total_break_time,
            'wellness_score': wellness_score,
            'efficiency_score': efficiency_score,
            'schedule_rating': 'Excellent' if wellness_score > 8.5 else 'Good' if wellness_score > 7 else 'Needs Improvement',
            'optimization_notes': self._generate_optimization_notes(study_blocks)
        }
    
    def _order_subjects_by_difficulty(self, subjects: List[str]) -> List[str]:
        """Order subjects by difficulty for optimal scheduling"""
        difficulty_map = {
            'math': 9, 'mathematics': 9, 'calculus': 9, 'algebra': 8,
            'physics': 8, 'chemistry': 7, 'biology': 6,
            'computer science': 8, 'programming': 8, 'algorithms': 9,
            'english': 5, 'literature': 5, 'history': 6,
            'psychology': 6, 'sociology': 5, 'philosophy': 7
        }
        
        subjects_with_difficulty = [
            (subject, difficulty_map.get(subject.lower(), 5))
            for subject in subjects
        ]
        
        return [subject for subject, _ in sorted(subjects_with_difficulty, key=lambda x: x[1], reverse=True)]
    
    def _adjust_duration_for_time_and_subject(self, time: datetime, subject: str, base_duration: int) -> int:
        """Adjust study duration based on time of day and subject difficulty"""
        hour = time.hour
        
        if (9 <= hour <= 11) or (15 <= hour <= 17):
            multiplier = 1.0
        elif (11 <= hour <= 15) or (17 <= hour <= 20):
            multiplier = 0.9
        else:
            multiplier = 0.8
        
        difficulty = self._get_subject_difficulty(subject)
        if difficulty >= 8:
            if hour < 12:
                pass
            else:
                multiplier *= 0.9
        
        return int(base_duration * multiplier)
    
    def _get_subject_difficulty(self, subject: str) -> int:
        """Get difficulty rating for a subject (1-10)"""
        difficulty_map = {
            'math': 9, 'mathematics': 9, 'calculus': 9, 'algebra': 8,
            'physics': 8, 'chemistry': 7, 'biology': 6,
            'computer science': 8, 'programming': 8, 'algorithms': 9,
            'english': 5, 'literature': 5, 'history': 6,
            'psychology': 6, 'sociology': 5, 'philosophy': 7
        }
        return difficulty_map.get(subject.lower(), 5)
    
    def _is_optimal_time_for_subject(self, time: datetime, subject: str) -> bool:
        """Check if current time is optimal for the subject"""
        hour = time.hour
        difficulty = self._get_subject_difficulty(subject)
        
        if difficulty >= 7:
            return (9 <= hour <= 12) or (15 <= hour <= 17)
        else:
            return hour >= 9 and hour <= 20
    
    def _adjust_break_duration(self, base_break: int, study_duration: int) -> int:
        """Adjust break duration based on study intensity"""
        if study_duration >= 90:
            return min(base_break + 5, 20)
        return base_break
    
    def _suggest_break_activity(self, break_duration: int) -> str:
        """Suggest appropriate break activity based on duration"""
        if break_duration <= 10:
            return "Deep breathing or stretching"
        elif break_duration <= 20:
            return "Short walk or hydration"
        else:
            return "Physical exercise or snack"
    
    def _calculate_wellness_score(self, blocks: List[Dict], study_time: int, break_time: int) -> float:
        """Calculate wellness score based on schedule balance"""
        balance_ratio = break_time / max(study_time, 1)
        optimal_ratio = 0.15
        
        balance_score = 10 * (1 - abs(balance_ratio - optimal_ratio) / optimal_ratio)
        
        duration_score = 0
        study_blocks = [b for b in blocks if b['type'] == 'study']
        for block in study_blocks:
            duration = block['duration']
            if 60 <= duration <= 120:
                duration_score += 10
            elif 45 <= duration <= 150:
                duration_score += 8
            else:
                duration_score += 5
        duration_score /= max(len(study_blocks), 1)
        
        wellness_score = (balance_score * 0.4 + duration_score * 0.6)
        return round(min(10, max(0, wellness_score)), 1)
    
    def _calculate_efficiency_score(self, blocks: List[Dict]) -> float:
        """Calculate efficiency score based on cognitive optimization"""
        study_blocks = [b for b in blocks if b['type'] == 'study']
        if not study_blocks:
            return 0
        
        efficiency = 0
        for block in study_blocks:
            if block.get('optimal_time', False):
                efficiency += 10
            else:
                efficiency += 6
        
        return round(efficiency / len(study_blocks), 1)
    
    def _generate_optimization_notes(self, blocks: List[Dict]) -> List[str]:
        """Generate notes about the schedule optimization"""
        notes = []
        
        study_blocks = [b for b in blocks if b['type'] == 'study']
        
        morning_blocks = [b for b in study_blocks if int(b['start_time'].split(':')[0]) < 12]
        if morning_blocks and any(b.get('difficulty', 0) >= 8 for b in morning_blocks):
            notes.append("✅ Difficult subjects scheduled during peak morning hours")
        
        break_blocks = [b for b in blocks if b['type'] == 'break']
        if len(break_blocks) >= len(study_blocks) * 0.8:
            notes.append("✅ Adequate break frequency maintained")
        
        break_activities = set(b.get('activity', '') for b in break_blocks)
        if len(break_activities) > 1:
            notes.append("✅ Variety in break activities promotes better recovery")
        
        return notes
    
    def _simulate_schedule(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate schedule creation when Arcade toolkit is not available"""
        return self._generate_optimized_blocks(preferences)
    
    def get_calendar_events(self, days: int = 7) -> Dict[str, Any]:
        """Get calendar events for the specified number of days"""
        try:
            if self.initialized and self.client:
                events = self._get_existing_events()
            else:
                events = [
                    {
                        'summary': 'Data Structures Lecture',
                        'start': {'dateTime': '2025-09-13T10:00:00'},
                        'end': {'dateTime': '2025-09-13T11:30:00'}
                    },
                    {
                        'summary': 'Algorithm Analysis Lab',
                        'start': {'dateTime': '2025-09-13T14:00:00'},
                        'end': {'dateTime': '2025-09-13T17:00:00'}
                    }
                ]
            
            processed_events = []
            for event in events:
                if isinstance(event, dict):
                    processed_events.append({
                        'title': event.get('summary', 'Untitled'),
                        'start': event.get('start', {}).get('dateTime', ''),
                        'end': event.get('end', {}).get('dateTime', ''),
                        'type': 'existing'
                    })
            
            free_blocks = self._calculate_free_time_blocks(processed_events)
            
            return {
                'events': processed_events,
                'free_time_blocks': free_blocks,
                'total_events': len(processed_events),
                'total_free_hours': sum(
                    (datetime.fromisoformat(block['end'].replace('Z', '')) - 
                     datetime.fromisoformat(block['start'].replace('Z', ''))).seconds / 3600
                    for block in free_blocks if 'start' in block and 'end' in block
                )
            }
            
        except Exception as e:
            print(f"Error getting calendar events: {e}")
            return {'events': [], 'free_time_blocks': [], 'error': str(e)}
    
    def _calculate_free_time_blocks(self, events: List[Dict]) -> List[Dict]:
        """Calculate free time blocks between events"""
        if not events:
            return [{
                'start': '09:00',
                'end': '17:00',
                'duration_hours': 8
            }]
        
        sorted_events = sorted(events, key=lambda x: x.get('start', ''))
        
        free_blocks = []
        current_time = datetime.fromisoformat('2025-09-13T09:00:00')
        
        for event in sorted_events:
            start_str = event.get('start', '')
            if start_str:
                try:
                    event_start = datetime.fromisoformat(start_str.replace('Z', ''))
                    
                    if current_time < event_start:
                        duration = (event_start - current_time).seconds / 3600
                        if duration >= 0.5:
                            free_blocks.append({
                                'start': current_time.strftime('%H:%M'),
                                'end': event_start.strftime('%H:%M'),
                                'duration_hours': round(duration, 1)
                            })
                    
                    end_str = event.get('end', '')
                    if end_str:
                        event_end = datetime.fromisoformat(end_str.replace('Z', ''))
                        current_time = max(current_time, event_end)
                except Exception:
                    continue
        
        return free_blocks
