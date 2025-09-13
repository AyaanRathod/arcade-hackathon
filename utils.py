"""
Utility functions for StudyBalance AI
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import re

def format_time(time_str: str) -> str:
    """Format time string for display"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')
    except:
        return time_str

def calculate_wellness_score(analysis: Dict[str, Any]) -> float:
    """Calculate overall wellness score from email analysis"""
    try:
        workload_score = analysis.get('workload_score', 5.0)
        urgent_emails = analysis.get('urgent_emails', 0)
        total_emails = analysis.get('total_emails', 1)
        
        # Calculate stress factor
        stress_factor = min(urgent_emails / max(total_emails, 1), 1.0)
        
        # Wellness score (inverse of stress)
        wellness = 10 - (workload_score * 0.6 + stress_factor * 4.0)
        
        return round(max(0, min(10, wellness)), 1)
        
    except Exception as e:
        print(f"Error calculating wellness score: {e}")
        return 5.0

def parse_study_subjects(subjects_input: str) -> List[str]:
    """Parse comma-separated subjects input"""
    if not subjects_input:
        return ['Math', 'Physics', 'Chemistry', 'English']
    
    subjects = [s.strip() for s in subjects_input.split(',')]
    return [s for s in subjects if s]  # Remove empty strings

def validate_time_format(time_str: str) -> bool:
    """Validate HH:MM time format"""
    pattern = r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def calculate_study_efficiency(study_blocks: List[Dict], total_time: int) -> Dict[str, Any]:
    """Calculate study efficiency metrics"""
    if not study_blocks:
        return {'efficiency': 0, 'focus_score': 0, 'recommendations': []}
    
    study_sessions = [b for b in study_blocks if b.get('type') == 'study']
    break_sessions = [b for b in study_blocks if b.get('type') == 'break']
    
    # Calculate metrics
    avg_study_duration = sum(s['duration'] for s in study_sessions) / len(study_sessions)
    total_break_time = sum(b['duration'] for b in break_sessions)
    break_ratio = total_break_time / max(total_time, 1)
    
    # Efficiency score (0-10)
    efficiency = 8.0  # Base score
    
    # Adjust for optimal study block length (60-120 minutes)
    if 60 <= avg_study_duration <= 120:
        efficiency += 1.0
    elif avg_study_duration > 120:
        efficiency -= 0.5
    
    # Adjust for break ratio (10-20% is optimal)
    if 0.1 <= break_ratio <= 0.2:
        efficiency += 1.0
    elif break_ratio < 0.05:
        efficiency -= 1.0
    
    # Focus score based on block consistency
    durations = [s['duration'] for s in study_sessions]
    consistency = 1.0 - (max(durations) - min(durations)) / max(max(durations), 1)
    focus_score = consistency * 10
    
    # Generate recommendations
    recommendations = []
    if avg_study_duration > 120:
        recommendations.append("Consider shorter study blocks (60-90 minutes) for better focus")
    if break_ratio < 0.1:
        recommendations.append("Add more breaks to prevent fatigue")
    if break_ratio > 0.25:
        recommendations.append("Consider longer study blocks with fewer breaks")
    
    return {
        'efficiency': round(efficiency, 1),
        'focus_score': round(focus_score, 1),
        'avg_study_duration': round(avg_study_duration, 1),
        'break_ratio': round(break_ratio * 100, 1),
        'recommendations': recommendations
    }

def get_time_of_day(hour: int) -> str:
    """Get time of day category"""
    if 6 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 17:
        return 'afternoon'
    elif 17 <= hour < 21:
        return 'evening'
    else:
        return 'night'

def generate_study_tips(subject: str, time_of_day: str) -> List[str]:
    """Generate study tips based on subject and time"""
    tips = {
        'morning': [
            "Perfect time for challenging subjects - your brain is fresh!",
            "Start with the most difficult material while energy is high",
            "Use active learning techniques like summarizing and questioning"
        ],
        'afternoon': [
            "Good time for review and practice problems",
            "Take advantage of stable energy levels",
            "Consider group study or collaborative learning"
        ],
        'evening': [
            "Focus on review and consolidation",
            "Light reading and note organization work well",
            "Avoid starting new complex topics"
        ],
        'night': [
            "Time to wind down - avoid intensive studying",
            "Light review or planning for tomorrow",
            "Consider relaxation techniques instead"
        ]
    }
    
    subject_tips = {
        'math': ["Work through problems step by step", "Use visual aids and diagrams"],
        'physics': ["Connect concepts to real-world examples", "Practice problem-solving methods"],
        'chemistry': ["Use molecular models and periodic table", "Practice balancing equations"],
        'english': ["Read actively with note-taking", "Analyze themes and literary devices"],
        'history': ["Create timelines and concept maps", "Connect events to modern contexts"]
    }
    
    general_tips = tips.get(time_of_day, tips['afternoon'])
    specific_tips = subject_tips.get(subject.lower(), ["Stay focused and take notes"])
    
    return general_tips + specific_tips

def format_duration(minutes: int) -> str:
    """Format duration in minutes to human-readable string"""
    if minutes < 60:
        return f"{minutes} minutes"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        return f"{hours}h {remaining_minutes}m"

def calculate_optimal_break_time(study_duration: int, difficulty: int = 5) -> int:
    """Calculate optimal break time based on study duration and difficulty"""
    base_break = 15  # minutes
    
    # Longer breaks for longer study sessions
    if study_duration >= 120:
        base_break = 20
    elif study_duration >= 90:
        base_break = 15
    else:
        base_break = 10
    
    # Adjust for difficulty (1-10 scale)
    difficulty_adjustment = (difficulty - 5) * 2  # -8 to +10 minutes
    
    optimal_break = base_break + difficulty_adjustment
    return max(5, min(30, optimal_break))  # Keep between 5-30 minutes