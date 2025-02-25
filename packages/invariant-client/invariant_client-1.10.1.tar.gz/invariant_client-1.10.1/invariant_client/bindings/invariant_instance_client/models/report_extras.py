from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, List


T = TypeVar("T", bound="ReportExtras")


@_attrs_define
class ReportExtras:
    """
    Attributes:
        report_uuid (str):
        network_name (str):
        cf_violations (int):
        ap_violations (int):
        status (str):
        errors_count (int):
        errors_lines (List[str]):
    """

    report_uuid: str
    network_name: str
    cf_violations: int
    ap_violations: int
    status: str
    errors_count: int
    errors_lines: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        report_uuid = self.report_uuid
        network_name = self.network_name
        cf_violations = self.cf_violations
        ap_violations = self.ap_violations
        status = self.status
        errors_count = self.errors_count
        errors_lines = self.errors_lines

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "report_uuid": report_uuid,
                "network_name": network_name,
                "cf_violations": cf_violations,
                "ap_violations": ap_violations,
                "status": status,
                "errors_count": errors_count,
                "errors_lines": errors_lines,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        report_uuid = d.pop("report_uuid")

        network_name = d.pop("network_name")

        cf_violations = d.pop("cf_violations")

        ap_violations = d.pop("ap_violations")

        status = d.pop("status")

        errors_count = d.pop("errors_count")

        errors_lines = cast(List[str], d.pop("errors_lines"))

        report_extras = cls(
            report_uuid=report_uuid,
            network_name=network_name,
            cf_violations=cf_violations,
            ap_violations=ap_violations,
            status=status,
            errors_count=errors_count,
            errors_lines=errors_lines,
        )

        report_extras.additional_properties = d
        return report_extras

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
