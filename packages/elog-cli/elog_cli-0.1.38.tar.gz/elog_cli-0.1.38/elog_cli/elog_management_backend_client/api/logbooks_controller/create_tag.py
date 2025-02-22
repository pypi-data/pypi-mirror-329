from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...models.new_tag_dto import NewTagDTO
from ...types import Response


def _get_kwargs(
    logbook_id: str,
    *,
    body: NewTagDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/v1/logbooks/{logbook_id}/tags",
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
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewTagDTO,
) -> Response[ApiResultResponseString]:
    """
    Args:
        logbook_id (str):
        body (NewTagDTO): DTO for the tag creation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
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
    body: NewTagDTO,
) -> Optional[ApiResultResponseString]:
    """
    Args:
        logbook_id (str):
        body (NewTagDTO): DTO for the tag creation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
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
    body: NewTagDTO,
) -> Response[ApiResultResponseString]:
    """
    Args:
        logbook_id (str):
        body (NewTagDTO): DTO for the tag creation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
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
    body: NewTagDTO,
) -> Optional[ApiResultResponseString]:
    """
    Args:
        logbook_id (str):
        body (NewTagDTO): DTO for the tag creation

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            logbook_id=logbook_id,
            client=client,
            body=body,
        )
    ).parsed
