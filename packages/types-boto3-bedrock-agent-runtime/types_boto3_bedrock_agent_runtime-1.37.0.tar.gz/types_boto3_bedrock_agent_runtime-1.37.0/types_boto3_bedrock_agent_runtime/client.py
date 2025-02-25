"""
Type annotations for bedrock-agent-runtime service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient

    session = Session()
    client: AgentsforBedrockRuntimeClient = session.client("bedrock-agent-runtime")
    ```
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import GetAgentMemoryPaginator, RerankPaginator, RetrievePaginator
from .type_defs import (
    DeleteAgentMemoryRequestTypeDef,
    GenerateQueryRequestTypeDef,
    GenerateQueryResponseTypeDef,
    GetAgentMemoryRequestTypeDef,
    GetAgentMemoryResponseTypeDef,
    InvokeAgentRequestTypeDef,
    InvokeAgentResponseTypeDef,
    InvokeFlowRequestTypeDef,
    InvokeFlowResponseTypeDef,
    InvokeInlineAgentRequestTypeDef,
    InvokeInlineAgentResponseTypeDef,
    OptimizePromptRequestTypeDef,
    OptimizePromptResponseTypeDef,
    RerankRequestTypeDef,
    RerankResponseTypeDef,
    RetrieveAndGenerateRequestTypeDef,
    RetrieveAndGenerateResponseTypeDef,
    RetrieveAndGenerateStreamRequestTypeDef,
    RetrieveAndGenerateStreamResponseTypeDef,
    RetrieveRequestTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("AgentsforBedrockRuntimeClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadGatewayException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    DependencyFailedException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ModelNotReadyException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class AgentsforBedrockRuntimeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client)
    [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentsforBedrockRuntimeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime.html#AgentsforBedrockRuntime.Client)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/can_paginate.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/generate_presigned_url.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#generate_presigned_url)
        """

    def delete_agent_memory(
        self, **kwargs: Unpack[DeleteAgentMemoryRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes memory from the specified memory identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/delete_agent_memory.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#delete_agent_memory)
        """

    def generate_query(
        self, **kwargs: Unpack[GenerateQueryRequestTypeDef]
    ) -> GenerateQueryResponseTypeDef:
        """
        Generates an SQL query from a natural language query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/generate_query.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#generate_query)
        """

    def get_agent_memory(
        self, **kwargs: Unpack[GetAgentMemoryRequestTypeDef]
    ) -> GetAgentMemoryResponseTypeDef:
        """
        Gets the sessions stored in the memory of the agent.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_agent_memory.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_agent_memory)
        """

    def invoke_agent(
        self, **kwargs: Unpack[InvokeAgentRequestTypeDef]
    ) -> InvokeAgentResponseTypeDef:
        """
        Sends a prompt for the agent to process and respond to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_agent.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_agent)
        """

    def invoke_flow(self, **kwargs: Unpack[InvokeFlowRequestTypeDef]) -> InvokeFlowResponseTypeDef:
        """
        Invokes an alias of a flow to run the inputs that you specify and return the
        output of each node as a stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_flow.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_flow)
        """

    def invoke_inline_agent(
        self, **kwargs: Unpack[InvokeInlineAgentRequestTypeDef]
    ) -> InvokeInlineAgentResponseTypeDef:
        """
        Invokes an inline Amazon Bedrock agent using the configurations you provide
        with the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/invoke_inline_agent.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#invoke_inline_agent)
        """

    def optimize_prompt(
        self, **kwargs: Unpack[OptimizePromptRequestTypeDef]
    ) -> OptimizePromptResponseTypeDef:
        """
        Optimizes a prompt for the task that you specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/optimize_prompt.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#optimize_prompt)
        """

    def rerank(self, **kwargs: Unpack[RerankRequestTypeDef]) -> RerankResponseTypeDef:
        """
        Reranks the relevance of sources based on queries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/rerank.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#rerank)
        """

    def retrieve(self, **kwargs: Unpack[RetrieveRequestTypeDef]) -> RetrieveResponseTypeDef:
        """
        Queries a knowledge base and retrieves information from it.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve)
        """

    def retrieve_and_generate(
        self, **kwargs: Unpack[RetrieveAndGenerateRequestTypeDef]
    ) -> RetrieveAndGenerateResponseTypeDef:
        """
        Queries a knowledge base and generates responses based on the retrieved results
        and using the specified foundation model or <a
        href="https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html">inference
        profile</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve_and_generate)
        """

    def retrieve_and_generate_stream(
        self, **kwargs: Unpack[RetrieveAndGenerateStreamRequestTypeDef]
    ) -> RetrieveAndGenerateStreamResponseTypeDef:
        """
        Queries a knowledge base and generates responses based on the retrieved
        results, with output in streaming format.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/retrieve_and_generate_stream.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#retrieve_and_generate_stream)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_agent_memory"]
    ) -> GetAgentMemoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["rerank"]
    ) -> RerankPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["retrieve"]
    ) -> RetrievePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/client/get_paginator.html)
        [Show types-boto3 documentation](https://youtype.github.io/types_boto3_docs/types_boto3_bedrock_agent_runtime/client/#get_paginator)
        """
