from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.logbook_summary_dto import LogbookSummaryDTO


T = TypeVar("T", bound="LogbookShiftDTO")


@_attrs_define
class LogbookShiftDTO:
    """DTO for the shift creation

    Attributes:
        id (Union[Unset, str]): Unique identifier of the shift
        logbook (Union[Unset, LogbookSummaryDTO]): Identify the single logbooks with essential information
        name (Union[Unset, str]): Is the name of the shift
        from_ (Union[Unset, str]): Is the time where the shift start in the day with the form HH:MM
        to (Union[Unset, str]): Is the time where the shift ends in the day with the form HH:MM
    """

    id: Union[Unset, str] = UNSET
    logbook: Union[Unset, "LogbookSummaryDTO"] = UNSET
    name: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        logbook: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.logbook, Unset):
            logbook = self.logbook.to_dict()

        name = self.name

        from_ = self.from_

        to = self.to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if logbook is not UNSET:
            field_dict["logbook"] = logbook
        if name is not UNSET:
            field_dict["name"] = name
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.logbook_summary_dto import LogbookSummaryDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _logbook = d.pop("logbook", UNSET)
        logbook: Union[Unset, LogbookSummaryDTO]
        if isinstance(_logbook, Unset):
            logbook = UNSET
        else:
            logbook = LogbookSummaryDTO.from_dict(_logbook)

        name = d.pop("name", UNSET)

        from_ = d.pop("from", UNSET)

        to = d.pop("to", UNSET)

        logbook_shift_dto = cls(
            id=id,
            logbook=logbook,
            name=name,
            from_=from_,
            to=to,
        )

        logbook_shift_dto.additional_properties = d
        return logbook_shift_dto

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
