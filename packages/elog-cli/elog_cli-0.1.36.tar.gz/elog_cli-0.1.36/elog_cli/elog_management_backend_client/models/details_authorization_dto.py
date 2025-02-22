from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.details_authorization_dto_owner_type import DetailsAuthorizationDTOOwnerType
from ..models.details_authorization_dto_permission import DetailsAuthorizationDTOPermission
from ..models.details_authorization_dto_resource_type import DetailsAuthorizationDTOResourceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DetailsAuthorizationDTO")


@_attrs_define
class DetailsAuthorizationDTO:
    """Identify a subject of an authorization with a specific level type and resourceType type

    Attributes:
        id (Union[Unset, str]): The id of the authorization
        owner_id (Union[Unset, str]): The ownerId of the authorization
        owner_name (Union[Unset, str]): The owner name of the authorization
        owner_type (Union[Unset, DetailsAuthorizationDTOOwnerType]): The owner type of the authorization [User, Group,
            Token]
        resource_id (Union[Unset, str]): The id of the authorized resourceType
        resource_type (Union[Unset, DetailsAuthorizationDTOResourceType]): The resource type that is authorized
        resource_name (Union[Unset, str]): The name of the authorized resourceType
        permission (Union[Unset, DetailsAuthorizationDTOPermission]): The type of the authorization [Read, Write, Admin]
    """

    id: Union[Unset, str] = UNSET
    owner_id: Union[Unset, str] = UNSET
    owner_name: Union[Unset, str] = UNSET
    owner_type: Union[Unset, DetailsAuthorizationDTOOwnerType] = UNSET
    resource_id: Union[Unset, str] = UNSET
    resource_type: Union[Unset, DetailsAuthorizationDTOResourceType] = UNSET
    resource_name: Union[Unset, str] = UNSET
    permission: Union[Unset, DetailsAuthorizationDTOPermission] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        owner_id = self.owner_id

        owner_name = self.owner_name

        owner_type: Union[Unset, str] = UNSET
        if not isinstance(self.owner_type, Unset):
            owner_type = self.owner_type.value

        resource_id = self.resource_id

        resource_type: Union[Unset, str] = UNSET
        if not isinstance(self.resource_type, Unset):
            resource_type = self.resource_type.value

        resource_name = self.resource_name

        permission: Union[Unset, str] = UNSET
        if not isinstance(self.permission, Unset):
            permission = self.permission.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if owner_id is not UNSET:
            field_dict["ownerId"] = owner_id
        if owner_name is not UNSET:
            field_dict["ownerName"] = owner_name
        if owner_type is not UNSET:
            field_dict["ownerType"] = owner_type
        if resource_id is not UNSET:
            field_dict["resourceId"] = resource_id
        if resource_type is not UNSET:
            field_dict["resourceType"] = resource_type
        if resource_name is not UNSET:
            field_dict["resourceName"] = resource_name
        if permission is not UNSET:
            field_dict["permission"] = permission

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        owner_id = d.pop("ownerId", UNSET)

        owner_name = d.pop("ownerName", UNSET)

        _owner_type = d.pop("ownerType", UNSET)
        owner_type: Union[Unset, DetailsAuthorizationDTOOwnerType]
        if isinstance(_owner_type, Unset):
            owner_type = UNSET
        else:
            owner_type = DetailsAuthorizationDTOOwnerType(_owner_type)

        resource_id = d.pop("resourceId", UNSET)

        _resource_type = d.pop("resourceType", UNSET)
        resource_type: Union[Unset, DetailsAuthorizationDTOResourceType]
        if isinstance(_resource_type, Unset):
            resource_type = UNSET
        else:
            resource_type = DetailsAuthorizationDTOResourceType(_resource_type)

        resource_name = d.pop("resourceName", UNSET)

        _permission = d.pop("permission", UNSET)
        permission: Union[Unset, DetailsAuthorizationDTOPermission]
        if isinstance(_permission, Unset):
            permission = UNSET
        else:
            permission = DetailsAuthorizationDTOPermission(_permission)

        details_authorization_dto = cls(
            id=id,
            owner_id=owner_id,
            owner_name=owner_name,
            owner_type=owner_type,
            resource_id=resource_id,
            resource_type=resource_type,
            resource_name=resource_name,
            permission=permission,
        )

        details_authorization_dto.additional_properties = d
        return details_authorization_dto

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
