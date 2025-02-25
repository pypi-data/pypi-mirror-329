from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.redirect import Redirect


T = TypeVar("T", bound="InitiateSSOResponse")


@_attrs_define
class InitiateSSOResponse:
    """
    Attributes:
        methods (List['Redirect']):
    """

    methods: List["Redirect"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        methods = []
        for methods_item_data in self.methods:
            methods_item = methods_item_data.to_dict()

            methods.append(methods_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "methods": methods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.redirect import Redirect

        d = src_dict.copy()
        methods = []
        _methods = d.pop("methods")
        for methods_item_data in _methods:
            methods_item = Redirect.from_dict(methods_item_data)

            methods.append(methods_item)

        initiate_sso_response = cls(
            methods=methods,
        )

        initiate_sso_response.additional_properties = d
        return initiate_sso_response

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
