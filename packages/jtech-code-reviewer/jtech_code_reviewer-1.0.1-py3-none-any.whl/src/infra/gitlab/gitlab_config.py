import gitlab


class GitLabConfig:
    """
    Configuration class for GitLab.

    Attributes:
        base_url (str): The base URL of the GitLab instance.
        token (str): The private token for the GitLab instance.
        _gitlab_instance (gitlab.Gitlab): The Gitlab client instance.
    """

    def __init__(self, base_url: str, token: str) -> None:
        self.base_url = base_url
        self.token = token
        self._gitlab_instance = None

    def connect(self) -> gitlab.Gitlab:
        """
        Connects to the GitLab instance.

        Returns:
            gitlab.Gitlab: The Gitlab client instance.
        """
        if not self._gitlab_instance:
            self._gitlab_instance = gitlab.Gitlab(self.base_url, private_token=self.token)
            self._gitlab_instance.auth()
        return self._gitlab_instance

    def get_client(self) -> gitlab.Gitlab:
        """
        Returns the Gitlab client instance.

        Returns:
            gitlab.Gitlab: The Gitlab client instance.
        """
        if self._gitlab_instance is None:
            self.connect()
        return self._gitlab_instance
