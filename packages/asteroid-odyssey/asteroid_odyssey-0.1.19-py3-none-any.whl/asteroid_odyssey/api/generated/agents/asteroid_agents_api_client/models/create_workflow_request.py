from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_workflow_request_provider import CreateWorkflowRequestProvider
from typing import cast
from typing import cast, List
from typing import Dict

if TYPE_CHECKING:
  from ..models.create_workflow_request_fields import CreateWorkflowRequestFields





T = TypeVar("T", bound="CreateWorkflowRequest")


@_attrs_define
class CreateWorkflowRequest:
    """ 
        Attributes:
            name (str): The name of the workflow. Example: My workflow.
            fields (CreateWorkflowRequestFields): JSON object containing static workflow configuration (e.g. a
                prompt_template). Example: {'model': 'gpt-4o', 'version': '2024-02-01'}.
            prompts (List[str]): The prompts for the workflow. They can have variables in them. They will be merged with the
                dynamic data passed when the workflow is executed. Example: ['Your name is {{.name}}, you speak {{.language}}',
                'Your task is {{.task}}'].
            provider (CreateWorkflowRequestProvider): The Language Model Provider for the Workflow Example: openai.
     """

    name: str
    fields: 'CreateWorkflowRequestFields'
    prompts: List[str]
    provider: CreateWorkflowRequestProvider
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.create_workflow_request_fields import CreateWorkflowRequestFields
        name = self.name

        fields = self.fields.to_dict()

        prompts = self.prompts



        provider = self.provider.value


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "fields": fields,
            "prompts": prompts,
            "provider": provider,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_workflow_request_fields import CreateWorkflowRequestFields
        d = src_dict.copy()
        name = d.pop("name")

        fields = CreateWorkflowRequestFields.from_dict(d.pop("fields"))




        prompts = cast(List[str], d.pop("prompts"))


        provider = CreateWorkflowRequestProvider(d.pop("provider"))




        create_workflow_request = cls(
            name=name,
            fields=fields,
            prompts=prompts,
            provider=provider,
        )


        create_workflow_request.additional_properties = d
        return create_workflow_request

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
