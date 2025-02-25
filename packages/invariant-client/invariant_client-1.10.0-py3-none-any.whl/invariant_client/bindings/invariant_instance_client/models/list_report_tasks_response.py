from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.report_task import ReportTask


T = TypeVar("T", bound="ListReportTasksResponse")


@_attrs_define
class ListReportTasksResponse:
    """
    Attributes:
        in_progress (List['ReportTask']):
    """

    in_progress: List["ReportTask"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        in_progress = []
        for in_progress_item_data in self.in_progress:
            in_progress_item = in_progress_item_data.to_dict()

            in_progress.append(in_progress_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "in_progress": in_progress,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.report_task import ReportTask

        d = src_dict.copy()
        in_progress = []
        _in_progress = d.pop("in_progress")
        for in_progress_item_data in _in_progress:
            in_progress_item = ReportTask.from_dict(in_progress_item_data)

            in_progress.append(in_progress_item)

        list_report_tasks_response = cls(
            in_progress=in_progress,
        )

        list_report_tasks_response.additional_properties = d
        return list_report_tasks_response

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
