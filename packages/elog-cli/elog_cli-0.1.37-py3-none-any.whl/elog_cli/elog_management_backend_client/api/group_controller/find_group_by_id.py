from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_group_details_dto import ApiResultResponseGroupDetailsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    group_id: str,
    *,
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeMembers"] = include_members

    params["includeAuthorizations"] = include_authorizations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/groups/{group_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseGroupDetailsDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseGroupDetailsDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseGroupDetailsDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseGroupDetailsDTO]:
    """Find a local group using an id

    Args:
        group_id (str):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseGroupDetailsDTO]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        include_members=include_members,
        include_authorizations=include_authorizations,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseGroupDetailsDTO]:
    """Find a local group using an id

    Args:
        group_id (str):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseGroupDetailsDTO
    """

    return sync_detailed(
        group_id=group_id,
        client=client,
        include_members=include_members,
        include_authorizations=include_authorizations,
    ).parsed


async def asyncio_detailed(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseGroupDetailsDTO]:
    """Find a local group using an id

    Args:
        group_id (str):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseGroupDetailsDTO]
    """

    kwargs = _get_kwargs(
        group_id=group_id,
        include_members=include_members,
        include_authorizations=include_authorizations,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    group_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_members: Union[Unset, bool] = UNSET,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseGroupDetailsDTO]:
    """Find a local group using an id

    Args:
        group_id (str):
        include_members (Union[Unset, bool]):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseGroupDetailsDTO
    """

    return (
        await asyncio_detailed(
            group_id=group_id,
            client=client,
            include_members=include_members,
            include_authorizations=include_authorizations,
        )
    ).parsed
