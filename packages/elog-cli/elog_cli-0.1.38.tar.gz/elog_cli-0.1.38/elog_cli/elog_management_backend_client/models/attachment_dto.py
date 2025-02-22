from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AttachmentDTO")


@_attrs_define
class AttachmentDTO:
    """Is the description fo an attachment

    Attributes:
        id (Union[Unset, str]): The id of the attachment
        file_name (Union[Unset, str]): The name of the file
        content_type (Union[Unset, str]): The content type of the file
        preview_state (Union[Unset, str]): The state of the preview processing
        mini_preview (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    file_name: Union[Unset, str] = UNSET
    content_type: Union[Unset, str] = UNSET
    preview_state: Union[Unset, str] = UNSET
    mini_preview: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        file_name = self.file_name

        content_type = self.content_type

        preview_state = self.preview_state

        mini_preview = self.mini_preview

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if content_type is not UNSET:
            field_dict["contentType"] = content_type
        if preview_state is not UNSET:
            field_dict["previewState"] = preview_state
        if mini_preview is not UNSET:
            field_dict["miniPreview"] = mini_preview

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        file_name = d.pop("fileName", UNSET)

        content_type = d.pop("contentType", UNSET)

        preview_state = d.pop("previewState", UNSET)

        mini_preview = d.pop("miniPreview", UNSET)

        attachment_dto = cls(
            id=id,
            file_name=file_name,
            content_type=content_type,
            preview_state=preview_state,
            mini_preview=mini_preview,
        )

        attachment_dto.additional_properties = d
        return attachment_dto

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
