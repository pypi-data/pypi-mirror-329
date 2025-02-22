from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asteroid_tool_call import AsteroidToolCall
from ...models.error_response import ErrorResponse
from typing import cast
from typing import cast, List
from typing import Dict
from uuid import UUID



def _get_kwargs(
    tool_call_id: UUID,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/tool_call/{tool_call_id}/history".format(tool_call_id=tool_call_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[ErrorResponse, List['AsteroidToolCall']]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = AsteroidToolCall.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())



        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[ErrorResponse, List['AsteroidToolCall']]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tool_call_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[ErrorResponse, List['AsteroidToolCall']]]:
    """ Get the modifications to a tool call

    Args:
        tool_call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['AsteroidToolCall']]]
     """


    kwargs = _get_kwargs(
        tool_call_id=tool_call_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    tool_call_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[ErrorResponse, List['AsteroidToolCall']]]:
    """ Get the modifications to a tool call

    Args:
        tool_call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['AsteroidToolCall']]
     """


    return sync_detailed(
        tool_call_id=tool_call_id,
client=client,

    ).parsed

async def asyncio_detailed(
    tool_call_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[ErrorResponse, List['AsteroidToolCall']]]:
    """ Get the modifications to a tool call

    Args:
        tool_call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['AsteroidToolCall']]]
     """


    kwargs = _get_kwargs(
        tool_call_id=tool_call_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    tool_call_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[ErrorResponse, List['AsteroidToolCall']]]:
    """ Get the modifications to a tool call

    Args:
        tool_call_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['AsteroidToolCall']]
     """


    return (await asyncio_detailed(
        tool_call_id=tool_call_id,
client=client,

    )).parsed
