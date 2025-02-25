from typing import Any, Dict, Type, TypeVar, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Dict
from typing import Literal
from typing import cast, List

if TYPE_CHECKING:
    from ..models.github_branch import GithubBranch
    from ..models.github_repository import GithubRepository


T = TypeVar("T", bound="GithubRepositoryData")


@_attrs_define
class GithubRepositoryData:
    """
    Attributes:
        integration_uuid (str):
        type (Literal['github']):
        stub (bool):
        url (str):
        github_repo (GithubRepository):
        branches (List['GithubBranch']):
        sot_branch (List[str]):
        sync_branches (List[str]):
    """

    integration_uuid: str
    type: Literal["github"]
    stub: bool
    url: str
    github_repo: "GithubRepository"
    branches: List["GithubBranch"]
    sot_branch: List[str]
    sync_branches: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        integration_uuid = self.integration_uuid
        type = self.type
        stub = self.stub
        url = self.url
        github_repo = self.github_repo.to_dict()

        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()

            branches.append(branches_item)

        sot_branch = self.sot_branch

        sync_branches = self.sync_branches

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "integration_uuid": integration_uuid,
                "type": type,
                "stub": stub,
                "url": url,
                "github_repo": github_repo,
                "branches": branches,
                "sot_branch": sot_branch,
                "sync_branches": sync_branches,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.github_branch import GithubBranch
        from ..models.github_repository import GithubRepository

        d = src_dict.copy()
        integration_uuid = d.pop("integration_uuid")

        type = d.pop("type")

        stub = d.pop("stub")

        url = d.pop("url")

        github_repo = GithubRepository.from_dict(d.pop("github_repo"))

        branches = []
        _branches = d.pop("branches")
        for branches_item_data in _branches:
            branches_item = GithubBranch.from_dict(branches_item_data)

            branches.append(branches_item)

        sot_branch = cast(List[str], d.pop("sot_branch"))

        sync_branches = cast(List[str], d.pop("sync_branches"))

        github_repository_data = cls(
            integration_uuid=integration_uuid,
            type=type,
            stub=stub,
            url=url,
            github_repo=github_repo,
            branches=branches,
            sot_branch=sot_branch,
            sync_branches=sync_branches,
        )

        github_repository_data.additional_properties = d
        return github_repository_data

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
