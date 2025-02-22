from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.supervision_status import SupervisionStatus
from typing import cast
from typing import Dict
from uuid import UUID



def _get_kwargs(
    supervision_request_id: UUID,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/supervision_request/{supervision_request_id}/status".format(supervision_request_id=supervision_request_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[SupervisionStatus]:
    if response.status_code == 200:
        response_200 = SupervisionStatus.from_dict(response.json())



        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[SupervisionStatus]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    supervision_request_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[SupervisionStatus]:
    """ Get a supervision request status

    Args:
        supervision_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SupervisionStatus]
     """


    kwargs = _get_kwargs(
        supervision_request_id=supervision_request_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    supervision_request_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[SupervisionStatus]:
    """ Get a supervision request status

    Args:
        supervision_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SupervisionStatus
     """


    return sync_detailed(
        supervision_request_id=supervision_request_id,
client=client,

    ).parsed

async def asyncio_detailed(
    supervision_request_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[SupervisionStatus]:
    """ Get a supervision request status

    Args:
        supervision_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SupervisionStatus]
     """


    kwargs = _get_kwargs(
        supervision_request_id=supervision_request_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    supervision_request_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[SupervisionStatus]:
    """ Get a supervision request status

    Args:
        supervision_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SupervisionStatus
     """


    return (await asyncio_detailed(
        supervision_request_id=supervision_request_id,
client=client,

    )).parsed
