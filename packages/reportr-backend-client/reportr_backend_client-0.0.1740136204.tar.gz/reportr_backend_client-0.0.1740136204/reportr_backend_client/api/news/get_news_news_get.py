from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.paginated_news_response import PaginatedNewsResponse
from ...models.timestamp_filter import TimestampFilter
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = 1,
    timestamp: TimestampFilter,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    json_timestamp = timestamp.value
    params["timestamp"] = json_timestamp

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/news",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PaginatedNewsResponse]]:
    if response.status_code == 200:
        response_200 = PaginatedNewsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, PaginatedNewsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    timestamp: TimestampFilter,
) -> Response[Union[HTTPValidationError, PaginatedNewsResponse]]:
    """Get News

     Fetches paginated news for a given page and timestamp filter.

    Args:
        page (Union[Unset, int]): Page number (minimum value: 1) Default: 1.
        timestamp (TimestampFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedNewsResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        timestamp=timestamp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    timestamp: TimestampFilter,
) -> Optional[Union[HTTPValidationError, PaginatedNewsResponse]]:
    """Get News

     Fetches paginated news for a given page and timestamp filter.

    Args:
        page (Union[Unset, int]): Page number (minimum value: 1) Default: 1.
        timestamp (TimestampFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedNewsResponse]
    """

    return sync_detailed(
        client=client,
        page=page,
        timestamp=timestamp,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    timestamp: TimestampFilter,
) -> Response[Union[HTTPValidationError, PaginatedNewsResponse]]:
    """Get News

     Fetches paginated news for a given page and timestamp filter.

    Args:
        page (Union[Unset, int]): Page number (minimum value: 1) Default: 1.
        timestamp (TimestampFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PaginatedNewsResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        timestamp=timestamp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = 1,
    timestamp: TimestampFilter,
) -> Optional[Union[HTTPValidationError, PaginatedNewsResponse]]:
    """Get News

     Fetches paginated news for a given page and timestamp filter.

    Args:
        page (Union[Unset, int]): Page number (minimum value: 1) Default: 1.
        timestamp (TimestampFilter):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PaginatedNewsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            timestamp=timestamp,
        )
    ).parsed
