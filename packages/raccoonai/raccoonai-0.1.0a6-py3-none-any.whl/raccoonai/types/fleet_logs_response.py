# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["FleetLogsResponse"]


class FleetLogsResponse(BaseModel):
    session_id: str
    """A unique identifier for the session."""

    session_logs: object
    """A dictionary containing the browser console logs for the session."""
