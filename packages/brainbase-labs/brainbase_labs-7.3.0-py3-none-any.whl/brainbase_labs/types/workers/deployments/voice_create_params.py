# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo

__all__ = ["VoiceCreateParams"]


class VoiceCreateParams(TypedDict, total=False):
    config: Required[str]

    flow_id: Required[Annotated[str, PropertyInfo(alias="flowId")]]

    name: Required[str]

    phone_number: Required[Annotated[str, PropertyInfo(alias="phoneNumber")]]
