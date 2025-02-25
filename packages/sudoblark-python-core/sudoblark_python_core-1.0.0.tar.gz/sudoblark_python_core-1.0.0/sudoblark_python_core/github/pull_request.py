import enum
from dataclasses import dataclass
from requests import Session
from requests import Response
from sudoblark_python_core.github.comments import Comment
from typing import List
from typing import Union
import json


class PullRequestState(enum.Enum):
    """Valid pull request states.

    Attributes:
        open (str): Open pull request
        closed (str): Closed pull request
        all (str): Any pull request
    """

    open = "open"
    closed = "closed"
    all = "all"


@dataclass
class PullRequest:
    """This class represents a PullRequest on a specific repository.

    It may be used to perform actions within the context of the PullRequest.

    Attributes:
        identifier (int): Unique identifier of the PullRequest
        number (int): User friendly number of the pull request
        client (requests.Session): Session used to make requests to the RESTAPI, intended
                          to be passed in when instance is created via Repository
        base_url (str): Base URL we should use for querying the RESTAPI within the context of the PullRequest
        title (str): Title given to the PullRequest
        repo (str): Name of the Repository which the instance is associated with
        state (PullRequestState): State of the pull request
    """

    identifier: int
    number: int
    client: Session
    base_url: str
    title: str
    repo: str
    state: PullRequestState

    def __post_init__(self):
        """
        Dataclass magic method, utilised in this instance to calculate useful
        values from, and populate said values in to, state.
        """
        self.comment_url = self.base_url.replace("pulls", "issues") + "/comments"

    def get_comments(self) -> List[Comment]:
        """
        Examples:
            ```python
            get_comments()
            ```

        Returns:
            All Comments on the PullRequest, empty if none found \
            or instance otherwise doesn't have access to, or fails to query, the RESTAPI.
        """
        comments: List[Comment] = []
        github_restapi_request: Response = self.client.get(url=self.comment_url)
        if github_restapi_request.status_code == 200:
            response_data = github_restapi_request.json()
            for comment in response_data:
                comments.append(
                    Comment(
                        identifier=comment["id"],
                        client=self.client,
                        base_url=comment["url"],
                        parent_identifier=self.number,
                        repository_name=self.repo,
                        pull_request=True,
                        issue=False,
                        body=comment["body"],
                        author=comment["user"]["login"],
                    )
                )
        return comments

    def post_comment(self, body: str) -> Union[Comment, None]:
        """
        Args:
            body (str): Body of the comment to post to the PullRequest

        Returns:
            Comment instance if successfully posted, else None
        """
        comment: Union[Comment, None] = None

        github_restapi_request: Response = self.client.post(
            url=self.comment_url,
            data=json.dumps({"body": body}),
        )
        if github_restapi_request.status_code == 201:
            response_data: dict = github_restapi_request.json()
            comment = Comment(
                identifier=response_data["id"],
                client=self.client,
                base_url=response_data["url"],
                parent_identifier=self.number,
                repository_name=self.repo,
                pull_request=True,
                issue=False,
                body=response_data["body"],
                author=response_data["user"]["login"],
            )
        return comment

    def __str__(self) -> str:
        """
        Returns:
            Information string representation
        """
        return f"Repo: {self.repo} , Pull request ID: {self.number} , Title: {self.title} , State: {self.state}"

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
