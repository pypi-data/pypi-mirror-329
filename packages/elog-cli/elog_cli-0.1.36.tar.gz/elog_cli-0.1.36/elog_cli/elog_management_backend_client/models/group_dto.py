from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GroupDTO")


@_attrs_define
class GroupDTO:
    """The group of the user

    Attributes:
        uid (Union[Unset, str]):
        common_name (Union[Unset, str]):
    """

    uid: Union[Unset, str] = UNSET
    common_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        common_name = self.common_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uid is not UNSET:
            field_dict["uid"] = uid
        if common_name is not UNSET:
            field_dict["commonName"] = common_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid", UNSET)

        common_name = d.pop("commonName", UNSET)

        group_dto = cls(
            uid=uid,
            common_name=common_name,
        )

        group_dto.additional_properties = d
        return group_dto

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
