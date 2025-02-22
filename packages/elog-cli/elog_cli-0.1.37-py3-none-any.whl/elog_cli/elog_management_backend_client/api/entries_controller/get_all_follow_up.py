from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_entry_summary_dto import ApiResultResponseListEntrySummaryDTO
from ...types import Response


def _get_kwargs(
    entry_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/entries/{entry_id}/follow-ups",
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
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Return all the follow-up logs for a specific entry identified by the id

    Args:
        entry_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Return all the follow-up logs for a specific entry identified by the id

    Args:
        entry_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListEntrySummaryDTO
    """

    return sync_detailed(
        entry_id=entry_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Return all the follow-up logs for a specific entry identified by the id

    Args:
        entry_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Return all the follow-up logs for a specific entry identified by the id

    Args:
        entry_id (str):

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
        )
    ).parsed
