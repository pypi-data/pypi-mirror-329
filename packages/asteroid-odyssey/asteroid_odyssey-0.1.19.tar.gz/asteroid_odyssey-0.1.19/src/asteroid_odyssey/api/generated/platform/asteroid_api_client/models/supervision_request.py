from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import Dict
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.supervision_status import SupervisionStatus





T = TypeVar("T", bound="SupervisionRequest")


@_attrs_define
class SupervisionRequest:
    """ 
        Attributes:
            supervisor_id (UUID):
            position_in_chain (int):
            id (Union[Unset, UUID]):
            chainexecution_id (Union[Unset, UUID]):
            status (Union[Unset, SupervisionStatus]):
            last_status_checked_at (Union[Unset, datetime.datetime]):
     """

    supervisor_id: UUID
    position_in_chain: int
    id: Union[Unset, UUID] = UNSET
    chainexecution_id: Union[Unset, UUID] = UNSET
    status: Union[Unset, 'SupervisionStatus'] = UNSET
    last_status_checked_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.supervision_status import SupervisionStatus
        supervisor_id = str(self.supervisor_id)

        position_in_chain = self.position_in_chain

        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = str(self.id)

        chainexecution_id: Union[Unset, str] = UNSET
        if not isinstance(self.chainexecution_id, Unset):
            chainexecution_id = str(self.chainexecution_id)

        status: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        last_status_checked_at: Union[Unset, str] = UNSET
        if not isinstance(self.last_status_checked_at, Unset):
            last_status_checked_at = self.last_status_checked_at.isoformat()


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "supervisor_id": supervisor_id,
            "position_in_chain": position_in_chain,
        })
        if id is not UNSET:
            field_dict["id"] = id
        if chainexecution_id is not UNSET:
            field_dict["chainexecution_id"] = chainexecution_id
        if status is not UNSET:
            field_dict["status"] = status
        if last_status_checked_at is not UNSET:
            field_dict["last_status_checked_at"] = last_status_checked_at

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.supervision_status import SupervisionStatus
        d = src_dict.copy()
        supervisor_id = UUID(d.pop("supervisor_id"))




        position_in_chain = d.pop("position_in_chain")

        _id = d.pop("id", UNSET)
        id: Union[Unset, UUID]
        if isinstance(_id,  Unset):
            id = UNSET
        else:
            id = UUID(_id)




        _chainexecution_id = d.pop("chainexecution_id", UNSET)
        chainexecution_id: Union[Unset, UUID]
        if isinstance(_chainexecution_id,  Unset):
            chainexecution_id = UNSET
        else:
            chainexecution_id = UUID(_chainexecution_id)




        _status = d.pop("status", UNSET)
        status: Union[Unset, SupervisionStatus]
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = SupervisionStatus.from_dict(_status)




        _last_status_checked_at = d.pop("last_status_checked_at", UNSET)
        last_status_checked_at: Union[Unset, datetime.datetime]
        if isinstance(_last_status_checked_at,  Unset):
            last_status_checked_at = UNSET
        else:
            last_status_checked_at = isoparse(_last_status_checked_at)




        supervision_request = cls(
            supervisor_id=supervisor_id,
            position_in_chain=position_in_chain,
            id=id,
            chainexecution_id=chainexecution_id,
            status=status,
            last_status_checked_at=last_status_checked_at,
        )


        supervision_request.additional_properties = d
        return supervision_request

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
