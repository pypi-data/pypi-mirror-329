from dataclasses import dataclass
from requests import Session
from requests import Response
from sudoblark_python_core.github.pull_request import PullRequest
from sudoblark_python_core.github.pull_request import PullRequestState
from typing import List
from typing import Union


@dataclass
class Repository:
    """This class represents aa Repository within GitHub.

    It may be used to perform actions within the context of the Repository.

    Attributes:
        identifier (int): Unique identifier of the Repository
        client (requests.Session): Session used to make requests to the RESTAPI, intended
                          to be passed in when instance is created via Client/Organisation
        base_url (str): Base URL we should use for querying the RESTAPI within the context of the Repository
        full_name (str): Full name of the Repository, in the form of owner/repository
        private (bool): True if the Repository is private, else False
    """

    identifier: int
    client: Session
    base_url: str
    full_name: str
    private: bool

    def get_pull_requests(self, state: PullRequestState = "open") -> List[PullRequest]:
        """
        Examples:
            ```python
            get_pull_requests()
            ```

        Args:
            state: Filter PullRequest instances to be of this state

        Returns:
            All PullRequests for the Repository, empty if none found \
            or instance otherwise doesn't have access to, or fails to query, the RESTAPI.
        """
        pull_requests: List[PullRequest] = []
        github_restapi_request: Response = self.client.get(
            url=f"{self.base_url}/pulls",
            params={"state": state},
        )
        if github_restapi_request.status_code == 200:
            response_data = github_restapi_request.json()
            for pull_request in response_data:
                pull_requests.append(
                    PullRequest(
                        identifier=pull_request["id"],
                        number=pull_request["number"],
                        client=self.client,
                        base_url=pull_request["url"],
                        title=pull_request["title"],
                        repo=self.full_name,
                        state=pull_request["state"],
                    )
                )
        return pull_requests

    def get_pull_request(self, identifier: int) -> Union[PullRequest, None]:
        """
        Args:
            identifier: The ID of the pull request we are querying for

        Examples:
            ```python
            get_pull_request(22)
            ```

        Returns:
            PullRequest instance if found, else None
        """
        pull_request: Union[None, PullRequest] = None

        github_restapi_request: Response = self.client.get(url=f"{self.base_url}/pulls/{identifier}")
        if github_restapi_request.status_code == 200:
            response_data: dict = github_restapi_request.json()
            pull_request = PullRequest(
                identifier=response_data["id"],
                number=response_data["number"],
                client=self.client,
                base_url=response_data["url"],
                title=response_data["title"],
                repo=self.full_name,
                state=response_data["state"],
            )
        return pull_request

    def __str__(self) -> str:
        """
        Returns:
            Information string representation
        """
        return self.full_name

    def __hash__(self) -> int:
        """
        Returns:
            Unique int representation of instance.
        """
        return hash(self.identifier)

    def __eq__(self, other: object) -> bool:
        """
        Args:
            other: Object to compare against

        Returns:
            True if instances are equal, False otherwise.
        """
        if not isinstance(other, type(self)):
            return False
        return self.identifier == other.identifier
