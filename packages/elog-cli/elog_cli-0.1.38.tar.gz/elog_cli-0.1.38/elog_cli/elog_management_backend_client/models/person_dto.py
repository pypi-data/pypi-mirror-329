from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PersonDTO")


@_attrs_define
class PersonDTO:
    """The list of members of the local group

    Attributes:
        uid (Union[Unset, str]):
        common_name (Union[Unset, str]):
        surname (Union[Unset, str]):
        gecos (Union[Unset, str]):
        mail (Union[Unset, str]):
    """

    uid: Union[Unset, str] = UNSET
    common_name: Union[Unset, str] = UNSET
    surname: Union[Unset, str] = UNSET
    gecos: Union[Unset, str] = UNSET
    mail: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        common_name = self.common_name

        surname = self.surname

        gecos = self.gecos

        mail = self.mail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uid is not UNSET:
            field_dict["uid"] = uid
        if common_name is not UNSET:
            field_dict["commonName"] = common_name
        if surname is not UNSET:
            field_dict["surname"] = surname
        if gecos is not UNSET:
            field_dict["gecos"] = gecos
        if mail is not UNSET:
            field_dict["mail"] = mail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        uid = d.pop("uid", UNSET)

        common_name = d.pop("commonName", UNSET)

        surname = d.pop("surname", UNSET)

        gecos = d.pop("gecos", UNSET)

        mail = d.pop("mail", UNSET)

        person_dto = cls(
            uid=uid,
            common_name=common_name,
            surname=surname,
            gecos=gecos,
            mail=mail,
        )

        person_dto.additional_properties = d
        return person_dto

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
