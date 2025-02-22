from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.details_authorization_dto import DetailsAuthorizationDTO
    from ..models.shift_dto import ShiftDTO
    from ..models.tag_dto import TagDTO


T = TypeVar("T", bound="LogbookDTO")


@_attrs_define
class LogbookDTO:
    """Identify the single logbooks

    Attributes:
        id (Union[Unset, str]): Unique identifier
        name (Union[Unset, str]): The name of the logbooks
        tags (Union[Unset, list['TagDTO']]): The tags associated to the logbooks
        shifts (Union[Unset, list['ShiftDTO']]): The shift associated to the logbooks
        read_all (Union[Unset, bool]): Indicate if the logbook entries can be read by all
        write_all (Union[Unset, bool]): Indicate if the logbook entries can be created by all
        authorizations (Union[Unset, list['DetailsAuthorizationDTO']]): The list of authorizations on logbook
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    tags: Union[Unset, list["TagDTO"]] = UNSET
    shifts: Union[Unset, list["ShiftDTO"]] = UNSET
    read_all: Union[Unset, bool] = UNSET
    write_all: Union[Unset, bool] = UNSET
    authorizations: Union[Unset, list["DetailsAuthorizationDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        shifts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.shifts, Unset):
            shifts = []
            for shifts_item_data in self.shifts:
                shifts_item = shifts_item_data.to_dict()
                shifts.append(shifts_item)

        read_all = self.read_all

        write_all = self.write_all

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
        if tags is not UNSET:
            field_dict["tags"] = tags
        if shifts is not UNSET:
            field_dict["shifts"] = shifts
        if read_all is not UNSET:
            field_dict["readAll"] = read_all
        if write_all is not UNSET:
            field_dict["writeAll"] = write_all
        if authorizations is not UNSET:
            field_dict["authorizations"] = authorizations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.details_authorization_dto import DetailsAuthorizationDTO
        from ..models.shift_dto import ShiftDTO
        from ..models.tag_dto import TagDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = TagDTO.from_dict(tags_item_data)

            tags.append(tags_item)

        shifts = []
        _shifts = d.pop("shifts", UNSET)
        for shifts_item_data in _shifts or []:
            shifts_item = ShiftDTO.from_dict(shifts_item_data)

            shifts.append(shifts_item)

        read_all = d.pop("readAll", UNSET)

        write_all = d.pop("writeAll", UNSET)

        authorizations = []
        _authorizations = d.pop("authorizations", UNSET)
        for authorizations_item_data in _authorizations or []:
            authorizations_item = DetailsAuthorizationDTO.from_dict(authorizations_item_data)

            authorizations.append(authorizations_item)

        logbook_dto = cls(
            id=id,
            name=name,
            tags=tags,
            shifts=shifts,
            read_all=read_all,
            write_all=write_all,
            authorizations=authorizations,
        )

        logbook_dto.additional_properties = d
        return logbook_dto

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
