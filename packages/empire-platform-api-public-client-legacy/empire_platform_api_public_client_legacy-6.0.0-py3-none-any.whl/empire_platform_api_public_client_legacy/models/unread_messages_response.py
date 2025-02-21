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



from pydantic import BaseModel, Field, conint

class UnreadMessagesResponse(BaseModel):
    """
    UnreadMessagesResponse
    """
    count: conint(strict=True, ge=0) = Field(default=..., description="Natural numbers {0, 1, 2, 3, ...} used for counting elements")
    __properties = ["count"]

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
    def from_json(cls, json_str: str) -> UnreadMessagesResponse:
        """Create an instance of UnreadMessagesResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UnreadMessagesResponse:
        """Create an instance of UnreadMessagesResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UnreadMessagesResponse.parse_obj(obj)

        _obj = UnreadMessagesResponse.parse_obj({
            "count": obj.get("count")
        })
        return _obj


