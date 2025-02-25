from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from dateutil.parser import isoparse
from typing import cast
import datetime
from ..types import UNSET, Unset


T = TypeVar("T", bound="UserMetadata")


@_attrs_define
class UserMetadata:
    """
    Attributes:
        is_superuser (bool):
        needs_invite_link_version (Union[None, Unset, int]):
        invite_link_expires_at (Union[None, Unset, datetime.datetime]):
    """

    is_superuser: bool
    needs_invite_link_version: Union[None, Unset, int] = UNSET
    invite_link_expires_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        is_superuser = self.is_superuser
        needs_invite_link_version: Union[None, Unset, int]
        if isinstance(self.needs_invite_link_version, Unset):
            needs_invite_link_version = UNSET

        else:
            needs_invite_link_version = self.needs_invite_link_version

        invite_link_expires_at: Union[None, Unset, str]
        if isinstance(self.invite_link_expires_at, Unset):
            invite_link_expires_at = UNSET

        elif isinstance(self.invite_link_expires_at, datetime.datetime):
            invite_link_expires_at = UNSET
            if not isinstance(self.invite_link_expires_at, Unset):
                invite_link_expires_at = self.invite_link_expires_at.isoformat()

        else:
            invite_link_expires_at = self.invite_link_expires_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "is_superuser": is_superuser,
            }
        )
        if needs_invite_link_version is not UNSET:
            field_dict["needs_invite_link_version"] = needs_invite_link_version
        if invite_link_expires_at is not UNSET:
            field_dict["invite_link_expires_at"] = invite_link_expires_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_superuser = d.pop("is_superuser")

        def _parse_needs_invite_link_version(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        needs_invite_link_version = _parse_needs_invite_link_version(
            d.pop("needs_invite_link_version", UNSET)
        )

        def _parse_invite_link_expires_at(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _invite_link_expires_at_type_0 = data
                invite_link_expires_at_type_0: Union[Unset, datetime.datetime]
                if isinstance(_invite_link_expires_at_type_0, Unset):
                    invite_link_expires_at_type_0 = UNSET
                else:
                    invite_link_expires_at_type_0 = isoparse(
                        _invite_link_expires_at_type_0
                    )

                return invite_link_expires_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        invite_link_expires_at = _parse_invite_link_expires_at(
            d.pop("invite_link_expires_at", UNSET)
        )

        user_metadata = cls(
            is_superuser=is_superuser,
            needs_invite_link_version=needs_invite_link_version,
            invite_link_expires_at=invite_link_expires_at,
        )

        user_metadata.additional_properties = d
        return user_metadata

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
