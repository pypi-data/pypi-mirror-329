from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Literal, Union
from ..types import UNSET, Unset


T = TypeVar("T", bound="CreateClientLoginSessionResponse")


@_attrs_define
class CreateClientLoginSessionResponse:
    """
    Attributes:
        status (int):
        pin (str):
        url (str):
        uuid (str):
        token (str):
        type (Union[Literal['urn:invariant:responses:init_client_login_response'], Unset]):  Default:
            'urn:invariant:responses:init_client_login_response'.
    """

    status: int
    pin: str
    url: str
    uuid: str
    token: str
    type: Union[
        Literal["urn:invariant:responses:init_client_login_response"], Unset
    ] = "urn:invariant:responses:init_client_login_response"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        pin = self.pin
        url = self.url
        uuid = self.uuid
        token = self.token
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "pin": pin,
                "url": url,
                "uuid": uuid,
                "token": token,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        status = d.pop("status")

        pin = d.pop("pin")

        url = d.pop("url")

        uuid = d.pop("uuid")

        token = d.pop("token")

        type = d.pop("type", UNSET)

        create_client_login_session_response = cls(
            status=status,
            pin=pin,
            url=url,
            uuid=uuid,
            token=token,
            type=type,
        )

        create_client_login_session_response.additional_properties = d
        return create_client_login_session_response

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
