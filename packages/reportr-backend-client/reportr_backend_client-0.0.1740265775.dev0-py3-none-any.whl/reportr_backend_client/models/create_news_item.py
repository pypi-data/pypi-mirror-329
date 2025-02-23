import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateNewsItem")


@_attrs_define
class CreateNewsItem:
    """
    Attributes:
        published_date (datetime.datetime):
        provider (str):
        news_item_id (str):
        headline (str):
        author (str):
        country (str):
        content (str):
        media (list[str]):
        topics (list[str]):
        subheadline (Union[None, Unset, str]):
        city (Union[None, Unset, str]):
        region (Union[None, Unset, str]):
        word_count (Union[None, Unset, int]):
    """

    published_date: datetime.datetime
    provider: str
    news_item_id: str
    headline: str
    author: str
    country: str
    content: str
    media: list[str]
    topics: list[str]
    subheadline: Union[None, Unset, str] = UNSET
    city: Union[None, Unset, str] = UNSET
    region: Union[None, Unset, str] = UNSET
    word_count: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        published_date = self.published_date.isoformat()

        provider = self.provider

        news_item_id = self.news_item_id

        headline = self.headline

        author = self.author

        country = self.country

        content = self.content

        media = self.media

        topics = self.topics

        subheadline: Union[None, Unset, str]
        if isinstance(self.subheadline, Unset):
            subheadline = UNSET
        else:
            subheadline = self.subheadline

        city: Union[None, Unset, str]
        if isinstance(self.city, Unset):
            city = UNSET
        else:
            city = self.city

        region: Union[None, Unset, str]
        if isinstance(self.region, Unset):
            region = UNSET
        else:
            region = self.region

        word_count: Union[None, Unset, int]
        if isinstance(self.word_count, Unset):
            word_count = UNSET
        else:
            word_count = self.word_count

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
                "content": content,
                "media": media,
                "topics": topics,
            }
        )
        if subheadline is not UNSET:
            field_dict["subheadline"] = subheadline
        if city is not UNSET:
            field_dict["city"] = city
        if region is not UNSET:
            field_dict["region"] = region
        if word_count is not UNSET:
            field_dict["word_count"] = word_count

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

        content = d.pop("content")

        media = cast(list[str], d.pop("media"))

        topics = cast(list[str], d.pop("topics"))

        def _parse_subheadline(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        subheadline = _parse_subheadline(d.pop("subheadline", UNSET))

        def _parse_city(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        city = _parse_city(d.pop("city", UNSET))

        def _parse_region(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        region = _parse_region(d.pop("region", UNSET))

        def _parse_word_count(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        word_count = _parse_word_count(d.pop("word_count", UNSET))

        create_news_item = cls(
            published_date=published_date,
            provider=provider,
            news_item_id=news_item_id,
            headline=headline,
            author=author,
            country=country,
            content=content,
            media=media,
            topics=topics,
            subheadline=subheadline,
            city=city,
            region=region,
            word_count=word_count,
        )

        create_news_item.additional_properties = d
        return create_news_item

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
