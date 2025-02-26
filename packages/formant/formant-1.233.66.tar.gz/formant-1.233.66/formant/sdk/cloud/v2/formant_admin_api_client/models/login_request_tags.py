from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="LoginRequestTags")


@attr.s(auto_attribs=True)
class LoginRequestTags:
    """
    Attributes:
        data (Union[Unset, Any]): Provide a tag set with the appropriate access level for devices, data and events.
        entities (Union[Unset, Any]): Provide a tag set with the appropriate access level for Formant entities (e.g.,
            views, command templates, users, teams).
    """

    data: Union[Unset, Any] = UNSET
    entities: Union[Unset, Any] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = self.data
        entities = self.entities

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if data is not UNSET:
            field_dict["data"] = data
        if entities is not UNSET:
            field_dict["entities"] = entities

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        data = d.pop("data", UNSET)

        entities = d.pop("entities", UNSET)

        login_request_tags = cls(
            data=data,
            entities=entities,
        )

        login_request_tags.additional_properties = d
        return login_request_tags

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
