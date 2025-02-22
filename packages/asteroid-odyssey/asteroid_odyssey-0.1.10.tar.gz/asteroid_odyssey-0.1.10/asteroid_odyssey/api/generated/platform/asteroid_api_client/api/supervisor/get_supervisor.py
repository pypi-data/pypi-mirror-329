from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.supervisor import Supervisor
from typing import cast
from typing import Dict
from uuid import UUID



def _get_kwargs(
    supervisor_id: UUID,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/supervisor/{supervisor_id}".format(supervisor_id=supervisor_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Supervisor]:
    if response.status_code == 200:
        response_200 = Supervisor.from_dict(response.json())



        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Supervisor]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    supervisor_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Supervisor]:
    """ Get a supervisor

    Args:
        supervisor_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Supervisor]
     """


    kwargs = _get_kwargs(
        supervisor_id=supervisor_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    supervisor_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Supervisor]:
    """ Get a supervisor

    Args:
        supervisor_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Supervisor
     """


    return sync_detailed(
        supervisor_id=supervisor_id,
client=client,

    ).parsed

async def asyncio_detailed(
    supervisor_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Supervisor]:
    """ Get a supervisor

    Args:
        supervisor_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Supervisor]
     """


    kwargs = _get_kwargs(
        supervisor_id=supervisor_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    supervisor_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Supervisor]:
    """ Get a supervisor

    Args:
        supervisor_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Supervisor
     """


    return (await asyncio_detailed(
        supervisor_id=supervisor_id,
client=client,

    )).parsed
