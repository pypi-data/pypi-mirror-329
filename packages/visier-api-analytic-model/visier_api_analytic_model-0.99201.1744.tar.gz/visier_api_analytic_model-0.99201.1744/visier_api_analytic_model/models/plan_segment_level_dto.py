# coding: utf-8

"""
    Visier Analytic Model APIs

    Visier APIs for retrieving and configuring your analytic model in Visier.

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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class PlanSegmentLevelDTO(BaseModel):
    """
    A dimension and dimension level that segments the plan.
    """ # noqa: E501
    display_name: Optional[StrictStr] = Field(default=None, description="The display name of the dimension level.", alias="displayName")
    id: Optional[StrictStr] = Field(default=None, description="The symbol name of the dimension appended with its level ID.")
    order: Optional[StrictInt] = Field(default=None, description="The number that describes the segment's position in the plan's overall structure.")
    segment_display_name: Optional[StrictStr] = Field(default=None, description="The display name of the dimension.", alias="segmentDisplayName")
    segment_id: Optional[StrictStr] = Field(default=None, description="The symbol name of the dimension.", alias="segmentId")
    __properties: ClassVar[List[str]] = ["displayName", "id", "order", "segmentDisplayName", "segmentId"]

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
        """Create an instance of PlanSegmentLevelDTO from a JSON string"""
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
        """Create an instance of PlanSegmentLevelDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "displayName": obj.get("displayName"),
            "id": obj.get("id"),
            "order": obj.get("order"),
            "segmentDisplayName": obj.get("segmentDisplayName"),
            "segmentId": obj.get("segmentId")
        })
        return _obj


