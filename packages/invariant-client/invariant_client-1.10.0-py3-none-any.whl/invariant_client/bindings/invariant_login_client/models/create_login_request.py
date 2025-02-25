from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal


T = TypeVar("T", bound="CreateLoginRequest")


@_attrs_define
class CreateLoginRequest:
    """This request creates a new login from an invite link. It does not require any credential.

    Attributes:
        type (Literal['new_login']):
        email (str):
        password (str):
        ilink (str):
    """

    type: Literal["new_login"]
    email: str
    password: str
    ilink: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        email = self.email
        password = self.password
        ilink = self.ilink

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "email": email,
                "password": password,
                "ilink": ilink,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        email = d.pop("email")

        password = d.pop("password")

        ilink = d.pop("ilink")

        create_login_request = cls(
            type=type,
            email=email,
            password=password,
            ilink=ilink,
        )

        create_login_request.additional_properties = d
        return create_login_request

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
