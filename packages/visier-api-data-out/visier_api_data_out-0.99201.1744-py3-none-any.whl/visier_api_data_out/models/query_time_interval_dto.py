# coding: utf-8

"""
    Visier Data Out APIs

    Visier APIs for getting data out of Visier, such as aggregate data and data version information.

    The version of the OpenAPI document: 22222222.99201.1744
    Contact: alpine@visier.com

    Please note that this SDK is currently in beta.
    Functionality and behavior may change in future releases.
    We encourage you to provide feedback and report any issues encountered during your use.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from visier_api_data_out.models.time_shift_dto import TimeShiftDTO
from typing import Optional, Set
from typing_extensions import Self

class QueryTimeIntervalDTO(BaseModel):
    """
    A QueryTimeInterval defines the time interval to query, including the \"from\" time, period type,  period count, time direction, and shift to apply
    """ # noqa: E501
    direction: Optional[StrictStr] = Field(default=None, description="The direction to extend. Default is BACKWARD. BACKWARD is useful when the time instant is the current date or with `dynamicDateFrom` because the query continuously retrieves the newest data from current date backwards.")
    dynamic_date_from: Optional[StrictStr] = Field(default=None, description="Dynamically select the date from which to extend in the specified `direction`. Valid values are `SOURCE` or `COMPLETE_PERIOD`. Both options determine the date using the request's `source` field. Whether the source is a metric, formula, or metrics, each source has earliest and latest data available dates to use. The `direction` determines whether the earliest or latest date is used.   * If `dynamicDateFrom` is `SOURCE`, the query returns data from a date determined by the `source` query definition element. If `dynamicDateFrom` is `COMPLETE_PERIOD`, the query returns data starting from the latest or earliest date with a complete period of data. `COMPLETE_PERIOD` returns periods defined by `intervalPeriodType`. If the period type is MONTH, it returns full months of data. If the period type is YEAR, it returns full years of data. When `dynamicDateFrom` is specified:  * If `source` is `metric`, then `dynamicDateFrom` considers the date range of available data for the metric.  * If `source` is `formula`, then `dynamicDateFrom` considers the date range of available data for the metric in the formula.  * If `source` is `analyticObject`, then `dynamicDateFrom` considers the date range of available data for the analytic object.  Then, if `direction` is `BACKWARD`, query backward from the data **end** date and if `direction` is `FORWARD`, query forward from the data **start** date.  This allows you to keep getting the latest or earliest data without changing your query every time there's new or updated data.    Example: If a tenant has Headcount metric data available from 2023-01-01 to 2024-01-01 (End date exclusive), specifying `dynamicDateFrom`: `SOURCE` with `direction`: `BACKWARD`  means the query will retrieve data backward from 2024-01-01. The effect is the same as if specifying a `fromDateTime` of 2024-01-01'T'00:00:00.000.    Example: If a tenant has Employee subject data available from 2023-01-01 to 2024-01-01 (End date exclusive), specifying `dynamicDateFrom`: `SOURCE` with `direction`: `FORWARD`   means the query will retrieve data forward from 2023-01-01. The effect is the same as if specifying a `fromDateTime` of 2023-01-01'T'00:00:00.000.   Example: If a tenant has Employee subject data available from 2023-01-10 to 2023-04-01 (End date exclusive), specifying `dynamicDateFrom`: `COMPLETE_PERIOD` with `direction`: `FORWARD`   means the query will retrieve data forward from 2023-02-01. The effect is the same as if specifying a `fromDateTime` of 2023-02-01'T'00:00:00.000.   Example: If a tenant has Employee subject data available from 2023-01-01 to 2023-03-15 (End date exclusive), specifying `dynamicDateFrom`: `COMPLETE_PERIOD` with `direction`: `BACKWARD`   means the query will retrieve data backward from 2023-03-01. The effect is the same as if specifying a `fromDateTime` of 2023-03-01'T'00:00:00.000.   Example: Retrieve a list of EmployeeIDs for the formula extending 1 month backward from the dynamic source date       {           \"source\": {               \"formula\": \"on Employee validUntil instant filterBy(isActiveEmployee) aggregate count(Employee.EmployeeID)\"           },            \"columns\": [                {                   \"columnDefinition\": {                       \"property\": {                           \"name\": \"Employee.EmployeeID\",                           \"qualifyingPath\": \"Employee\"                       }                   }                },                {                   \"columnDefinition\": {                       \"effectiveDateProperty\": {}                   }                }           ],           \"timeInterval\": {               \"dynamicDateFrom\": \"SOURCE\",               \"intervalPeriodType\": \"MONTH\",               \"intervalPeriodCount\": 1,               \"direction\": \"BACKWARD\"           }       }", alias="dynamicDateFrom")
    from_date_time: Optional[StrictStr] = Field(default=None, description="The instant from which to extend in the specified `direction`, as an ISO-8601 formatted date time string.  Valid formats: yyyy-MM-dd, yyyy-MM-dd'T'HH:mm:ss, yyyy-MM-dd'T'HH:mm:ss.SSS.  Events that occur on this date are excluded. Subject-based data that ends on this date is included.", alias="fromDateTime")
    from_instant: Optional[StrictStr] = Field(default=None, description="The instant from which to extend in the specified `direction`, in milliseconds since 1970-01-01T00:00:00Z.  Events that occur on this date are excluded. Subject-based data that ends on this date is included.  Note: Epochs are expressed as 64-bit integers and represented as stringified longs in JSON due to  JSON's inherent limitation in representing large numbers.", alias="fromInstant")
    interval_period_count: Optional[StrictInt] = Field(default=None, description="The number of time periods per interval.", alias="intervalPeriodCount")
    interval_period_type: Optional[StrictStr] = Field(default=None, description="The time period type for each interval. Default is MONTH.", alias="intervalPeriodType")
    shift: Optional[TimeShiftDTO] = Field(default=None, description="The amount of time to shift the time interval by, such as backward by one year. Default is none.")
    __properties: ClassVar[List[str]] = ["direction", "dynamicDateFrom", "fromDateTime", "fromInstant", "intervalPeriodCount", "intervalPeriodType", "shift"]

    @field_validator('direction')
    def direction_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['BACKWARD', 'FORWARD']):
            raise ValueError("must be one of enum values ('BACKWARD', 'FORWARD')")
        return value

    @field_validator('dynamic_date_from')
    def dynamic_date_from_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['SOURCE', 'COMPLETE_PERIOD']):
            raise ValueError("must be one of enum values ('SOURCE', 'COMPLETE_PERIOD')")
        return value

    @field_validator('interval_period_type')
    def interval_period_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['MONTH', 'DAY', 'WEEK', 'QUARTER', 'YEAR']):
            raise ValueError("must be one of enum values ('MONTH', 'DAY', 'WEEK', 'QUARTER', 'YEAR')")
        return value

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of QueryTimeIntervalDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of shift
        if self.shift:
            _dict['shift'] = self.shift.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of QueryTimeIntervalDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "direction": obj.get("direction"),
            "dynamicDateFrom": obj.get("dynamicDateFrom"),
            "fromDateTime": obj.get("fromDateTime"),
            "fromInstant": obj.get("fromInstant"),
            "intervalPeriodCount": obj.get("intervalPeriodCount"),
            "intervalPeriodType": obj.get("intervalPeriodType"),
            "shift": TimeShiftDTO.from_dict(obj["shift"]) if obj.get("shift") is not None else None
        })
        return _obj


