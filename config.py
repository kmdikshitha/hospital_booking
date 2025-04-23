import os

class Config:
    MYSQL_HOST = 'localhost'  # Change to your MySQL host
    MYSQL_USER = 'root'  # Change to your MySQL username
    MYSQL_PASSWORD = 'new_password'  # Change to your MySQL password
    MYSQL_DB = 'hospital_booking'  # Database name

    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable Flask-SQLAlchemy modification tracking
    
    # JWT Configuration
    JWT_SECRET_KEY = '4dbce7d57c803436fbbdcbeb9719918e651df0db2e9c6f399a3321252a10c581'  # Change this to a strong secret key
