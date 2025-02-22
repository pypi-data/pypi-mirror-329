from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_user_group_management_authorization_level import (
    ApiResultResponseListUserGroupManagementAuthorizationLevel,
)
from ...types import Response


def _get_kwargs(
    user_ids: list[str],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v2/auth/local/group/authorize/{user_ids}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListUserGroupManagementAuthorizationLevel.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_ids: list[str],
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    """Get current user authorization on group management

    Args:
        user_ids (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListUserGroupManagementAuthorizationLevel]
    """

    kwargs = _get_kwargs(
        user_ids=user_ids,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_ids: list[str],
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    """Get current user authorization on group management

    Args:
        user_ids (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListUserGroupManagementAuthorizationLevel
    """

    return sync_detailed(
        user_ids=user_ids,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_ids: list[str],
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    """Get current user authorization on group management

    Args:
        user_ids (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListUserGroupManagementAuthorizationLevel]
    """

    kwargs = _get_kwargs(
        user_ids=user_ids,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_ids: list[str],
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseListUserGroupManagementAuthorizationLevel]:
    """Get current user authorization on group management

    Args:
        user_ids (list[str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListUserGroupManagementAuthorizationLevel
    """

    return (
        await asyncio_detailed(
            user_ids=user_ids,
            client=client,
        )
    ).parsed
