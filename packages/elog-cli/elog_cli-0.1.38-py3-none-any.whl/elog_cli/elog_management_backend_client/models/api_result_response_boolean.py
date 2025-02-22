from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ApiResultResponseBoolean")


@_attrs_define
class ApiResultResponseBoolean:
    """
    Attributes:
        error_code (int): Is the error code returned from api
        error_message (Union[Unset, str]): In case of error not equal to 0, an error message can be reported by api,
            indicating what problem is occurred
        error_domain (Union[Unset, str]): In case of error not equal to 0, an error domain can be reported by api,
            indicating where the problem is occurred
        payload (Union[Unset, bool]): Is the value returned by api
    """

    error_code: int
    error_message: Union[Unset, str] = UNSET
    error_domain: Union[Unset, str] = UNSET
    payload: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_code = self.error_code

        error_message = self.error_message

        error_domain = self.error_domain

        payload = self.payload

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
        d = src_dict.copy()
        error_code = d.pop("errorCode")

        error_message = d.pop("errorMessage", UNSET)

        error_domain = d.pop("errorDomain", UNSET)

        payload = d.pop("payload", UNSET)

        api_result_response_boolean = cls(
            error_code=error_code,
            error_message=error_message,
            error_domain=error_domain,
            payload=payload,
        )

        api_result_response_boolean.additional_properties = d
        return api_result_response_boolean

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
