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


from typing import Union
from pydantic import BaseModel, Field, StrictInt, confloat, conint

class SourceAuctionResult(BaseModel):
    """
    SourceAuctionResult
    """
    available_allocated_capacity: StrictInt = Field(default=..., alias="availableAllocatedCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    clearing_price: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="clearingPrice", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    __properties = ["availableAllocatedCapacity", "clearingPrice"]

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
    def from_json(cls, json_str: str) -> SourceAuctionResult:
        """Create an instance of SourceAuctionResult from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SourceAuctionResult:
        """Create an instance of SourceAuctionResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SourceAuctionResult.parse_obj(obj)

        _obj = SourceAuctionResult.parse_obj({
            "available_allocated_capacity": obj.get("availableAllocatedCapacity"),
            "clearing_price": obj.get("clearingPrice")
        })
        return _obj


