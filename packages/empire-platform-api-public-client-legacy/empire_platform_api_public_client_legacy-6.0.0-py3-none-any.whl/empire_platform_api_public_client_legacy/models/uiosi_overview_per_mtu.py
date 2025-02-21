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

from datetime import datetime

from pydantic import BaseModel, Field, StrictInt
from empire_platform_api_public_client_legacy.models.uiosi_not_resold import UiosiNotResold
from empire_platform_api_public_client_legacy.models.uiosi_resold import UiosiResold

class UiosiOverviewPerMtu(BaseModel):
    """
    UiosiOverviewPerMtu
    """
    mtu: datetime = Field(default=..., description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ")
    allocated_capacity: StrictInt = Field(default=..., alias="allocatedCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    unnominated_capacity: StrictInt = Field(default=..., alias="unnominatedCapacity", description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    resold: UiosiResold = Field(...)
    not_resold: UiosiNotResold = Field(default=..., alias="notResold")
    __properties = ["mtu", "allocatedCapacity", "unnominatedCapacity", "resold", "notResold"]

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
    def from_json(cls, json_str: str) -> UiosiOverviewPerMtu:
        """Create an instance of UiosiOverviewPerMtu from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of resold
        if self.resold:
            _dict['resold'] = self.resold.to_dict()
        # override the default output from pydantic by calling `to_dict()` of not_resold
        if self.not_resold:
            _dict['notResold'] = self.not_resold.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UiosiOverviewPerMtu:
        """Create an instance of UiosiOverviewPerMtu from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UiosiOverviewPerMtu.parse_obj(obj)

        _obj = UiosiOverviewPerMtu.parse_obj({
            "mtu": obj.get("mtu"),
            "allocated_capacity": obj.get("allocatedCapacity"),
            "unnominated_capacity": obj.get("unnominatedCapacity"),
            "resold": UiosiResold.from_dict(obj.get("resold")) if obj.get("resold") is not None else None,
            "not_resold": UiosiNotResold.from_dict(obj.get("notResold")) if obj.get("notResold") is not None else None
        })
        return _obj


