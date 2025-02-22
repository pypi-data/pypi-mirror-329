from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.update_authorization_dto_permission import UpdateAuthorizationDTOPermission
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateAuthorizationDTO")


@_attrs_define
class UpdateAuthorizationDTO:
    """Update authorization information

    Attributes:
        permission (Union[Unset, UpdateAuthorizationDTOPermission]): The authorization type
    """

    permission: Union[Unset, UpdateAuthorizationDTOPermission] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        permission: Union[Unset, str] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, UpdateAuthorizationDTOPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = UpdateAuthorizationDTOPermission(_permission)

        update_authorization_dto = cls(
            permission=permission,
        )

        update_authorization_dto.additional_properties = d
        return update_authorization_dto

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
