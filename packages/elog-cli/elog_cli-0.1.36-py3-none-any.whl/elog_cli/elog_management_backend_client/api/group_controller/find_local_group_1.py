from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_group_details_dto import ApiResultResponseListGroupDetailsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    anchor: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["anchor"] = anchor

    params["context"] = context

    params["limit"] = limit

    params["search"] = search

    params["includeMembers"] = include_members

    params["includeAuthorizations"] = include_authorizations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/groups",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListGroupDetailsDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListGroupDetailsDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListGroupDetailsDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    anchor: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseListGroupDetailsDTO]:
    """Find the local group using a query parameter

    Args:
        anchor (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListGroupDetailsDTO]
    """

    kwargs = _get_kwargs(
        anchor=anchor,
        context=context,
        limit=limit,
        search=search,
        include_members=include_members,
        include_authorizations=include_authorizations,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    anchor: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseListGroupDetailsDTO]:
    """Find the local group using a query parameter

    Args:
        anchor (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListGroupDetailsDTO
    """

    return sync_detailed(
        client=client,
        anchor=anchor,
        context=context,
        limit=limit,
        search=search,
        include_members=include_members,
        include_authorizations=include_authorizations,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    anchor: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseListGroupDetailsDTO]:
    """Find the local group using a query parameter

    Args:
        anchor (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListGroupDetailsDTO]
    """

    kwargs = _get_kwargs(
        anchor=anchor,
        context=context,
        limit=limit,
        search=search,
        include_members=include_members,
        include_authorizations=include_authorizations,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    anchor: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseListGroupDetailsDTO]:
    """Find the local group using a query parameter

    Args:
        anchor (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListGroupDetailsDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            anchor=anchor,
            context=context,
            limit=limit,
            search=search,
            include_members=include_members,
            include_authorizations=include_authorizations,
        )
    ).parsed
