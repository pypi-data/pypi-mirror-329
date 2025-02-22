from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entry_import_dto import EntryImportDTO


T = TypeVar("T", bound="ImportEntryDTO")


@_attrs_define
class ImportEntryDTO:
    """
    Attributes:
        entry (EntryImportDTO): Is the model for the new ELog creation
        reader_user_ids (Union[Unset, list[str]]):
    """

    entry: "EntryImportDTO"
    reader_user_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry = self.entry.to_dict()

        reader_user_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.reader_user_ids, Unset):
            reader_user_ids = self.reader_user_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entry": entry,
            }
        )
        if reader_user_ids is not UNSET:
            field_dict["readerUserIds"] = reader_user_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_import_dto import EntryImportDTO

        d = src_dict.copy()
        entry = EntryImportDTO.from_dict(d.pop("entry"))

        reader_user_ids = cast(list[str], d.pop("readerUserIds", UNSET))

        import_entry_dto = cls(
            entry=entry,
            reader_user_ids=reader_user_ids,
        )

        import_entry_dto.additional_properties = d
        return import_entry_dto

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
