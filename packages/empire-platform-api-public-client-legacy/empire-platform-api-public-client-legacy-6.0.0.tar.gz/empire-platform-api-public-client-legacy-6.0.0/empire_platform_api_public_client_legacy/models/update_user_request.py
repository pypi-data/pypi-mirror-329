# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr, constr, validator
from empire_platform_api_public_client_legacy.models.user_role import UserRole

class UpdateUserRequest(BaseModel):
    """
    UpdateUserRequest
    """
    name: StrictStr = Field(...)
    phone_number: constr(strict=True) = Field(default=..., alias="phoneNumber")
    role: UserRole = Field(...)
    job_title: Optional[StrictStr] = Field(default=None, alias="jobTitle")
    __properties = ["name", "phoneNumber", "role", "jobTitle"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UpdateUserRequest:
        """Create an instance of UpdateUserRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateUserRequest:
        """Create an instance of UpdateUserRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateUserRequest.parse_obj(obj)

        _obj = UpdateUserRequest.parse_obj({
            "name": obj.get("name"),
            "phone_number": obj.get("phoneNumber"),
            "role": obj.get("role"),
            "job_title": obj.get("jobTitle")
        })
        return _obj


