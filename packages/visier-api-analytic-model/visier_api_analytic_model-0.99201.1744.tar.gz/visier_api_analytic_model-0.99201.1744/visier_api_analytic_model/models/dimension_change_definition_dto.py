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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DimensionChangeDefinitionDTO(BaseModel):
    """
    DimensionChangeDefinitionDTO
    """ # noqa: E501
    description: Optional[StrictStr] = Field(default=None, description="A short description of the dimension. Descriptions provide in-context help for your users while working in Visier.")
    display_name: Optional[StrictStr] = Field(default=None, description="The user-friendly name for the dimension.", alias="displayName")
    id: Optional[StrictStr] = Field(default=None, description="The symbol name of the dimension; for example, `Career_Level` or `Employee.Vaccination_Status`")
    short_display_name: Optional[StrictStr] = Field(default=None, description="A shortened version of the display name. If the dimension is visible in the solution experience, this name is displayed in visualization titles.", alias="shortDisplayName")
    __properties: ClassVar[List[str]] = ["description", "displayName", "id", "shortDisplayName"]

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
        """Create an instance of DimensionChangeDefinitionDTO from a JSON string"""
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
        """Create an instance of DimensionChangeDefinitionDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "description": obj.get("description"),
            "displayName": obj.get("displayName"),
            "id": obj.get("id"),
            "shortDisplayName": obj.get("shortDisplayName")
        })
        return _obj


