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
from pydantic import BaseModel, Field, StrictInt, constr, validator
from empire_platform_api_public_client_legacy.models.default_nomination_declaration_type import DefaultNominationDeclarationType

class DefaultNominationMtu(BaseModel):
    """
    DefaultNominationMtu
    """
    mtu: constr(strict=True) = Field(default=..., description="The first moment (inclusive) of an MTU period in local time, minute resolution, interpreted in **System Time**  - string, interpreted in `hh:mm` format - only `XX:00`, `XX:15`, `XX:30` and `XX:45` are valid values (depending on MTU size) ")
    type: DefaultNominationDeclarationType = Field(...)
    value: Optional[StrictInt] = Field(default=None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    __properties = ["mtu", "type", "value"]

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
    def from_json(cls, json_str: str) -> DefaultNominationMtu:
        """Create an instance of DefaultNominationMtu from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DefaultNominationMtu:
        """Create an instance of DefaultNominationMtu from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DefaultNominationMtu.parse_obj(obj)

        _obj = DefaultNominationMtu.parse_obj({
            "mtu": obj.get("mtu"),
            "type": obj.get("type"),
            "value": obj.get("value")
        })
        return _obj


