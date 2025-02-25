from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import cast, List
from ..types import UNSET, Unset


T = TypeVar("T", bound="FileIndex")


@_attrs_define
class FileIndex:
    """
    Attributes:
        all_files (List[str]):
        volume (Union[None, Unset, str]):
    """

    all_files: List[str]
    volume: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        all_files = self.all_files

        volume: Union[None, Unset, str]
        if isinstance(self.volume, Unset):
            volume = UNSET

        else:
            volume = self.volume

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "all_files": all_files,
            }
        )
        if volume is not UNSET:
            field_dict["volume"] = volume

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        all_files = cast(List[str], d.pop("all_files"))

        def _parse_volume(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        volume = _parse_volume(d.pop("volume", UNSET))

        file_index = cls(
            all_files=all_files,
            volume=volume,
        )

        file_index.additional_properties = d
        return file_index

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
