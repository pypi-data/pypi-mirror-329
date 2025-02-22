import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthenticationTokenDTO")


@_attrs_define
class AuthenticationTokenDTO:
    """The authentication token

    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        email (Union[Unset, str]):
        expiration (Union[Unset, datetime.date]):
        token (Union[Unset, str]):
        application_managed (Union[Unset, bool]):
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.date] = UNSET
    token: Union[Unset, str] = UNSET
    application_managed: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        email = self.email

        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        token = self.token

        application_managed = self.application_managed

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if email is not UNSET:
            field_dict["email"] = email
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if token is not UNSET:
            field_dict["token"] = token
        if application_managed is not UNSET:
            field_dict["applicationManaged"] = application_managed

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        email = d.pop("email", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.date]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration).date()

        token = d.pop("token", UNSET)

        application_managed = d.pop("applicationManaged", UNSET)

        authentication_token_dto = cls(
            id=id,
            name=name,
            email=email,
            expiration=expiration,
            token=token,
            application_managed=application_managed,
        )

        authentication_token_dto.additional_properties = d
        return authentication_token_dto

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
