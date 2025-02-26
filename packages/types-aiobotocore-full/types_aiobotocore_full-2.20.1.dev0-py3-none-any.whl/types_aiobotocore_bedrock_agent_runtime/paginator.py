"""
Type annotations for bedrock-agent-runtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from types_aiobotocore_bedrock_agent_runtime.paginator import (
        GetAgentMemoryPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agent-runtime") as client:
        client: AgentsforBedrockRuntimeClient

        get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
        rerank_paginator: RerankPaginator = client.get_paginator("rerank")
        retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _GetAgentMemoryPaginatorBase = AioPaginator[GetAgentMemoryResponseTypeDef]
else:
    _GetAgentMemoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAgentMemoryPaginator(_GetAgentMemoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgentMemoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAgentMemoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
        """


if TYPE_CHECKING:
    _RerankPaginatorBase = AioPaginator[RerankResponseTypeDef]
else:
    _RerankPaginatorBase = AioPaginator  # type: ignore[assignment]


class RerankPaginator(_RerankPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#rerankpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RerankRequestPaginateTypeDef]
    ) -> AioPageIterator[RerankResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#rerankpaginator)
        """


if TYPE_CHECKING:
    _RetrievePaginatorBase = AioPaginator[RetrieveResponseTypeDef]
else:
    _RetrievePaginatorBase = AioPaginator  # type: ignore[assignment]


class RetrievePaginator(_RetrievePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RetrieveRequestPaginateTypeDef]
    ) -> AioPageIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
