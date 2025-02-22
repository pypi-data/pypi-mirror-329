from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.shift_dto import ShiftDTO
    from ..models.tag_dto import TagDTO


T = TypeVar("T", bound="UpdateLogbookDTO")


@_attrs_define
class UpdateLogbookDTO:
    """Update a logbooks information

    Attributes:
        name (Union[Unset, str]): The name of the logbooks
        read_all (Union[Unset, bool]): Indicate if the logbook can be read by all
        write_all (Union[Unset, bool]): Indicate if the logbook can be written by all
        tags (Union[Unset, list['TagDTO']]): The tags associated to the logbooks
        shifts (Union[Unset, list['ShiftDTO']]): The shift associated to the logbooks
    """

    name: Union[Unset, str] = UNSET
    read_all: Union[Unset, bool] = UNSET
    write_all: Union[Unset, bool] = UNSET
    tags: Union[Unset, list["TagDTO"]] = UNSET
    shifts: Union[Unset, list["ShiftDTO"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        read_all = self.read_all

        write_all = self.write_all

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if read_all is not UNSET:
            field_dict["readAll"] = read_all
        if write_all is not UNSET:
            field_dict["writeAll"] = write_all
        if tags is not UNSET:
            field_dict["tags"] = tags
        if shifts is not UNSET:
            field_dict["shifts"] = shifts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.shift_dto import ShiftDTO
        from ..models.tag_dto import TagDTO

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        read_all = d.pop("readAll", UNSET)

        write_all = d.pop("writeAll", UNSET)

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

        update_logbook_dto = cls(
            name=name,
            read_all=read_all,
            write_all=write_all,
            tags=tags,
            shifts=shifts,
        )

        update_logbook_dto.additional_properties = d
        return update_logbook_dto

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
