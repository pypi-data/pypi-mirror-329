from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_authorization_dto_owner_type import NewAuthorizationDTOOwnerType
from ..models.new_authorization_dto_permission import NewAuthorizationDTOPermission
from ..models.new_authorization_dto_resource_type import NewAuthorizationDTOResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewAuthorizationDTO")


@_attrs_define
class NewAuthorizationDTO:
    """New authorization for a user on a elog resourceType

    Attributes:
        resource_type (NewAuthorizationDTOResourceType): The resourceType type that need to be authorized
        owner_id (str): The ownerId id of the authorization
        owner_type (NewAuthorizationDTOOwnerType): The ownerId type of the authorization [User, Group, Token]
        permission (NewAuthorizationDTOPermission): The authorization type [Read, Write, Admin]
        resource_id (Union[Unset, str]): The resourceType id that need to be authorized
    """

    resource_type: NewAuthorizationDTOResourceType
    owner_id: str
    owner_type: NewAuthorizationDTOOwnerType
    permission: NewAuthorizationDTOPermission
    resource_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_type = self.resource_type.value

        owner_id = self.owner_id

        owner_type = self.owner_type.value

        permission = self.permission.value

        resource_id = self.resource_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resourceType": resource_type,
                "ownerId": owner_id,
                "ownerType": owner_type,
                "permission": permission,
            }
        )
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        resource_type = NewAuthorizationDTOResourceType(d.pop("resourceType"))

        owner_id = d.pop("ownerId")

        owner_type = NewAuthorizationDTOOwnerType(d.pop("ownerType"))

        permission = NewAuthorizationDTOPermission(d.pop("permission"))

        resource_id = d.pop("resourceId", UNSET)

        new_authorization_dto = cls(
            resource_type=resource_type,
            owner_id=owner_id,
            owner_type=owner_type,
            permission=permission,
            resource_id=resource_id,
        )

        new_authorization_dto.additional_properties = d
        return new_authorization_dto

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
