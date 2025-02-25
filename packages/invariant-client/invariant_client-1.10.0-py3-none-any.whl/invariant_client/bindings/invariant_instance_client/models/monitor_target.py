from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from dateutil.parser import isoparse
import datetime

if TYPE_CHECKING:
    from ..models.monitor_target_metadata import MonitorTargetMetadata


T = TypeVar("T", bound="MonitorTarget")


@_attrs_define
class MonitorTarget:
    """
    Attributes:
        uuid (str):
        organization_uuid (str):
        metadata (MonitorTargetMetadata):
        is_active (bool):
        created_at (datetime.datetime):
    """

    uuid: str
    organization_uuid: str
    metadata: "MonitorTargetMetadata"
    is_active: bool
    created_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        organization_uuid = self.organization_uuid
        metadata = self.metadata.to_dict()

        is_active = self.is_active
        created_at = self.created_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization_uuid": organization_uuid,
                "metadata": metadata,
                "is_active": is_active,
                "created_at": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.monitor_target_metadata import MonitorTargetMetadata

        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization_uuid = d.pop("organization_uuid")

        metadata = MonitorTargetMetadata.from_dict(d.pop("metadata"))

        is_active = d.pop("is_active")

        created_at = isoparse(d.pop("created_at"))

        monitor_target = cls(
            uuid=uuid,
            organization_uuid=organization_uuid,
            metadata=metadata,
            is_active=is_active,
            created_at=created_at,
        )

        monitor_target.additional_properties = d
        return monitor_target

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
