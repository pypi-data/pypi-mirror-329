import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_list_entry_summary_dto import ApiResultResponseListEntrySummaryDTO
from ...models.authorization_cache import AuthorizationCache
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    authorization_cache: "AuthorizationCache",
    anchor: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,
    last_n_shifts: Union[Unset, int] = UNSET,
    context_size: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    tags: Union[Unset, list[str]] = UNSET,
    logbooks: Union[Unset, list[str]] = UNSET,
    authors: Union[Unset, list[str]] = UNSET,
    sort_by_log_date: Union[Unset, bool] = False,
    hide_summaries: Union[Unset, bool] = False,
    require_all_tags: Union[Unset, bool] = False,
    origin_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_authorization_cache = authorization_cache.to_dict()
    params.update(json_authorization_cache)

    params["anchor"] = anchor

    json_start_date: Union[Unset, str] = UNSET
    if not isinstance(start_date, Unset):
        json_start_date = start_date.isoformat()
    params["startDate"] = json_start_date

    json_end_date: Union[Unset, str] = UNSET
    if not isinstance(end_date, Unset):
        json_end_date = end_date.isoformat()
    params["endDate"] = json_end_date

    params["lastNShifts"] = last_n_shifts

    params["contextSize"] = context_size

    params["limit"] = limit

    params["search"] = search

    json_tags: Union[Unset, list[str]] = UNSET
    if not isinstance(tags, Unset):
        json_tags = tags

    params["tags"] = json_tags

    json_logbooks: Union[Unset, list[str]] = UNSET
    if not isinstance(logbooks, Unset):
        json_logbooks = logbooks

    params["logbooks"] = json_logbooks

    json_authors: Union[Unset, list[str]] = UNSET
    if not isinstance(authors, Unset):
        json_authors = authors

    params["authors"] = json_authors

    params["sortByLogDate"] = sort_by_log_date

    params["hideSummaries"] = hide_summaries

    params["requireAllTags"] = require_all_tags

    params["originId"] = origin_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/entries",
        "params": params,
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
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    anchor: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,
    last_n_shifts: Union[Unset, int] = UNSET,
    context_size: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    tags: Union[Unset, list[str]] = UNSET,
    logbooks: Union[Unset, list[str]] = UNSET,
    authors: Union[Unset, list[str]] = UNSET,
    sort_by_log_date: Union[Unset, bool] = False,
    hide_summaries: Union[Unset, bool] = False,
    require_all_tags: Union[Unset, bool] = False,
    origin_id: Union[Unset, str] = UNSET,
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Perform the query on all log data

    Args:
        authorization_cache (AuthorizationCache):
        anchor (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        last_n_shifts (Union[Unset, int]):
        context_size (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        logbooks (Union[Unset, list[str]]):
        authors (Union[Unset, list[str]]):
        sort_by_log_date (Union[Unset, bool]):  Default: False.
        hide_summaries (Union[Unset, bool]):  Default: False.
        require_all_tags (Union[Unset, bool]):  Default: False.
        origin_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        authorization_cache=authorization_cache,
        anchor=anchor,
        start_date=start_date,
        end_date=end_date,
        last_n_shifts=last_n_shifts,
        context_size=context_size,
        limit=limit,
        search=search,
        tags=tags,
        logbooks=logbooks,
        authors=authors,
        sort_by_log_date=sort_by_log_date,
        hide_summaries=hide_summaries,
        require_all_tags=require_all_tags,
        origin_id=origin_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    anchor: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,
    last_n_shifts: Union[Unset, int] = UNSET,
    context_size: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    tags: Union[Unset, list[str]] = UNSET,
    logbooks: Union[Unset, list[str]] = UNSET,
    authors: Union[Unset, list[str]] = UNSET,
    sort_by_log_date: Union[Unset, bool] = False,
    hide_summaries: Union[Unset, bool] = False,
    require_all_tags: Union[Unset, bool] = False,
    origin_id: Union[Unset, str] = UNSET,
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Perform the query on all log data

    Args:
        authorization_cache (AuthorizationCache):
        anchor (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        last_n_shifts (Union[Unset, int]):
        context_size (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        logbooks (Union[Unset, list[str]]):
        authors (Union[Unset, list[str]]):
        sort_by_log_date (Union[Unset, bool]):  Default: False.
        hide_summaries (Union[Unset, bool]):  Default: False.
        require_all_tags (Union[Unset, bool]):  Default: False.
        origin_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListEntrySummaryDTO
    """

    return sync_detailed(
        client=client,
        authorization_cache=authorization_cache,
        anchor=anchor,
        start_date=start_date,
        end_date=end_date,
        last_n_shifts=last_n_shifts,
        context_size=context_size,
        limit=limit,
        search=search,
        tags=tags,
        logbooks=logbooks,
        authors=authors,
        sort_by_log_date=sort_by_log_date,
        hide_summaries=hide_summaries,
        require_all_tags=require_all_tags,
        origin_id=origin_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    anchor: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,
    last_n_shifts: Union[Unset, int] = UNSET,
    context_size: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    tags: Union[Unset, list[str]] = UNSET,
    logbooks: Union[Unset, list[str]] = UNSET,
    authors: Union[Unset, list[str]] = UNSET,
    sort_by_log_date: Union[Unset, bool] = False,
    hide_summaries: Union[Unset, bool] = False,
    require_all_tags: Union[Unset, bool] = False,
    origin_id: Union[Unset, str] = UNSET,
) -> Response[ApiResultResponseListEntrySummaryDTO]:
    """Perform the query on all log data

    Args:
        authorization_cache (AuthorizationCache):
        anchor (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        last_n_shifts (Union[Unset, int]):
        context_size (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        logbooks (Union[Unset, list[str]]):
        authors (Union[Unset, list[str]]):
        sort_by_log_date (Union[Unset, bool]):  Default: False.
        hide_summaries (Union[Unset, bool]):  Default: False.
        require_all_tags (Union[Unset, bool]):  Default: False.
        origin_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseListEntrySummaryDTO]
    """

    kwargs = _get_kwargs(
        authorization_cache=authorization_cache,
        anchor=anchor,
        start_date=start_date,
        end_date=end_date,
        last_n_shifts=last_n_shifts,
        context_size=context_size,
        limit=limit,
        search=search,
        tags=tags,
        logbooks=logbooks,
        authors=authors,
        sort_by_log_date=sort_by_log_date,
        hide_summaries=hide_summaries,
        require_all_tags=require_all_tags,
        origin_id=origin_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    authorization_cache: "AuthorizationCache",
    anchor: Union[Unset, str] = UNSET,
    start_date: Union[Unset, datetime.datetime] = UNSET,
    end_date: Union[Unset, datetime.datetime] = UNSET,
    last_n_shifts: Union[Unset, int] = UNSET,
    context_size: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    search: Union[Unset, str] = UNSET,
    tags: Union[Unset, list[str]] = UNSET,
    logbooks: Union[Unset, list[str]] = UNSET,
    authors: Union[Unset, list[str]] = UNSET,
    sort_by_log_date: Union[Unset, bool] = False,
    hide_summaries: Union[Unset, bool] = False,
    require_all_tags: Union[Unset, bool] = False,
    origin_id: Union[Unset, str] = UNSET,
) -> Optional[ApiResultResponseListEntrySummaryDTO]:
    """Perform the query on all log data

    Args:
        authorization_cache (AuthorizationCache):
        anchor (Union[Unset, str]):
        start_date (Union[Unset, datetime.datetime]):
        end_date (Union[Unset, datetime.datetime]):
        last_n_shifts (Union[Unset, int]):
        context_size (Union[Unset, int]):
        limit (Union[Unset, int]):
        search (Union[Unset, str]):
        tags (Union[Unset, list[str]]):
        logbooks (Union[Unset, list[str]]):
        authors (Union[Unset, list[str]]):
        sort_by_log_date (Union[Unset, bool]):  Default: False.
        hide_summaries (Union[Unset, bool]):  Default: False.
        require_all_tags (Union[Unset, bool]):  Default: False.
        origin_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseListEntrySummaryDTO
    """

    return (
        await asyncio_detailed(
            client=client,
            authorization_cache=authorization_cache,
            anchor=anchor,
            start_date=start_date,
            end_date=end_date,
            last_n_shifts=last_n_shifts,
            context_size=context_size,
            limit=limit,
            search=search,
            tags=tags,
            logbooks=logbooks,
            authors=authors,
            sort_by_log_date=sort_by_log_date,
            hide_summaries=hide_summaries,
            require_all_tags=require_all_tags,
            origin_id=origin_id,
        )
    ).parsed
