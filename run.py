import os

from app import creat_app

config_name = os.getenv("FLASK_ENV")
"""Get the app environment from the .env file"""

app = creat_app(config_name)
"""Defining configuration to be used"""

if __name__ == "__main__":
    app.run()
