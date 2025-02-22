# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["LamIntegrationRunResponse", "UnionMember0", "IntegrationResponse"]


class UnionMember0(BaseModel):
    integration_id: str
    """A unique identifier for the integration in use."""

    livestream_url: str
    """The Livestream URL"""

    message: str
    """A message providing the thought summary if the status is processing currently."""

    properties: object
    """Additional metadata or details related to the integration task."""

    task_status: str
    """The current status of the extraction task.

    For example: 'STARTING', 'PROCESSING', 'DONE', 'HUMAN_INTERACTION', or
    'FAILURE'.
    """


class IntegrationResponse(BaseModel):
    integration_id: str
    """A unique identifier for the integration in use."""

    livestream_url: str
    """The Livestream URL"""

    message: str
    """A message providing the thought summary if the status is processing currently."""

    properties: object
    """Additional metadata or details related to the integration task."""

    task_status: str
    """The current status of the extraction task.

    For example: 'STARTING', 'PROCESSING', 'DONE', 'HUMAN_INTERACTION', or
    'FAILURE'.
    """


LamIntegrationRunResponse: TypeAlias = Union[List[UnionMember0], IntegrationResponse]
