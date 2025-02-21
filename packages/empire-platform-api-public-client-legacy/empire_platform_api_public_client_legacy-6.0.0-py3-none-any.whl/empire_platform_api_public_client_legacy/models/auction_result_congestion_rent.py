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
from pydantic import BaseModel, Field, confloat, conint

class AuctionResultCongestionRent(BaseModel):
    """
    * `ocRevenue` - Revenue materialised from selling the OC at marginal price * `returnsRevenue` - Revenue materialised from returns * `totalRevenue` - All revenues summed up   # noqa: E501
    """
    oc_revenue: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="ocRevenue", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    returns_revenue: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="returnsRevenue", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    total_revenue: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="totalRevenue", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    __properties = ["ocRevenue", "returnsRevenue", "totalRevenue"]

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
    def from_json(cls, json_str: str) -> AuctionResultCongestionRent:
        """Create an instance of AuctionResultCongestionRent from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AuctionResultCongestionRent:
        """Create an instance of AuctionResultCongestionRent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return AuctionResultCongestionRent.parse_obj(obj)

        _obj = AuctionResultCongestionRent.parse_obj({
            "oc_revenue": obj.get("ocRevenue"),
            "returns_revenue": obj.get("returnsRevenue"),
            "total_revenue": obj.get("totalRevenue")
        })
        return _obj


