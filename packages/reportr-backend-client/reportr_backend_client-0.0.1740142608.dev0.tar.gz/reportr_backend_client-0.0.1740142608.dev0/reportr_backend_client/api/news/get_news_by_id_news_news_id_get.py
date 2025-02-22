from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.news_item_response import NewsItemResponse
from ...types import Response


def _get_kwargs(
    news_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/news/{news_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, NewsItemResponse]]:
    if response.status_code == 200:
        response_200 = NewsItemResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, NewsItemResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    news_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, NewsItemResponse]]:
    """Get News By Id

     Fetch a specific news item by its ID.
    :param news_id: The ID of the news item to retrieve.
    :param news_service: Injected NewsService instance.
    :return: The specific news item or a 404 if not found.

    Args:
        news_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, NewsItemResponse]]
    """

    kwargs = _get_kwargs(
        news_id=news_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    news_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, NewsItemResponse]]:
    """Get News By Id

     Fetch a specific news item by its ID.
    :param news_id: The ID of the news item to retrieve.
    :param news_service: Injected NewsService instance.
    :return: The specific news item or a 404 if not found.

    Args:
        news_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, NewsItemResponse]
    """

    return sync_detailed(
        news_id=news_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    news_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, NewsItemResponse]]:
    """Get News By Id

     Fetch a specific news item by its ID.
    :param news_id: The ID of the news item to retrieve.
    :param news_service: Injected NewsService instance.
    :return: The specific news item or a 404 if not found.

    Args:
        news_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, NewsItemResponse]]
    """

    kwargs = _get_kwargs(
        news_id=news_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    news_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, NewsItemResponse]]:
    """Get News By Id

     Fetch a specific news item by its ID.
    :param news_id: The ID of the news item to retrieve.
    :param news_service: Injected NewsService instance.
    :return: The specific news item or a 404 if not found.

    Args:
        news_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, NewsItemResponse]
    """

    return (
        await asyncio_detailed(
            news_id=news_id,
            client=client,
        )
    ).parsed
