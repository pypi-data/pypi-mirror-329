from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict

if TYPE_CHECKING:
    from ..models.organization_summary import OrganizationSummary
    from ..models.login_summary import LoginSummary


T = TypeVar("T", bound="UserSummary")


@_attrs_define
class UserSummary:
    """
    Attributes:
        uuid (str):
        organization (OrganizationSummary):
        login (LoginSummary):
        email (str):
        is_active (bool):
        is_superuser (bool):
    """

    uuid: str
    organization: "OrganizationSummary"
    login: "LoginSummary"
    email: str
    is_active: bool
    is_superuser: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid
        organization = self.organization.to_dict()

        login = self.login.to_dict()

        email = self.email
        is_active = self.is_active
        is_superuser = self.is_superuser

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "organization": organization,
                "login": login,
                "email": email,
                "is_active": is_active,
                "is_superuser": is_superuser,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.organization_summary import OrganizationSummary
        from ..models.login_summary import LoginSummary

        d = src_dict.copy()
        uuid = d.pop("uuid")

        organization = OrganizationSummary.from_dict(d.pop("organization"))

        login = LoginSummary.from_dict(d.pop("login"))

        email = d.pop("email")

        is_active = d.pop("is_active")

        is_superuser = d.pop("is_superuser")

        user_summary = cls(
            uuid=uuid,
            organization=organization,
            login=login,
            email=email,
            is_active=is_active,
            is_superuser=is_superuser,
        )

        user_summary.additional_properties = d
        return user_summary

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
