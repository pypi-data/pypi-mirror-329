from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.logbook_summary_dto import LogbookSummaryDTO


T = TypeVar("T", bound="AuthorizationCache")


@_attrs_define
class AuthorizationCache:
    """
    Attributes:
        authorized_logbook_id (Union[Unset, list[str]]):
        authorized_logbook_summaries (Union[Unset, list['LogbookSummaryDTO']]):
        root_user (Union[Unset, bool]):
    """

    authorized_logbook_id: Union[Unset, list[str]] = UNSET
    authorized_logbook_summaries: Union[Unset, list["LogbookSummaryDTO"]] = UNSET
    root_user: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        authorized_logbook_id: Union[Unset, list[str]] = UNSET
        if not isinstance(self.authorized_logbook_id, Unset):
            authorized_logbook_id = self.authorized_logbook_id

        authorized_logbook_summaries: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.authorized_logbook_summaries, Unset):
            authorized_logbook_summaries = []
            for authorized_logbook_summaries_item_data in self.authorized_logbook_summaries:
                authorized_logbook_summaries_item = authorized_logbook_summaries_item_data.to_dict()
                authorized_logbook_summaries.append(authorized_logbook_summaries_item)

        root_user = self.root_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if authorized_logbook_id is not UNSET:
            field_dict["authorizedLogbookId"] = authorized_logbook_id
        if authorized_logbook_summaries is not UNSET:
            field_dict["authorizedLogbookSummaries"] = authorized_logbook_summaries
        if root_user is not UNSET:
            field_dict["rootUser"] = root_user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.logbook_summary_dto import LogbookSummaryDTO

        d = src_dict.copy()
        authorized_logbook_id = cast(list[str], d.pop("authorizedLogbookId", UNSET))

        authorized_logbook_summaries = []
        _authorized_logbook_summaries = d.pop("authorizedLogbookSummaries", UNSET)
        for authorized_logbook_summaries_item_data in _authorized_logbook_summaries or []:
            authorized_logbook_summaries_item = LogbookSummaryDTO.from_dict(authorized_logbook_summaries_item_data)

            authorized_logbook_summaries.append(authorized_logbook_summaries_item)

        root_user = d.pop("rootUser", UNSET)

        authorization_cache = cls(
            authorized_logbook_id=authorized_logbook_id,
            authorized_logbook_summaries=authorized_logbook_summaries,
            root_user=root_user,
        )

        authorization_cache.additional_properties = d
        return authorization_cache

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
