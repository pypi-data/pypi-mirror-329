import datetime
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.attachment_dto import AttachmentDTO
    from ..models.entry_summary_dto import EntrySummaryDTO
    from ..models.logbook_shift_dto import LogbookShiftDTO
    from ..models.logbook_summary_dto import LogbookSummaryDTO
    from ..models.tag_dto import TagDTO


T = TypeVar("T", bound="EntryDTO")


@_attrs_define
class EntryDTO:
    """Identify the single elog record

    Attributes:
        id (Union[Unset, str]): record primary key
        superseded_by (Union[Unset, EntrySummaryDTO]): Contains the minimal set of information of the entry
        entry_type (Union[Unset, str]): the type of the entry
        logbooks (Union[Unset, list['LogbookSummaryDTO']]): the logbooks where the entry belong
        tags (Union[Unset, list['TagDTO']]): the tags of the entry
        title (Union[Unset, str]): the title of the entry
        text (Union[Unset, str]): the text of the entry
        logged_by (Union[Unset, str]): the author of the entry
        attachments (Union[Unset, list['AttachmentDTO']]): the attachments of the entry
        follow_ups (Union[Unset, list['EntrySummaryDTO']]): the follow up of the entry
        following_up (Union[Unset, EntrySummaryDTO]): Contains the minimal set of information of the entry
        history (Union[Unset, list['EntrySummaryDTO']]): the history of the entry
        shifts (Union[Unset, list['LogbookShiftDTO']]): The shift which the entry belong, if any match the event date
        references_in_body (Union[Unset, bool]):
        references (Union[Unset, list['EntrySummaryDTO']]): The entries referenced from this one
        referenced_by (Union[Unset, list['EntrySummaryDTO']]): The entries that reference this one
        summarize_shift (Union[Unset, str]): the id of the shift where this entry is a summarization
        summary_date (Union[Unset, datetime.datetime]): the date of the summary
        logged_at (Union[Unset, datetime.datetime]): the date of the entry
        event_at (Union[Unset, datetime.datetime]): the date of the event
    """

    id: Union[Unset, str] = UNSET
    superseded_by: Union[Unset, "EntrySummaryDTO"] = UNSET
    entry_type: Union[Unset, str] = UNSET
    logbooks: Union[Unset, list["LogbookSummaryDTO"]] = UNSET
    tags: Union[Unset, list["TagDTO"]] = UNSET
    title: Union[Unset, str] = UNSET
    text: Union[Unset, str] = UNSET
    logged_by: Union[Unset, str] = UNSET
    attachments: Union[Unset, list["AttachmentDTO"]] = UNSET
    follow_ups: Union[Unset, list["EntrySummaryDTO"]] = UNSET
    following_up: Union[Unset, "EntrySummaryDTO"] = UNSET
    history: Union[Unset, list["EntrySummaryDTO"]] = UNSET
    shifts: Union[Unset, list["LogbookShiftDTO"]] = UNSET
    references_in_body: Union[Unset, bool] = UNSET
    references: Union[Unset, list["EntrySummaryDTO"]] = UNSET
    referenced_by: Union[Unset, list["EntrySummaryDTO"]] = UNSET
    summarize_shift: Union[Unset, str] = UNSET
    summary_date: Union[Unset, datetime.datetime] = UNSET
    logged_at: Union[Unset, datetime.datetime] = UNSET
    event_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        superseded_by: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.superseded_by, Unset):
            superseded_by = self.superseded_by.to_dict()

        entry_type = self.entry_type

        logbooks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.logbooks, Unset):
            logbooks = []
            for logbooks_item_data in self.logbooks:
                logbooks_item = logbooks_item_data.to_dict()
                logbooks.append(logbooks_item)

        tags: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = []
            for tags_item_data in self.tags:
                tags_item = tags_item_data.to_dict()
                tags.append(tags_item)

        title = self.title

        text = self.text

        logged_by = self.logged_by

        attachments: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        follow_ups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.follow_ups, Unset):
            follow_ups = []
            for follow_ups_item_data in self.follow_ups:
                follow_ups_item = follow_ups_item_data.to_dict()
                follow_ups.append(follow_ups_item)

        following_up: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.following_up, Unset):
            following_up = self.following_up.to_dict()

        history: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.history, Unset):
            history = []
            for history_item_data in self.history:
                history_item = history_item_data.to_dict()
                history.append(history_item)

        shifts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.shifts, Unset):
            shifts = []
            for shifts_item_data in self.shifts:
                shifts_item = shifts_item_data.to_dict()
                shifts.append(shifts_item)

        references_in_body = self.references_in_body

        references: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.references, Unset):
            references = []
            for references_item_data in self.references:
                references_item = references_item_data.to_dict()
                references.append(references_item)

        referenced_by: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.referenced_by, Unset):
            referenced_by = []
            for referenced_by_item_data in self.referenced_by:
                referenced_by_item = referenced_by_item_data.to_dict()
                referenced_by.append(referenced_by_item)

        summarize_shift = self.summarize_shift

        summary_date: Union[Unset, str] = UNSET
        if not isinstance(self.summary_date, Unset):
            summary_date = self.summary_date.isoformat()

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
        if superseded_by is not UNSET:
            field_dict["supersededBy"] = superseded_by
        if entry_type is not UNSET:
            field_dict["entryType"] = entry_type
        if logbooks is not UNSET:
            field_dict["logbooks"] = logbooks
        if tags is not UNSET:
            field_dict["tags"] = tags
        if title is not UNSET:
            field_dict["title"] = title
        if text is not UNSET:
            field_dict["text"] = text
        if logged_by is not UNSET:
            field_dict["loggedBy"] = logged_by
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if follow_ups is not UNSET:
            field_dict["followUps"] = follow_ups
        if following_up is not UNSET:
            field_dict["followingUp"] = following_up
        if history is not UNSET:
            field_dict["history"] = history
        if shifts is not UNSET:
            field_dict["shifts"] = shifts
        if references_in_body is not UNSET:
            field_dict["referencesInBody"] = references_in_body
        if references is not UNSET:
            field_dict["references"] = references
        if referenced_by is not UNSET:
            field_dict["referencedBy"] = referenced_by
        if summarize_shift is not UNSET:
            field_dict["summarizeShift"] = summarize_shift
        if summary_date is not UNSET:
            field_dict["summaryDate"] = summary_date
        if logged_at is not UNSET:
            field_dict["loggedAt"] = logged_at
        if event_at is not UNSET:
            field_dict["eventAt"] = event_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.attachment_dto import AttachmentDTO
        from ..models.entry_summary_dto import EntrySummaryDTO
        from ..models.logbook_shift_dto import LogbookShiftDTO
        from ..models.logbook_summary_dto import LogbookSummaryDTO
        from ..models.tag_dto import TagDTO

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _superseded_by = d.pop("supersededBy", UNSET)
        superseded_by: Union[Unset, EntrySummaryDTO]
        if isinstance(_superseded_by, Unset):
            superseded_by = UNSET
        else:
            superseded_by = EntrySummaryDTO.from_dict(_superseded_by)

        entry_type = d.pop("entryType", UNSET)

        logbooks = []
        _logbooks = d.pop("logbooks", UNSET)
        for logbooks_item_data in _logbooks or []:
            logbooks_item = LogbookSummaryDTO.from_dict(logbooks_item_data)

            logbooks.append(logbooks_item)

        tags = []
        _tags = d.pop("tags", UNSET)
        for tags_item_data in _tags or []:
            tags_item = TagDTO.from_dict(tags_item_data)

            tags.append(tags_item)

        title = d.pop("title", UNSET)

        text = d.pop("text", UNSET)

        logged_by = d.pop("loggedBy", UNSET)

        attachments = []
        _attachments = d.pop("attachments", UNSET)
        for attachments_item_data in _attachments or []:
            attachments_item = AttachmentDTO.from_dict(attachments_item_data)

            attachments.append(attachments_item)

        follow_ups = []
        _follow_ups = d.pop("followUps", UNSET)
        for follow_ups_item_data in _follow_ups or []:
            follow_ups_item = EntrySummaryDTO.from_dict(follow_ups_item_data)

            follow_ups.append(follow_ups_item)

        _following_up = d.pop("followingUp", UNSET)
        following_up: Union[Unset, EntrySummaryDTO]
        if isinstance(_following_up, Unset):
            following_up = UNSET
        else:
            following_up = EntrySummaryDTO.from_dict(_following_up)

        history = []
        _history = d.pop("history", UNSET)
        for history_item_data in _history or []:
            history_item = EntrySummaryDTO.from_dict(history_item_data)

            history.append(history_item)

        shifts = []
        _shifts = d.pop("shifts", UNSET)
        for shifts_item_data in _shifts or []:
            shifts_item = LogbookShiftDTO.from_dict(shifts_item_data)

            shifts.append(shifts_item)

        references_in_body = d.pop("referencesInBody", UNSET)

        references = []
        _references = d.pop("references", UNSET)
        for references_item_data in _references or []:
            references_item = EntrySummaryDTO.from_dict(references_item_data)

            references.append(references_item)

        referenced_by = []
        _referenced_by = d.pop("referencedBy", UNSET)
        for referenced_by_item_data in _referenced_by or []:
            referenced_by_item = EntrySummaryDTO.from_dict(referenced_by_item_data)

            referenced_by.append(referenced_by_item)

        summarize_shift = d.pop("summarizeShift", UNSET)

        _summary_date = d.pop("summaryDate", UNSET)
        summary_date: Union[Unset, datetime.datetime]
        if isinstance(_summary_date, Unset):
            summary_date = UNSET
        else:
            summary_date = isoparse(_summary_date)

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

        entry_dto = cls(
            id=id,
            superseded_by=superseded_by,
            entry_type=entry_type,
            logbooks=logbooks,
            tags=tags,
            title=title,
            text=text,
            logged_by=logged_by,
            attachments=attachments,
            follow_ups=follow_ups,
            following_up=following_up,
            history=history,
            shifts=shifts,
            references_in_body=references_in_body,
            references=references,
            referenced_by=referenced_by,
            summarize_shift=summarize_shift,
            summary_date=summary_date,
            logged_at=logged_at,
            event_at=event_at,
        )

        entry_dto.additional_properties = d
        return entry_dto

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
