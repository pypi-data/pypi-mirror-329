from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast, Union
from typing import Union


T = TypeVar("T", bound="BaseErrorResponse")


@_attrs_define
class BaseErrorResponse:
    """Based on RFC7807 - see BaseResponse.

    Attributes:
        status (int):
        type (Union[None, str]):
        title (str):
        detail (str):
        instance (Union[None, Unset, str]):
    """

    status: int
    type: Union[None, str]
    title: str
    detail: str
    instance: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        type: Union[None, str]

        type = self.type

        title = self.title
        detail = self.detail
        instance: Union[None, Unset, str]
        if isinstance(self.instance, Unset):
            instance = UNSET

        else:
            instance = self.instance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "type": type,
                "title": title,
                "detail": detail,
            }
        )
        if instance is not UNSET:
            field_dict["instance"] = instance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        def _parse_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        type = _parse_type(d.pop("type"))

        title = d.pop("title")

        detail = d.pop("detail")

        def _parse_instance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instance = _parse_instance(d.pop("instance", UNSET))

        base_error_response = cls(
            status=status,
            type=type,
            title=title,
            detail=detail,
            instance=instance,
        )

        base_error_response.additional_properties = d
        return base_error_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
