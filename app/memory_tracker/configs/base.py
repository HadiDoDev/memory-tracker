import pathlib
import os


class Config(object):
    DEBUG = False
    TESTING = False


BASE_DIR = pathlib.Path(__file__).resolve(strict=True).parent.parent.parent

SQLITE_DATABASE_URI = os.path.join(BASE_DIR, 'memory_tracker/db/memorytracker.db')
