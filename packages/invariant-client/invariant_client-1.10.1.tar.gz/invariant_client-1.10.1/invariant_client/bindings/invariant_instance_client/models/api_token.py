from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from dateutil.parser import isoparse
from typing import Dict
from typing import cast
import datetime
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.api_token_metadata import APITokenMetadata


T = TypeVar("T", bound="APIToken")


@_attrs_define
class APIToken:
    """
    Attributes:
        uuid (str):
        organization_uuid (str):
        user_uuid (str):
        metadata (APITokenMetadata):
        created_at (datetime.datetime):
        deleted_at (Union[None, Unset, datetime.datetime]):
    """

    uuid: str
    organization_uuid: str
    user_uuid: str
    metadata: "APITokenMetadata"
    created_at: datetime.datetime
    deleted_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        organization_uuid = self.organization_uuid
        user_uuid = self.user_uuid
        metadata = self.metadata.to_dict()

        created_at = self.created_at.isoformat()

        deleted_at: Union[None, Unset, str]
        if isinstance(self.deleted_at, Unset):
            deleted_at = UNSET

        elif isinstance(self.deleted_at, datetime.datetime):
            deleted_at = UNSET
            if not isinstance(self.deleted_at, Unset):
                deleted_at = self.deleted_at.isoformat()

        else:
            deleted_at = self.deleted_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization_uuid": organization_uuid,
                "user_uuid": user_uuid,
                "metadata": metadata,
                "created_at": created_at,
            }
        )
        if deleted_at is not UNSET:
            field_dict["deleted_at"] = deleted_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.api_token_metadata import APITokenMetadata

        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization_uuid = d.pop("organization_uuid")

        user_uuid = d.pop("user_uuid")

        metadata = APITokenMetadata.from_dict(d.pop("metadata"))

        created_at = isoparse(d.pop("created_at"))

        def _parse_deleted_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                _deleted_at_type_0 = data
                deleted_at_type_0: Union[Unset, datetime.datetime]
                if isinstance(_deleted_at_type_0, Unset):
                    deleted_at_type_0 = UNSET
                else:
                    deleted_at_type_0 = isoparse(_deleted_at_type_0)

                return deleted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deleted_at = _parse_deleted_at(d.pop("deleted_at", UNSET))

        api_token = cls(
            uuid=uuid,
            organization_uuid=organization_uuid,
            user_uuid=user_uuid,
            metadata=metadata,
            created_at=created_at,
            deleted_at=deleted_at,
        )

        api_token.additional_properties = d
        return api_token

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
