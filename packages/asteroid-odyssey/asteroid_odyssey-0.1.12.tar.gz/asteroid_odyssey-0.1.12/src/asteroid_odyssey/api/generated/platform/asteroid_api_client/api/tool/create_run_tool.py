from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_run_tool_body import CreateRunToolBody
from ...models.tool import Tool
from typing import cast
from typing import Dict
from uuid import UUID



def _get_kwargs(
    run_id: UUID,
    *,
    body: CreateRunToolBody,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/run/{run_id}/tool".format(run_id=run_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Tool]:
    if response.status_code == 200:
        response_200 = Tool.from_dict(response.json())



        return response_200
    if response.status_code == 201:
        response_201 = Tool.from_dict(response.json())



        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Tool]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRunToolBody,

) -> Response[Tool]:
    """ Create a new tool for a run

    Args:
        run_id (UUID):
        body (CreateRunToolBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Tool]
     """


    kwargs = _get_kwargs(
        run_id=run_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRunToolBody,

) -> Optional[Tool]:
    """ Create a new tool for a run

    Args:
        run_id (UUID):
        body (CreateRunToolBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Tool
     """


    return sync_detailed(
        run_id=run_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRunToolBody,

) -> Response[Tool]:
    """ Create a new tool for a run

    Args:
        run_id (UUID):
        body (CreateRunToolBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Tool]
     """


    kwargs = _get_kwargs(
        run_id=run_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRunToolBody,

) -> Optional[Tool]:
    """ Create a new tool for a run

    Args:
        run_id (UUID):
        body (CreateRunToolBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Tool
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,
body=body,

    )).parsed
