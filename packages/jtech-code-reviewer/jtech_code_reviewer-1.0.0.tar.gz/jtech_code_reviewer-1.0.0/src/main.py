from dotenv import load_dotenv

from src.api.api import API
from src.infra.config.constants import Constants
from src.infra.config.logging_config import get_logger
from src.infra.config.settings import Config

LOGGER = get_logger()

load_dotenv()


def main():
    LOGGER.info(f">>> Running: {Constants.PROJECT_DESCRIPTION}")
    LOGGER.info(f">>> Version: {Constants.PROJECT_VERSION}")
    app = API().app
    import uvicorn
    uvicorn.run(app, host=Config.SERVER_HOST, port=Config.SERVER_PORT, log_level=Config.SERVER_LEVEL)


if __name__ == "__main__":
    main()
