from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.create_news_item import CreateNewsItem


T = TypeVar("T", bound="PaginatedNewsResponse")


@_attrs_define
class PaginatedNewsResponse:
    """
    Attributes:
        page (int):
        page_size (int):
        total_pages (int):
        total_items (int):
        news (list['CreateNewsItem']):
    """

    page: int
    page_size: int
    total_pages: int
    total_items: int
    news: list["CreateNewsItem"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        page_size = self.page_size

        total_pages = self.total_pages

        total_items = self.total_items

        news = []
        for news_item_data in self.news:
            news_item = news_item_data.to_dict()
            news.append(news_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages,
                "total_items": total_items,
                "news": news,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_news_item import CreateNewsItem

        d = src_dict.copy()
        page = d.pop("page")

        page_size = d.pop("page_size")

        total_pages = d.pop("total_pages")

        total_items = d.pop("total_items")

        news = []
        _news = d.pop("news")
        for news_item_data in _news:
            news_item = CreateNewsItem.from_dict(news_item_data)

            news.append(news_item)

        paginated_news_response = cls(
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            total_items=total_items,
            news=news,
        )

        paginated_news_response.additional_properties = d
        return paginated_news_response

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
