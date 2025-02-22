from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.details_authorization_dto import DetailsAuthorizationDTO


T = TypeVar("T", bound="UserDetailsDTO")


@_attrs_define
class UserDetailsDTO:
    """User details

    Attributes:
        id (Union[Unset, str]): The id of the user
        name (Union[Unset, str]): The name of the user
        surname (Union[Unset, str]): The surname of the user
        gecos (Union[Unset, str]): The gecos of the user
        email (Union[Unset, str]): The email of the user
        is_root (Union[Unset, bool]): The user has root role
        can_manage_group (Union[Unset, bool]): The user can manage the groups
        authorizations (Union[Unset, list['DetailsAuthorizationDTO']]): The authorization of the user on elog resources
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    surname: Union[Unset, str] = UNSET
    gecos: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    is_root: Union[Unset, bool] = UNSET
    can_manage_group: Union[Unset, bool] = UNSET
    authorizations: Union[Unset, list["DetailsAuthorizationDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        surname = self.surname

        gecos = self.gecos

        email = self.email

        is_root = self.is_root

        can_manage_group = self.can_manage_group

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
        if surname is not UNSET:
            field_dict["surname"] = surname
        if gecos is not UNSET:
            field_dict["gecos"] = gecos
        if email is not UNSET:
            field_dict["email"] = email
        if is_root is not UNSET:
            field_dict["isRoot"] = is_root
        if can_manage_group is not UNSET:
            field_dict["canManageGroup"] = can_manage_group
        if authorizations is not UNSET:
            field_dict["authorizations"] = authorizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.details_authorization_dto import DetailsAuthorizationDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        surname = d.pop("surname", UNSET)

        gecos = d.pop("gecos", UNSET)

        email = d.pop("email", UNSET)

        is_root = d.pop("isRoot", UNSET)

        can_manage_group = d.pop("canManageGroup", UNSET)

        authorizations = []
        _authorizations = d.pop("authorizations", UNSET)
        for authorizations_item_data in _authorizations or []:
            authorizations_item = DetailsAuthorizationDTO.from_dict(authorizations_item_data)

            authorizations.append(authorizations_item)

        user_details_dto = cls(
            id=id,
            name=name,
            surname=surname,
            gecos=gecos,
            email=email,
            is_root=is_root,
            can_manage_group=can_manage_group,
            authorizations=authorizations,
        )

        user_details_dto.additional_properties = d
        return user_details_dto

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
