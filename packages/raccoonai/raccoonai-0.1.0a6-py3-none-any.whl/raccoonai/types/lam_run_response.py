# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["LamRunResponse"]


class LamRunResponse(BaseModel):
    livestream_url: str
    """The Livestream URL"""

    message: str
    """A message providing the thought summary if the status is processing currently."""

    properties: object
    """Additional metadata or details related to the run task."""

    task_status: str
    """The current status of the extraction task.

    For example: 'STARTING', 'PROCESSING', 'DONE', 'HUMAN_INTERACTION', or
    'FAILURE'.
    """
