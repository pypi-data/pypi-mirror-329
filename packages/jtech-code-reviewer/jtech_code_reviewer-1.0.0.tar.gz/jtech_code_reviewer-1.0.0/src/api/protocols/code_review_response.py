from typing import Optional

from gitlab.v4.objects import MergeRequest
from pydantic import BaseModel

from src.infra.config.settings import Config


class CodeReviewResponse(BaseModel):
    """
    Represents a code review response.
    """
    author: Optional[str]
    project_id: Optional[int]
    iid: Optional[int]
    title: Optional[str]
    description: Optional[str]
    state: Optional[str]
    created_at: Optional[str]
    message: Optional[str]

    def to_dict(self):
        """
        Converts the CodeReviewResponse instance to a dictionary.

        Returns:
            dict: A dictionary representation of the CodeReviewResponse instance.
        """
        return {
            "author": self.author,
            "project_id": self.project_id,
            "iid": self.iid,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "created_at": self.created_at,
            "message": self.message
        }

    @classmethod
    def from_dict(cls, data):
        """
        Creates a CodeReviewResponse instance from a dictionary.

        Args:
            data (dict): A dictionary containing the code review response data.

        Returns:
            CodeReviewResponse: A CodeReviewResponse instance created from the dictionary.
        """
        return cls(
            author=data["author"],
            project_id=data["project_id"],
            iid=data["iid"],
            title=data["title"],
            description=data["description"],
            state=data["state"],
            created_at=data["created_at"],
            message=data["message"]
        )

    def to_json(self):
        """
        Converts the CodeReviewResponse instance to a JSON-serializable dictionary.

        Returns:
            dict: A JSON-serializable dictionary representation of the CodeReviewResponse instance.
        """
        return {
            "author": self.author,
            "project_id": self.project_id,
            "iid": self.iid,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "created_at": self.created_at,
            "message": self.message
        }

    @classmethod
    def from_json(cls, data):
        """
        Creates a CodeReviewResponse instance from a JSON-serializable dictionary.

        Args:
            data (dict): A JSON-serializable dictionary containing the code review response data.

        Returns:
            CodeReviewResponse: A CodeReviewResponse instance created from the dictionary.
        """
        return cls(
            author=data["author"],
            project_id=data["project_id"],
            iid=data["iid"],
            title=data["title"],
            description=data["description"],
            state=data["state"],
            created_at=data["created_at"],
            message=data["message"]
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return (
            f"CodeReviewResponse(project_id={self.project_id}, iid={self.iid}, title={self.title}, description={self.description}, state={self.state}, created_at={self.created_at}"
            f", message={self.message}, author={self.author}), "
        )

    def __str__(self):
        return (
            f"CodeReviewResponse(project_id={self.project_id}, iid={self.iid}, title={self.title}, description={self.description}, state={self.state}, created_at={self.created_at}"
            f", message={self.message}, author={self.author})")

    @staticmethod
    def of(project_id: int, iid: int, mr: MergeRequest):
        """
        Generates a code review response.

        Args:
            project_id (int): The ID of the project.
            iid (int): The IID of the merge request.
            mr (MergeRequest): The merge request instance.

        Returns:
            CodeReviewResponse: The code review response.
        """
        return CodeReviewResponse(
            author=mr.author["name"],
            project_id=project_id,
            iid=iid,
            title=mr.title,
            description=f"Code review completed for merge request '{mr.iid}'",
            state="success",
            created_at=mr.created_at,
            message=f"Code review completed successfully: {mr.title} - {mr.author['name']} - {mr.web_url}"
        )

    @staticmethod
    def no_changes(project_id: int, iid: int, mr: MergeRequest):
        """
        Generates a code review response when no changes are found.

        Args:
            project_id (int): The ID of the project.
            iid (int): The IID of the merge request.
            mr (MergeRequest): The merge request instance.

        Returns:
            CodeReviewResponse: The code review response.
        """
        return CodeReviewResponse(
            project_id=project_id,
            iid=iid,
            title=mr.title,
            description=f"No diffs found for merge request '{mr.iid}'",
            state="no_changes",
            created_at=mr.created_at,
            message=f"No code changes to review for merge request: {mr.title} - {mr.author['name']} - {mr.web_url}",
            author=mr.author
        )

    @staticmethod
    def max_reviews(project_id: int, iid: int, mr: MergeRequest):
        """
        Generates a code review response when the maximum number of reviews is reached.

        Args:
            project_id (int): The ID of the project.
            iid (int): The IID of the merge request.
            mr (MergeRequest): The merge request instance.

        Returns:
            CodeReviewResponse: The code review response.
        """
        return CodeReviewResponse(
            project_id=project_id,
            iid=iid,
            title=mr.title,
            description=f"The maximum number of code reviews ({Config.MAX_CODE_REVIEWS}) has been reached.",
            state="max_reviews_reached",
            created_at=mr.created_at,
            message=f"No further code reviews will be performed for merge request: {mr.title} - {mr.author['name']} - {mr.web_url}",
            author=mr.author['name']
        )

    @staticmethod
    def error(project_id: int, iid: int, e: Exception):
        """
        Generates a code review response when an error occurs.

        Args:
            project_id (int): The ID of the project.
            iid (int): The IID of the merge request.
            e (Exception): The exception that occurred.

        Returns:
            CodeReviewResponse: The code review response.
        """
        return CodeReviewResponse(
            project_id=project_id,
            iid=iid,
            title="Error",
            description="An error occurred while performing the code review",
            state="error",
            created_at=None,
            message=str(e),
            author=None
        )
