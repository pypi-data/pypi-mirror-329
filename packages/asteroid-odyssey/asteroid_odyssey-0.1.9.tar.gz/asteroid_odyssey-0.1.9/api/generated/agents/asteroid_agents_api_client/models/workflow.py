from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import cast, List
from typing import Dict
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.workflow_fields import WorkflowFields





T = TypeVar("T", bound="Workflow")


@_attrs_define
class Workflow:
    """ 
        Attributes:
            id (Union[Unset, UUID]): Workflow identifier.
            agent_id (Union[Unset, UUID]): Identifier of the associated agent.
            name (Union[Unset, str]): Workflow name.
            fields (Union[Unset, WorkflowFields]): Workflow configuration. Example: {'model': 'gpt-4o', 'version':
                '2024-02-01'}.
            prompts (Union[Unset, List[str]]): The prompts for the workflow. They can have variables in them. They will be
                merged with the dynamic data passed when the workflow is executed. Example: ['Your name is {{.name}}, you speak
                {{.language}}', 'Your task is {{.task}}'].
            prompt_variables (Union[Unset, List[str]]): The variables in the prompts. Example: ['name', 'language', 'task'].
     """

    id: Union[Unset, UUID] = UNSET
    agent_id: Union[Unset, UUID] = UNSET
    name: Union[Unset, str] = UNSET
    fields: Union[Unset, 'WorkflowFields'] = UNSET
    prompts: Union[Unset, List[str]] = UNSET
    prompt_variables: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.workflow_fields import WorkflowFields
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        agent_id: Union[Unset, str] = UNSET
        if not isinstance(self.agent_id, Unset):
            agent_id = str(self.agent_id)

        name = self.name

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        prompts: Union[Unset, List[str]] = UNSET
        if not isinstance(self.prompts, Unset):
            prompts = self.prompts



        prompt_variables: Union[Unset, List[str]] = UNSET
        if not isinstance(self.prompt_variables, Unset):
            prompt_variables = self.prompt_variables




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if name is not UNSET:
            field_dict["name"] = name
        if fields is not UNSET:
            field_dict["fields"] = fields
        if prompts is not UNSET:
            field_dict["prompts"] = prompts
        if prompt_variables is not UNSET:
            field_dict["prompt_variables"] = prompt_variables

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow_fields import WorkflowFields
        d = src_dict.copy()
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _agent_id = d.pop("agent_id", UNSET)
        agent_id: Union[Unset, UUID]
        if isinstance(_agent_id,  Unset):
            agent_id = UNSET
        else:
            agent_id = UUID(_agent_id)




        name = d.pop("name", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, WorkflowFields]
        if isinstance(_fields,  Unset):
            fields = UNSET
        else:
            fields = WorkflowFields.from_dict(_fields)




        prompts = cast(List[str], d.pop("prompts", UNSET))


        prompt_variables = cast(List[str], d.pop("prompt_variables", UNSET))


        workflow = cls(
            id=id,
            agent_id=agent_id,
            name=name,
            fields=fields,
            prompts=prompts,
            prompt_variables=prompt_variables,
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
