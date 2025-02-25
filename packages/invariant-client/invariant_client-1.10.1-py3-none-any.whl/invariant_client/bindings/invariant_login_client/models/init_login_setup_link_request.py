from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Literal
from typing import Union
from typing import cast, Union


T = TypeVar("T", bound="InitLoginSetupLinkRequest")


@_attrs_define
class InitLoginSetupLinkRequest:
    """This request initiates a login session based on a managed user setup link.

    Attributes:
        type (Literal['init_login_setup']):
        slink (str):
        email (Union[None, Unset, str]):
    """

    type: Literal["init_login_setup"]
    slink: str
    email: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        slink = self.slink
        email: Union[None, Unset, str]
        if isinstance(self.email, Unset):
            email = UNSET

        else:
            email = self.email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "slink": slink,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        slink = d.pop("slink")

        def _parse_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        email = _parse_email(d.pop("email", UNSET))

        init_login_setup_link_request = cls(
            type=type,
            slink=slink,
            email=email,
        )

        init_login_setup_link_request.additional_properties = d
        return init_login_setup_link_request

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
