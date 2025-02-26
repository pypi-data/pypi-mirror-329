from src.core.agents.code_review_agent import CodeReviewAgent
from src.core.generativeai.generative_ia_client import GenerativeAIClient
from src.core.gitlab.mergerequest.merge_request_service import MergeRequestService
from src.core.mongo.prompt_repository import PromptRepository
from src.core.mongo.review_repository import ReviewRepository
from src.core.services.code_review_service import CodeReviewService
from src.infra.config.constants import Constants
from src.infra.config.logging_config import get_logger
from src.infra.config.settings import Config
from src.infra.gitlab.gitlab_config import GitLabConfig

LOGGER = get_logger()


class DependencyContainer:
    """
    Dependency container class for managing instances of services and repositories.

    Attributes:
        _instances (dict): The dictionary of instances.
    """
    _instances = {}

    @classmethod
    def get_prompt_repository(cls) -> PromptRepository:
        """
        Returns the PromptRepository instance.

        Returns:
            PromptRepository: The PromptRepository instance.
        """
        if "prompt_repository" not in cls._instances:
            LOGGER.debug(">>> Creating PromptRepository instance")
            cls._instances["prompt_repository"] = PromptRepository(
                mongodb_host=Config.MONGODB_HOST,
                mongodb_port=Config.MONGODB_PORT,
                db_name=Config.MONGODB_DB_NAME,
                collection_name=Config.MONGODB_COLLECTION_PROMPT
            )
        return cls._instances["prompt_repository"]

    @classmethod
    def get_review_repository(cls) -> ReviewRepository:
        """
        Returns the ReviewRepository instance.

        Returns:
            ReviewRepository: The ReviewRepository instance.
        """
        if "review_repository" not in cls._instances:
            LOGGER.debug(">>> Creating ReviewRepository instance")
            cls._instances["review_repository"] = ReviewRepository(
                mongodb_host=Config.MONGODB_HOST,
                mongodb_port=Config.MONGODB_PORT,
                db_name=Config.MONGODB_DB_NAME,
                collection_name=Config.MONGODB_COLLECTION_NAME
            )
        return cls._instances["review_repository"]

    @classmethod
    def get_gitlab_config(cls) -> GitLabConfig:
        """
        Returns the GitLabConfig instance.

        Returns:
            GitLabConfig: The GitLabConfig instance.
        """
        if "gitlab_config" not in cls._instances:
            LOGGER.debug(">>> Creating GitLabConfig instance")
            cls._instances["gitlab_config"] = GitLabConfig(Config.GITLAB_URL, Config.GITLAB_TOKEN)
        return cls._instances["gitlab_config"]

    @classmethod
    def get_merge_request_service(cls) -> MergeRequestService:
        """
        Returns the MergeRequestService instance.

        Returns:
            MergeRequestService: The MergeRequestService instance.
        """
        if "merge_request_service" not in cls._instances:
            LOGGER.debug(">>> Creating MergeRequestService instance")
            gitlab_client = cls.get_gitlab_config().get_client()
            cls._instances["merge_request_service"] = MergeRequestService(gitlab_client)
        return cls._instances["merge_request_service"]

    @classmethod
    def get_generative_ai_client(cls) -> GenerativeAIClient:
        """
        Returns the GenerativeAIClient instance.

        Returns:
            GenerativeAIClient: The GenerativeAIClient instance
        """
        if "generative_ai_client" not in cls._instances:
            LOGGER.debug(">>> Creating GenerativeAIClient instance")
            cls._instances["generative_ai_client"] = GenerativeAIClient()
        return cls._instances["generative_ai_client"]

    @classmethod
    def get_code_review_agent(cls) -> CodeReviewAgent:
        """
        Returns the CodeReviewAgent instance.

        Returns:
            CodeReviewAgent: The CodeReviewAgent instance.
        """
        if "code_review_agent" not in cls._instances:
            LOGGER.debug(">>> Creating CodeReviewAgent instance")
            generative_ai_client = cls.get_generative_ai_client()
            cls._instances["code_review_agent"] = CodeReviewAgent(
                manifest_path=Constants.MANIFESTO_PATH,
                ai_client=generative_ai_client,
                prompt_repository=cls.get_prompt_repository()
            )
        return cls._instances["code_review_agent"]

    @classmethod
    def get_code_review_service(cls):
        """
        Returns the CodeReviewService instance.

        Returns:
            CodeReviewService: The CodeReviewService instance.
        """
        if "code_review_service" not in cls._instances:
            LOGGER.debug(">>> Creating CodeReviewService instance")
            cls._instances["code_review_service"] = CodeReviewService(
                merge_request_service=cls.get_merge_request_service(),
                review_repository=cls.get_review_repository(),
                code_review_agent=cls.get_code_review_agent()
            )
        return cls._instances["code_review_service"]
