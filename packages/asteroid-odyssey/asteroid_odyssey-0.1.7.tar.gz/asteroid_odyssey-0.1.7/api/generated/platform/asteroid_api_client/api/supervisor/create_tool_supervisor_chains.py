from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.chain_request import ChainRequest
from typing import cast
from typing import cast, List
from typing import Dict
from uuid import UUID



def _get_kwargs(
    tool_id: UUID,
    *,
    body: List['ChainRequest'],

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/tool/{tool_id}/supervisors".format(tool_id=tool_id,),
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)




    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[List[UUID]]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in (_response_201):
            response_201_item = UUID(response_201_item_data)



            response_201.append(response_201_item)

        return response_201
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[List[UUID]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tool_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: List['ChainRequest'],

) -> Response[List[UUID]]:
    """ Create new chains with supervisors for a tool

    Args:
        tool_id (UUID):
        body (List['ChainRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[UUID]]
     """


    kwargs = _get_kwargs(
        tool_id=tool_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tool_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: List['ChainRequest'],

) -> Optional[List[UUID]]:
    """ Create new chains with supervisors for a tool

    Args:
        tool_id (UUID):
        body (List['ChainRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[UUID]
     """


    return sync_detailed(
        tool_id=tool_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    tool_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: List['ChainRequest'],

) -> Response[List[UUID]]:
    """ Create new chains with supervisors for a tool

    Args:
        tool_id (UUID):
        body (List['ChainRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List[UUID]]
     """


    kwargs = _get_kwargs(
        tool_id=tool_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tool_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
    body: List['ChainRequest'],

) -> Optional[List[UUID]]:
    """ Create new chains with supervisors for a tool

    Args:
        tool_id (UUID):
        body (List['ChainRequest']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List[UUID]
     """


    return (await asyncio_detailed(
        tool_id=tool_id,
client=client,
body=body,

    )).parsed
