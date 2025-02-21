# coding: utf-8

"""
    Visier Data In APIs

    Visier APIs for sending data to Visier and running data load jobs.

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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DirectDataSchemaFieldDTO(BaseModel):
    """
    The definition of each field in an object's schema.
    """ # noqa: E501
    data_type: Optional[StrictStr] = Field(default=None, description="The column's data type.", alias="dataType")
    empty_values_allowed: Optional[StrictBool] = Field(default=None, description="If true, the value may be empty.", alias="emptyValuesAllowed")
    formats: Optional[List[StrictStr]] = Field(default=None, description="The column's accepted formats, such as date formats like \"yyyy-MM-dd\".")
    is_mandatory: Optional[StrictBool] = Field(default=None, description="If true, the field must contain a value to successfully load data into the object.", alias="isMandatory")
    name: Optional[StrictStr] = Field(default=None, description="The field's column name. Column names are case sensitive.")
    __properties: ClassVar[List[str]] = ["dataType", "emptyValuesAllowed", "formats", "isMandatory", "name"]

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
        """Create an instance of DirectDataSchemaFieldDTO from a JSON string"""
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
        """Create an instance of DirectDataSchemaFieldDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "dataType": obj.get("dataType"),
            "emptyValuesAllowed": obj.get("emptyValuesAllowed"),
            "formats": obj.get("formats"),
            "isMandatory": obj.get("isMandatory"),
            "name": obj.get("name")
        })
        return _obj


