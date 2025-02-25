from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union
from typing import Literal
from typing import cast
from typing import cast, Union
from typing import Dict
from typing import cast, List

if TYPE_CHECKING:
    from ..models.validation_error_response_part import ValidationErrorResponsePart


T = TypeVar("T", bound="ValidationErrorResponse")


@_attrs_define
class ValidationErrorResponse:
    """
    Attributes:
        status (int):
        type (Literal['urn:invariant:errors:validation']):
        title (Literal['There was a problem with your request.']):
        detail (str):
        validations (List['ValidationErrorResponsePart']):
        instance (Union[None, Unset, str]):
    """

    status: int
    type: Literal["urn:invariant:errors:validation"]
    title: Literal["There was a problem with your request."]
    detail: str
    validations: List["ValidationErrorResponsePart"]
    instance: Union[None, Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status
        type = self.type
        title = self.title
        detail = self.detail
        validations = []
        for validations_item_data in self.validations:
            validations_item = validations_item_data.to_dict()

            validations.append(validations_item)

        instance: Union[None, Unset, str]
        if isinstance(self.instance, Unset):
            instance = UNSET

        else:
            instance = self.instance

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "type": type,
                "title": title,
                "detail": detail,
                "validations": validations,
            }
        )
        if instance is not UNSET:
            field_dict["instance"] = instance

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.validation_error_response_part import ValidationErrorResponsePart

        d = src_dict.copy()
        status = d.pop("status")

        type = d.pop("type")

        title = d.pop("title")

        detail = d.pop("detail")

        validations = []
        _validations = d.pop("validations")
        for validations_item_data in _validations:
            validations_item = ValidationErrorResponsePart.from_dict(
                validations_item_data
            )

            validations.append(validations_item)

        def _parse_instance(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        instance = _parse_instance(d.pop("instance", UNSET))

        validation_error_response = cls(
            status=status,
            type=type,
            title=title,
            detail=detail,
            validations=validations,
            instance=instance,
        )

        validation_error_response.additional_properties = d
        return validation_error_response

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
