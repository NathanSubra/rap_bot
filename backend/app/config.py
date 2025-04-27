import os, pathlib
BASE_DIR = pathlib.Path(__file__).resolve().parent
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI") or f"sqlite:///{BASE_DIR.parent.parent / 'instance' / 'rapbot.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "replace-me")
