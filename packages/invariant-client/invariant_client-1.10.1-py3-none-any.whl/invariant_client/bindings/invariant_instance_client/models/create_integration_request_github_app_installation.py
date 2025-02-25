from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import Dict
from typing import Literal

if TYPE_CHECKING:
    from ..models.create_integration_request_github_app_installation_data import (
        CreateIntegrationRequestGithubAppInstallationData,
    )


T = TypeVar("T", bound="CreateIntegrationRequestGithubAppInstallation")


@_attrs_define
class CreateIntegrationRequestGithubAppInstallation:
    """
    Attributes:
        type (Literal['github_app_installation']):
        github_app_install (CreateIntegrationRequestGithubAppInstallationData):
    """

    type: Literal["github_app_installation"]
    github_app_install: "CreateIntegrationRequestGithubAppInstallationData"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type
        github_app_install = self.github_app_install.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "github_app_install": github_app_install,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_integration_request_github_app_installation_data import (
            CreateIntegrationRequestGithubAppInstallationData,
        )

        d = src_dict.copy()
        type = d.pop("type")

        github_app_install = (
            CreateIntegrationRequestGithubAppInstallationData.from_dict(
                d.pop("github_app_install")
            )
        )

        create_integration_request_github_app_installation = cls(
            type=type,
            github_app_install=github_app_install,
        )

        create_integration_request_github_app_installation.additional_properties = d
        return create_integration_request_github_app_installation

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
