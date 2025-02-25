from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, Union
from typing import cast, List


T = TypeVar("T", bound="TabInfoParametersType0")


@_attrs_define
class TabInfoParametersType0:
    """ """

    additional_properties: Dict[
        str, Union[List[int], List[str], bool, int, str]
    ] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            if isinstance(prop, list):
                field_dict[prop_name] = prop

            elif isinstance(prop, list):
                field_dict[prop_name] = prop

            else:
                field_dict[prop_name] = prop

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        tab_info_parameters_type_0 = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():

            def _parse_additional_property(
                data: object,
            ) -> Union[List[int], List[str], bool, int, str]:
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_3 = cast(List[str], data)

                    return additional_property_type_3
                except:  # noqa: E722
                    pass
                try:
                    if not isinstance(data, list):
                        raise TypeError()
                    additional_property_type_4 = cast(List[int], data)

                    return additional_property_type_4
                except:  # noqa: E722
                    pass
                return cast(Union[List[int], List[str], bool, int, str], data)

            additional_property = _parse_additional_property(prop_dict)

            additional_properties[prop_name] = additional_property

        tab_info_parameters_type_0.additional_properties = additional_properties
        return tab_info_parameters_type_0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Union[List[int], List[str], bool, int, str]:
        return self.additional_properties[key]

    def __setitem__(
        self, key: str, value: Union[List[int], List[str], bool, int, str]
    ) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
