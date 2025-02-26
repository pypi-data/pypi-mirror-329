# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from brainbase_labs import BrainbaseLabs, AsyncBrainbaseLabs
from brainbase_labs.types.workers.deployments import (
    VoiceDeployment,
    VoiceListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVoice:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployments.voice.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployments.voice.with_raw_response.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: BrainbaseLabs) -> None:
        with client.workers.deployments.voice.with_streaming_response.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.create(
                worker_id="",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployments.voice.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployments.voice.with_raw_response.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: BrainbaseLabs) -> None:
        with client.workers.deployments.voice.with_streaming_response.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.retrieve(
                deployment_id="deploymentId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.retrieve(
                deployment_id="",
                worker_id="workerId",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployments.voice.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployments.voice.with_raw_response.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: BrainbaseLabs) -> None:
        with client.workers.deployments.voice.with_streaming_response.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.update(
                deployment_id="deploymentId",
                worker_id="",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.update(
                deployment_id="",
                worker_id="workerId",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployments.voice.list(
            "workerId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployments.voice.with_raw_response.list(
            "workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: BrainbaseLabs) -> None:
        with client.workers.deployments.voice.with_streaming_response.list(
            "workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceListResponse, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployments.voice.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        )
        assert voice is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployments.voice.with_raw_response.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert voice is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: BrainbaseLabs) -> None:
        with client.workers.deployments.voice.with_streaming_response.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert voice is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.delete(
                deployment_id="deploymentId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            client.workers.deployments.voice.with_raw_response.delete(
                deployment_id="",
                worker_id="workerId",
            )


class TestAsyncVoice:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployments.voice.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployments.voice.with_raw_response.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployments.voice.with_streaming_response.create(
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.create(
                worker_id="",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployments.voice.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployments.voice.with_raw_response.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployments.voice.with_streaming_response.retrieve(
            deployment_id="deploymentId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.retrieve(
                deployment_id="deploymentId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.retrieve(
                deployment_id="",
                worker_id="workerId",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployments.voice.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployments.voice.with_raw_response.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceDeployment, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployments.voice.with_streaming_response.update(
            deployment_id="deploymentId",
            worker_id="workerId",
            config="config",
            flow_id="flowId",
            name="name",
            phone_number="phoneNumber",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceDeployment, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.update(
                deployment_id="deploymentId",
                worker_id="",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.update(
                deployment_id="",
                worker_id="workerId",
                config="config",
                flow_id="flowId",
                name="name",
                phone_number="phoneNumber",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployments.voice.list(
            "workerId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployments.voice.with_raw_response.list(
            "workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployments.voice.with_streaming_response.list(
            "workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceListResponse, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.list(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployments.voice.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        )
        assert voice is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployments.voice.with_raw_response.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert voice is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployments.voice.with_streaming_response.delete(
            deployment_id="deploymentId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert voice is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.delete(
                deployment_id="deploymentId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `deployment_id` but received ''"):
            await async_client.workers.deployments.voice.with_raw_response.delete(
                deployment_id="",
                worker_id="workerId",
            )
