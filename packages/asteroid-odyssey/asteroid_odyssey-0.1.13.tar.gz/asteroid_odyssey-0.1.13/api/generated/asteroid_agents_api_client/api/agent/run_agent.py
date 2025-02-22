from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.job import Job
from ...types import Response


def _get_kwargs(
    agent_name: str,
    *,
    body: Job,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": f"/agents/{agent_name}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[str]:
    print(f"Response: {response}")
    if response.status_code == 202:
        response_202 = cast(str, response.json())
        return response_202
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
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
    body: Job,
) -> Response[str]:
    """Run an agent on the given input

    Args:
        agent_name (str):
        body (Job):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
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
    body: Job,
) -> Optional[str]:
    """Run an agent on the given input

    Args:
        agent_name (str):
        body (Job):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
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
    body: Job,
) -> Response[str]:
    """Run an agent on the given input

    Args:
        agent_name (str):
        body (Job):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        agent_name=agent_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    agent_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: Job,
) -> Optional[str]:
    """Run an agent on the given input

    Args:
        agent_name (str):
        body (Job):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            agent_name=agent_name,
            client=client,
            body=body,
        )
    ).parsed
