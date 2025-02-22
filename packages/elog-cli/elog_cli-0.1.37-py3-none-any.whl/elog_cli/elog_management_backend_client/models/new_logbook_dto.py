from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NewLogbookDTO")


@_attrs_define
class NewLogbookDTO:
    """Identify the single logbooks

    Attributes:
        name (str): The name of the logbook
        read_all (Union[Unset, bool]): The read all open authorization of the logbook
        write_all (Union[Unset, bool]): The write all open authorization of the logbook
    """

    name: str
    read_all: Union[Unset, bool] = UNSET
    write_all: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        read_all = self.read_all

        write_all = self.write_all

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if read_all is not UNSET:
            field_dict["readAll"] = read_all
        if write_all is not UNSET:
            field_dict["writeAll"] = write_all

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        read_all = d.pop("readAll", UNSET)

        write_all = d.pop("writeAll", UNSET)

        new_logbook_dto = cls(
            name=name,
            read_all=read_all,
            write_all=write_all,
        )

        new_logbook_dto.additional_properties = d
        return new_logbook_dto

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
