# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from headlessagents import HeadlessAgents, AsyncHeadlessAgents
from headlessagents.types import (
    CallAgentResponse,
    CheckHealthResponse,
    RetrieveAgentStatsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_call_agent(self, client: HeadlessAgents) -> None:
        client_ = client.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        )
        assert_matches_type(CallAgentResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_call_agent_with_all_params(self, client: HeadlessAgents) -> None:
        client_ = client.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
            conversation_id="bc8e506e4a6f49ad",
        )
        assert_matches_type(CallAgentResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_call_agent(self, client: HeadlessAgents) -> None:
        response = client.with_raw_response.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CallAgentResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_call_agent(self, client: HeadlessAgents) -> None:
        with client.with_streaming_response.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CallAgentResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_call_agent(self, client: HeadlessAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.with_raw_response.call_agent(
                agent_id="",
                request="What is the weather like in San Francisco?",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_check_health(self, client: HeadlessAgents) -> None:
        client_ = client.check_health()
        assert_matches_type(CheckHealthResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_check_health(self, client: HeadlessAgents) -> None:
        response = client.with_raw_response.check_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CheckHealthResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_check_health(self, client: HeadlessAgents) -> None:
        with client.with_streaming_response.check_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CheckHealthResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_agent_stats(self, client: HeadlessAgents) -> None:
        client_ = client.retrieve_agent_stats(
            "agent_id",
        )
        assert_matches_type(RetrieveAgentStatsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve_agent_stats(self, client: HeadlessAgents) -> None:
        response = client.with_raw_response.retrieve_agent_stats(
            "agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(RetrieveAgentStatsResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve_agent_stats(self, client: HeadlessAgents) -> None:
        with client.with_streaming_response.retrieve_agent_stats(
            "agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(RetrieveAgentStatsResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve_agent_stats(self, client: HeadlessAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            client.with_raw_response.retrieve_agent_stats(
                "",
            )


class TestAsyncClient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_call_agent(self, async_client: AsyncHeadlessAgents) -> None:
        client = await async_client.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        )
        assert_matches_type(CallAgentResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_call_agent_with_all_params(self, async_client: AsyncHeadlessAgents) -> None:
        client = await async_client.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
            conversation_id="bc8e506e4a6f49ad",
        )
        assert_matches_type(CallAgentResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_call_agent(self, async_client: AsyncHeadlessAgents) -> None:
        response = await async_client.with_raw_response.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CallAgentResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_call_agent(self, async_client: AsyncHeadlessAgents) -> None:
        async with async_client.with_streaming_response.call_agent(
            agent_id="agent_id",
            request="What is the weather like in San Francisco?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CallAgentResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_call_agent(self, async_client: AsyncHeadlessAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.with_raw_response.call_agent(
                agent_id="",
                request="What is the weather like in San Francisco?",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_check_health(self, async_client: AsyncHeadlessAgents) -> None:
        client = await async_client.check_health()
        assert_matches_type(CheckHealthResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_check_health(self, async_client: AsyncHeadlessAgents) -> None:
        response = await async_client.with_raw_response.check_health()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CheckHealthResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_check_health(self, async_client: AsyncHeadlessAgents) -> None:
        async with async_client.with_streaming_response.check_health() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CheckHealthResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_agent_stats(self, async_client: AsyncHeadlessAgents) -> None:
        client = await async_client.retrieve_agent_stats(
            "agent_id",
        )
        assert_matches_type(RetrieveAgentStatsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve_agent_stats(self, async_client: AsyncHeadlessAgents) -> None:
        response = await async_client.with_raw_response.retrieve_agent_stats(
            "agent_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(RetrieveAgentStatsResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve_agent_stats(self, async_client: AsyncHeadlessAgents) -> None:
        async with async_client.with_streaming_response.retrieve_agent_stats(
            "agent_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(RetrieveAgentStatsResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve_agent_stats(self, async_client: AsyncHeadlessAgents) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `agent_id` but received ''"):
            await async_client.with_raw_response.retrieve_agent_stats(
                "",
            )
