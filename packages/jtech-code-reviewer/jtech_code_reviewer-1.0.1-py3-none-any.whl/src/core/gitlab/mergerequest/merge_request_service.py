from gitlab import Gitlab
from gitlab.v4.objects import Project, MergeRequest

from src.core.exceptions.mergerequest_bad_request_exception import MergeRequestBadRequestException
from src.core.exceptions.mergerequest_not_found_exception import MergeRequestNotFoundException
from src.infra.config.constants import Constants
from src.infra.config.logging_config import get_logger

LOGGER = get_logger()


class MergeRequestService:
    """
    Service class for managing merge requests.

    Attributes:
        gitlab_client (Gitlab): The Gitlab client instance
    """

    def __init__(self, gitlab_client: Gitlab) -> None:
        self.gitlab_client = gitlab_client

    def get_merge_requests(self, project: Project, state: str = 'opened') -> list:
        """
        Returns a list of merge requests for the given project.

        Args:
            project (Project): The project instance
            state (str): The state of the merge requests to fetch. Default is 'opened'.

        Returns:
            list: A list of merge requests for the project

        Raises:
            MergeRequestNotFoundException: If an error occurs while fetching the merge requests.
        """
        try:
            LOGGER.debug(f">>> Getting merge requests for project '{project.name}' with state '{state}'")
            full_project = self.gitlab_client.projects.get(project.id)
            merge_requests = full_project.mergerequests.list(state=state, order_by='updated_at', get_all=True)
            return merge_requests
        except Exception as e:
            LOGGER.error(f"::: Error getting merge requests for project {project.name}: {str(e)}")
            raise MergeRequestNotFoundException(f"Error getting merge requests for project {project.name}: {str(e)}")

    def get_merge_request_by_id(self, project_id: int, merge_request_id: int):
        """
        Returns a merge request by its ID.

        Args:
            project_id (int): The ID of the project
            merge_request_id (int): The ID of the merge request

        Returns:
            MergeRequest: The merge request instance

        Raises:
            MergeRequestNotFoundException: If an error occurs while fetching the merge request.
        """
        try:
            LOGGER.debug(f">>> Getting merge request {merge_request_id} for project {project_id}")
            project_full = self.gitlab_client.projects.get(project_id)
            merge_request = project_full.mergerequests.get(merge_request_id)
            return merge_request
        except Exception as e:
            LOGGER.error(f"::: Error getting merge request for project {project_id}: {str(e)}")
            raise MergeRequestNotFoundException(f"Error getting merge request for project {project_id}: {str(e)}")

    def get_merge_request_diffs(self, merge_request: MergeRequest) -> list:
        """
        Returns diffs for a given merge request as a list.

        Args:
            merge_request (MergeRequest): The merge request instance

        Returns:
            list: A list of diffs for the merge request

        Raises:
            MergeRequestBadRequestException: If an error occurs while fetching the diffs.
        """
        try:
            LOGGER.debug(f">>> Getting diffs for merge request {merge_request.title}")
            changes = merge_request.changes().get('changes', [])

            filtered_changes = [
                change for change in changes
                if not any(change.get("new_path", "").endswith(ext) or change.get("old_path", "").endswith(ext)
                           for ext in Constants.IGNORED_FILE_EXTENSIONS)
            ]

            LOGGER.debug(f"Filtered changes: {len(filtered_changes)} files remaining")
            return filtered_changes
        except Exception as e:
            LOGGER.error(f"::: Error fetching diffs for merge request {merge_request.title}: {str(e)}")
            raise MergeRequestBadRequestException(f"Error fetching diffs for merge request {merge_request.title}: {str(e)}")

    def add_comment_to_merge_request(self, merge_request: MergeRequest, comment: str) -> None:
        """
        Adds a comment to the merge request.

        Args:
            merge_request (MergeRequest): The merge request instance
            comment (str): The comment text to add

        Raises:
            MergeRequestBadRequestException: If an error occurs while adding the comment.
        """
        try:
            merge_request.notes.create({'body': comment})
            LOGGER.debug(f"<<< Comment added to merge request {merge_request.id}")
        except Exception as e:
            LOGGER.error(f"Error adding comment to merge request {merge_request.id}: {str(e)}")
            raise MergeRequestBadRequestException(f"Error adding comment to merge request {merge_request.id}: {str(e)}")
