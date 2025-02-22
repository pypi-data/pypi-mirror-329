from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.authorization_dto import AuthorizationDTO
    from ..models.person_dto import PersonDTO


T = TypeVar("T", bound="PersonDetailsDTO")


@_attrs_define
class PersonDetailsDTO:
    """Details of a person

    Attributes:
        person (Union[Unset, PersonDTO]): The list of members of the local group
        authorizations (Union[Unset, list['AuthorizationDTO']]): List of authorizations
    """

    person: Union[Unset, "PersonDTO"] = UNSET
    authorizations: Union[Unset, list["AuthorizationDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        person: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.person, Unset):
            person = self.person.to_dict()

        authorizations: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.authorizations, Unset):
            authorizations = []
            for authorizations_item_data in self.authorizations:
                authorizations_item = authorizations_item_data.to_dict()
                authorizations.append(authorizations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if person is not UNSET:
            field_dict["person"] = person
        if authorizations is not UNSET:
            field_dict["authorizations"] = authorizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.authorization_dto import AuthorizationDTO
        from ..models.person_dto import PersonDTO

        d = src_dict.copy()
        _person = d.pop("person", UNSET)
        person: Union[Unset, PersonDTO]
        if isinstance(_person, Unset):
            person = UNSET
        else:
            person = PersonDTO.from_dict(_person)

        authorizations = []
        _authorizations = d.pop("authorizations", UNSET)
        for authorizations_item_data in _authorizations or []:
            authorizations_item = AuthorizationDTO.from_dict(authorizations_item_data)

            authorizations.append(authorizations_item)

        person_details_dto = cls(
            person=person,
            authorizations=authorizations,
        )

        person_details_dto.additional_properties = d
        return person_details_dto

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
