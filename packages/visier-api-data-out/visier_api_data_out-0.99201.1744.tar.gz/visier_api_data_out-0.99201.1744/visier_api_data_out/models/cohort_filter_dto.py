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

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from visier_api_data_out.models.key_group_filter_dto import KeyGroupFilterDTO
from visier_api_data_out.models.query_time_interval_dto import QueryTimeIntervalDTO
from typing import Optional, Set
from typing_extensions import Self

class CohortFilterDTO(BaseModel):
    """
    Use a cohort filter to define a population as it existed during a specific time period.  Cohort filters allow you to define a population in terms of a collection of filters, known as a key group.  The cohort's defined time interval is independent of the query's time. The cohort's time interval is the  time at which the key group should be applied.  Cohorts are typically used to follow populations and understand changes to the population over time,  such as promotion and resignation rates.
    """ # noqa: E501
    exclude: Optional[StrictBool] = Field(default=None, description="If true, the population is defined by those excluded by the filters. Default is false.")
    key_group: Optional[KeyGroupFilterDTO] = Field(default=None, description="A key group is a collection of filters that define the shape of the analysis population.", alias="keyGroup")
    time_interval: Optional[QueryTimeIntervalDTO] = Field(default=None, description="The time at which to apply the key group, such as a specific day or period of months.", alias="timeInterval")
    __properties: ClassVar[List[str]] = ["exclude", "keyGroup", "timeInterval"]

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
        """Create an instance of CohortFilterDTO from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of key_group
        if self.key_group:
            _dict['keyGroup'] = self.key_group.to_dict()
        # override the default output from pydantic by calling `to_dict()` of time_interval
        if self.time_interval:
            _dict['timeInterval'] = self.time_interval.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CohortFilterDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "exclude": obj.get("exclude"),
            "keyGroup": KeyGroupFilterDTO.from_dict(obj["keyGroup"]) if obj.get("keyGroup") is not None else None,
            "timeInterval": QueryTimeIntervalDTO.from_dict(obj["timeInterval"]) if obj.get("timeInterval") is not None else None
        })
        return _obj


