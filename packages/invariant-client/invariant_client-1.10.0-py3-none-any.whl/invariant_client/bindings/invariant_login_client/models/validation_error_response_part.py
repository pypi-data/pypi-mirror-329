from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, List


T = TypeVar("T", bound="ValidationErrorResponsePart")


@_attrs_define
class ValidationErrorResponsePart:
    """
    Attributes:
        loc (List[str]):
        msg (str):
        type (str):
    """

    loc: List[str]
    msg: str
    type: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        loc = self.loc

        msg = self.msg
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "loc": loc,
                "msg": msg,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        loc = cast(List[str], d.pop("loc"))

        msg = d.pop("msg")

        type = d.pop("type")

        validation_error_response_part = cls(
            loc=loc,
            msg=msg,
            type=type,
        )

        validation_error_response_part.additional_properties = d
        return validation_error_response_part

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
