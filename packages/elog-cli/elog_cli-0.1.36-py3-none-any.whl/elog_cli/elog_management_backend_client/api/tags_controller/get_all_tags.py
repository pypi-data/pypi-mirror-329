from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_tag_dto import ApiResultResponseListTagDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    logbooks: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_logbooks: Union[Unset, list[str]] = UNSET
    if not isinstance(logbooks, Unset):
        json_logbooks = logbooks

    params["logbooks"] = json_logbooks

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/tags",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListTagDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListTagDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListTagDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    logbooks: Union[Unset, list[str]] = UNSET,
) -> Response[ApiResultResponseListTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbooks (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListTagDTO]
    """

    kwargs = _get_kwargs(
        logbooks=logbooks,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    logbooks: Union[Unset, list[str]] = UNSET,
) -> Optional[ApiResultResponseListTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbooks (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListTagDTO
    """

    return sync_detailed(
        client=client,
        logbooks=logbooks,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    logbooks: Union[Unset, list[str]] = UNSET,
) -> Response[ApiResultResponseListTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbooks (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListTagDTO]
    """

    kwargs = _get_kwargs(
        logbooks=logbooks,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    logbooks: Union[Unset, list[str]] = UNSET,
) -> Optional[ApiResultResponseListTagDTO]:
    """Return all tags that belong to logbook identified by a list of ids

    Args:
        logbooks (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListTagDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            logbooks=logbooks,
        )
    ).parsed
