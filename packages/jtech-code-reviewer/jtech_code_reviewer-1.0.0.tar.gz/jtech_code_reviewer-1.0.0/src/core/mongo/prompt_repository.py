from pymongo import MongoClient

from src.core.exceptions.prompt_not_found_exception import PromptNotFoundException
from src.infra.config.logging_config import get_logger

LOGGER = get_logger()


class PromptRepository:
    def __init__(self, mongodb_host: str, mongodb_port: int, db_name: str, collection_name: str) -> None:
        self.client = MongoClient(mongodb_host, mongodb_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_prompt(self, prompt: str) -> None:
        """
        Saves the prompt to MongoDB.

        Args:
            prompt (str): The prompt to save.
        """
        try:
            self.collection.insert_one({"prompt": prompt})
            LOGGER.debug(f"<<< Prompt saved successfully: {prompt}")
        except Exception as e:
            LOGGER.error(f"::: Error saving prompt: {str(e)} :::")

    def get_prompt(self) -> str:
        """
        Retrieves a prompt from MongoDB.

        Returns:
            str: The prompt.
        """
        try:
            prompt = self.collection.find_one()
            LOGGER.debug(f"<<< Prompt retrieved successfully: {prompt['prompt']}")
            return prompt["prompt"]
        except Exception as e:
            LOGGER.error(f"::: Error retrieving prompt: {str(e)} :::")
            raise PromptNotFoundException("Prompt not found")
