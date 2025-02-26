import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.partial_workflow_tags import PartialWorkflowTags


T = TypeVar("T", bound="PartialWorkflow")


@attr.s(auto_attribs=True)
class PartialWorkflow:
    """
    Attributes:
        organization_id (Union[Unset, str]):
        name (Union[Unset, str]):
        workflow (Union[Unset, Any]):
        intelligence_graph (Union[Unset, Any]):
        tags (Union[Unset, PartialWorkflowTags]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    organization_id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    workflow: Union[Unset, Any] = UNSET
    intelligence_graph: Union[Unset, Any] = UNSET
    tags: Union[Unset, "PartialWorkflowTags"] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        organization_id = self.organization_id
        name = self.name
        workflow = self.workflow
        intelligence_graph = self.intelligence_graph
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
        field_dict.update({})
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if name is not UNSET:
            field_dict["name"] = name
        if workflow is not UNSET:
            field_dict["workflow"] = workflow
        if intelligence_graph is not UNSET:
            field_dict["intelligenceGraph"] = intelligence_graph
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
        from ..models.partial_workflow_tags import PartialWorkflowTags

        d = src_dict.copy()
        organization_id = d.pop("organizationId", UNSET)

        name = d.pop("name", UNSET)

        workflow = d.pop("workflow", UNSET)

        intelligence_graph = d.pop("intelligenceGraph", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PartialWorkflowTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PartialWorkflowTags.from_dict(_tags)

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

        partial_workflow = cls(
            organization_id=organization_id,
            name=name,
            workflow=workflow,
            intelligence_graph=intelligence_graph,
            tags=tags,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        partial_workflow.additional_properties = d
        return partial_workflow

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
