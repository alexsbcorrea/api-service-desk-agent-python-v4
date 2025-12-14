from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from app.database.db import db
from app.socketio.events import socketio
import app.models

#Routes
from app.routes.user import user_bp
from app.routes.preservice import preservice_bp
from app.routes.thread import thread_bp
from app.routes.message import message_bp
#Routes

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(preservice_bp, url_prefix='/api')
    app.register_blueprint(thread_bp, url_prefix='/api')
    app.register_blueprint(message_bp, url_prefix='/api')

    return app