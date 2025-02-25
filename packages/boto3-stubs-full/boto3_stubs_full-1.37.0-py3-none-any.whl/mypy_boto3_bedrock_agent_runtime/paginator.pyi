"""
Type annotations for bedrock-agent-runtime service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from mypy_boto3_bedrock_agent_runtime.paginator import (
        GetAgentMemoryPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")

    get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
    rerank_paginator: RerankPaginator = client.get_paginator("rerank")
    retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetAgentMemoryRequestPaginateTypeDef,
    GetAgentMemoryResponseTypeDef,
    RerankRequestPaginateTypeDef,
    RerankResponseTypeDef,
    RetrieveRequestPaginateTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("GetAgentMemoryPaginator", "RerankPaginator", "RetrievePaginator")

if TYPE_CHECKING:
    _GetAgentMemoryPaginatorBase = Paginator[GetAgentMemoryResponseTypeDef]
else:
    _GetAgentMemoryPaginatorBase = Paginator  # type: ignore[assignment]

class GetAgentMemoryPaginator(_GetAgentMemoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgentMemoryRequestPaginateTypeDef]
    ) -> PageIterator[GetAgentMemoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
        """

if TYPE_CHECKING:
    _RerankPaginatorBase = Paginator[RerankResponseTypeDef]
else:
    _RerankPaginatorBase = Paginator  # type: ignore[assignment]

class RerankPaginator(_RerankPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#rerankpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RerankRequestPaginateTypeDef]
    ) -> PageIterator[RerankResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#rerankpaginator)
        """

if TYPE_CHECKING:
    _RetrievePaginatorBase = Paginator[RetrieveResponseTypeDef]
else:
    _RetrievePaginatorBase = Paginator  # type: ignore[assignment]

class RetrievePaginator(_RetrievePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RetrieveRequestPaginateTypeDef]
    ) -> PageIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
