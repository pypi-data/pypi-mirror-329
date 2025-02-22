import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.details_authorization_dto import DetailsAuthorizationDTO


T = TypeVar("T", bound="ApplicationDetailsDTO")


@_attrs_define
class ApplicationDetailsDTO:
    """Application details

    Attributes:
        id (Union[Unset, str]): The id of the application
        name (Union[Unset, str]): The name of the application
        email (Union[Unset, str]): The description of the application
        token (Union[Unset, str]): The token of the application
        expiration (Union[Unset, datetime.date]): The expiration of the token
        application_managed (Union[Unset, bool]): True if the application is managed internally by the backend
        authorizations (Union[Unset, list['DetailsAuthorizationDTO']]): The list of authorizations of the application
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    email: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    expiration: Union[Unset, datetime.date] = UNSET
    application_managed: Union[Unset, bool] = UNSET
    authorizations: Union[Unset, list["DetailsAuthorizationDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        email = self.email

        token = self.token

        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        application_managed = self.application_managed

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
        if email is not UNSET:
            field_dict["email"] = email
        if token is not UNSET:
            field_dict["token"] = token
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if application_managed is not UNSET:
            field_dict["applicationManaged"] = application_managed
        if authorizations is not UNSET:
            field_dict["authorizations"] = authorizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.details_authorization_dto import DetailsAuthorizationDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        email = d.pop("email", UNSET)

        token = d.pop("token", UNSET)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.date]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration).date()

        application_managed = d.pop("applicationManaged", UNSET)

        authorizations = []
        _authorizations = d.pop("authorizations", UNSET)
        for authorizations_item_data in _authorizations or []:
            authorizations_item = DetailsAuthorizationDTO.from_dict(authorizations_item_data)

            authorizations.append(authorizations_item)

        application_details_dto = cls(
            id=id,
            name=name,
            email=email,
            token=token,
            expiration=expiration,
            application_managed=application_managed,
            authorizations=authorizations,
        )

        application_details_dto.additional_properties = d
        return application_details_dto

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
