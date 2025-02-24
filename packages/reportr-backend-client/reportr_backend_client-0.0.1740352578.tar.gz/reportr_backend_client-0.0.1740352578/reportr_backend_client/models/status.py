from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Status")


@_attrs_define
class Status:
    """
    Attributes:
        healthy (Union[None, Unset, bool]):
        ready (Union[None, Unset, bool]):
        current_version (Union[None, Unset, str]):
        expected_version (Union[None, Unset, str]):
    """

    healthy: Union[None, Unset, bool] = UNSET
    ready: Union[None, Unset, bool] = UNSET
    current_version: Union[None, Unset, str] = UNSET
    expected_version: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        healthy: Union[None, Unset, bool]
        if isinstance(self.healthy, Unset):
            healthy = UNSET
        else:
            healthy = self.healthy

        ready: Union[None, Unset, bool]
        if isinstance(self.ready, Unset):
            ready = UNSET
        else:
            ready = self.ready

        current_version: Union[None, Unset, str]
        if isinstance(self.current_version, Unset):
            current_version = UNSET
        else:
            current_version = self.current_version

        expected_version: Union[None, Unset, str]
        if isinstance(self.expected_version, Unset):
            expected_version = UNSET
        else:
            expected_version = self.expected_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if healthy is not UNSET:
            field_dict["healthy"] = healthy
        if ready is not UNSET:
            field_dict["ready"] = ready
        if current_version is not UNSET:
            field_dict["current_version"] = current_version
        if expected_version is not UNSET:
            field_dict["expected_version"] = expected_version

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_healthy(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        healthy = _parse_healthy(d.pop("healthy", UNSET))

        def _parse_ready(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        ready = _parse_ready(d.pop("ready", UNSET))

        def _parse_current_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        current_version = _parse_current_version(d.pop("current_version", UNSET))

        def _parse_expected_version(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        expected_version = _parse_expected_version(d.pop("expected_version", UNSET))

        status = cls(
            healthy=healthy,
            ready=ready,
            current_version=current_version,
            expected_version=expected_version,
        )

        status.additional_properties = d
        return status

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
