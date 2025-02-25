from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, Union
from typing import cast, List


T = TypeVar("T", bound="CreateNotificationGroupRequest")


@_attrs_define
class CreateNotificationGroupRequest:
    """
    Attributes:
        name (str):
        comment (str):
        email_targets (Union[List[str], None]):
        network_subscriptions (Union[List[str], None]):
    """

    name: str
    comment: str
    email_targets: Union[List[str], None]
    network_subscriptions: Union[List[str], None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        comment = self.comment
        email_targets: Union[List[str], None]

        if isinstance(self.email_targets, list):
            email_targets = self.email_targets

        else:
            email_targets = self.email_targets

        network_subscriptions: Union[List[str], None]

        if isinstance(self.network_subscriptions, list):
            network_subscriptions = self.network_subscriptions

        else:
            network_subscriptions = self.network_subscriptions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "comment": comment,
                "email_targets": email_targets,
                "network_subscriptions": network_subscriptions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        comment = d.pop("comment")

        def _parse_email_targets(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                email_targets_type_0 = cast(List[str], data)

                return email_targets_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        email_targets = _parse_email_targets(d.pop("email_targets"))

        def _parse_network_subscriptions(data: object) -> Union[List[str], None]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                network_subscriptions_type_0 = cast(List[str], data)

                return network_subscriptions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None], data)

        network_subscriptions = _parse_network_subscriptions(
            d.pop("network_subscriptions")
        )

        create_notification_group_request = cls(
            name=name,
            comment=comment,
            email_targets=email_targets,
            network_subscriptions=network_subscriptions,
        )

        create_notification_group_request.additional_properties = d
        return create_notification_group_request

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
