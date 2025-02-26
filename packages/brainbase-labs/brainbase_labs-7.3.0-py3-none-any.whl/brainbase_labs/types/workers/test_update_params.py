# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["TestUpdateParams"]


class TestUpdateParams(TypedDict, total=False):
    worker_id: Required[Annotated[str, PropertyInfo(alias="workerId")]]

    checkpoints: Required[str]

    description: Required[str]

    flow_id: Required[Annotated[str, PropertyInfo(alias="flowId")]]

    name: Required[str]

    system_prompt: Required[Annotated[str, PropertyInfo(alias="systemPrompt")]]

    test_mode: Required[Annotated[str, PropertyInfo(alias="testMode")]]
