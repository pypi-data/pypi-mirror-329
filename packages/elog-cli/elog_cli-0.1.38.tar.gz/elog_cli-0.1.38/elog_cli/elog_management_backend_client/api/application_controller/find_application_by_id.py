from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_application_details_dto import ApiResultResponseApplicationDetailsDTO
from ...types import UNSET, Response, Unset


def _get_kwargs(
    application_id: str,
    *,
    include_authorizations: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeAuthorizations"] = include_authorizations

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/applications/{application_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseApplicationDetailsDTO]:
    if response.status_code == 200:
        response_200 = ApiResultResponseApplicationDetailsDTO.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseApplicationDetailsDTO]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseApplicationDetailsDTO]:
    """Find an application details using application id

    Args:
        application_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseApplicationDetailsDTO]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        include_authorizations=include_authorizations,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseApplicationDetailsDTO]:
    """Find an application details using application id

    Args:
        application_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseApplicationDetailsDTO
    """

    return sync_detailed(
        application_id=application_id,
        client=client,
        include_authorizations=include_authorizations,
    ).parsed


async def asyncio_detailed(
    application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Response[ApiResultResponseApplicationDetailsDTO]:
    """Find an application details using application id

    Args:
        application_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseApplicationDetailsDTO]
    """

    kwargs = _get_kwargs(
        application_id=application_id,
        include_authorizations=include_authorizations,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    application_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    include_authorizations: Union[Unset, bool] = UNSET,
) -> Optional[ApiResultResponseApplicationDetailsDTO]:
    """Find an application details using application id

    Args:
        application_id (str):
        include_authorizations (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseApplicationDetailsDTO
    """

    return (
        await asyncio_detailed(
            application_id=application_id,
            client=client,
            include_authorizations=include_authorizations,
        )
    ).parsed
