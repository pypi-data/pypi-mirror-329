import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewsItemResponse")


@_attrs_define
class NewsItemResponse:
    """
    Attributes:
        published_date (datetime.datetime):
        provider (str):
        news_item_id (str):
        headline (str):
        author (str):
        country (str):
        city (str):
        region (str):
        content (str):
        subheadline (Union[None, Unset, str]):
        word_count (Union[None, Unset, int]):  Default: 0.
        media (Union[Unset, list[str]]):
        topics (Union[Unset, list[str]]):
    """

    published_date: datetime.datetime
    provider: str
    news_item_id: str
    headline: str
    author: str
    country: str
    city: str
    region: str
    content: str
    subheadline: Union[None, Unset, str] = UNSET
    word_count: Union[None, Unset, int] = 0
    media: Union[Unset, list[str]] = UNSET
    topics: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        published_date = self.published_date.isoformat()

        provider = self.provider

        news_item_id = self.news_item_id

        headline = self.headline

        author = self.author

        country = self.country

        city = self.city

        region = self.region

        content = self.content

        subheadline: Union[None, Unset, str]
        if isinstance(self.subheadline, Unset):
            subheadline = UNSET
        else:
            subheadline = self.subheadline

        word_count: Union[None, Unset, int]
        if isinstance(self.word_count, Unset):
            word_count = UNSET
        else:
            word_count = self.word_count

        media: Union[Unset, list[str]] = UNSET
        if not isinstance(self.media, Unset):
            media = self.media

        topics: Union[Unset, list[str]] = UNSET
        if not isinstance(self.topics, Unset):
            topics = self.topics

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "published_date": published_date,
                "provider": provider,
                "news_item_id": news_item_id,
                "headline": headline,
                "author": author,
                "country": country,
                "city": city,
                "region": region,
                "content": content,
            }
        )
        if subheadline is not UNSET:
            field_dict["subheadline"] = subheadline
        if word_count is not UNSET:
            field_dict["word_count"] = word_count
        if media is not UNSET:
            field_dict["media"] = media
        if topics is not UNSET:
            field_dict["topics"] = topics

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        published_date = isoparse(d.pop("published_date"))

        provider = d.pop("provider")

        news_item_id = d.pop("news_item_id")

        headline = d.pop("headline")

        author = d.pop("author")

        country = d.pop("country")

        city = d.pop("city")

        region = d.pop("region")

        content = d.pop("content")

        def _parse_subheadline(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subheadline = _parse_subheadline(d.pop("subheadline", UNSET))

        def _parse_word_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        word_count = _parse_word_count(d.pop("word_count", UNSET))

        media = cast(list[str], d.pop("media", UNSET))

        topics = cast(list[str], d.pop("topics", UNSET))

        news_item_response = cls(
            published_date=published_date,
            provider=provider,
            news_item_id=news_item_id,
            headline=headline,
            author=author,
            country=country,
            city=city,
            region=region,
            content=content,
            subheadline=subheadline,
            word_count=word_count,
            media=media,
            topics=topics,
        )

        news_item_response.additional_properties = d
        return news_item_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
