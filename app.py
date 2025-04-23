from flask import Flask
from flask_jwt_extended import JWTManager
from models import db  
from routes import routes
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Load configuration
app.config.from_object(Config)

# Initialize the database with Flask app
db.init_app(app)

# Initialize JWT manager with the Flask app
jwt = JWTManager(app)

# Register routes blueprint
app.register_blueprint(routes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
