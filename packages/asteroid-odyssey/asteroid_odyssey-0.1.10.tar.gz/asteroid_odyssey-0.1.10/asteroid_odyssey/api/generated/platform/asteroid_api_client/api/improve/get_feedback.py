from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.feedback import Feedback
from typing import cast
from typing import cast, List
from typing import Dict
from uuid import UUID



def _get_kwargs(
    run_id: UUID,

) -> Dict[str, Any]:
    

    

    

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/run/{run_id}/feedback".format(run_id=run_id,),
    }


    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Union[ErrorResponse, List['Feedback']]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = Feedback.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())



        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Union[ErrorResponse, List['Feedback']]]:
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

) -> Response[Union[ErrorResponse, List['Feedback']]]:
    """ Get feedback for a run

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['Feedback']]]
     """


    kwargs = _get_kwargs(
        run_id=run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[ErrorResponse, List['Feedback']]]:
    """ Get feedback for a run

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['Feedback']]
     """


    return sync_detailed(
        run_id=run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Response[Union[ErrorResponse, List['Feedback']]]:
    """ Get feedback for a run

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, List['Feedback']]]
     """


    kwargs = _get_kwargs(
        run_id=run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    run_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],

) -> Optional[Union[ErrorResponse, List['Feedback']]]:
    """ Get feedback for a run

    Args:
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, List['Feedback']]
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,

    )).parsed
