from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Literal


T = TypeVar("T", bound="OIDCLoginMethod")


@_attrs_define
class OIDCLoginMethod:
    """
    Attributes:
        type (Literal['oidc']):
        organization_uuid (str):
        integration_uuid (str):
    """

    type: Literal["oidc"]
    organization_uuid: str
    integration_uuid: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        organization_uuid = self.organization_uuid
        integration_uuid = self.integration_uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "organization_uuid": organization_uuid,
                "integration_uuid": integration_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = d.pop("type")

        organization_uuid = d.pop("organization_uuid")

        integration_uuid = d.pop("integration_uuid")

        oidc_login_method = cls(
            type=type,
            organization_uuid=organization_uuid,
            integration_uuid=integration_uuid,
        )

        oidc_login_method.additional_properties = d
        return oidc_login_method

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
