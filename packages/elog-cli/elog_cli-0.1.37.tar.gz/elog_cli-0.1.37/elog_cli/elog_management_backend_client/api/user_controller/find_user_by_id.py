from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_user_details_dto import ApiResultResponseUserDetailsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    user_id: str,
    *,
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeAuthorizations"] = include_authorizations

    params["includeInheritance"] = include_inheritance

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/users/{user_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseUserDetailsDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseUserDetailsDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseUserDetailsDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseUserDetailsDTO]:
    """Get a single user by id

    Args:
        user_id (str):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseUserDetailsDTO]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseUserDetailsDTO]:
    """Get a single user by id

    Args:
        user_id (str):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseUserDetailsDTO
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    ).parsed


async def asyncio_detailed(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseUserDetailsDTO]:
    """Get a single user by id

    Args:
        user_id (str):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseUserDetailsDTO]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        include_authorizations=include_authorizations,
        include_inheritance=include_inheritance,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    include_inheritance: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseUserDetailsDTO]:
    """Get a single user by id

    Args:
        user_id (str):
        include_authorizations (Union[Unset, bool]):
        include_inheritance (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseUserDetailsDTO
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            include_authorizations=include_authorizations,
            include_inheritance=include_inheritance,
        )
    ).parsed
