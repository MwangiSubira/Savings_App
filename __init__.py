from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from app.config import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
db = SQLAlchemy(app)


# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.auth import bp as auth_bp
    from app.routes.wallet import bp as wallet_bp
    from app.routes.goal import bp as goal_bp
    from app.routes.group import bp as group_bp
    from app.routes.savings import bp as savings_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(wallet_bp, url_prefix='/wallets')
    app.register_blueprint(goal_bp, url_prefix='/goals')
    app.register_blueprint(group_bp, url_prefix='/groups')
    app.register_blueprint(savings_bp, url_prefix='/savings')

    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    return app