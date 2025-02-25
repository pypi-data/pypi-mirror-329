from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
    from ..models.external_status_data_integration import ExternalStatusDataIntegration


T = TypeVar("T", bound="ExternalStatusIntegration")


@_attrs_define
class ExternalStatusIntegration:
    """
    Attributes:
        organization_uuid (str):
        subject_uuid (str):
        data (ExternalStatusDataIntegration):
        created_at (datetime.datetime):
    """

    organization_uuid: str
    subject_uuid: str
    data: "ExternalStatusDataIntegration"
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization_uuid = self.organization_uuid
        subject_uuid = self.subject_uuid
        data = self.data.to_dict()

        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "organization_uuid": organization_uuid,
                "subject_uuid": subject_uuid,
                "data": data,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_status_data_integration import (
            ExternalStatusDataIntegration,
        )

        d = src_dict.copy()
        organization_uuid = d.pop("organization_uuid")

        subject_uuid = d.pop("subject_uuid")

        data = ExternalStatusDataIntegration.from_dict(d.pop("data"))

        created_at = isoparse(d.pop("created_at"))

        external_status_integration = cls(
            organization_uuid=organization_uuid,
            subject_uuid=subject_uuid,
            data=data,
            created_at=created_at,
        )

        external_status_integration.additional_properties = d
        return external_status_integration

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
