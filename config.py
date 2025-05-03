import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret'
    
    # Check if we are in a production environment or not
    if os.getenv('FLASK_ENV') == 'production':
        # Use Render's persistent storage for SQLite
        SQLALCHEMY_DATABASE_URI = 'sqlite:///mnt/data/hospital.db'
    else:
        # Use the local directory for SQLite when developing locally
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hospital.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
