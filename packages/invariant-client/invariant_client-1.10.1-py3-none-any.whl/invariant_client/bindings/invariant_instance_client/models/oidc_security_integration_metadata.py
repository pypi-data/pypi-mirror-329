from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal


T = TypeVar("T", bound="OIDCSecurityIntegrationMetadata")


@_attrs_define
class OIDCSecurityIntegrationMetadata:
    """
    Attributes:
        type (Literal['oidc']):
        name (str):
        server_metadata_url (str):
        client_id (str):
        client_secret (str):
    """

    type: Literal["oidc"]
    name: str
    server_metadata_url: str
    client_id: str
    client_secret: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        name = self.name
        server_metadata_url = self.server_metadata_url
        client_id = self.client_id
        client_secret = self.client_secret

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "name": name,
                "server_metadata_url": server_metadata_url,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        name = d.pop("name")

        server_metadata_url = d.pop("server_metadata_url")

        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret")

        oidc_security_integration_metadata = cls(
            type=type,
            name=name,
            server_metadata_url=server_metadata_url,
            client_id=client_id,
            client_secret=client_secret,
        )

        oidc_security_integration_metadata.additional_properties = d
        return oidc_security_integration_metadata

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
