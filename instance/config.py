import os
"""We are importing os to use the environment variable exported in .nve file"""
class Config(object):
    """Parent configuration class contains infomation where all other environments will inherit"""
    DEGUG = False
    TESTING = False
    SECRET = os.getenv("SECRET", "precious")
    """This gets the secret key from the .env file"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")


class DevelopmentConfig(Config):
    """Configuration for development"""
    DEBUG = True


class TestingConfig(Config):
    """Configuration for Testing with seperate database"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")

class StagingConfig(Config):
    """Configurations for staging"""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production"""
    TESTING = False
    DEBUG = False

app_config = {
"development": DevelopmentConfig,
"testing": TestingConfig,
"staging": StagingConfig,
"production": ProductionConfig
}
