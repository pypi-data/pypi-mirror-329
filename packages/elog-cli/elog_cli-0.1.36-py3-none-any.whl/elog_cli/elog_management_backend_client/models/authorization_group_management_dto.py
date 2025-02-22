from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthorizationGroupManagementDTO")


@_attrs_define
class AuthorizationGroupManagementDTO:
    """Group management authorization

    Attributes:
        add_users (Union[Unset, list[str]]): List of the user to add as authorized to manage group
        remove_users (Union[Unset, list[str]]): List of the user to remove as authorized to manage group
    """

    add_users: Union[Unset, list[str]] = UNSET
    remove_users: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        add_users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.add_users, Unset):
            add_users = self.add_users

        remove_users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.remove_users, Unset):
            remove_users = self.remove_users

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if add_users is not UNSET:
            field_dict["addUsers"] = add_users
        if remove_users is not UNSET:
            field_dict["removeUsers"] = remove_users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        add_users = cast(list[str], d.pop("addUsers", UNSET))

        remove_users = cast(list[str], d.pop("removeUsers", UNSET))

        authorization_group_management_dto = cls(
            add_users=add_users,
            remove_users=remove_users,
        )

        authorization_group_management_dto.additional_properties = d
        return authorization_group_management_dto

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
