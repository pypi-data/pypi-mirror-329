from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_tag_dto import ApiResultResponseTagDTO
from ...models.update_tag_dto import UpdateTagDTO
from ...types import Response


def _get_kwargs(
    logbook_id: str,
    tag_id: str,
    *,
    body: UpdateTagDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/v1/logbooks/{logbook_id}/tags/{tag_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseTagDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseTagDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseTagDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    logbook_id: str,
    tag_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateTagDTO,
) -> Response[ApiResultResponseTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbook_id (str):
        tag_id (str):
        body (UpdateTagDTO): DTO for the tag update

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseTagDTO]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        tag_id=tag_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    logbook_id: str,
    tag_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateTagDTO,
) -> Optional[ApiResultResponseTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbook_id (str):
        tag_id (str):
        body (UpdateTagDTO): DTO for the tag update

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseTagDTO
    """

    return sync_detailed(
        logbook_id=logbook_id,
        tag_id=tag_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    logbook_id: str,
    tag_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateTagDTO,
) -> Response[ApiResultResponseTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbook_id (str):
        tag_id (str):
        body (UpdateTagDTO): DTO for the tag update

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseTagDTO]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        tag_id=tag_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    logbook_id: str,
    tag_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: UpdateTagDTO,
) -> Optional[ApiResultResponseTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbook_id (str):
        tag_id (str):
        body (UpdateTagDTO): DTO for the tag update

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseTagDTO
    """

    return (
        await asyncio_detailed(
            logbook_id=logbook_id,
            tag_id=tag_id,
            client=client,
            body=body,
        )
    ).parsed
