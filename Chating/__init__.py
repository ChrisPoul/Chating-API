import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    CORS(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from .models import db
    db.init_app(app)
    Migrate(app, db)

    from .api import api
    api.init_app(app)

    return app
