from dataclasses import dataclass
from requests import Session
from requests import Response
from typing import List
from typing import Union

from sudoblark_python_core.github.repository import Repository


@dataclass
class Organisation:
    """This class represents an Organisation within GitHub.

    It may be used to perform actions within the context of the organisation.

    Attributes:
        identifier (int): Unique identifier of the organisation within GitHub
        company (str): The company associated with the organisation
        repos_url (str): RESTAPI endpoint for retrieval of repos in the organisation
        client (requests.Session): Session used to make requests to the RESTAPI, intended
                          to be passed in when instance is created via Client
        base_url (str): Base URL we should use for querying the RESTAPI within the context of the organisation

    """

    identifier: int
    company: str
    repos_url: str
    client: Session
    base_url: str

    def get_repository(self, name: str) -> Union[Repository, None]:
        """
        Args:
            name: The name of the repository we are querying for

        Examples:
            ```python
            get_repository('sudoblark.python.core')
            ```

        Returns:
            Repository instance if found, else None
        """
        repository: Union[None, Repository] = None

        base_github_api_url: str = self.base_url.split("/orgs")[0]

        github_restapi_request: Response = self.client.get(url=f"{base_github_api_url}/repos/{self.company}/{name}")
        if github_restapi_request.status_code == 200:
            response_data: dict = github_restapi_request.json()
            repository = Repository(
                identifier=response_data["id"],
                client=self.client,
                base_url=response_data["url"],
                full_name=response_data["full_name"],
                private=response_data["private"],
            )
        return repository

    def get_repositories(self) -> List[Repository]:
        """
        Examples:
            ```python
            get_repositories()
            ```

        Returns:
            All repositories within the organisation, empty if none found \
            or instance otherwise doesn't have access to, or fails to query, the RESTAPI.
        """
        repositories: List[Repository] = []
        github_restapi_request: Response = self.client.get(url=f"{self.base_url}/repos")
        if github_restapi_request.status_code == 200:
            response_data: dict = github_restapi_request.json()
            for repository in response_data:
                repositories.append(
                    Repository(
                        identifier=repository["id"],
                        client=self.client,
                        base_url=repository["url"],
                        full_name=repository["full_name"],
                        private=repository["private"],
                    )
                )
        return repositories

    def __str__(self) -> str:
        """
        Returns:
            Information string representation
        """
        return self.company

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
