"""
Configuration settings for StudyBalance AI
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Arcade.dev settings
    ARCADE_API_KEY = os.getenv('ARCADE_API_KEY')
    ARCADE_USER_ID = os.getenv('ARCADE_USER_ID')
    
    # Application settings
    APP_NAME = 'StudyBalance AI'
    VERSION = '1.0.0'
    
    # Wellness nudging defaults
    DEFAULT_BREAK_INTERVAL = 90  # minutes
    DEFAULT_HYDRATION_INTERVAL = 60  # minutes
    DEFAULT_STUDY_DURATION = 90  # minutes
    DEFAULT_BREAK_DURATION = 15  # minutes
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        required = ['ARCADE_API_KEY', 'ARCADE_USER_ID']
        missing = [key for key in required if not getattr(Config, key)]
        
        if missing:
            print(f"⚠️ Missing required configuration: {', '.join(missing)}")
            print("Please check your .env file")
            return False
        
        return True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False