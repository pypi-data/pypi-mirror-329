from typing import Any, Dict, Type, TypeVar

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field


T = TypeVar("T", bound="POCReportData")


@_attrs_define
class POCReportData:
    """
    Attributes:
        issues (str):
        edges (str):
        routers (str):
        nodes (str):
        external_ports (str):
        rule_findings (str):
        connect_to (str):
    """

    issues: str
    edges: str
    routers: str
    nodes: str
    external_ports: str
    rule_findings: str
    connect_to: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        issues = self.issues
        edges = self.edges
        routers = self.routers
        nodes = self.nodes
        external_ports = self.external_ports
        rule_findings = self.rule_findings
        connect_to = self.connect_to

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "issues": issues,
                "edges": edges,
                "routers": routers,
                "nodes": nodes,
                "external_ports": external_ports,
                "rule_findings": rule_findings,
                "connectTo": connect_to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        issues = d.pop("issues")

        edges = d.pop("edges")

        routers = d.pop("routers")

        nodes = d.pop("nodes")

        external_ports = d.pop("external_ports")

        rule_findings = d.pop("rule_findings")

        connect_to = d.pop("connectTo")

        poc_report_data = cls(
            issues=issues,
            edges=edges,
            routers=routers,
            nodes=nodes,
            external_ports=external_ports,
            rule_findings=rule_findings,
            connect_to=connect_to,
        )

        poc_report_data.additional_properties = d
        return poc_report_data

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
