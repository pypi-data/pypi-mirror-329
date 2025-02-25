from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import cast, List
from ..types import UNSET, Unset


T = TypeVar("T", bound="NotificationGroupMetadata")


@_attrs_define
class NotificationGroupMetadata:
    """
    Attributes:
        name (str):
        comment (Union[None, Unset, str]):
        email_targets (Union[List[str], None, Unset]):
        network_subscriptions (Union[List[str], None, Unset]):
    """

    name: str
    comment: Union[None, Unset, str] = UNSET
    email_targets: Union[List[str], None, Unset] = UNSET
    network_subscriptions: Union[List[str], None, Unset] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        comment: Union[None, Unset, str]
        if isinstance(self.comment, Unset):
            comment = UNSET

        else:
            comment = self.comment

        email_targets: Union[List[str], None, Unset]
        if isinstance(self.email_targets, Unset):
            email_targets = UNSET

        elif isinstance(self.email_targets, list):
            email_targets = UNSET
            if not isinstance(self.email_targets, Unset):
                email_targets = self.email_targets

        else:
            email_targets = self.email_targets

        network_subscriptions: Union[List[str], None, Unset]
        if isinstance(self.network_subscriptions, Unset):
            network_subscriptions = UNSET

        elif isinstance(self.network_subscriptions, list):
            network_subscriptions = UNSET
            if not isinstance(self.network_subscriptions, Unset):
                network_subscriptions = self.network_subscriptions

        else:
            network_subscriptions = self.network_subscriptions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if comment is not UNSET:
            field_dict["comment"] = comment
        if email_targets is not UNSET:
            field_dict["email_targets"] = email_targets
        if network_subscriptions is not UNSET:
            field_dict["network_subscriptions"] = network_subscriptions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        def _parse_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        comment = _parse_comment(d.pop("comment", UNSET))

        def _parse_email_targets(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                email_targets_type_0 = cast(List[str], data)

                return email_targets_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        email_targets = _parse_email_targets(d.pop("email_targets", UNSET))

        def _parse_network_subscriptions(data: object) -> Union[List[str], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                network_subscriptions_type_0 = cast(List[str], data)

                return network_subscriptions_type_0
            except:  # noqa: E722
                pass
            return cast(Union[List[str], None, Unset], data)

        network_subscriptions = _parse_network_subscriptions(
            d.pop("network_subscriptions", UNSET)
        )

        notification_group_metadata = cls(
            name=name,
            comment=comment,
            email_targets=email_targets,
            network_subscriptions=network_subscriptions,
        )

        notification_group_metadata.additional_properties = d
        return notification_group_metadata

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
