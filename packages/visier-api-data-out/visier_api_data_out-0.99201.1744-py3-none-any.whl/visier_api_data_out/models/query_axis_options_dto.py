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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class QueryAxisOptionsDTO(BaseModel):
    """
    QueryAxisOptions allows you to customize an axis in the query, such as changing the display mode for its cell set values or providing a custom column name.  Only available when the Accept header is a table format, such as text/csv or application/jsonlines.
    """ # noqa: E501
    column_name: Optional[StrictStr] = Field(default=None, description="If specified, returns the column name of the axis in the response.", alias="columnName")
    member_display_mode: Optional[StrictStr] = Field(default=None, description="Options to override the display mode for the axis. This overrides the query-level `memberDisplayMode` options value in the query.  Only available for non-time axes. Use the QueryAxisMemberDisplayMode `memberDisplayMode` to apply different display modes to different axes.  For example, let's say your query has the `memberDisplayMode` as `DISPLAY` but you want to fetch the object name for a specific dimension.  With QueryAxisMemberDisplayMode `memberDisplayMode`, you can override that dimension's `memberDisplayMode` to `DEFAULT` instead of `DISPLAY`.   Valid values are `UNCHANGED`, `DEFAULT`, `COMPACT`, `DISPLAY`, or `MDX`. Default is `UNCHANGED`.", alias="memberDisplayMode")
    __properties: ClassVar[List[str]] = ["columnName", "memberDisplayMode"]

    @field_validator('member_display_mode')
    def member_display_mode_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['UNCHANGED', 'DEFAULT', 'COMPACT', 'DISPLAY', 'MDX']):
            raise ValueError("must be one of enum values ('UNCHANGED', 'DEFAULT', 'COMPACT', 'DISPLAY', 'MDX')")
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
        """Create an instance of QueryAxisOptionsDTO from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of QueryAxisOptionsDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "columnName": obj.get("columnName"),
            "memberDisplayMode": obj.get("memberDisplayMode")
        })
        return _obj


