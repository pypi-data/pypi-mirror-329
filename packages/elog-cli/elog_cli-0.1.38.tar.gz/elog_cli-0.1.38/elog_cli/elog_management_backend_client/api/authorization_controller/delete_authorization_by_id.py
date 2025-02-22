from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_boolean import ApiResultResponseBoolean
from ...types import Response


def _get_kwargs(
    authorization_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/v1/authorizations/{authorization_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseBoolean]:
    if response.status_code == 200:
        response_200 = ApiResultResponseBoolean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseBoolean]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseBoolean]:
    """Manage authorization for logbook user authorization

    Args:
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        authorization_id=authorization_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseBoolean]:
    """Manage authorization for logbook user authorization

    Args:
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return sync_detailed(
        authorization_id=authorization_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseBoolean]:
    """Manage authorization for logbook user authorization

    Args:
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        authorization_id=authorization_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    authorization_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseBoolean]:
    """Manage authorization for logbook user authorization

    Args:
        authorization_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return (
        await asyncio_detailed(
            authorization_id=authorization_id,
            client=client,
        )
    ).parsed
