# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .workers.workers import Workers

__all__ = ["WorkerListResponse"]

WorkerListResponse: TypeAlias = List[Workers]
