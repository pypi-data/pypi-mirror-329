"""
Sudoblark Core Python library

This is a core library, written in Python, to provide a good, known, fully unit tested
working class library to assist Sudoblark in code writing activities.

Public interfaces are exported for interaction with various RESTAPIs.

Full documentation is available online here: TODO

It is also packaged, and included, with every GitHub release.
"""

from .github.client import (  # noqa: F401 # Imported but not used for readability reasons
    Client as GitHubClient,
)
