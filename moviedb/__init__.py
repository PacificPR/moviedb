from flask import Flask, session, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://may:venom123@localhost/imdb'
    app.config['SECRET_KEY'] = 'thisisasecret'

    db.init_app(app)
    CORS(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
