from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Dict
from typing import cast, List

if TYPE_CHECKING:
    from ..models.integration_data_github_app_installation_data_extra import (
        IntegrationDataGithubAppInstallationDataExtra,
    )


T = TypeVar("T", bound="IntegrationDataGithubAppInstallationData")


@_attrs_define
class IntegrationDataGithubAppInstallationData:
    """
    Attributes:
        user_creator (str):
        gh_creator (str):
        installation_id (str):
        target_orgs (List[str]):
        target_repos (List[str]):
        extra (IntegrationDataGithubAppInstallationDataExtra):
    """

    user_creator: str
    gh_creator: str
    installation_id: str
    target_orgs: List[str]
    target_repos: List[str]
    extra: "IntegrationDataGithubAppInstallationDataExtra"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_creator = self.user_creator
        gh_creator = self.gh_creator
        installation_id = self.installation_id
        target_orgs = self.target_orgs

        target_repos = self.target_repos

        extra = self.extra.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_creator": user_creator,
                "gh_creator": gh_creator,
                "installation_id": installation_id,
                "target_orgs": target_orgs,
                "target_repos": target_repos,
                "extra": extra,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.integration_data_github_app_installation_data_extra import (
            IntegrationDataGithubAppInstallationDataExtra,
        )

        d = src_dict.copy()
        user_creator = d.pop("user_creator")

        gh_creator = d.pop("gh_creator")

        installation_id = d.pop("installation_id")

        target_orgs = cast(List[str], d.pop("target_orgs"))

        target_repos = cast(List[str], d.pop("target_repos"))

        extra = IntegrationDataGithubAppInstallationDataExtra.from_dict(d.pop("extra"))

        integration_data_github_app_installation_data = cls(
            user_creator=user_creator,
            gh_creator=gh_creator,
            installation_id=installation_id,
            target_orgs=target_orgs,
            target_repos=target_repos,
            extra=extra,
        )

        integration_data_github_app_installation_data.additional_properties = d
        return integration_data_github_app_installation_data

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
