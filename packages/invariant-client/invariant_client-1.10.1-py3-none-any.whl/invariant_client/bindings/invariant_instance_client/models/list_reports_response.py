from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.report_extras import ReportExtras
    from ..models.report import Report


T = TypeVar("T", bound="ListReportsResponse")


@_attrs_define
class ListReportsResponse:
    """
    Attributes:
        reports (List['Report']):
        with_extras (List['ReportExtras']):
    """

    reports: List["Report"]
    with_extras: List["ReportExtras"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        reports = []
        for reports_item_data in self.reports:
            reports_item = reports_item_data.to_dict()

            reports.append(reports_item)

        with_extras = []
        for with_extras_item_data in self.with_extras:
            with_extras_item = with_extras_item_data.to_dict()

            with_extras.append(with_extras_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reports": reports,
                "with_extras": with_extras,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report_extras import ReportExtras
        from ..models.report import Report

        d = src_dict.copy()
        reports = []
        _reports = d.pop("reports")
        for reports_item_data in _reports:
            reports_item = Report.from_dict(reports_item_data)

            reports.append(reports_item)

        with_extras = []
        _with_extras = d.pop("with_extras")
        for with_extras_item_data in _with_extras:
            with_extras_item = ReportExtras.from_dict(with_extras_item_data)

            with_extras.append(with_extras_item)

        list_reports_response = cls(
            reports=reports,
            with_extras=with_extras,
        )

        list_reports_response.additional_properties = d
        return list_reports_response

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
