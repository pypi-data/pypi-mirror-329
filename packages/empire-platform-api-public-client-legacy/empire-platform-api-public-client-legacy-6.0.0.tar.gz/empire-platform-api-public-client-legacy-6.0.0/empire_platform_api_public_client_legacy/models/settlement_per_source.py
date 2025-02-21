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


from typing import List, Union
from pydantic import BaseModel, Field, confloat, conint, conlist
from empire_platform_api_public_client_legacy.models.settlement_item import SettlementItem
from empire_platform_api_public_client_legacy.models.settlement_source_type import SettlementSourceType
from empire_platform_api_public_client_legacy.models.settlement_sub_source_type import SettlementSubSourceType

class SettlementPerSource(BaseModel):
    """
    SettlementPerSource
    """
    source: SettlementSourceType = Field(...)
    sub_source: SettlementSubSourceType = Field(default=..., alias="subSource")
    total_amount: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="totalAmount", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    values: conlist(SettlementItem) = Field(...)
    __properties = ["source", "subSource", "totalAmount", "values"]

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
    def from_json(cls, json_str: str) -> SettlementPerSource:
        """Create an instance of SettlementPerSource from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in values (list)
        _items = []
        if self.values:
            for _item in self.values:
                if _item:
                    _items.append(_item.to_dict())
            _dict['values'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SettlementPerSource:
        """Create an instance of SettlementPerSource from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SettlementPerSource.parse_obj(obj)

        _obj = SettlementPerSource.parse_obj({
            "source": obj.get("source"),
            "sub_source": obj.get("subSource"),
            "total_amount": obj.get("totalAmount"),
            "values": [SettlementItem.from_dict(_item) for _item in obj.get("values")] if obj.get("values") is not None else None
        })
        return _obj


