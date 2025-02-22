import datetime
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryImportDTO")


@_attrs_define
class EntryImportDTO:
    """Is the model for the new ELog creation

    Attributes:
        logbooks (list[str]): Is the logbooks where the new log belong
        title (str): The title of the log
        text (str): The content of the log
        origin_id (Union[Unset, str]): Identifier for unique find the record into the original system
        supersede_of_by_origin_id (Union[Unset, str]): Is the original id for which this entry is supersede
        references_by_origin_id (Union[Unset, list[str]]): Is the list of the original ids where this entry reference to
        last_name (Union[Unset, str]): The last name of user that generates the entry
        first_name (Union[Unset, str]): The first name of user that generates the entry
        user_name (Union[Unset, str]): The username of user that generates the entry
        note (Union[Unset, str]): Is the general note field
        tags (Union[Unset, list[str]]): The tags describes represent the log
        logged_at (Union[Unset, datetime.datetime]): The timestamp when the event is occurred
        event_at (Union[Unset, datetime.datetime]): The timestamp when the event is occurred
    """

    logbooks: list[str]
    title: str
    text: str
    origin_id: Union[Unset, str] = UNSET
    supersede_of_by_origin_id: Union[Unset, str] = UNSET
    references_by_origin_id: Union[Unset, list[str]] = UNSET
    last_name: Union[Unset, str] = UNSET
    first_name: Union[Unset, str] = UNSET
    user_name: Union[Unset, str] = UNSET
    note: Union[Unset, str] = UNSET
    tags: Union[Unset, list[str]] = UNSET
    logged_at: Union[Unset, datetime.datetime] = UNSET
    event_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        logbooks = self.logbooks

        title = self.title

        text = self.text

        origin_id = self.origin_id

        supersede_of_by_origin_id = self.supersede_of_by_origin_id

        references_by_origin_id: Union[Unset, list[str]] = UNSET
        if not isinstance(self.references_by_origin_id, Unset):
            references_by_origin_id = self.references_by_origin_id

        last_name = self.last_name

        first_name = self.first_name

        user_name = self.user_name

        note = self.note

        tags: Union[Unset, list[str]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        logged_at: Union[Unset, str] = UNSET
        if not isinstance(self.logged_at, Unset):
            logged_at = self.logged_at.isoformat()

        event_at: Union[Unset, str] = UNSET
        if not isinstance(self.event_at, Unset):
            event_at = self.event_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logbooks": logbooks,
                "title": title,
                "text": text,
            }
        )
        if origin_id is not UNSET:
            field_dict["originId"] = origin_id
        if supersede_of_by_origin_id is not UNSET:
            field_dict["supersedeOfByOriginId"] = supersede_of_by_origin_id
        if references_by_origin_id is not UNSET:
            field_dict["referencesByOriginId"] = references_by_origin_id
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if user_name is not UNSET:
            field_dict["userName"] = user_name
        if note is not UNSET:
            field_dict["note"] = note
        if tags is not UNSET:
            field_dict["tags"] = tags
        if logged_at is not UNSET:
            field_dict["loggedAt"] = logged_at
        if event_at is not UNSET:
            field_dict["eventAt"] = event_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        logbooks = cast(list[str], d.pop("logbooks"))

        title = d.pop("title")

        text = d.pop("text")

        origin_id = d.pop("originId", UNSET)

        supersede_of_by_origin_id = d.pop("supersedeOfByOriginId", UNSET)

        references_by_origin_id = cast(list[str], d.pop("referencesByOriginId", UNSET))

        last_name = d.pop("lastName", UNSET)

        first_name = d.pop("firstName", UNSET)

        user_name = d.pop("userName", UNSET)

        note = d.pop("note", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _logged_at = d.pop("loggedAt", UNSET)
        logged_at: Union[Unset, datetime.datetime]
        if isinstance(_logged_at, Unset):
            logged_at = UNSET
        else:
            logged_at = isoparse(_logged_at)

        _event_at = d.pop("eventAt", UNSET)
        event_at: Union[Unset, datetime.datetime]
        if isinstance(_event_at, Unset):
            event_at = UNSET
        else:
            event_at = isoparse(_event_at)

        entry_import_dto = cls(
            logbooks=logbooks,
            title=title,
            text=text,
            origin_id=origin_id,
            supersede_of_by_origin_id=supersede_of_by_origin_id,
            references_by_origin_id=references_by_origin_id,
            last_name=last_name,
            first_name=first_name,
            user_name=user_name,
            note=note,
            tags=tags,
            logged_at=logged_at,
            event_at=event_at,
        )

        entry_import_dto.additional_properties = d
        return entry_import_dto

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
