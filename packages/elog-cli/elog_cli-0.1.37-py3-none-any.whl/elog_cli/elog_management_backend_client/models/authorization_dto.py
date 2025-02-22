from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.authorization_dto_authorization_type import AuthorizationDTOAuthorizationType
from ..models.authorization_dto_owner_type import AuthorizationDTOOwnerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthorizationDTO")


@_attrs_define
class AuthorizationDTO:
    """The authorization of the user on the resources returned in the payload

    Attributes:
        id (Union[Unset, str]): Is unique id of the authorizations
        authorization_type (Union[Unset, AuthorizationDTOAuthorizationType]): Is the type of the authorizations [User,
            Group, Application]
        owner (Union[Unset, str]): Is the subject owner of the authorizations
        owner_type (Union[Unset, AuthorizationDTOOwnerType]): Is the type of the owner [User, Group, Application]
        resource (Union[Unset, str]): The resource eof the authorizations
        authority (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    authorization_type: Union[Unset, AuthorizationDTOAuthorizationType] = UNSET
    owner: Union[Unset, str] = UNSET
    owner_type: Union[Unset, AuthorizationDTOOwnerType] = UNSET
    resource: Union[Unset, str] = UNSET
    authority: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        authorization_type: Union[Unset, str] = UNSET
        if not isinstance(self.authorization_type, Unset):
            authorization_type = self.authorization_type.value

        owner = self.owner

        owner_type: Union[Unset, str] = UNSET
        if not isinstance(self.owner_type, Unset):
            owner_type = self.owner_type.value

        resource = self.resource

        authority = self.authority

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if authorization_type is not UNSET:
            field_dict["authorizationType"] = authorization_type
        if owner is not UNSET:
            field_dict["owner"] = owner
        if owner_type is not UNSET:
            field_dict["ownerType"] = owner_type
        if resource is not UNSET:
            field_dict["resource"] = resource
        if authority is not UNSET:
            field_dict["authority"] = authority

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _authorization_type = d.pop("authorizationType", UNSET)
        authorization_type: Union[Unset, AuthorizationDTOAuthorizationType]
        if isinstance(_authorization_type, Unset):
            authorization_type = UNSET
        else:
            authorization_type = AuthorizationDTOAuthorizationType(_authorization_type)

        owner = d.pop("owner", UNSET)

        _owner_type = d.pop("ownerType", UNSET)
        owner_type: Union[Unset, AuthorizationDTOOwnerType]
        if isinstance(_owner_type, Unset):
            owner_type = UNSET
        else:
            owner_type = AuthorizationDTOOwnerType(_owner_type)

        resource = d.pop("resource", UNSET)

        authority = d.pop("authority", UNSET)

        authorization_dto = cls(
            id=id,
            authorization_type=authorization_type,
            owner=owner,
            owner_type=owner_type,
            resource=resource,
            authority=authority,
        )

        authorization_dto.additional_properties = d
        return authorization_dto

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
