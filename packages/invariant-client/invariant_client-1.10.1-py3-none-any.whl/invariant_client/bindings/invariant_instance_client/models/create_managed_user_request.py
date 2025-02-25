from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union
from typing import cast, Union
from typing import Dict
from typing import cast
from typing import cast, List
from ..types import UNSET, Unset
from typing import Literal

if TYPE_CHECKING:
    from ..models.oidc_login_method import OIDCLoginMethod
    from ..models.basic_auth_login_method import BasicAuthLoginMethod


T = TypeVar("T", bound="CreateManagedUserRequest")


@_attrs_define
class CreateManagedUserRequest:
    """
    Attributes:
        type (Literal['managed']):
        email (str):
        allowed_methods (Union[List[Union['BasicAuthLoginMethod', 'OIDCLoginMethod']], None, Unset]):
        send_invite (Union[Unset, bool]):
        use_setup_code (Union[Unset, bool]):
        is_superuser (Union[Unset, bool]):
    """

    type: Literal["managed"]
    email: str
    allowed_methods: Union[
        List[Union["BasicAuthLoginMethod", "OIDCLoginMethod"]], None, Unset
    ] = UNSET
    send_invite: Union[Unset, bool] = False
    use_setup_code: Union[Unset, bool] = False
    is_superuser: Union[Unset, bool] = False
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        type = self.type
        email = self.email
        allowed_methods: Union[List[Dict[str, Any]], None, Unset]
        if isinstance(self.allowed_methods, Unset):
            allowed_methods = UNSET

        elif isinstance(self.allowed_methods, list):
            allowed_methods = UNSET
            if not isinstance(self.allowed_methods, Unset):
                allowed_methods = []
                for allowed_methods_type_0_item_data in self.allowed_methods:
                    allowed_methods_type_0_item: Dict[str, Any]

                    if isinstance(
                        allowed_methods_type_0_item_data, BasicAuthLoginMethod
                    ):
                        allowed_methods_type_0_item = (
                            allowed_methods_type_0_item_data.to_dict()
                        )

                    else:
                        allowed_methods_type_0_item = (
                            allowed_methods_type_0_item_data.to_dict()
                        )

                    allowed_methods.append(allowed_methods_type_0_item)

        else:
            allowed_methods = self.allowed_methods

        send_invite = self.send_invite
        use_setup_code = self.use_setup_code
        is_superuser = self.is_superuser

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "email": email,
            }
        )
        if allowed_methods is not UNSET:
            field_dict["allowed_methods"] = allowed_methods
        if send_invite is not UNSET:
            field_dict["send_invite"] = send_invite
        if use_setup_code is not UNSET:
            field_dict["use_setup_code"] = use_setup_code
        if is_superuser is not UNSET:
            field_dict["is_superuser"] = is_superuser

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.oidc_login_method import OIDCLoginMethod
        from ..models.basic_auth_login_method import BasicAuthLoginMethod

        d = src_dict.copy()
        type = d.pop("type")

        email = d.pop("email")

        def _parse_allowed_methods(
            data: object,
        ) -> Union[List[Union["BasicAuthLoginMethod", "OIDCLoginMethod"]], None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_methods_type_0 = UNSET
                _allowed_methods_type_0 = data
                for allowed_methods_type_0_item_data in _allowed_methods_type_0 or []:

                    def _parse_allowed_methods_type_0_item(
                        data: object,
                    ) -> Union["BasicAuthLoginMethod", "OIDCLoginMethod"]:
                        try:
                            if not isinstance(data, dict):
                                raise TypeError()
                            allowed_methods_type_0_item_type_0 = (
                                BasicAuthLoginMethod.from_dict(data)
                            )

                            return allowed_methods_type_0_item_type_0
                        except:  # noqa: E722
                            pass
                        if not isinstance(data, dict):
                            raise TypeError()
                        allowed_methods_type_0_item_type_1 = OIDCLoginMethod.from_dict(
                            data
                        )

                        return allowed_methods_type_0_item_type_1

                    allowed_methods_type_0_item = _parse_allowed_methods_type_0_item(
                        allowed_methods_type_0_item_data
                    )

                    allowed_methods_type_0.append(allowed_methods_type_0_item)

                return allowed_methods_type_0
            except:  # noqa: E722
                pass
            return cast(
                Union[
                    List[Union["BasicAuthLoginMethod", "OIDCLoginMethod"]], None, Unset
                ],
                data,
            )

        allowed_methods = _parse_allowed_methods(d.pop("allowed_methods", UNSET))

        send_invite = d.pop("send_invite", UNSET)

        use_setup_code = d.pop("use_setup_code", UNSET)

        is_superuser = d.pop("is_superuser", UNSET)

        create_managed_user_request = cls(
            type=type,
            email=email,
            allowed_methods=allowed_methods,
            send_invite=send_invite,
            use_setup_code=use_setup_code,
            is_superuser=is_superuser,
        )

        create_managed_user_request.additional_properties = d
        return create_managed_user_request

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
