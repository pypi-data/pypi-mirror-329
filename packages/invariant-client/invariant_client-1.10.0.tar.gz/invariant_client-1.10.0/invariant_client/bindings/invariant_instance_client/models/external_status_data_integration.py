from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast, Union
from dateutil.parser import isoparse
from ..models.generic_state import GenericState
from typing import Dict
from typing import cast
import datetime
from typing import Literal

if TYPE_CHECKING:
    from ..models.error_info import ErrorInfo


T = TypeVar("T", bound="ExternalStatusDataIntegration")


@_attrs_define
class ExternalStatusDataIntegration:
    """
    Attributes:
        type (Literal['integration']):
        state (GenericState):
        error (Union['ErrorInfo', None]):
        last_used_at (datetime.datetime):
        modified_at (datetime.datetime):
    """

    type: Literal["integration"]
    state: GenericState
    error: Union["ErrorInfo", None]
    last_used_at: datetime.datetime
    modified_at: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.error_info import ErrorInfo

        type = self.type
        state = self.state.value

        error: Union[Dict[str, Any], None]

        if isinstance(self.error, ErrorInfo):
            error = self.error.to_dict()

        else:
            error = self.error

        last_used_at = self.last_used_at.isoformat()

        modified_at = self.modified_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "state": state,
                "error": error,
                "last_used_at": last_used_at,
                "modified_at": modified_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.error_info import ErrorInfo

        d = src_dict.copy()
        type = d.pop("type")

        state = GenericState(d.pop("state"))

        def _parse_error(data: object) -> Union["ErrorInfo", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                error_type_0 = ErrorInfo.from_dict(data)

                return error_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ErrorInfo", None], data)

        error = _parse_error(d.pop("error"))

        last_used_at = isoparse(d.pop("last_used_at"))

        modified_at = isoparse(d.pop("modified_at"))

        external_status_data_integration = cls(
            type=type,
            state=state,
            error=error,
            last_used_at=last_used_at,
            modified_at=modified_at,
        )

        external_status_data_integration.additional_properties = d
        return external_status_data_integration

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
