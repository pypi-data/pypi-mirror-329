from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """
    Attributes:
        name (str): The name of the agent Example: my_agent.
        description (str): The description of the agent Example: This agent is used to queue jobs.
        image_url (str): The image URL of the agent Example: /images/agents/default_web.jpeg.
        required_fields (List[str]): The required fields for the agent Example: ['task'].
    """

    name: str
    description: str
    image_url: str
    required_fields: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        image_url = self.image_url

        required_fields = self.required_fields

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "image_url": image_url,
                "required_fields": required_fields,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        image_url = d.pop("image_url")

        required_fields = cast(List[str], d.pop("required_fields"))

        agent = cls(
            name=name,
            description=description,
            image_url=image_url,
            required_fields=required_fields,
        )

        agent.additional_properties = d
        return agent

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
