from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_details_dto import UserDetailsDTO


T = TypeVar("T", bound="ApiResultResponseUserDetailsDTO")


@_attrs_define
class ApiResultResponseUserDetailsDTO:
    """
    Attributes:
        error_code (int): Is the error code returned from api
        error_message (Union[Unset, str]): In case of error not equal to 0, an error message can be reported by api,
            indicating what problem is occurred
        error_domain (Union[Unset, str]): In case of error not equal to 0, an error domain can be reported by api,
            indicating where the problem is occurred
        payload (Union[Unset, UserDetailsDTO]): User details
    """

    error_code: int
    error_message: Union[Unset, str] = UNSET
    error_domain: Union[Unset, str] = UNSET
    payload: Union[Unset, "UserDetailsDTO"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_code = self.error_code

        error_message = self.error_message

        error_domain = self.error_domain

        payload: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "errorCode": error_code,
            }
        )
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message
        if error_domain is not UNSET:
            field_dict["errorDomain"] = error_domain
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.user_details_dto import UserDetailsDTO

        d = src_dict.copy()
        error_code = d.pop("errorCode")

        error_message = d.pop("errorMessage", UNSET)

        error_domain = d.pop("errorDomain", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: Union[Unset, UserDetailsDTO]
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = UserDetailsDTO.from_dict(_payload)

        api_result_response_user_details_dto = cls(
            error_code=error_code,
            error_message=error_message,
            error_domain=error_domain,
            payload=payload,
        )

        api_result_response_user_details_dto.additional_properties = d
        return api_result_response_user_details_dto

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
