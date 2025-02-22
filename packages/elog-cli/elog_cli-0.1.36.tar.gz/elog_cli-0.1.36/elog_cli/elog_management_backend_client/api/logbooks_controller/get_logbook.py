from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_logbook_dto import ApiResultResponseLogbookDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    logbook_id: str,
    *,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeAuthorizations"] = include_authorizations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/logbooks/{logbook_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseLogbookDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseLogbookDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseLogbookDTO]:
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
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseLogbookDTO]:
    """Return a full logbook by id

     Not all field are returned, for example authorization filed are filled depending on
    #includeAuthorizations
    parameter that is optiona

    Args:
        logbook_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseLogbookDTO]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        include_authorizations=include_authorizations,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseLogbookDTO]:
    """Return a full logbook by id

     Not all field are returned, for example authorization filed are filled depending on
    #includeAuthorizations
    parameter that is optiona

    Args:
        logbook_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseLogbookDTO
    """

    return sync_detailed(
        logbook_id=logbook_id,
        client=client,
        include_authorizations=include_authorizations,
    ).parsed


async def asyncio_detailed(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseLogbookDTO]:
    """Return a full logbook by id

     Not all field are returned, for example authorization filed are filled depending on
    #includeAuthorizations
    parameter that is optiona

    Args:
        logbook_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseLogbookDTO]
    """

    kwargs = _get_kwargs(
        logbook_id=logbook_id,
        include_authorizations=include_authorizations,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    logbook_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseLogbookDTO]:
    """Return a full logbook by id

     Not all field are returned, for example authorization filed are filled depending on
    #includeAuthorizations
    parameter that is optiona

    Args:
        logbook_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseLogbookDTO
    """

    return (
        await asyncio_detailed(
            logbook_id=logbook_id,
            client=client,
            include_authorizations=include_authorizations,
        )
    ).parsed
