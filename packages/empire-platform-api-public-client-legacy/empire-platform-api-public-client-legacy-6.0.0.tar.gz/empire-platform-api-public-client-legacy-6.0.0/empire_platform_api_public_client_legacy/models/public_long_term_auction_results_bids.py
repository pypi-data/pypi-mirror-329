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
from pydantic import BaseModel, Field, StrictInt
from empire_platform_api_public_client_legacy.models.bid_value import BidValue
from empire_platform_api_public_client_legacy.models.public_auction_bid_status import PublicAuctionBidStatus

class PublicLongTermAuctionResultsBids(BaseModel):
    """
    PublicLongTermAuctionResultsBids
    """
    value: BidValue = Field(...)
    allocated_capacity: Optional[StrictInt] = Field(default=None, alias="allocatedCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    status: PublicAuctionBidStatus = Field(...)
    __properties = ["value", "allocatedCapacity", "status"]

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
    def from_json(cls, json_str: str) -> PublicLongTermAuctionResultsBids:
        """Create an instance of PublicLongTermAuctionResultsBids from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PublicLongTermAuctionResultsBids:
        """Create an instance of PublicLongTermAuctionResultsBids from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PublicLongTermAuctionResultsBids.parse_obj(obj)

        _obj = PublicLongTermAuctionResultsBids.parse_obj({
            "value": BidValue.from_dict(obj.get("value")) if obj.get("value") is not None else None,
            "allocated_capacity": obj.get("allocatedCapacity"),
            "status": obj.get("status")
        })
        return _obj


