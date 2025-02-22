from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.failure_category import FailureCategory
from ..models.failure_report_severity import FailureReportSeverity
from ..types import UNSET, Unset
from dateutil.parser import isoparse
from typing import cast
from typing import cast, List
from typing import Dict
from typing import Union
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.supervision_result import SupervisionResult
  from ..models.failure_report_tool_context import FailureReportToolContext





T = TypeVar("T", bound="FailureReport")


@_attrs_define
class FailureReport:
    """ Detailed information about a specific failure

        Attributes:
            run_id (UUID):
            timestamp (datetime.datetime):
            failure_category (FailureCategory):
            failure_reason (str): Detailed explanation of the failure
            supervisor_decisions (List['SupervisionResult']):
            severity (FailureReportSeverity):
            tool_context (Union[Unset, FailureReportToolContext]):
            remediation_suggestion (Union[Unset, str]): Suggested action to prevent similar failures
     """

    run_id: UUID
    timestamp: datetime.datetime
    failure_category: FailureCategory
    failure_reason: str
    supervisor_decisions: List['SupervisionResult']
    severity: FailureReportSeverity
    tool_context: Union[Unset, 'FailureReportToolContext'] = UNSET
    remediation_suggestion: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.supervision_result import SupervisionResult
        from ..models.failure_report_tool_context import FailureReportToolContext
        run_id = str(self.run_id)

        timestamp = self.timestamp.isoformat()

        failure_category = self.failure_category.value

        failure_reason = self.failure_reason

        supervisor_decisions = []
        for supervisor_decisions_item_data in self.supervisor_decisions:
            supervisor_decisions_item = supervisor_decisions_item_data.to_dict()
            supervisor_decisions.append(supervisor_decisions_item)



        severity = self.severity.value

        tool_context: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tool_context, Unset):
            tool_context = self.tool_context.to_dict()

        remediation_suggestion = self.remediation_suggestion


        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "run_id": run_id,
            "timestamp": timestamp,
            "failure_category": failure_category,
            "failure_reason": failure_reason,
            "supervisor_decisions": supervisor_decisions,
            "severity": severity,
        })
        if tool_context is not UNSET:
            field_dict["tool_context"] = tool_context
        if remediation_suggestion is not UNSET:
            field_dict["remediation_suggestion"] = remediation_suggestion

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.supervision_result import SupervisionResult
        from ..models.failure_report_tool_context import FailureReportToolContext
        d = src_dict.copy()
        run_id = UUID(d.pop("run_id"))




        timestamp = isoparse(d.pop("timestamp"))




        failure_category = FailureCategory(d.pop("failure_category"))




        failure_reason = d.pop("failure_reason")

        supervisor_decisions = []
        _supervisor_decisions = d.pop("supervisor_decisions")
        for supervisor_decisions_item_data in (_supervisor_decisions):
            supervisor_decisions_item = SupervisionResult.from_dict(supervisor_decisions_item_data)



            supervisor_decisions.append(supervisor_decisions_item)


        severity = FailureReportSeverity(d.pop("severity"))




        _tool_context = d.pop("tool_context", UNSET)
        tool_context: Union[Unset, FailureReportToolContext]
        if isinstance(_tool_context,  Unset):
            tool_context = UNSET
        else:
            tool_context = FailureReportToolContext.from_dict(_tool_context)




        remediation_suggestion = d.pop("remediation_suggestion", UNSET)

        failure_report = cls(
            run_id=run_id,
            timestamp=timestamp,
            failure_category=failure_category,
            failure_reason=failure_reason,
            supervisor_decisions=supervisor_decisions,
            severity=severity,
            tool_context=tool_context,
            remediation_suggestion=remediation_suggestion,
        )


        failure_report.additional_properties = d
        return failure_report

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
