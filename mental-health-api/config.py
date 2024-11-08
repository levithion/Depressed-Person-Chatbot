#mental-health-api/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mental_health.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False