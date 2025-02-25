from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Union
from typing import Literal
from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.public import Public
    from ..models.basic_auth_login_method import BasicAuthLoginMethod


T = TypeVar("T", bound="AuthnChallenge")


@_attrs_define
class AuthnChallenge:
    """The user must provide a primary authentication credential.

    Attributes:
        type (Literal['authn']):
        allowed_methods (List[Union['BasicAuthLoginMethod', 'Public']]):
    """

    type: Literal["authn"]
    allowed_methods: List[Union["BasicAuthLoginMethod", "Public"]]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        type = self.type
        allowed_methods = []
        for allowed_methods_item_data in self.allowed_methods:
            allowed_methods_item: Dict[str, Any]

            if isinstance(allowed_methods_item_data, BasicAuthLoginMethod):
                allowed_methods_item = allowed_methods_item_data.to_dict()

            else:
                allowed_methods_item = allowed_methods_item_data.to_dict()

            allowed_methods.append(allowed_methods_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "allowed_methods": allowed_methods,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.public import Public
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        d = src_dict.copy()
        type = d.pop("type")

        allowed_methods = []
        _allowed_methods = d.pop("allowed_methods")
        for allowed_methods_item_data in _allowed_methods:

            def _parse_allowed_methods_item(
                data: object,
            ) -> Union["BasicAuthLoginMethod", "Public"]:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    allowed_methods_item_type_0 = BasicAuthLoginMethod.from_dict(data)

                    return allowed_methods_item_type_0
                except:  # noqa: E722
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                allowed_methods_item_type_1 = Public.from_dict(data)

                return allowed_methods_item_type_1

            allowed_methods_item = _parse_allowed_methods_item(
                allowed_methods_item_data
            )

            allowed_methods.append(allowed_methods_item)

        authn_challenge = cls(
            type=type,
            allowed_methods=allowed_methods,
        )

        authn_challenge.additional_properties = d
        return authn_challenge

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
