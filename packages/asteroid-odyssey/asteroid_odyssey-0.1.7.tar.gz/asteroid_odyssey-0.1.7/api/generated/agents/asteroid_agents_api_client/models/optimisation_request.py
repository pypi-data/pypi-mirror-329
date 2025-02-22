from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="OptimisationRequest")


@_attrs_define
class OptimisationRequest:
    """ 
        Attributes:
            run_id (UUID): The run ID that we want to subject to optimisation Example: 123e4567-e89b-12d3-a456-426614174000.
     """

    run_id: UUID
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        run_id = str(self.run_id)


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "run_id": run_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        run_id = UUID(d.pop("run_id"))




        optimisation_request = cls(
            run_id=run_id,
        )


        optimisation_request.additional_properties = d
        return optimisation_request

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
