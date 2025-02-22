from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_local_group_dto import ApiResultResponseLocalGroupDTO
from ...types import Response


def _get_kwargs(
    local_group_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v2/auth/local/group/{local_group_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseLocalGroupDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseLocalGroupDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseLocalGroupDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    local_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseLocalGroupDTO]:
    """Find a local group using an id

    Args:
        local_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseLocalGroupDTO]
    """

    kwargs = _get_kwargs(
        local_group_id=local_group_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    local_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseLocalGroupDTO]:
    """Find a local group using an id

    Args:
        local_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseLocalGroupDTO
    """

    return sync_detailed(
        local_group_id=local_group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    local_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseLocalGroupDTO]:
    """Find a local group using an id

    Args:
        local_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseLocalGroupDTO]
    """

    kwargs = _get_kwargs(
        local_group_id=local_group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    local_group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseLocalGroupDTO]:
    """Find a local group using an id

    Args:
        local_group_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseLocalGroupDTO
    """

    return (
        await asyncio_detailed(
            local_group_id=local_group_id,
            client=client,
        )
    ).parsed
