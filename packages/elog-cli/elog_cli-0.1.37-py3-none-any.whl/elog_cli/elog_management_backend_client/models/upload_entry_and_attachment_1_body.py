import json
from io import BytesIO
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, File, FileJsonType, Unset

if TYPE_CHECKING:
    from ..models.entry_import_dto import EntryImportDTO


T = TypeVar("T", bound="UploadEntryAndAttachment1Body")


@_attrs_define
class UploadEntryAndAttachment1Body:
    """
    Attributes:
        entry (EntryImportDTO): Is the model for the new ELog creation
        files (Union[Unset, list[File]]):
    """

    entry: "EntryImportDTO"
    files: Union[Unset, list[File]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry = self.entry.to_dict()

        files: Union[Unset, list[FileJsonType]] = UNSET
        if not isinstance(self.files, Unset):
            files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_tuple()

                files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "entry": entry,
            }
        )
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        entry = (None, json.dumps(self.entry.to_dict()).encode(), "application/json")

        files: Union[Unset, tuple[None, bytes, str]] = UNSET
        if not isinstance(self.files, Unset):
            _temp_files = []
            for files_item_data in self.files:
                files_item = files_item_data.to_tuple()

                _temp_files.append(files_item)
            files = (None, json.dumps(_temp_files).encode(), "application/json")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "entry": entry,
            }
        )
        if files is not UNSET:
            field_dict["files"] = files

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.entry_import_dto import EntryImportDTO

        d = src_dict.copy()
        entry = EntryImportDTO.from_dict(d.pop("entry"))

        files = []
        _files = d.pop("files", UNSET)
        for files_item_data in _files or []:
            files_item = File(payload=BytesIO(files_item_data))

            files.append(files_item)

        upload_entry_and_attachment_1_body = cls(
            entry=entry,
            files=files,
        )

        upload_entry_and_attachment_1_body.additional_properties = d
        return upload_entry_and_attachment_1_body

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
