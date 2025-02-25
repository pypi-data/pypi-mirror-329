from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal
from ..models.new_password_request_authn_type import NewPasswordRequestAuthnType


T = TypeVar("T", bound="NewPasswordRequest")


@_attrs_define
class NewPasswordRequest:
    """Respond to the new_password challenge. The user is either setting an initial password or using password reset.

    Attributes:
        type (Literal['new_password']):
        password (str):
        authn_type (NewPasswordRequestAuthnType):
        authn (str):
    """

    type: Literal["new_password"]
    password: str
    authn_type: NewPasswordRequestAuthnType
    authn: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        password = self.password
        authn_type = self.authn_type.value

        authn = self.authn

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "password": password,
                "authn_type": authn_type,
                "authn": authn,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        password = d.pop("password")

        authn_type = NewPasswordRequestAuthnType(d.pop("authn_type"))

        authn = d.pop("authn")

        new_password_request = cls(
            type=type,
            password=password,
            authn_type=authn_type,
            authn=authn,
        )

        new_password_request.additional_properties = d
        return new_password_request

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
