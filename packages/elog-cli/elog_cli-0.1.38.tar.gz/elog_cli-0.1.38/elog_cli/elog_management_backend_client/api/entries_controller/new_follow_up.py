from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...models.entry_new_dto import EntryNewDTO
from ...types import Response


def _get_kwargs(
    entry_id: str,
    *,
    body: EntryNewDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1/entries/{entry_id}/follow-ups",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseString]:
    if response.status_code == 201:
        response_201 = ApiResultResponseString.from_dict(response.json())

        return response_201
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
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EntryNewDTO,
) -> Response[ApiResultResponseString]:
    """Create a new follow-up log for the the log identified by the id

    Args:
        entry_id (str):
        body (EntryNewDTO): Is the new entry that will follow-up the entry identified by the
            entryId

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EntryNewDTO,
) -> Optional[ApiResultResponseString]:
    """Create a new follow-up log for the the log identified by the id

    Args:
        entry_id (str):
        body (EntryNewDTO): Is the new entry that will follow-up the entry identified by the
            entryId

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return sync_detailed(
        entry_id=entry_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EntryNewDTO,
) -> Response[ApiResultResponseString]:
    """Create a new follow-up log for the the log identified by the id

    Args:
        entry_id (str):
        body (EntryNewDTO): Is the new entry that will follow-up the entry identified by the
            entryId

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        entry_id=entry_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    entry_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: EntryNewDTO,
) -> Optional[ApiResultResponseString]:
    """Create a new follow-up log for the the log identified by the id

    Args:
        entry_id (str):
        body (EntryNewDTO): Is the new entry that will follow-up the entry identified by the
            entryId

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            entry_id=entry_id,
            client=client,
            body=body,
        )
    ).parsed
