from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal


T = TypeVar("T", bound="Redirect")


@_attrs_define
class Redirect:
    """
    Attributes:
        type (Literal['oidc']):
        name (str):
        redirect_url (str):
        integration_uuid (str):
    """

    type: Literal["oidc"]
    name: str
    redirect_url: str
    integration_uuid: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        name = self.name
        redirect_url = self.redirect_url
        integration_uuid = self.integration_uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "name": name,
                "redirect_url": redirect_url,
                "integration_uuid": integration_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        name = d.pop("name")

        redirect_url = d.pop("redirect_url")

        integration_uuid = d.pop("integration_uuid")

        redirect = cls(
            type=type,
            name=name,
            redirect_url=redirect_url,
            integration_uuid=integration_uuid,
        )

        redirect.additional_properties = d
        return redirect

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
