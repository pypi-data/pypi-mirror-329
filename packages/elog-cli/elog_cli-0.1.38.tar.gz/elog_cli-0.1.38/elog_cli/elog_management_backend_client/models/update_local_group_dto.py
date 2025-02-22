from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateLocalGroupDTO")


@_attrs_define
class UpdateLocalGroupDTO:
    """
    Attributes:
        name (Union[Unset, str]): The name of the local group
        description (Union[Unset, str]): The description of the local group
        members (Union[Unset, list[str]]): The list of members of the local group
    """

    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    members: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        members: Union[Unset, list[str]] = UNSET
        if not isinstance(self.members, Unset):
            members = self.members

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        members = cast(list[str], d.pop("members", UNSET))

        update_local_group_dto = cls(
            name=name,
            description=description,
            members=members,
        )

        update_local_group_dto.additional_properties = d
        return update_local_group_dto

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
