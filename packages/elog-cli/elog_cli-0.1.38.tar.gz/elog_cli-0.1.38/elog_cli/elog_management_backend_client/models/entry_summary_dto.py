import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attachment_dto import AttachmentDTO
    from ..models.logbook_shift_dto import LogbookShiftDTO
    from ..models.logbook_summary_dto import LogbookSummaryDTO
    from ..models.tag_dto import TagDTO


T = TypeVar("T", bound="EntrySummaryDTO")


@_attrs_define
class EntrySummaryDTO:
    """Contains the minimal set of information of the entry

    Attributes:
        id (Union[Unset, str]): Unique identifier of the entry
        logbooks (Union[Unset, list['LogbookSummaryDTO']]): The logbooks which the entry is associated
        title (Union[Unset, str]): The title of the entry
        logged_by (Union[Unset, str]): The user tha insert the entry
        tags (Union[Unset, list['TagDTO']]): The tags that describes the entry
        attachments (Union[Unset, list['AttachmentDTO']]): The attachment list of the entry
        is_empty (Union[Unset, bool]): Whether the entry is empty or not
        shifts (Union[Unset, list['LogbookShiftDTO']]): The shift which the entry belong, if any
        references (Union[Unset, list[str]]): The entries referenced by this one
        referenced_by (Union[Unset, list[str]]): The entries that refer to this one
        following_up (Union[Unset, str]): The id of the entry that is followUp for this the current entry is a follow
            ups
        follow_ups (Union[Unset, list[str]]): The list of entries that are follow ups of the current entry
        is_supersede (Union[Unset, bool]): This entry is a supersede
        note (Union[Unset, str]): The entry notes
        logged_at (Union[Unset, datetime.datetime]): The timestamp when the entry has been created
        event_at (Union[Unset, datetime.datetime]): The timestamp when the event described by the entry happened
    """

    id: Union[Unset, str] = UNSET
    logbooks: Union[Unset, list["LogbookSummaryDTO"]] = UNSET
    title: Union[Unset, str] = UNSET
    logged_by: Union[Unset, str] = UNSET
    tags: Union[Unset, list["TagDTO"]] = UNSET
    attachments: Union[Unset, list["AttachmentDTO"]] = UNSET
    is_empty: Union[Unset, bool] = UNSET
    shifts: Union[Unset, list["LogbookShiftDTO"]] = UNSET
    references: Union[Unset, list[str]] = UNSET
    referenced_by: Union[Unset, list[str]] = UNSET
    following_up: Union[Unset, str] = UNSET
    follow_ups: Union[Unset, list[str]] = UNSET
    is_supersede: Union[Unset, bool] = UNSET
    note: Union[Unset, str] = UNSET
    logged_at: Union[Unset, datetime.datetime] = UNSET
    event_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        logbooks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.logbooks, Unset):
            logbooks = []
            for logbooks_item_data in self.logbooks:
                logbooks_item = logbooks_item_data.to_dict()
                logbooks.append(logbooks_item)

        title = self.title

        logged_by = self.logged_by

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        is_empty = self.is_empty

        shifts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.shifts, Unset):
            shifts = []
            for shifts_item_data in self.shifts:
                shifts_item = shifts_item_data.to_dict()
                shifts.append(shifts_item)

        references: Union[Unset, list[str]] = UNSET
        if not isinstance(self.references, Unset):
            references = self.references

        referenced_by: Union[Unset, list[str]] = UNSET
        if not isinstance(self.referenced_by, Unset):
            referenced_by = self.referenced_by

        following_up = self.following_up

        follow_ups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.follow_ups, Unset):
            follow_ups = self.follow_ups

        is_supersede = self.is_supersede

        note = self.note

        logged_at: Union[Unset, str] = UNSET
        if not isinstance(self.logged_at, Unset):
            logged_at = self.logged_at.isoformat()

        event_at: Union[Unset, str] = UNSET
        if not isinstance(self.event_at, Unset):
            event_at = self.event_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if logbooks is not UNSET:
            field_dict["logbooks"] = logbooks
        if title is not UNSET:
            field_dict["title"] = title
        if logged_by is not UNSET:
            field_dict["loggedBy"] = logged_by
        if tags is not UNSET:
            field_dict["tags"] = tags
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if is_empty is not UNSET:
            field_dict["isEmpty"] = is_empty
        if shifts is not UNSET:
            field_dict["shifts"] = shifts
        if references is not UNSET:
            field_dict["references"] = references
        if referenced_by is not UNSET:
            field_dict["referencedBy"] = referenced_by
        if following_up is not UNSET:
            field_dict["followingUp"] = following_up
        if follow_ups is not UNSET:
            field_dict["followUps"] = follow_ups
        if is_supersede is not UNSET:
            field_dict["isSupersede"] = is_supersede
        if note is not UNSET:
            field_dict["note"] = note
        if logged_at is not UNSET:
            field_dict["loggedAt"] = logged_at
        if event_at is not UNSET:
            field_dict["eventAt"] = event_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.attachment_dto import AttachmentDTO
        from ..models.logbook_shift_dto import LogbookShiftDTO
        from ..models.logbook_summary_dto import LogbookSummaryDTO
        from ..models.tag_dto import TagDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        logbooks = []
        _logbooks = d.pop("logbooks", UNSET)
        for logbooks_item_data in _logbooks or []:
            logbooks_item = LogbookSummaryDTO.from_dict(logbooks_item_data)

            logbooks.append(logbooks_item)

        title = d.pop("title", UNSET)

        logged_by = d.pop("loggedBy", UNSET)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = TagDTO.from_dict(tags_item_data)

            tags.append(tags_item)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = AttachmentDTO.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        is_empty = d.pop("isEmpty", UNSET)

        shifts = []
        _shifts = d.pop("shifts", UNSET)
        for shifts_item_data in _shifts or []:
            shifts_item = LogbookShiftDTO.from_dict(shifts_item_data)

            shifts.append(shifts_item)

        references = cast(list[str], d.pop("references", UNSET))

        referenced_by = cast(list[str], d.pop("referencedBy", UNSET))

        following_up = d.pop("followingUp", UNSET)

        follow_ups = cast(list[str], d.pop("followUps", UNSET))

        is_supersede = d.pop("isSupersede", UNSET)

        note = d.pop("note", UNSET)

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

        entry_summary_dto = cls(
            id=id,
            logbooks=logbooks,
            title=title,
            logged_by=logged_by,
            tags=tags,
            attachments=attachments,
            is_empty=is_empty,
            shifts=shifts,
            references=references,
            referenced_by=referenced_by,
            following_up=following_up,
            follow_ups=follow_ups,
            is_supersede=is_supersede,
            note=note,
            logged_at=logged_at,
            event_at=event_at,
        )

        entry_summary_dto.additional_properties = d
        return entry_summary_dto

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
