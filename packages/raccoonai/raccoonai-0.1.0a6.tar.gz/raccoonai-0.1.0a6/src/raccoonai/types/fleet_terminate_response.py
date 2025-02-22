# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["FleetTerminateResponse"]


class FleetTerminateResponse(BaseModel):
    session_id: str
    """A unique identifier for the session."""

    status: str
    """The current status of the session.

    Possible values include 'running', 'unknown', or 'terminated'.
    """
