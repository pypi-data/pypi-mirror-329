from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import cast, List
from typing import Dict

if TYPE_CHECKING:
  from ..models.workflow import Workflow
  from ..models.execution import Execution





T = TypeVar("T", bound="WorkflowExecution")


@_attrs_define
class WorkflowExecution:
    """ 
        Attributes:
            workflow (Workflow):
            executions (List['Execution']):
     """

    workflow: 'Workflow'
    executions: List['Execution']
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.workflow import Workflow
        from ..models.execution import Execution
        workflow = self.workflow.to_dict()

        executions = []
        for executions_item_data in self.executions:
            executions_item = executions_item_data.to_dict()
            executions.append(executions_item)




        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "workflow": workflow,
            "executions": executions,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.workflow import Workflow
        from ..models.execution import Execution
        d = src_dict.copy()
        workflow = Workflow.from_dict(d.pop("workflow"))




        executions = []
        _executions = d.pop("executions")
        for executions_item_data in (_executions):
            executions_item = Execution.from_dict(executions_item_data)



            executions.append(executions_item)


        workflow_execution = cls(
            workflow=workflow,
            executions=executions,
        )


        workflow_execution.additional_properties = d
        return workflow_execution

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
