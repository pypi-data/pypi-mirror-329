from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.person_dto import PersonDTO


T = TypeVar("T", bound="UserGroupManagementAuthorizationLevel")


@_attrs_define
class UserGroupManagementAuthorizationLevel:
    """Is the value returned by api

    Attributes:
        user (Union[Unset, PersonDTO]): The list of members of the local group
        can_manage_group (Union[Unset, bool]):
    """

    user: Union[Unset, "PersonDTO"] = UNSET
    can_manage_group: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        can_manage_group = self.can_manage_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if can_manage_group is not UNSET:
            field_dict["canManageGroup"] = can_manage_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.person_dto import PersonDTO

        d = src_dict.copy()
        _user = d.pop("user", UNSET)
        user: Union[Unset, PersonDTO]
        if isinstance(_user, Unset):
            user = UNSET
        else:
            user = PersonDTO.from_dict(_user)

        can_manage_group = d.pop("canManageGroup", UNSET)

        user_group_management_authorization_level = cls(
            user=user,
            can_manage_group=can_manage_group,
        )

        user_group_management_authorization_level.additional_properties = d
        return user_group_management_authorization_level

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
