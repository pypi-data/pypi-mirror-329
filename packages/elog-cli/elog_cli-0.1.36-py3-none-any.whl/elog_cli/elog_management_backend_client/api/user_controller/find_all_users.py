from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_user_details_dto import ApiResultResponseListUserDetailsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    anchor: Union[Unset, str] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["search"] = search

    params["context"] = context

    params["limit"] = limit

    params["anchor"] = anchor

    params["includeAuthorizations"] = include_authorizations

    params["includeInheritance"] = include_inheritance

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/users",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListUserDetailsDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListUserDetailsDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListUserDetailsDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    anchor: Union[Unset, str] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseListUserDetailsDTO]:
    """Search from all users

    Args:
        search (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        anchor (Union[Unset, str]):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListUserDetailsDTO]
    """

    kwargs = _get_kwargs(
        search=search,
        context=context,
        limit=limit,
        anchor=anchor,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    anchor: Union[Unset, str] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseListUserDetailsDTO]:
    """Search from all users

    Args:
        search (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        anchor (Union[Unset, str]):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListUserDetailsDTO
    """

    return sync_detailed(
        client=client,
        search=search,
        context=context,
        limit=limit,
        anchor=anchor,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    anchor: Union[Unset, str] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseListUserDetailsDTO]:
    """Search from all users

    Args:
        search (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        anchor (Union[Unset, str]):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListUserDetailsDTO]
    """

    kwargs = _get_kwargs(
        search=search,
        context=context,
        limit=limit,
        anchor=anchor,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    search: Union[Unset, str] = UNSET,
    context: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    anchor: Union[Unset, str] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseListUserDetailsDTO]:
    """Search from all users

    Args:
        search (Union[Unset, str]):
        context (Union[Unset, int]):
        limit (Union[Unset, int]):
        anchor (Union[Unset, str]):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListUserDetailsDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            search=search,
            context=context,
            limit=limit,
            anchor=anchor,
            include_authorizations=include_authorizations,
            include_inheritance=include_inheritance,
        )
    ).parsed
