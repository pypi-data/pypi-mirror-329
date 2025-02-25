from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Literal, Union


T = TypeVar("T", bound="RefreshResponse")


@_attrs_define
class RefreshResponse:
    """
    Attributes:
        access_token (str):
        status (Union[Literal[200], Unset]):  Default: 200.
        type (Union[Literal['urn:invariant:responses:refresh_response'], Unset]):  Default:
            'urn:invariant:responses:refresh_response'.
    """

    access_token: str
    status: Union[Literal[200], Unset] = 200
    type: Union[
        Literal["urn:invariant:responses:refresh_response"], Unset
    ] = "urn:invariant:responses:refresh_response"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        access_token = self.access_token
        status = self.status
        type = self.type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "access_token": access_token,
            }
        )
        if status is not UNSET:
            field_dict["status"] = status
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        access_token = d.pop("access_token")

        status = d.pop("status", UNSET)

        type = d.pop("type", UNSET)

        refresh_response = cls(
            access_token=access_token,
            status=status,
            type=type,
        )

        refresh_response.additional_properties = d
        return refresh_response

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
