# import os
# basedir = os.path.abspath(os.path.dirname(__file__))

# class Config:
#     SECRET_KEY = 'your-secret'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'hospital.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


import os

from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret')
    SQLALCHEMY_DATABASE_URI = (
        'postgresql://{username}:{password}@{host}:{port}/{database_name}'
        .format(
            username=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT', 5432),
            database_name=os.getenv('POSTGRES_DB')
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
