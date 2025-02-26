from typing import List

import gitlab
from gitlab.v4.objects import Group


class GroupService:
    """
    Service class for managing groups.

    Attributes:
        gitlab_client (gitlab.Gitlab): The Gitlab client instance.
    """

    def __init__(self, gitlab_client: gitlab.Gitlab) -> None:
        self.gitlab_client = gitlab_client

    def get_groups(self, search: str) -> List[Group]:
        """
        Returns a list of groups for the given search query.

        Args:
            search (str): The search query to filter groups by.

        Returns:
            list: A list of groups matching the search query.
        """
        return self.gitlab_client.groups.list(search=search, get_all=True)

    def get_group_by_id(self, group_id: int) -> Group:
        """
        Returns a group by its ID.

        Args:
            group_id (int): The ID of the group.

        Returns:
            Group: The group instance.
        """
        return self.gitlab_client.groups.get(group_id)
