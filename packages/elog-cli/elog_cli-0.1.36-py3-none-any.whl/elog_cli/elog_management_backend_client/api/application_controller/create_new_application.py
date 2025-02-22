from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...models.new_application_dto import NewApplicationDTO
from ...types import Response


def _get_kwargs(
    *,
    body: NewApplicationDTO,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/applications",
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
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewApplicationDTO,
) -> Response[ApiResultResponseString]:
    """Create new authentication token

     Create a new application, an application is created along with a jwt token that permit to access the
    REST without the needs of a user/password
    it should be submitted in the http header along with the http request

    Args:
        body (NewApplicationDTO): Are the information to create the a new application

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewApplicationDTO,
) -> Optional[ApiResultResponseString]:
    """Create new authentication token

     Create a new application, an application is created along with a jwt token that permit to access the
    REST without the needs of a user/password
    it should be submitted in the http header along with the http request

    Args:
        body (NewApplicationDTO): Are the information to create the a new application

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewApplicationDTO,
) -> Response[ApiResultResponseString]:
    """Create new authentication token

     Create a new application, an application is created along with a jwt token that permit to access the
    REST without the needs of a user/password
    it should be submitted in the http header along with the http request

    Args:
        body (NewApplicationDTO): Are the information to create the a new application

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: NewApplicationDTO,
) -> Optional[ApiResultResponseString]:
    """Create new authentication token

     Create a new application, an application is created along with a jwt token that permit to access the
    REST without the needs of a user/password
    it should be submitted in the http header along with the http request

    Args:
        body (NewApplicationDTO): Are the information to create the a new application

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
