import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    A class to manage configuration settings loaded from environment variables.
    """
    # Redmine
    REDMINE_TOKEN = os.getenv('REDMINE_TOKEN', '5e6d691bb38270c50618c769faa7aff6fa2083db')
    REDMINE_URL = os.getenv('REDMINE_URL', 'https://jtech.easyredmine.com')

    # API
    API_V1_STR = '/api/v1'

    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', 6379)
    REDIS_DB = os.getenv('REDIS_DB', 1)
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

    ENV = os.getenv('ENV', 'dev')

    # GitLab configuration
    GITLAB_URL = os.getenv('GITLAB_URL', 'https://gitlab.com')
    GITLAB_TOKEN = os.getenv('GITLAB_TOKEN', 'glpat-KisCrenUWP6_SjyJsxnG')

    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # MongoDB configuration
    MONGODB_HOST = os.getenv('MONGODB_HOST', 'localhost')
    MONGODB_PORT = int(os.getenv('MONGODB_PORT', 27017))
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'jtech-code-review')
    MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME', 'reviews')
    MONGODB_COLLECTION_PROMPT = os.getenv('MONGODB_COLLECTION_PROMPT', 'prompt')

    # Max number of reviews to be fetched from MongoDB
    MAX_CODE_REVIEWS = int(os.getenv('MAX_CODE_REVIEWS', 2))

    # Server
    SERVER_HOST = os.getenv('SERVER_HOST', 'localhost')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
    SERVER_LEVEL = os.getenv('SERVER_LEVEL', 'info')
