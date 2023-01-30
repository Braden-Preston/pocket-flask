from flask import Flask
from flask_session import Session

from client.config import Config
from client.auth import login_manager, auth
from client.views import app as routes

# Initialize a Flask instance
app = Flask(__name__)

# Configure from environment-based config
app.config.from_object(Config)

# Set up server-side sessions
session_store = Session()
session_store.init_app(app)

# Register login manager + routes
login_manager.init_app(app)
app.register_blueprint(auth)

# Add application routes
app.register_blueprint(routes)
