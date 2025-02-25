from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json

from ..types import UNSET

from typing import Union
from ..types import File, FileJsonType
from typing import List
from io import BytesIO


T = TypeVar("T", bound="BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost")


@_attrs_define
class BodyUploadSnapshotOrganizationNameApiV1UploadsnapshotPost:
    """
    Attributes:
        file (Union[File, List[File]]):
    """

    file: Union[File, List[File]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file: Union[FileJsonType, List[FileJsonType]]

        if isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = []
            for file_type_1_item_data in self.file:
                file_type_1_item = file_type_1_item_data.to_tuple()

                file.append(file_type_1_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file: Union[File, List[File]]

        if isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            _temp_file = []
            for file_type_1_item_data in self.file:
                file_type_1_item = file_type_1_item_data.to_tuple()

                _temp_file.append(file_type_1_item)
            file = (None, json.dumps(_temp_file).encode(), "application/json")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                key: (None, str(value).encode(), "text/plain")
                for key, value in self.additional_properties.items()
            }
        )
        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_file(data: object) -> Union[File, List[File]]:
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                file_type_0 = File(payload=BytesIO(data))

                return file_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            file_type_1 = UNSET
            _file_type_1 = data
            for file_type_1_item_data in _file_type_1:
                file_type_1_item = File(payload=BytesIO(file_type_1_item_data))

                file_type_1.append(file_type_1_item)

            return file_type_1

        file = _parse_file(d.pop("file"))

        body_upload_snapshot_organization_name_api_v1_uploadsnapshot_post = cls(
            file=file,
        )

        body_upload_snapshot_organization_name_api_v1_uploadsnapshot_post.additional_properties = d
        return body_upload_snapshot_organization_name_api_v1_uploadsnapshot_post

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
