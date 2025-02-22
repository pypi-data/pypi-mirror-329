from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.workflow_execution_request import WorkflowExecutionRequest
from typing import cast
from typing import Dict
from uuid import UUID



def _get_kwargs(
    workflow_id: UUID,
    *,
    body: WorkflowExecutionRequest,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}






    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/workflow/{workflow_id}".format(workflow_id=workflow_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, str]]:
    if response.status_code == 202:
        response_202 = cast(str, response.json())
        return response_202
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[Any, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowExecutionRequest,

) -> Response[Union[Any, str]]:
    """ Execute a saved workflow for an agent

    Args:
        workflow_id (UUID):
        body (WorkflowExecutionRequest): Dynamic values to be merged into the saved workflow
            configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
     """


    kwargs = _get_kwargs(
        workflow_id=workflow_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    workflow_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowExecutionRequest,

) -> Optional[Union[Any, str]]:
    """ Execute a saved workflow for an agent

    Args:
        workflow_id (UUID):
        body (WorkflowExecutionRequest): Dynamic values to be merged into the saved workflow
            configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
     """


    result = sync_detailed(
        workflow_id=workflow_id,
client=client,
body=body,

    ).parsed

    return result

async def asyncio_detailed(
    workflow_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowExecutionRequest,

) -> Response[Union[Any, str]]:
    """ Execute a saved workflow for an agent

    Args:
        workflow_id (UUID):
        body (WorkflowExecutionRequest): Dynamic values to be merged into the saved workflow
            configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
     """


    kwargs = _get_kwargs(
        workflow_id=workflow_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    workflow_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: WorkflowExecutionRequest,

) -> Optional[Union[Any, str]]:
    """ Execute a saved workflow for an agent

    Args:
        workflow_id (UUID):
        body (WorkflowExecutionRequest): Dynamic values to be merged into the saved workflow
            configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
     """


    return (await asyncio_detailed(
        workflow_id=workflow_id,
client=client,
body=body,

    )).parsed
