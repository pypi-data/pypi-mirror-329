from langchain_core.prompts import ChatPromptTemplate

from src.core.exceptions.mergerequest_bad_request_exception import MergeRequestBadRequestException
from src.core.exceptions.prompt_not_found_exception import PromptNotFoundException
from src.infra.config.constants import Constants
from src.infra.config.logging_config import get_logger
from src.infra.utils.pdf_reader import ReadPDF
from src.infra.utils.txt_reader import ReadText

LOGGER = get_logger()


class CodeReviewAgent:
    """
    A code review agent that provides feedback on code changes based on a given manifesto.

    Args:
        manifest_path (str): The path to the manifesto PDF file.
        ai_client: The AI client to use for generating responses.
    """

    def __init__(self, manifest_path: str, ai_client, prompt_repository) -> None:
        self.manifest_text = self._load_manifest(manifest_path)
        self.ai_client = ai_client
        self.prompt_repository = prompt_repository
        self.prompt_template = self._generate_prompt_template()

    def review_code(self, diff) -> str:
        """
        Reviews the code changes and provides feedback.

        Args:
            diff (str): The code changes to review

        Returns:
            str: The feedback on the code changes
        """
        feedback = []
        try:
            response = self.ai_client.get_response(self.prompt_template, manifesto=self.manifest_text, diff=diff)
            feedback.append(f"Review:\n{response}")
        except MergeRequestBadRequestException as e:
            LOGGER.error(f"::: Error reviewing code for file {diff}: {str(e)}")
            raise MergeRequestBadRequestException(f"::: Error reviewing code for file {diff}: {str(e)}")
        return "\n".join(feedback)

    def _generate_prompt_template(self) -> ChatPromptTemplate:
        """
        Generates a chat prompt template for code review.

        Returns:
            ChatPromptTemplate: The generated chat prompt template
        """

        try:
            template = self.prompt_repository.get_prompt()
            return ChatPromptTemplate.from_template(template)
        except PromptNotFoundException as e:
            text = ReadText(Constants.PROMPT_TEMPLATE_PATH).extract_text()
            self.prompt_repository.save_prompt(text)
            template = self.prompt_repository.get_prompt()
            return ChatPromptTemplate.from_template(template)

    def _load_manifest(self, manifest_path: str) -> str:
        """
        Loads the manifesto text from the given PDF file.

        Args:
            manifest_path (str): The path to the manifesto PDF file.

        Returns:
            str: The text extracted from the manifesto PDF.
        """
        reader = ReadPDF(manifest_path)
        return reader.extract_text()
