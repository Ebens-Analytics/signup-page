from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from urllib.parse import quote

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{quote("09061354410@btc")}@localhost:3306/testdb'
    app.secret_key = 'SOME KEY'
    
    
    db.init_app(app)
    bcrypt = Bcrypt(app)
    migrate = Migrate(app, db)
    
    
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for('index'))
    
    
    from routes import register_routes
    register_routes(app, db, bcrypt)
    
    return app
