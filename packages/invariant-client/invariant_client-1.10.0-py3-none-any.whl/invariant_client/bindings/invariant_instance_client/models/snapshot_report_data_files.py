from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Dict
from typing import cast, Union

if TYPE_CHECKING:
    from ..models.file_index import FileIndex


T = TypeVar("T", bound="SnapshotReportDataFiles")


@_attrs_define
class SnapshotReportDataFiles:
    """ """

    additional_properties: Dict[str, Union["FileIndex", str]] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        from ..models.file_index import FileIndex

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, FileIndex):
                field_dict[prop_name] = prop.to_dict()

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.file_index import FileIndex

        d = src_dict.copy()
        snapshot_report_data_files = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(data: object) -> Union["FileIndex", str]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    additional_property_type_1 = FileIndex.from_dict(data)

                    return additional_property_type_1
                except:  # noqa: E722
                    pass
                return cast(Union["FileIndex", str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        snapshot_report_data_files.additional_properties = additional_properties
        return snapshot_report_data_files

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union["FileIndex", str]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Union["FileIndex", str]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
