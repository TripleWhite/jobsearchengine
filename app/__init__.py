from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 更宽松的CORS配置用于调试
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:5177"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    db.init_app(app)
    migrate.init_app(app, db)
    
    # Note: MCP client is automatically provided by Cline at runtime
    # and can be accessed via current_app.mcp

    from app.routes import auth_bp, user_bp, admin_bp, job_bp
    # 添加全局API前缀
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(job_bp, url_prefix='/api/job')

    return app

from app import models
