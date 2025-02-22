from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_entry_dto import ApiResultResponseEntryDTO
from ...models.authorization_cache import AuthorizationCache
from ...types import UNSET, Response, Unset


def _get_kwargs(
    entry_id: str,
    *,
    authorization_cache: "AuthorizationCache",
    include_follow_ups: Union[Unset, bool] = UNSET,
    include_following_ups: Union[Unset, bool] = UNSET,
    include_history: Union[Unset, bool] = UNSET,
    include_references: Union[Unset, bool] = UNSET,
    include_referenced_by: Union[Unset, bool] = UNSET,
    include_superseded_by: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_authorization_cache = authorization_cache.to_dict()
    params.update(json_authorization_cache)

    params["includeFollowUps"] = include_follow_ups

    params["includeFollowingUps"] = include_following_ups

    params["includeHistory"] = include_history

    params["includeReferences"] = include_references

    params["includeReferencedBy"] = include_referenced_by

    params["includeSupersededBy"] = include_superseded_by

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/entries/{entry_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseEntryDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseEntryDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseEntryDTO]:
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
    include_follow_ups: Union[Unset, bool] = UNSET,
    include_following_ups: Union[Unset, bool] = UNSET,
    include_history: Union[Unset, bool] = UNSET,
    include_references: Union[Unset, bool] = UNSET,
    include_referenced_by: Union[Unset, bool] = UNSET,
    include_superseded_by: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseEntryDTO]:
    """Return the full entry log information

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):
        include_follow_ups (Union[Unset, bool]):
        include_following_ups (Union[Unset, bool]):
        include_history (Union[Unset, bool]):
        include_references (Union[Unset, bool]):
        include_referenced_by (Union[Unset, bool]):
        include_superseded_by (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseEntryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        authorization_cache=authorization_cache,
        include_follow_ups=include_follow_ups,
        include_following_ups=include_following_ups,
        include_history=include_history,
        include_references=include_references,
        include_referenced_by=include_referenced_by,
        include_superseded_by=include_superseded_by,
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
    include_follow_ups: Union[Unset, bool] = UNSET,
    include_following_ups: Union[Unset, bool] = UNSET,
    include_history: Union[Unset, bool] = UNSET,
    include_references: Union[Unset, bool] = UNSET,
    include_referenced_by: Union[Unset, bool] = UNSET,
    include_superseded_by: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseEntryDTO]:
    """Return the full entry log information

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):
        include_follow_ups (Union[Unset, bool]):
        include_following_ups (Union[Unset, bool]):
        include_history (Union[Unset, bool]):
        include_references (Union[Unset, bool]):
        include_referenced_by (Union[Unset, bool]):
        include_superseded_by (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseEntryDTO
    """

    return sync_detailed(
        entry_id=entry_id,
        client=client,
        authorization_cache=authorization_cache,
        include_follow_ups=include_follow_ups,
        include_following_ups=include_following_ups,
        include_history=include_history,
        include_references=include_references,
        include_referenced_by=include_referenced_by,
        include_superseded_by=include_superseded_by,
    ).parsed


async def asyncio_detailed(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    include_follow_ups: Union[Unset, bool] = UNSET,
    include_following_ups: Union[Unset, bool] = UNSET,
    include_history: Union[Unset, bool] = UNSET,
    include_references: Union[Unset, bool] = UNSET,
    include_referenced_by: Union[Unset, bool] = UNSET,
    include_superseded_by: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseEntryDTO]:
    """Return the full entry log information

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):
        include_follow_ups (Union[Unset, bool]):
        include_following_ups (Union[Unset, bool]):
        include_history (Union[Unset, bool]):
        include_references (Union[Unset, bool]):
        include_referenced_by (Union[Unset, bool]):
        include_superseded_by (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseEntryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        authorization_cache=authorization_cache,
        include_follow_ups=include_follow_ups,
        include_following_ups=include_following_ups,
        include_history=include_history,
        include_references=include_references,
        include_referenced_by=include_referenced_by,
        include_superseded_by=include_superseded_by,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    include_follow_ups: Union[Unset, bool] = UNSET,
    include_following_ups: Union[Unset, bool] = UNSET,
    include_history: Union[Unset, bool] = UNSET,
    include_references: Union[Unset, bool] = UNSET,
    include_referenced_by: Union[Unset, bool] = UNSET,
    include_superseded_by: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseEntryDTO]:
    """Return the full entry log information

    Args:
        entry_id (str):
        authorization_cache (AuthorizationCache):
        include_follow_ups (Union[Unset, bool]):
        include_following_ups (Union[Unset, bool]):
        include_history (Union[Unset, bool]):
        include_references (Union[Unset, bool]):
        include_referenced_by (Union[Unset, bool]):
        include_superseded_by (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseEntryDTO
    """

    return (
        await asyncio_detailed(
            entry_id=entry_id,
            client=client,
            authorization_cache=authorization_cache,
            include_follow_ups=include_follow_ups,
            include_following_ups=include_following_ups,
            include_history=include_history,
            include_references=include_references,
            include_referenced_by=include_referenced_by,
            include_superseded_by=include_superseded_by,
        )
    ).parsed
