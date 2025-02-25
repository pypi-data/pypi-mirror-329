from dataclasses import dataclass
from requests import Session
from requests import Response
import json

from sudoblark_python_core.github import pull_request


@dataclass
class Comment:
    """This class represents a comment on either an Issue or a PullRequest.

    It may be used to perform actions within the context of the comment.

    Attributes:
        identifier (int): Unique identifier of the organisation within GitHub
        client (requests.Session): Session used to make requests to the RESTAPI, intended
                          to be passed in when instance is created via Client
        base_url (str): Base URL we should use for querying the RESTAPI within the context of the comment
        parent_identifier (str): Identifier of the PullRequest/Issue which this comment relates to
        repository_name (str): Name of the repository this comment relates to
        pull_request (bool): If this comment is associated with a pull request
        issue (bool): If this comment is associated with an issue
        body (str): The body of the comment
    """

    identifier: int
    client: Session
    base_url: str
    parent_identifier: int
    repository_name: str
    pull_request: bool
    issue: bool
    body: str
    author: str

    def update(self, body: str) -> bool:
        """
        Args:
            body (str): Additional content to append to the existing comment body.

        Returns:
            True if appended, else False.
        """
        updated: bool = False

        github_restapi_request: Response = self.client.patch(
            url=self.base_url,
            data=json.dumps({"body": self.body + body}),
        )
        if github_restapi_request.status_code == 201:
            response_data: dict = github_restapi_request.json()
            self.body = response_data["body"]
            self.author = response_data["user"]["login"]
            updated = True
        return updated

    def overwrite(self, body: str) -> bool:
        """
        Args:
            body (str): Content to overwrite the existing comment body with.

        Returns:
            True if overwritten, else False.
        """
        updated: bool = False

        github_restapi_request: Response = self.client.patch(
            url=self.base_url,
            data=json.dumps({"body": body}),
        )
        if github_restapi_request.status_code == 200:
            response_data: dict = github_restapi_request.json()
            self.body = response_data["body"]
            self.author = response_data["user"]["login"]
            updated = True
        return updated

    def delete(self) -> bool:
        """
        Returns:
            True if deleted, else False.
        """
        deleted: bool = False

        github_restapi_request: Response = self.client.delete(url=self.base_url)
        if github_restapi_request.status_code == 204:
            deleted = True
        return deleted

    def __str__(self) -> str:
        """
        Returns:
            Information string representation
        """
        parent_type = "Pull Request" if pull_request else "Issue"
        return f"Comment ID: {self.identifier}, For: {parent_type} {self.parent_identifier}, On: {self.repository_name}"

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
