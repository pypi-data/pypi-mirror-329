import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...types import Response


def _get_kwargs(
    shift_id: str,
    date: datetime.date,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/entries/{shift_id}/summaries/{date}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseString]:
    if response.status_code == 200:
        response_200 = ApiResultResponseString.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseString]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    shift_id: str,
    date: datetime.date,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseString]:
    """Find the summary id for a specific shift and date

    Args:
        shift_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        shift_id=shift_id,
        date=date,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    shift_id: str,
    date: datetime.date,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseString]:
    """Find the summary id for a specific shift and date

    Args:
        shift_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return sync_detailed(
        shift_id=shift_id,
        date=date,
        client=client,
    ).parsed


async def asyncio_detailed(
    shift_id: str,
    date: datetime.date,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseString]:
    """Find the summary id for a specific shift and date

    Args:
        shift_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        shift_id=shift_id,
        date=date,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    shift_id: str,
    date: datetime.date,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseString]:
    """Find the summary id for a specific shift and date

    Args:
        shift_id (str):
        date (datetime.date):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            shift_id=shift_id,
            date=date,
            client=client,
        )
    ).parsed
