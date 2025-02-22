from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast, List






T = TypeVar("T", bound="Agent")


@_attrs_define
class Agent:
    """ 
        Attributes:
            name (str): The name of the agent Example: my_agent.
            description (str): The description of the agent Example: This agent is used to queue jobs.
            visibility (str): The visibility of the agent Example: public.
            required_fields (List[str]): The required fields for the agent Example: ['system_prompt_template'].
            required_prompts (List[str]): The prompts for the agent Example: ['Hello {{.name}}, your model is {{.model}}'].
     """

    name: str
    description: str
    visibility: str
    required_fields: List[str]
    required_prompts: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        description = self.description

        visibility = self.visibility

        required_fields = self.required_fields



        required_prompts = self.required_prompts




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "visibility": visibility,
            "required_fields": required_fields,
            "required_prompts": required_prompts,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        visibility = d.pop("visibility")

        required_fields = cast(List[str], d.pop("required_fields"))


        required_prompts = cast(List[str], d.pop("required_prompts"))


        agent = cls(
            name=name,
            description=description,
            visibility=visibility,
            required_fields=required_fields,
            required_prompts=required_prompts,
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
