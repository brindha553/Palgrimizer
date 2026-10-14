import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'palgrimizer-enterprise-super-secret-key-2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'palgrimizer.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32MB max upload
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'rtf', 'png', 'jpg', 'jpeg'}
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'palgrimizer-jwt-secret-key-9988')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
