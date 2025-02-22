from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.asteroid_chat import AsteroidChat
from ...models.chat_ids import ChatIds
from ...models.error_response import ErrorResponse
from typing import cast
from typing import Dict
from uuid import UUID



def _get_kwargs(
    run_id: UUID,
    *,
    body: AsteroidChat,

) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}


    

    

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/run/{run_id}/chat".format(run_id=run_id,),
    }

    _body = body.to_dict()


    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[ChatIds, ErrorResponse]]:
    if response.status_code == 201:
        response_201 = ChatIds.from_dict(response.json())



        return response_201
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())



        return response_400
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())



        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[ChatIds, ErrorResponse]]:
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
    body: AsteroidChat,

) -> Response[Union[ChatIds, ErrorResponse]]:
    """ Create a new chat completion request from an existing run

    Args:
        run_id (UUID):
        body (AsteroidChat): The raw b64 encoded JSON of the request and response data
            sent/received from the LLM.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatIds, ErrorResponse]]
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
    body: AsteroidChat,

) -> Optional[Union[ChatIds, ErrorResponse]]:
    """ Create a new chat completion request from an existing run

    Args:
        run_id (UUID):
        body (AsteroidChat): The raw b64 encoded JSON of the request and response data
            sent/received from the LLM.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatIds, ErrorResponse]
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
    body: AsteroidChat,

) -> Response[Union[ChatIds, ErrorResponse]]:
    """ Create a new chat completion request from an existing run

    Args:
        run_id (UUID):
        body (AsteroidChat): The raw b64 encoded JSON of the request and response data
            sent/received from the LLM.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChatIds, ErrorResponse]]
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
    body: AsteroidChat,

) -> Optional[Union[ChatIds, ErrorResponse]]:
    """ Create a new chat completion request from an existing run

    Args:
        run_id (UUID):
        body (AsteroidChat): The raw b64 encoded JSON of the request and response data
            sent/received from the LLM.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChatIds, ErrorResponse]
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,
body=body,

    )).parsed
