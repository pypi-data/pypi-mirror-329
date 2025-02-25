from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import Dict
from typing import cast
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.snapshot_report_data_files import SnapshotReportDataFiles
    from ..models.comparison_reportdata import ComparisonReportdata
    from ..models.file_index import FileIndex


T = TypeVar("T", bound="SnapshotReportData")


@_attrs_define
class SnapshotReportData:
    """
    Attributes:
        files (SnapshotReportDataFiles):
        summary (Union['FileIndex', str]):
        status (Union['FileIndex', str]):
        errors (Union['FileIndex', str]):
        solutions (Union['FileIndex', None, Unset, str]):
        compare_to (Union['ComparisonReportdata', None, Unset]):
    """

    files: "SnapshotReportDataFiles"
    summary: Union["FileIndex", str]
    status: Union["FileIndex", str]
    errors: Union["FileIndex", str]
    solutions: Union["FileIndex", None, Unset, str] = UNSET
    compare_to: Union["ComparisonReportdata", None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.comparison_reportdata import ComparisonReportdata
        from ..models.file_index import FileIndex

        files = self.files.to_dict()

        summary: Union[Dict[str, Any], str]

        if isinstance(self.summary, FileIndex):
            summary = self.summary.to_dict()

        else:
            summary = self.summary

        status: Union[Dict[str, Any], str]

        if isinstance(self.status, FileIndex):
            status = self.status.to_dict()

        else:
            status = self.status

        errors: Union[Dict[str, Any], str]

        if isinstance(self.errors, FileIndex):
            errors = self.errors.to_dict()

        else:
            errors = self.errors

        solutions: Union[Dict[str, Any], None, Unset, str]
        if isinstance(self.solutions, Unset):
            solutions = UNSET

        elif isinstance(self.solutions, FileIndex):
            solutions = UNSET
            if not isinstance(self.solutions, Unset):
                solutions = self.solutions.to_dict()

        else:
            solutions = self.solutions

        compare_to: Union[Dict[str, Any], None, Unset]
        if isinstance(self.compare_to, Unset):
            compare_to = UNSET

        elif isinstance(self.compare_to, ComparisonReportdata):
            compare_to = UNSET
            if not isinstance(self.compare_to, Unset):
                compare_to = self.compare_to.to_dict()

        else:
            compare_to = self.compare_to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
                "summary": summary,
                "status": status,
                "errors": errors,
            }
        )
        if solutions is not UNSET:
            field_dict["solutions"] = solutions
        if compare_to is not UNSET:
            field_dict["compare_to"] = compare_to

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.snapshot_report_data_files import SnapshotReportDataFiles
        from ..models.comparison_reportdata import ComparisonReportdata
        from ..models.file_index import FileIndex

        d = src_dict.copy()
        files = SnapshotReportDataFiles.from_dict(d.pop("files"))

        def _parse_summary(data: object) -> Union["FileIndex", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                summary_type_1 = FileIndex.from_dict(data)

                return summary_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FileIndex", str], data)

        summary = _parse_summary(d.pop("summary"))

        def _parse_status(data: object) -> Union["FileIndex", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                status_type_1 = FileIndex.from_dict(data)

                return status_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FileIndex", str], data)

        status = _parse_status(d.pop("status"))

        def _parse_errors(data: object) -> Union["FileIndex", str]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                errors_type_1 = FileIndex.from_dict(data)

                return errors_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FileIndex", str], data)

        errors = _parse_errors(d.pop("errors"))

        def _parse_solutions(data: object) -> Union["FileIndex", None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _solutions_type_1 = data
                solutions_type_1: Union[Unset, FileIndex]
                if isinstance(_solutions_type_1, Unset):
                    solutions_type_1 = UNSET
                else:
                    solutions_type_1 = FileIndex.from_dict(_solutions_type_1)

                return solutions_type_1
            except:  # noqa: E722
                pass
            return cast(Union["FileIndex", None, Unset, str], data)

        solutions = _parse_solutions(d.pop("solutions", UNSET))

        def _parse_compare_to(
            data: object,
        ) -> Union["ComparisonReportdata", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _compare_to_type_0 = data
                compare_to_type_0: Union[Unset, ComparisonReportdata]
                if isinstance(_compare_to_type_0, Unset):
                    compare_to_type_0 = UNSET
                else:
                    compare_to_type_0 = ComparisonReportdata.from_dict(
                        _compare_to_type_0
                    )

                return compare_to_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ComparisonReportdata", None, Unset], data)

        compare_to = _parse_compare_to(d.pop("compare_to", UNSET))

        snapshot_report_data = cls(
            files=files,
            summary=summary,
            status=status,
            errors=errors,
            solutions=solutions,
            compare_to=compare_to,
        )

        snapshot_report_data.additional_properties = d
        return snapshot_report_data

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
