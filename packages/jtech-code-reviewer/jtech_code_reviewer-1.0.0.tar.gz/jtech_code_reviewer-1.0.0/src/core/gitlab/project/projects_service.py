from typing import List

import gitlab
from gitlab.v4.objects import Group, Project


class ProjectService:
    """
    Service class for managing projects.

    Attributes:
        gitlab_client (gitlab.Gitlab): The Gitlab client instance.
    """

    def __init__(self, gitlab_client: gitlab.Gitlab) -> None:
        self.gitlab_client = gitlab_client

    def get_projects(self, search: str) -> List[Project]:
        """
        Returns a list of projects for the given search query.

        Args:
            search (str): The search query to filter projects by.

        Returns:
            list: A list of projects matching the search query.
        """
        return self.gitlab_client.projects.list(search=search, get_all=True)

    def get_projects_by_group(self, group: Group) -> list:
        """
        Returns a list of projects for the given group.

        Args:
            group (Group): The group instance.

        Returns:
            list: A list of projects for the given group.
        """
        return group.projects.list(all=True)

    def get_project_by_id(self, project_id: int) -> Project:
        """
        Returns a project by its ID.

        Args:
            project_id (int): The ID of the project.

        Returns:
            Project: The project instance.
        """
        return self.gitlab_client.projects.get(project_id)
