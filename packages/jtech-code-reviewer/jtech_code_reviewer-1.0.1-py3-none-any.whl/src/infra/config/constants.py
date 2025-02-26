import os

from src import __version__
from src.infra.config.settings import Config


class Constants:
    """
    A class to hold constant values and paths used throughout the project.
    """

    MONGODB_URI = f"mongodb://{Config.MONGODB_HOST}:{Config.MONGODB_PORT}/{Config.MONGODB_DB_NAME}?readPreference=primary&ssl=false&directConnection=true"
    PROJECT_DIR_BY_MAIN_FILE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    RESOURCES_DIR = os.path.join(PROJECT_DIR_BY_MAIN_FILE, "../resources")
    LOGGING_CONFIG = os.path.join(PROJECT_DIR_BY_MAIN_FILE, "../logging.yml")
    MANIFESTO_PATH = os.path.join(RESOURCES_DIR, "manifesto.pdf")
    AUTH_PATH = os.path.join(RESOURCES_DIR, "auth.json")
    PROMPT_TEMPLATE_PATH = os.path.join(RESOURCES_DIR, "prompt.txt")

    PROJECT_NAME = "Jtech Code Review"
    PROJECT_DESCRIPTION = "Jtech Code Review API"
    PROJECT_VERSION = __version__.VERSION

    IGNORED_FILE_EXTENSIONS = [".py", ".ts", ".txt"]
