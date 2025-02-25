from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from dateutil.parser import isoparse
import datetime


T = TypeVar("T", bound="ReportTask")


@_attrs_define
class ReportTask:
    """
    Attributes:
        uuid (str):
        organization_uuid (str):
        created_at (datetime.datetime):
        urn (str):
        type (str):
        initiator_urn (str):
        worker_pod (str):
        was_killed (bool):
    """

    uuid: str
    organization_uuid: str
    created_at: datetime.datetime
    urn: str
    type: str
    initiator_urn: str
    worker_pod: str
    was_killed: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        organization_uuid = self.organization_uuid
        created_at = self.created_at.isoformat()

        urn = self.urn
        type = self.type
        initiator_urn = self.initiator_urn
        worker_pod = self.worker_pod
        was_killed = self.was_killed

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization_uuid": organization_uuid,
                "created_at": created_at,
                "urn": urn,
                "type": type,
                "initiator_urn": initiator_urn,
                "worker_pod": worker_pod,
                "was_killed": was_killed,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization_uuid = d.pop("organization_uuid")

        created_at = isoparse(d.pop("created_at"))

        urn = d.pop("urn")

        type = d.pop("type")

        initiator_urn = d.pop("initiator_urn")

        worker_pod = d.pop("worker_pod")

        was_killed = d.pop("was_killed")

        report_task = cls(
            uuid=uuid,
            organization_uuid=organization_uuid,
            created_at=created_at,
            urn=urn,
            type=type,
            initiator_urn=initiator_urn,
            worker_pod=worker_pod,
            was_killed=was_killed,
        )

        report_task.additional_properties = d
        return report_task

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
