from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import List

if TYPE_CHECKING:
    from ..models.tab_info import TabInfo


T = TypeVar("T", bound="UserTabsConfig")


@_attrs_define
class UserTabsConfig:
    """
    Attributes:
        tabs (List['TabInfo']):
    """

    tabs: List["TabInfo"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tabs = []
        for tabs_item_data in self.tabs:
            tabs_item = tabs_item_data.to_dict()

            tabs.append(tabs_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "tabs": tabs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.tab_info import TabInfo

        d = src_dict.copy()
        tabs = []
        _tabs = d.pop("tabs")
        for tabs_item_data in _tabs:
            tabs_item = TabInfo.from_dict(tabs_item_data)

            tabs.append(tabs_item)

        user_tabs_config = cls(
            tabs=tabs,
        )

        user_tabs_config.additional_properties = d
        return user_tabs_config

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
