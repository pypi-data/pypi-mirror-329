from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.logbook_summary_dto import LogbookSummaryDTO


T = TypeVar("T", bound="TagDTO")


@_attrs_define
class TagDTO:
    """DTO for the tags

    Attributes:
        id (Union[Unset, str]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        logbook (Union[Unset, LogbookSummaryDTO]): Identify the single logbooks with essential information
    """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    logbook: Union[Unset, "LogbookSummaryDTO"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        logbook: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.logbook, Unset):
            logbook = self.logbook.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if logbook is not UNSET:
            field_dict["logbook"] = logbook

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.logbook_summary_dto import LogbookSummaryDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        _logbook = d.pop("logbook", UNSET)
        logbook: Union[Unset, LogbookSummaryDTO]
        if isinstance(_logbook, Unset):
            logbook = UNSET
        else:
            logbook = LogbookSummaryDTO.from_dict(_logbook)

        tag_dto = cls(
            id=id,
            name=name,
            description=description,
            logbook=logbook,
        )

        tag_dto.additional_properties = d
        return tag_dto

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
