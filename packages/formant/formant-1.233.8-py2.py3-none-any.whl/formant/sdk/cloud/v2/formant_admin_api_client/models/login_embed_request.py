from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.login_request_tags import LoginRequestTags


T = TypeVar("T", bound="LoginEmbedRequest")


@attr.s(auto_attribs=True)
class LoginEmbedRequest:
    """
    Attributes:
        email (str): Email address of your service account.
        password (str): Password of your service account.
        token_expiration_seconds (Union[Unset, int]): Number of seconds the token will be valid.
        tags (Union[Unset, LoginRequestTags]):
    """

    email: str
    password: str
    token_expiration_seconds: Union[Unset, int] = UNSET
    tags: Union[Unset, "LoginRequestTags"] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        email = self.email
        password = self.password
        token_expiration_seconds = self.token_expiration_seconds
        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
            }
        )
        if token_expiration_seconds is not UNSET:
            field_dict["tokenExpirationSeconds"] = token_expiration_seconds
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.login_request_tags import LoginRequestTags

        d = src_dict.copy()
        email = d.pop("email")

        password = d.pop("password")

        token_expiration_seconds = d.pop("tokenExpirationSeconds", UNSET)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, LoginRequestTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = LoginRequestTags.from_dict(_tags)

        login_embed_request = cls(
            email=email,
            password=password,
            token_expiration_seconds=token_expiration_seconds,
            tags=tags,
        )

        login_embed_request.additional_properties = d
        return login_embed_request

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
