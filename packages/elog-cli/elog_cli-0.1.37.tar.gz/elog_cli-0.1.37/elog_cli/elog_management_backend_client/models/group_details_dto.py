from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.details_authorization_dto import DetailsAuthorizationDTO
    from ..models.user_details_dto import UserDetailsDTO


T = TypeVar("T", bound="GroupDetailsDTO")


@_attrs_define
class GroupDetailsDTO:
    """Group details

    Attributes:
        id (Union[Unset, str]): The id of the group
        name (Union[Unset, str]): The name of the group
        description (Union[Unset, str]): The description of the group
        members (Union[Unset, list['UserDetailsDTO']]): The list of members of the group
        authorizations (Union[Unset, list['DetailsAuthorizationDTO']]): The list of authorizations of the group
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    members: Union[Unset, list["UserDetailsDTO"]] = UNSET
    authorizations: Union[Unset, list["DetailsAuthorizationDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        members: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.members, Unset):
            members = []
            for members_item_data in self.members:
                members_item = members_item_data.to_dict()
                members.append(members_item)

        authorizations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.authorizations, Unset):
            authorizations = []
            for authorizations_item_data in self.authorizations:
                authorizations_item = authorizations_item_data.to_dict()
                authorizations.append(authorizations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if members is not UNSET:
            field_dict["members"] = members
        if authorizations is not UNSET:
            field_dict["authorizations"] = authorizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.details_authorization_dto import DetailsAuthorizationDTO
        from ..models.user_details_dto import UserDetailsDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        members = []
        _members = d.pop("members", UNSET)
        for members_item_data in _members or []:
            members_item = UserDetailsDTO.from_dict(members_item_data)

            members.append(members_item)

        authorizations = []
        _authorizations = d.pop("authorizations", UNSET)
        for authorizations_item_data in _authorizations or []:
            authorizations_item = DetailsAuthorizationDTO.from_dict(authorizations_item_data)

            authorizations.append(authorizations_item)

        group_details_dto = cls(
            id=id,
            name=name,
            description=description,
            members=members,
            authorizations=authorizations,
        )

        group_details_dto.additional_properties = d
        return group_details_dto

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
