from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import cast, Union
from typing import Dict

if TYPE_CHECKING:
    from ..models.login_config_public import LoginConfigPublic
    from ..models.user import User


T = TypeVar("T", bound="OrganizationMemberWithExtras")


@_attrs_define
class OrganizationMemberWithExtras:
    """
    Attributes:
        user (User):
        login (Union['LoginConfigPublic', None]):
    """

    user: "User"
    login: Union["LoginConfigPublic", None]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.login_config_public import LoginConfigPublic

        user = self.user.to_dict()

        login: Union[Dict[str, Any], None]

        if isinstance(self.login, LoginConfigPublic):
            login = self.login.to_dict()

        else:
            login = self.login

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user": user,
                "login": login,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.login_config_public import LoginConfigPublic
        from ..models.user import User

        d = src_dict.copy()
        user = User.from_dict(d.pop("user"))

        def _parse_login(data: object) -> Union["LoginConfigPublic", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                login_type_0 = LoginConfigPublic.from_dict(data)

                return login_type_0
            except:  # noqa: E722
                pass
            return cast(Union["LoginConfigPublic", None], data)

        login = _parse_login(d.pop("login"))

        organization_member_with_extras = cls(
            user=user,
            login=login,
        )

        organization_member_with_extras.additional_properties = d
        return organization_member_with_extras

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
