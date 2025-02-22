from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_boolean import ApiResultResponseBoolean
from ...models.shift_dto import ShiftDTO
from ...types import Response


def _get_kwargs(
    logbook_id: str,
    *,
    body: list["ShiftDTO"],
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/logbooks/{logbook_id}/shifts",
    }

    _body = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _body.append(body_item)

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseBoolean]:
    if response.status_code == 201:
        response_201 = ApiResultResponseBoolean.from_dict(response.json())

        return response_201
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
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ShiftDTO"],
) -> Response[ApiResultResponseBoolean]:
    """
    Args:
        logbook_id (str):
        body (list['ShiftDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ShiftDTO"],
) -> Optional[ApiResultResponseBoolean]:
    """
    Args:
        logbook_id (str):
        body (list['ShiftDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return sync_detailed(
        logbook_id=logbook_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ShiftDTO"],
) -> Response[ApiResultResponseBoolean]:
    """
    Args:
        logbook_id (str):
        body (list['ShiftDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: list["ShiftDTO"],
) -> Optional[ApiResultResponseBoolean]:
    """
    Args:
        logbook_id (str):
        body (list['ShiftDTO']):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return (
        await asyncio_detailed(
            logbook_id=logbook_id,
            client=client,
            body=body,
        )
    ).parsed
