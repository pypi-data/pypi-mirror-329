# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

__all__ = ["FleetCreateParams", "Advanced", "Settings"]


class FleetCreateParams(TypedDict, total=False):
    advanced: Optional[Advanced]
    """
    Advanced configuration options for the session, such as ad-blocking and CAPTCHA
    solving.
    """

    app_name: Optional[str]
    """
    The name of the app for which the session is going to run for, used for
    streamlining authentication.
    """

    browser_type: Optional[str]
    """The type of browser to use.

    Supported values include 'chromium', 'firefox', and 'webkit'.
    """

    headless: Optional[bool]
    """Whether to run the browser in headless mode."""

    raccoon_passcode: Optional[str]
    """
    The raccoon passcode associated with the end user on behalf of which the call is
    being made if any.
    """

    session_timeout: Optional[int]
    """The timeout for the browser session in seconds."""

    settings: Optional[Settings]
    """
    Configuration settings for the browser, such as viewport size and User-Agent
    string.
    """

    url: Optional[str]
    """The entrypoint url for the session."""


class Advanced(TypedDict, total=False):
    block_ads: Optional[bool]
    """Whether to block advertisements during the browser session."""

    proxy: Optional[bool]
    """Whether to use a proxy for the browser session."""

    solve_captchas: Optional[bool]
    """Whether to attempt automatic CAPTCHA solving."""


class Settings(TypedDict, total=False):
    locales: Optional[List[str]]
    """A list of locales or languages to use for the browser session.

    These determine language preferences.
    """

    user_agent: Optional[str]
    """The User-Agent string to use for the browser.

    Defaults to internal auto user-agent rotation mechanism.
    """

    viewport: Optional[Dict[str, int]]
    """The viewport size (screen dimensions) for the browser in pixels."""
