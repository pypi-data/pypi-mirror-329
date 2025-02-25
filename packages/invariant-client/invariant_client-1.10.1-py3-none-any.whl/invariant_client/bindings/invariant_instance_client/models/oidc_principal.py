from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="OIDCPrincipal")


@_attrs_define
class OIDCPrincipal:
    """
    Attributes:
        organization_uuid (str):
        integration_uuid (str):
        principal_id (str):
    """

    organization_uuid: str
    integration_uuid: str
    principal_id: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization_uuid = self.organization_uuid
        integration_uuid = self.integration_uuid
        principal_id = self.principal_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_uuid": organization_uuid,
                "integration_uuid": integration_uuid,
                "principal_id": principal_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        organization_uuid = d.pop("organization_uuid")

        integration_uuid = d.pop("integration_uuid")

        principal_id = d.pop("principal_id")

        oidc_principal = cls(
            organization_uuid=organization_uuid,
            integration_uuid=integration_uuid,
            principal_id=principal_id,
        )

        oidc_principal.additional_properties = d
        return oidc_principal

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
