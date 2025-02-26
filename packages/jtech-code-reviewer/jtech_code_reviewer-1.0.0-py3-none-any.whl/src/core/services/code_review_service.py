from src.api.protocols.code_review_response import CodeReviewResponse
from src.core.agents.code_review_agent import CodeReviewAgent
from src.core.exceptions.mergerequest_not_found_exception import MergeRequestNotFoundException
from src.core.gitlab.mergerequest.merge_request_service import MergeRequestService
from src.core.mongo.review_repository import ReviewRepository
from src.infra.config.logging_config import get_logger
from src.infra.config.settings import Config
from src.infra.utils.extract import Extract

LOGGER = get_logger()


class CodeReviewService:
    """
    A service class to perform code reviews on merge requests.
    """

    def __init__(self, merge_request_service: MergeRequestService,
                 review_repository: ReviewRepository,
                 code_review_agent: CodeReviewAgent):
        self.merge_request_service = merge_request_service
        self.repository_service = review_repository
        self.code_review_agent = code_review_agent

    def code_review(self, project_id, iid) -> CodeReviewResponse:
        """
        Perform a code review on a given merge request.

        Args:
            project_id (int): The ID of the project.
            iid (int): The ID of the merge request.

        Returns:
            CodeReviewResponse: An object containing the results of the code review.

        Raises:
            MergeRequestNotFoundException: If the merge request is not found.
        """
        try:
            current_review_count = self.repository_service.get_review_count(project_id, iid)
            if current_review_count > Config.MAX_CODE_REVIEWS:
                LOGGER.debug(f"::: Maximum number of code reviews reached for merge request '{iid}' :::")

                mr = self.merge_request_service.get_merge_request_by_id(project_id, iid)
                if not mr:
                    raise MergeRequestNotFoundException(f"::: Merge request '{iid}' not found :::")

                return CodeReviewResponse.max_reviews(project_id, iid, mr)

            mr = self.merge_request_service.get_merge_request_by_id(project_id, iid)
            if not mr:
                raise MergeRequestNotFoundException(f"::: Merge request '{iid}' not found :::")

            LOGGER.debug(f">>> Performing code review on merge request '{mr.iid}'")
            diffs = self.merge_request_service.get_merge_request_diffs(mr)

            if not diffs:
                LOGGER.debug(f"::: No diffs found for merge request '{mr.iid}' :::")
                return CodeReviewResponse.no_changes(project_id, iid, mr)
            
            diffs = [diff for diff in diffs if diff.get("new_path", "").endswith(".java")]

            for diff in diffs:
                response = self.code_review_agent.review_code(diff)

                comment_text = Extract.extract_review_content(response)
                review_data = {
                    "file": diff,
                    "review": comment_text
                }
                self.repository_service.save_review(project_id, iid, review_data)
                self.merge_request_service.add_comment_to_merge_request(mr, comment_text)

            self.repository_service.increment_review_count(project_id, iid)

            LOGGER.debug(f"<<< Code review completed for merge request '{mr.iid}'")
            return CodeReviewResponse.of(project_id, iid, mr)

        except MergeRequestNotFoundException as e:
            LOGGER.error(str(e))
            raise e

        except Exception as e:
            LOGGER.error(f"::: An error occurred during the code review process: {str(e)} :::")
            return CodeReviewResponse.error(project_id, iid, e)
