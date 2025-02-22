# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from raccoonai import RaccoonAI, AsyncRaccoonAI
from tests.utils import assert_matches_type
from raccoonai.types import (
    LamRunResponse,
    LamExtractResponse,
    LamIntegrationRunResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLam:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_extract_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    def test_method_extract_with_all_params_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.ycombinator.com/companies",
            chat_history=[{}],
            max_count=5,
            schema={
                "address": {
                    "city": "What city is the company located in?",
                    "country": "Which country is the company located in?",
                },
                "funding_season": "The funding season like W24 as a string",
                "name": "Name of the company as a string",
            },
            stream=False,
        )
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    def test_raw_response_extract_overload_1(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = response.parse()
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    def test_streaming_response_extract_overload_1(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = response.parse()
            assert_matches_type(LamExtractResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_extract_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )
        lam_stream.response.close()

    @parametrize
    def test_method_extract_with_all_params_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.ycombinator.com/companies",
            chat_history=[{}],
            max_count=5,
            schema={
                "address": {
                    "city": "What city is the company located in?",
                    "country": "Which country is the company located in?",
                },
                "funding_season": "The funding season like W24 as a string",
                "name": "Name of the company as a string",
            },
        )
        lam_stream.response.close()

    @parametrize
    def test_raw_response_extract_overload_2(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_extract_overload_2(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_integration_run_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        )
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    def test_method_integration_run_with_all_params_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            integration_id="integration_id",
            properties={},
            stream=False,
        )
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    def test_raw_response_integration_run_overload_1(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = response.parse()
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    def test_streaming_response_integration_run_overload_1(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = response.parse()
            assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_integration_run_overload_1(self, client: RaccoonAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_name` but received ''"):
            client.lam.with_raw_response.integration_run(
                app_name="",
                raccoon_passcode="raccoon_passcode",
            )

    @parametrize
    def test_method_integration_run_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        )
        lam_stream.response.close()

    @parametrize
    def test_method_integration_run_with_all_params_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            integration_id="integration_id",
            properties={},
        )
        lam_stream.response.close()

    @parametrize
    def test_raw_response_integration_run_overload_2(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_integration_run_overload_2(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_integration_run_overload_2(self, client: RaccoonAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_name` but received ''"):
            client.lam.with_raw_response.integration_run(
                app_name="",
                raccoon_passcode="raccoon_passcode",
                stream=True,
            )

    @parametrize
    def test_method_run_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    def test_method_run_with_all_params_overload_1(self, client: RaccoonAI) -> None:
        lam = client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.amazon.com",
            chat_history=[{}],
            stream=False,
        )
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    def test_raw_response_run_overload_1(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = response.parse()
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    def test_streaming_response_run_overload_1(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = response.parse()
            assert_matches_type(LamRunResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_run_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )
        lam_stream.response.close()

    @parametrize
    def test_method_run_with_all_params_overload_2(self, client: RaccoonAI) -> None:
        lam_stream = client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.amazon.com",
            chat_history=[{}],
        )
        lam_stream.response.close()

    @parametrize
    def test_raw_response_run_overload_2(self, client: RaccoonAI) -> None:
        response = client.lam.with_raw_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_run_overload_2(self, client: RaccoonAI) -> None:
        with client.lam.with_streaming_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True


class TestAsyncLam:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_extract_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    async def test_method_extract_with_all_params_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.ycombinator.com/companies",
            chat_history=[{}],
            max_count=5,
            schema={
                "address": {
                    "city": "What city is the company located in?",
                    "country": "Which country is the company located in?",
                },
                "funding_season": "The funding season like W24 as a string",
                "name": "Name of the company as a string",
            },
            stream=False,
        )
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    async def test_raw_response_extract_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = await response.parse()
        assert_matches_type(LamExtractResponse, lam, path=["response"])

    @parametrize
    async def test_streaming_response_extract_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = await response.parse()
            assert_matches_type(LamExtractResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_extract_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_method_extract_with_all_params_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.ycombinator.com/companies",
            chat_history=[{}],
            max_count=5,
            schema={
                "address": {
                    "city": "What city is the company located in?",
                    "country": "Which country is the company located in?",
                },
                "funding_season": "The funding season like W24 as a string",
                "name": "Name of the company as a string",
            },
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_raw_response_extract_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_extract_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.extract(
            query="Find YCombinator startups who got funded in W24.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_integration_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        )
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    async def test_method_integration_run_with_all_params_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            integration_id="integration_id",
            properties={},
            stream=False,
        )
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    async def test_raw_response_integration_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = await response.parse()
        assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

    @parametrize
    async def test_streaming_response_integration_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = await response.parse()
            assert_matches_type(LamIntegrationRunResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_integration_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_name` but received ''"):
            await async_client.lam.with_raw_response.integration_run(
                app_name="",
                raccoon_passcode="raccoon_passcode",
            )

    @parametrize
    async def test_method_integration_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_method_integration_run_with_all_params_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            integration_id="integration_id",
            properties={},
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_raw_response_integration_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_integration_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.integration_run(
            app_name="app_name",
            raccoon_passcode="raccoon_passcode",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_integration_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `app_name` but received ''"):
            await async_client.lam.with_raw_response.integration_run(
                app_name="",
                raccoon_passcode="raccoon_passcode",
                stream=True,
            )

    @parametrize
    async def test_method_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    async def test_method_run_with_all_params_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        lam = await async_client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.amazon.com",
            chat_history=[{}],
            stream=False,
        )
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    async def test_raw_response_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lam = await response.parse()
        assert_matches_type(LamRunResponse, lam, path=["response"])

    @parametrize
    async def test_streaming_response_run_overload_1(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lam = await response.parse()
            assert_matches_type(LamRunResponse, lam, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_method_run_with_all_params_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        lam_stream = await async_client.lam.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
            advanced={
                "block_ads": True,
                "proxy": True,
                "solve_captchas": True,
            },
            app_url="https://www.amazon.com",
            chat_history=[{}],
        )
        await lam_stream.response.aclose()

    @parametrize
    async def test_raw_response_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        response = await async_client.lam.with_raw_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_run_overload_2(self, async_client: AsyncRaccoonAI) -> None:
        async with async_client.lam.with_streaming_response.run(
            query="Find the price of iphone 16 on Amazon.",
            raccoon_passcode="<end-user-raccoon-passcode>",
            stream=True,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True
