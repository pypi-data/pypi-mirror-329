from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_entry_summary_dto import ApiResultResponseListEntrySummaryDTO
from ...models.authorization_cache import AuthorizationCache
from ...types import UNSET, Response


def _get_kwargs(
    entry_id: str,
    *,
    authorization_cache: "AuthorizationCache",
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_authorization_cache = authorization_cache.to_dict()
    params.update(json_authorization_cache)

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/entries/{entry_id}/references",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListEntrySummaryDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Return all the references for a specific entry identified by the id

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        authorization_cache=authorization_cache,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Return all the references for a specific entry identified by the id

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListEntrySummaryDTO
    """

    return sync_detailed(
        entry_id=entry_id,
        client=client,
        authorization_cache=authorization_cache,
    ).parsed


async def asyncio_detailed(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Return all the references for a specific entry identified by the id

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        authorization_cache=authorization_cache,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Return all the references for a specific entry identified by the id

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListEntrySummaryDTO
    """

    return (
        await asyncio_detailed(
            entry_id=entry_id,
            client=client,
            authorization_cache=authorization_cache,
        )
    ).parsed
