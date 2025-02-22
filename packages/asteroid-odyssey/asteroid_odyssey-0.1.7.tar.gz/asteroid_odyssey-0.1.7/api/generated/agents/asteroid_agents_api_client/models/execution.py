from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
from typing import Dict
from typing import Union
from uuid import UUID

if TYPE_CHECKING:
  from ..models.execution_dynamic_data import ExecutionDynamicData





T = TypeVar("T", bound="Execution")


@_attrs_define
class Execution:
    """ 
        Attributes:
            id (Union[Unset, UUID]): Execution identifier.
            run_id (Union[Unset, UUID]): Run ID.
            dynamic_data (Union[Unset, ExecutionDynamicData]): Dynamic data to be merged into the saved workflow
                configuration. Example: {'name': 'Alice', 'model': 'gpt-4o'}.
            workflow_id (Union[Unset, UUID]): Workflow ID.
     """

    id: Union[Unset, UUID] = UNSET
    run_id: Union[Unset, UUID] = UNSET
    dynamic_data: Union[Unset, 'ExecutionDynamicData'] = UNSET
    workflow_id: Union[Unset, UUID] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.execution_dynamic_data import ExecutionDynamicData
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        run_id: Union[Unset, str] = UNSET
        if not isinstance(self.run_id, Unset):
            run_id = str(self.run_id)

        dynamic_data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.dynamic_data, Unset):
            dynamic_data = self.dynamic_data.to_dict()

        workflow_id: Union[Unset, str] = UNSET
        if not isinstance(self.workflow_id, Unset):
            workflow_id = str(self.workflow_id)


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if run_id is not UNSET:
            field_dict["run_id"] = run_id
        if dynamic_data is not UNSET:
            field_dict["dynamic_data"] = dynamic_data
        if workflow_id is not UNSET:
            field_dict["workflow_id"] = workflow_id

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.execution_dynamic_data import ExecutionDynamicData
        d = src_dict.copy()
        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _run_id = d.pop("run_id", UNSET)
        run_id: Union[Unset, UUID]
        if isinstance(_run_id,  Unset):
            run_id = UNSET
        else:
            run_id = UUID(_run_id)




        _dynamic_data = d.pop("dynamic_data", UNSET)
        dynamic_data: Union[Unset, ExecutionDynamicData]
        if isinstance(_dynamic_data,  Unset):
            dynamic_data = UNSET
        else:
            dynamic_data = ExecutionDynamicData.from_dict(_dynamic_data)




        _workflow_id = d.pop("workflow_id", UNSET)
        workflow_id: Union[Unset, UUID]
        if isinstance(_workflow_id,  Unset):
            workflow_id = UNSET
        else:
            workflow_id = UUID(_workflow_id)




        execution = cls(
            id=id,
            run_id=run_id,
            dynamic_data=dynamic_data,
            workflow_id=workflow_id,
        )


        execution.additional_properties = d
        return execution

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
