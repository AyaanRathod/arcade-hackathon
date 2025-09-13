"""
Gmail Analysis using Arcade.dev Gmail Toolkit
Analyzes email patterns for stress indicators and workload assessment
"""

from typing import Dict, List, Any
from datetime import datetime, timedelta

class GmailAnalyzer:
    """Analyzes Gmail using Arcade.dev Gmail toolkit for stress patterns"""
    
    def __init__(self, api_key: str, user_id: str):
        self.api_key = api_key
        self.user_id = user_id
        self.client = None
        self.initialized = False
        
    def initialize(self):
        """Initialize Arcade.dev client"""
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
    
    def analyze_email_patterns(self, days_back: int = 7) -> Dict[str, Any]:
        """
        Analyze Gmail patterns for the specified number of days
        
        Args:
            days_back: Number of days to analyze (default: 7)
            
        Returns:
            Dictionary containing analysis results
        """
        if not self.initialized:
            if not self.initialize():
                return self._simulate_analysis(days_back)
        
        try:
            return self._analyze_with_arcade_toolkit(days_back)
        except Exception as e:
            print(f"Error in Gmail analysis: {e}")
            return self._simulate_analysis(days_back)
    
    def _analyze_with_arcade_toolkit(self, days_back: int) -> Dict[str, Any]:
        """Use real Arcade.dev Gmail toolkit for analysis"""
        
        try:
            if not self.client:
                return self._simulate_analysis(days_back)
                
            # Try to execute Gmail tools directly
            emails_response = self.client.tools.execute(
                tool_name="Gmail.ListEmails",
                input={"n_emails": 50},
                user_id=self.user_id
            )
            
            # Parse and analyze the email data
            emails_data = []
            if emails_response and hasattr(emails_response, 'output') and emails_response.output:
                if hasattr(emails_response.output, 'value') and emails_response.output.value:
                    response_value = emails_response.output.value
                    if isinstance(response_value, list):
                        emails_data = response_value
            
            # Analyze the fetched emails
            analysis = self._analyze_email_content(emails_data, days_back)
            analysis['real_data'] = True
            return analysis
            
        except Exception as e:
            print(f"Error using Arcade Gmail toolkit: {e}")
            
            # Check if it's an authorization error
            error_str = str(e)
            if "tool_authorization_required" in error_str or "authorization required" in error_str:
                print("🔐 AUTHORIZATION REQUIRED!")
                print("📌 You need to authorize Gmail access in the arcade.dev dashboard")
                print("🌐 Visit: https://api.arcade.dev/dashboard")
                print("✅ Steps:")
                print("   1. Go to your arcade.dev dashboard")
                print("   2. Find your project/tools section")
                print("   3. Authorize Gmail toolkit")
                print("   4. Return here and try the analysis again")
                
                # Return a special response indicating auth is needed
                return {
                    'total_emails': 0,
                    'work_emails': 0,
                    'urgent_emails': 0,
                    'stress_keywords_found': [],
                    'peak_hours': [],
                    'workload_score': 0,
                    'burnout_risk': 'unknown',
                    'recommendations': [
                        '🔐 Gmail authorization required',
                        '🌐 Visit https://api.arcade.dev/dashboard to authorize Gmail access',
                        '📧 Once authorized, real email analysis will work'
                    ],
                    'auth_required': True,
                    'auth_url': 'https://api.arcade.dev/dashboard',
                    'real_data': False
                }
            
            print("💡 Authorization may be needed. Visit https://api.arcade.dev/dashboard")
            return self._simulate_analysis(days_back)
    
    def _analyze_email_content(self, emails: List[Dict], days_back: int) -> Dict[str, Any]:
        """Analyze email content for stress indicators"""
        
        stress_keywords = [
            'urgent', 'deadline', 'asap', 'emergency', 'critical',
            'overdue', 'late', 'failed', 'missing', 'important',
            'immediately', 'quickly', 'rush', 'priority'
        ]
        
        work_keywords = [
            'assignment', 'homework', 'project', 'exam', 'test',
            'quiz', 'submission', 'grade', 'course', 'class',
            'study', 'lecture', 'professor', 'teacher'
        ]
        
        total_emails = len(emails) if emails else 0
        urgent_count = 0
        work_count = 0
        stress_keywords_found = []
        hourly_distribution = {}
        
        cutoff_date = datetime.now() - timedelta(days=days_back)
        recent_emails = []
        
        for email in emails or []:
            try:
                email_date = None
                if isinstance(email, dict):
                    if 'date' in email:
                        date_str = str(email['date'])
                        if 'T' in date_str:
                            date_str = date_str.replace('Z', '+00:00')
                            email_date = datetime.fromisoformat(date_str)
                    elif 'timestamp' in email:
                        email_date = datetime.fromtimestamp(float(email['timestamp']))
                
                if email_date and email_date >= cutoff_date:
                    recent_emails.append(email)
                elif not email_date:
                    recent_emails.append(email)
            except Exception:
                recent_emails.append(email)
        
        total_emails = len(recent_emails)
        
        for email in recent_emails:
            if not isinstance(email, dict):
                continue
                
            subject = str(email.get('subject', '')).lower()
            body = str(email.get('body', '') or email.get('snippet', '') or email.get('text', '')).lower()
            sender = str(email.get('sender', '') or email.get('from', '')).lower()
            
            email_text = f"{subject} {body} {sender}"
            
            for keyword in stress_keywords:
                if keyword in email_text:
                    urgent_count += 1
                    if keyword not in stress_keywords_found:
                        stress_keywords_found.append(keyword)
                    break
            
            for keyword in work_keywords:
                if keyword in email_text:
                    work_count += 1
                    break
            
            try:
                email_time = None
                if 'date' in email:
                    date_str = str(email['date']).replace('Z', '+00:00')
                    email_time = datetime.fromisoformat(date_str)
                elif 'timestamp' in email:
                    email_time = datetime.fromtimestamp(float(email['timestamp']))
                
                if email_time:
                    hour = email_time.hour
                    hourly_distribution[hour] = hourly_distribution.get(hour, 0) + 1
            except Exception:
                pass
        
        peak_hours = []
        if hourly_distribution:
            max_count = max(hourly_distribution.values())
            for hour, count in hourly_distribution.items():
                if count >= max_count * 0.7:
                    peak_hours.append(f"{hour:02d}:00-{(hour+1)%24:02d}:00")
        
        if total_emails > 0:
            urgent_ratio = urgent_count / total_emails
            work_ratio = work_count / total_emails
            workload_score = min(10, (urgent_ratio * 5 + work_ratio * 3) * 10)
        else:
            workload_score = 0
        
        if workload_score >= 7:
            burnout_risk = 'high'
        elif workload_score >= 4:
            burnout_risk = 'moderate'
        else:
            burnout_risk = 'low'
        
        recommendations = []
        if total_emails > 0:
            if urgent_count > total_emails * 0.25:
                recommendations.append('High urgency emails detected - consider prioritization techniques')
            if len(peak_hours) > 3:
                recommendations.append('Email scattered throughout day - try batching email checks')
            if any(hour for hour in hourly_distribution.keys() if hour >= 22 or hour <= 6):
                recommendations.append('Late night/early morning emails - set email boundaries')
            if work_count > total_emails * 0.6:
                recommendations.append('High volume of academic emails - consider organizing with filters')
        
        if not recommendations:
            recommendations.append('Email patterns look healthy - keep up the good work!')
        
        return {
            'total_emails': total_emails,
            'urgent_emails': urgent_count,
            'work_emails': work_count,
            'stress_keywords_found': stress_keywords_found,
            'peak_hours': peak_hours,
            'workload_score': round(workload_score, 1),
            'burnout_risk': burnout_risk,
            'recommendations': recommendations,
            'analysis_date': datetime.now().isoformat(),
            'days_analyzed': days_back,
            'hourly_distribution': hourly_distribution
        }
    
    def _simulate_analysis(self, days_back: int) -> Dict[str, Any]:
        """Simulate Gmail analysis when Arcade toolkit is not available"""
        import random
        
        total_emails = random.randint(20, 60)
        urgent_emails = random.randint(3, total_emails // 3)
        work_emails = random.randint(total_emails // 2, total_emails - 5)
        
        return {
            'total_emails': total_emails,
            'urgent_emails': urgent_emails,
            'work_emails': work_emails,
            'stress_keywords_found': ['deadline', 'urgent', 'assignment'],
            'peak_hours': ['09:00-11:00', '14:00-16:00', '20:00-22:00'],
            'workload_score': round(random.uniform(3.0, 8.5), 1),
            'burnout_risk': random.choice(['low', 'moderate', 'high']),
            'recommendations': [
                'Consider email batching - check only 3 times daily',
                'High stress keywords detected - practice mindfulness',
                'Late evening emails - set boundaries after 9 PM'
            ],
            'analysis_date': datetime.now().isoformat(),
            'days_analyzed': days_back,
            'simulation_mode': True,
            'hourly_distribution': {9: 3, 10: 5, 14: 4, 15: 6, 20: 2}
        }