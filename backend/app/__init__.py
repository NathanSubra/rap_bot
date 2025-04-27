from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()
    return app
