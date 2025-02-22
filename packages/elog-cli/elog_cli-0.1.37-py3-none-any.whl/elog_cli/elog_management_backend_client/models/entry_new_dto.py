import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.summarizes_dto import SummarizesDTO


T = TypeVar("T", bound="EntryNewDTO")


@_attrs_define
class EntryNewDTO:
    """Is the new entry that will follow-up the entry identified by the entryId

    Attributes:
        logbooks (list[str]): Is the logbooks where the new log belong
        title (str): The title of the log
        text (str): The content of the log
        note (Union[Unset, str]): Is the general note field
        tags (Union[Unset, list[str]]): The tags describes represent the log
        attachments (Union[Unset, list[str]]): The list of the attachment of the log
        summarizes (Union[Unset, SummarizesDTO]): DTO for shift summarization
        event_at (Union[Unset, datetime.datetime]): The timestamp when the event is occurred
        user_ids_to_notify (Union[Unset, list[str]]): The list user that need to be notify by email
    """

    logbooks: list[str]
    title: str
    text: str
    note: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    attachments: Union[Unset, list[str]] = UNSET
    summarizes: Union[Unset, "SummarizesDTO"] = UNSET
    event_at: Union[Unset, datetime.datetime] = UNSET
    user_ids_to_notify: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logbooks = self.logbooks

        title = self.title

        text = self.text

        note = self.note

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        attachments: Union[Unset, list[str]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = self.attachments

        summarizes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.summarizes, Unset):
            summarizes = self.summarizes.to_dict()

        event_at: Union[Unset, str] = UNSET
        if not isinstance(self.event_at, Unset):
            event_at = self.event_at.isoformat()

        user_ids_to_notify: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_ids_to_notify, Unset):
            user_ids_to_notify = self.user_ids_to_notify

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logbooks": logbooks,
                "title": title,
                "text": text,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if tags is not UNSET:
            field_dict["tags"] = tags
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if summarizes is not UNSET:
            field_dict["summarizes"] = summarizes
        if event_at is not UNSET:
            field_dict["eventAt"] = event_at
        if user_ids_to_notify is not UNSET:
            field_dict["userIdsToNotify"] = user_ids_to_notify

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.summarizes_dto import SummarizesDTO

        d = src_dict.copy()
        logbooks = cast(list[str], d.pop("logbooks"))

        title = d.pop("title")

        text = d.pop("text")

        note = d.pop("note", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        attachments = cast(list[str], d.pop("attachments", UNSET))

        _summarizes = d.pop("summarizes", UNSET)
        summarizes: Union[Unset, SummarizesDTO]
        if isinstance(_summarizes, Unset):
            summarizes = UNSET
        else:
            summarizes = SummarizesDTO.from_dict(_summarizes)

        _event_at = d.pop("eventAt", UNSET)
        event_at: Union[Unset, datetime.datetime]
        if isinstance(_event_at, Unset):
            event_at = UNSET
        else:
            event_at = isoparse(_event_at)

        user_ids_to_notify = cast(list[str], d.pop("userIdsToNotify", UNSET))

        entry_new_dto = cls(
            logbooks=logbooks,
            title=title,
            text=text,
            note=note,
            tags=tags,
            attachments=attachments,
            summarizes=summarizes,
            event_at=event_at,
            user_ids_to_notify=user_ids_to_notify,
        )

        entry_new_dto.additional_properties = d
        return entry_new_dto

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
