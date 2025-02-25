from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict

if TYPE_CHECKING:
    from ..models.flags_response_environment import FlagsResponseEnvironment
    from ..models.flags_response_flags import FlagsResponseFlags


T = TypeVar("T", bound="FlagsResponse")


@_attrs_define
class FlagsResponse:
    """
    Attributes:
        etag (str):
        environment (FlagsResponseEnvironment):
        flags (FlagsResponseFlags):
    """

    etag: str
    environment: "FlagsResponseEnvironment"
    flags: "FlagsResponseFlags"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        etag = self.etag
        environment = self.environment.to_dict()

        flags = self.flags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "etag": etag,
                "environment": environment,
                "flags": flags,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.flags_response_environment import FlagsResponseEnvironment
        from ..models.flags_response_flags import FlagsResponseFlags

        d = src_dict.copy()
        etag = d.pop("etag")

        environment = FlagsResponseEnvironment.from_dict(d.pop("environment"))

        flags = FlagsResponseFlags.from_dict(d.pop("flags"))

        flags_response = cls(
            etag=etag,
            environment=environment,
            flags=flags,
        )

        flags_response.additional_properties = d
        return flags_response

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
