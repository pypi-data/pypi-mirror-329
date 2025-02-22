import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.summarizes_dto import SummarizesDTO


T = TypeVar("T", bound="NewEntryDTO")


@_attrs_define
class NewEntryDTO:
    """Is the model for the new entry creation using name on logbook and tags instead id

    Attributes:
        logbooks (list[str]): Are the logbooks name where the new log entry belong
        title (str): The title of the log
        text (str): The content of the log
        note (Union[Unset, str]): Is the general note field
        tags (Union[Unset, list[str]]): The tags label that describes entry on each logbook
        summarizes (Union[Unset, SummarizesDTO]): DTO for shift summarization
        event_at (Union[Unset, datetime.datetime]): The timestamp when the event is occurred
        user_ids_to_notify (Union[Unset, list[str]]): The list user that need to be notify by email
        user_creator_id (Union[Unset, str]): Use this field to create a new entry on behalf of another user
        supersede_of (Union[Unset, str]): The entry id that this entry will supersede
    """

    logbooks: list[str]
    title: str
    text: str
    note: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    summarizes: Union[Unset, "SummarizesDTO"] = UNSET
    event_at: Union[Unset, datetime.datetime] = UNSET
    user_ids_to_notify: Union[Unset, list[str]] = UNSET
    user_creator_id: Union[Unset, str] = UNSET
    supersede_of: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logbooks = self.logbooks

        title = self.title

        text = self.text

        note = self.note

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        summarizes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.summarizes, Unset):
            summarizes = self.summarizes.to_dict()

        event_at: Union[Unset, str] = UNSET
        if not isinstance(self.event_at, Unset):
            event_at = self.event_at.isoformat()

        user_ids_to_notify: Union[Unset, list[str]] = UNSET
        if not isinstance(self.user_ids_to_notify, Unset):
            user_ids_to_notify = self.user_ids_to_notify

        user_creator_id = self.user_creator_id

        supersede_of = self.supersede_of

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
        if summarizes is not UNSET:
            field_dict["summarizes"] = summarizes
        if event_at is not UNSET:
            field_dict["eventAt"] = event_at
        if user_ids_to_notify is not UNSET:
            field_dict["userIdsToNotify"] = user_ids_to_notify
        if user_creator_id is not UNSET:
            field_dict["userCreatorId"] = user_creator_id
        if supersede_of is not UNSET:
            field_dict["supersedeOf"] = supersede_of

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

        user_creator_id = d.pop("userCreatorId", UNSET)

        supersede_of = d.pop("supersedeOf", UNSET)

        new_entry_dto = cls(
            logbooks=logbooks,
            title=title,
            text=text,
            note=note,
            tags=tags,
            summarizes=summarizes,
            event_at=event_at,
            user_ids_to_notify=user_ids_to_notify,
            user_creator_id=user_creator_id,
            supersede_of=supersede_of,
        )

        new_entry_dto.additional_properties = d
        return new_entry_dto

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
