from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Union
from typing import Dict
from typing import List
from typing import Literal

if TYPE_CHECKING:
    from ..models.oidc_login_method import OIDCLoginMethod
    from ..models.basic_auth_login_method import BasicAuthLoginMethod


T = TypeVar("T", bound="ModifyDefaultLoginMethodsRequest")


@_attrs_define
class ModifyDefaultLoginMethodsRequest:
    """
    Attributes:
        policy_key (Literal['default_allowed_methods']):
        value (List[Union['BasicAuthLoginMethod', 'OIDCLoginMethod']]):
    """

    policy_key: Literal["default_allowed_methods"]
    value: List[Union["BasicAuthLoginMethod", "OIDCLoginMethod"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        policy_key = self.policy_key
        value = []
        for value_item_data in self.value:
            value_item: Dict[str, Any]

            if isinstance(value_item_data, BasicAuthLoginMethod):
                value_item = value_item_data.to_dict()

            else:
                value_item = value_item_data.to_dict()

            value.append(value_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "policy_key": policy_key,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.oidc_login_method import OIDCLoginMethod
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        d = src_dict.copy()
        policy_key = d.pop("policy_key")

        value = []
        _value = d.pop("value")
        for value_item_data in _value:

            def _parse_value_item(
                data: object,
            ) -> Union["BasicAuthLoginMethod", "OIDCLoginMethod"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    value_item_type_0 = BasicAuthLoginMethod.from_dict(data)

                    return value_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                value_item_type_1 = OIDCLoginMethod.from_dict(data)

                return value_item_type_1

            value_item = _parse_value_item(value_item_data)

            value.append(value_item)

        modify_default_login_methods_request = cls(
            policy_key=policy_key,
            value=value,
        )

        modify_default_login_methods_request.additional_properties = d
        return modify_default_login_methods_request

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
