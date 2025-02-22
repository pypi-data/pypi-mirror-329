from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_logbook_dto import ApiResultResponseListLogbookDTO
from ...models.get_all_logbook_filter_for_authorization_types import GetAllLogbookFilterForAuthorizationTypes
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_authorizations: Union[Unset, bool] = UNSET,
    filter_for_authorization_types: Union[Unset, GetAllLogbookFilterForAuthorizationTypes] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeAuthorizations"] = include_authorizations

    json_filter_for_authorization_types: Union[Unset, str] = UNSET
    if not isinstance(filter_for_authorization_types, Unset):
        json_filter_for_authorization_types = filter_for_authorization_types.value

    params["filterForAuthorizationTypes"] = json_filter_for_authorization_types

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/logbooks",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseListLogbookDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseListLogbookDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseListLogbookDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    filter_for_authorization_types: Union[Unset, GetAllLogbookFilterForAuthorizationTypes] = UNSET,
) -> Response[ApiResultResponseListLogbookDTO]:
    """Return all authorized logbook

    Args:
        include_authorizations (Union[Unset, bool]):
        filter_for_authorization_types (Union[Unset, GetAllLogbookFilterForAuthorizationTypes]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListLogbookDTO]
    """

    kwargs = _get_kwargs(
        include_authorizations=include_authorizations,
        filter_for_authorization_types=filter_for_authorization_types,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    filter_for_authorization_types: Union[Unset, GetAllLogbookFilterForAuthorizationTypes] = UNSET,
) -> Optional[ApiResultResponseListLogbookDTO]:
    """Return all authorized logbook

    Args:
        include_authorizations (Union[Unset, bool]):
        filter_for_authorization_types (Union[Unset, GetAllLogbookFilterForAuthorizationTypes]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListLogbookDTO
    """

    return sync_detailed(
        client=client,
        include_authorizations=include_authorizations,
        filter_for_authorization_types=filter_for_authorization_types,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    filter_for_authorization_types: Union[Unset, GetAllLogbookFilterForAuthorizationTypes] = UNSET,
) -> Response[ApiResultResponseListLogbookDTO]:
    """Return all authorized logbook

    Args:
        include_authorizations (Union[Unset, bool]):
        filter_for_authorization_types (Union[Unset, GetAllLogbookFilterForAuthorizationTypes]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListLogbookDTO]
    """

    kwargs = _get_kwargs(
        include_authorizations=include_authorizations,
        filter_for_authorization_types=filter_for_authorization_types,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
    filter_for_authorization_types: Union[Unset, GetAllLogbookFilterForAuthorizationTypes] = UNSET,
) -> Optional[ApiResultResponseListLogbookDTO]:
    """Return all authorized logbook

    Args:
        include_authorizations (Union[Unset, bool]):
        filter_for_authorization_types (Union[Unset, GetAllLogbookFilterForAuthorizationTypes]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListLogbookDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            include_authorizations=include_authorizations,
            filter_for_authorization_types=filter_for_authorization_types,
        )
    ).parsed
