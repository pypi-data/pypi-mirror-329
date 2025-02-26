import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workflow_tags import WorkflowTags


T = TypeVar("T", bound="Workflow")


@attr.s(auto_attribs=True)
class Workflow:
    """
    Attributes:
        name (str):
        workflow (Any):
        intelligence_graph (Any):
        organization_id (Union[Unset, str]):
        tags (Union[Unset, WorkflowTags]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    name: str
    workflow: Any
    intelligence_graph: Any
    organization_id: Union[Unset, str] = UNSET
    tags: Union[Unset, "WorkflowTags"] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        workflow = self.workflow
        intelligence_graph = self.intelligence_graph
        organization_id = self.organization_id
        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "workflow": workflow,
                "intelligenceGraph": intelligence_graph,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_tags import WorkflowTags

        d = src_dict.copy()
        name = d.pop("name")

        workflow = d.pop("workflow")

        intelligence_graph = d.pop("intelligenceGraph")

        organization_id = d.pop("organizationId", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, WorkflowTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = WorkflowTags.from_dict(_tags)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        workflow = cls(
            name=name,
            workflow=workflow,
            intelligence_graph=intelligence_graph,
            organization_id=organization_id,
            tags=tags,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        workflow.additional_properties = d
        return workflow

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
