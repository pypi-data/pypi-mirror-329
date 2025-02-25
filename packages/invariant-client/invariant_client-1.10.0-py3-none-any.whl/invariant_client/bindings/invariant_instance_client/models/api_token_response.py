from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.api_token import APIToken


T = TypeVar("T", bound="APITokenResponse")


@_attrs_define
class APITokenResponse:
    """List of APITokens

    Attributes:
        api_tokens (List['APIToken']):
    """

    api_tokens: List["APIToken"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        api_tokens = []
        for api_tokens_item_data in self.api_tokens:
            api_tokens_item = api_tokens_item_data.to_dict()

            api_tokens.append(api_tokens_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "api_tokens": api_tokens,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_token import APIToken

        d = src_dict.copy()
        api_tokens = []
        _api_tokens = d.pop("api_tokens")
        for api_tokens_item_data in _api_tokens:
            api_tokens_item = APIToken.from_dict(api_tokens_item_data)

            api_tokens.append(api_tokens_item)

        api_token_response = cls(
            api_tokens=api_tokens,
        )

        api_token_response.additional_properties = d
        return api_token_response

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
