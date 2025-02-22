from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_workflow_request import CreateWorkflowRequest
from typing import cast
from typing import Dict



def _get_kwargs(
    agent_name: str,
    *,
    body: CreateWorkflowRequest,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/workflow/{agent_name}/create".format(agent_name=agent_name,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[Any, str]]:
    if response.status_code == 201:
        response_201 = cast(str, response.json())
        return response_201
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
    agent_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkflowRequest,

) -> Response[Union[Any, str]]:
    """ Create a new workflow for an agent

    Args:
        agent_name (str):
        body (CreateWorkflowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
     """


    kwargs = _get_kwargs(
        agent_name=agent_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    agent_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkflowRequest,

) -> Optional[Union[Any, str]]:
    """ Create a new workflow for an agent

    Args:
        agent_name (str):
        body (CreateWorkflowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
     """


    return sync_detailed(
        agent_name=agent_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    agent_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkflowRequest,

) -> Response[Union[Any, str]]:
    """ Create a new workflow for an agent

    Args:
        agent_name (str):
        body (CreateWorkflowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
     """


    kwargs = _get_kwargs(
        agent_name=agent_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    agent_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateWorkflowRequest,

) -> Optional[Union[Any, str]]:
    """ Create a new workflow for an agent

    Args:
        agent_name (str):
        body (CreateWorkflowRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
     """


    return (await asyncio_detailed(
        agent_name=agent_name,
client=client,
body=body,

    )).parsed
