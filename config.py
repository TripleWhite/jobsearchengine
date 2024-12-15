import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-this')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-key-change-this')
    JWT_EXPIRATION_HOURS = float(os.getenv('JWT_EXPIRATION_HOURS', '2'))

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'instance/app.log')
    LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    @classmethod
    def init_app(cls, app):
        """初始化应用配置"""
        # 确保日志目录存在
        os.makedirs(os.path.dirname(cls.LOG_FILE), exist_ok=True)

        # 配置日志处理器
        file_handler = RotatingFileHandler(
            cls.LOG_FILE,
            maxBytes=cls.LOG_MAX_SIZE,
            backupCount=cls.LOG_BACKUP_COUNT
        )
        file_handler.setFormatter(logging.Formatter(cls.LOG_FORMAT))
        file_handler.setLevel(cls.LOG_LEVEL)

        # 添加到应用日志处理器
        app.logger.addHandler(file_handler)
        app.logger.setLevel(cls.LOG_LEVEL)

        # 设置 Werkzeug 日志
        logging.getLogger('werkzeug').addHandler(file_handler)

    @classmethod
    def get_jwt_expiration(cls):
        """Get the JWT expiration time in hours"""
        if hasattr(cls, '_jwt_expiration_override'):
            return cls._jwt_expiration_override
        return cls.JWT_EXPIRATION_HOURS

    @classmethod
    def set_jwt_expiration(cls, hours):
        """Set a temporary JWT expiration time override"""
        cls._jwt_expiration_override = hours

    @classmethod
    def reset_jwt_expiration(cls):
        """Reset JWT expiration time to default"""
        if hasattr(cls, '_jwt_expiration_override'):
            delattr(cls, '_jwt_expiration_override')
