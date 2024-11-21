from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "fcd3cd4a2e4348f53a8ea345c1bb4b71"
app.config["UPLOAD_FOLDER"] = "static/midia"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"




from fakepinterest import routes

from fakepinterest.models import Usuario


@login_manager.user_loader
def load_usuario(id_usuario):
    user = Usuario.query.get(int(id_usuario))
    if user is None:
        return None
    return user
