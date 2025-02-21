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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from visier_api_data_in.models.job_status_with_start_time import JobStatusWithStartTime
from typing import Optional, Set
from typing_extensions import Self

class JobStatusListResponse(BaseModel):
    """
    JobStatusListResponse
    """ # noqa: E501
    job_status: Optional[List[JobStatusWithStartTime]] = Field(default=None, description="The specific status to restrict the list of jobs to.", alias="jobStatus")
    query_end_time: Optional[StrictStr] = Field(default=None, description="The end time from which to retrieve job statuses.", alias="queryEndTime")
    query_start_time: Optional[StrictStr] = Field(default=None, description="The start time from which to retrieve job statuses.", alias="queryStartTime")
    __properties: ClassVar[List[str]] = ["jobStatus", "queryEndTime", "queryStartTime"]

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
        """Create an instance of JobStatusListResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in job_status (list)
        _items = []
        if self.job_status:
            for _item_job_status in self.job_status:
                if _item_job_status:
                    _items.append(_item_job_status.to_dict())
            _dict['jobStatus'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of JobStatusListResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "jobStatus": [JobStatusWithStartTime.from_dict(_item) for _item in obj["jobStatus"]] if obj.get("jobStatus") is not None else None,
            "queryEndTime": obj.get("queryEndTime"),
            "queryStartTime": obj.get("queryStartTime")
        })
        return _obj


