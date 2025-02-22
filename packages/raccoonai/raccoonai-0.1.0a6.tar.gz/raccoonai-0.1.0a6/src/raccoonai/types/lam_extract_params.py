# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["LamExtractParamsBase", "Advanced", "LamExtractParamsNonStreaming", "LamExtractParamsStreaming"]


class LamExtractParamsBase(TypedDict, total=False):
    query: Required[str]
    """The input query string for the request. This is typically the main prompt."""

    raccoon_passcode: Required[str]
    """
    The raccoon passcode associated with the end user on behalf of which the call is
    being made.
    """

    advanced: Optional[Advanced]
    """
    Advanced configuration options for the session, such as ad-blocking and CAPTCHA
    solving.
    """

    app_url: Optional[str]
    """This is the entrypoint URL for the web agent."""

    chat_history: Optional[Iterable[object]]
    """
    The history of the conversation as a list of messages or objects you might use
    while building a chat app to give the model context of the past conversation.
    """

    max_count: Optional[int]
    """The maximum number of results to extract."""

    schema: object
    """The expected schema for the response.

    This is a dictionary where the keys describe the fields and the values describe
    their purposes.
    """


class Advanced(TypedDict, total=False):
    block_ads: Optional[bool]
    """Whether to block advertisements during the browser session."""

    proxy: Optional[bool]
    """Whether to use a proxy for the browser session."""

    solve_captchas: Optional[bool]
    """Whether to attempt automatic CAPTCHA solving."""


class LamExtractParamsNonStreaming(LamExtractParamsBase, total=False):
    stream: Optional[Literal[False]]
    """Whether the response should be streamed back or not."""


class LamExtractParamsStreaming(LamExtractParamsBase):
    stream: Required[Literal[True]]
    """Whether the response should be streamed back or not."""


LamExtractParams = Union[LamExtractParamsNonStreaming, LamExtractParamsStreaming]
