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
from typing import List
from pydantic import BaseModel, Field, conlist
from empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_netted_nominations import PublicAggregatedNominationsOverviewResponseMtusNettedNominations
from empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_values import PublicAggregatedNominationsOverviewResponseMtusValues

class PublicAggregatedNominationsOverviewResponseMtus(BaseModel):
    """
    PublicAggregatedNominationsOverviewResponseMtus
    """
    mtu: datetime = Field(default=..., description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ")
    values: conlist(PublicAggregatedNominationsOverviewResponseMtusValues) = Field(...)
    netted_nominations: PublicAggregatedNominationsOverviewResponseMtusNettedNominations = Field(default=..., alias="nettedNominations")
    __properties = ["mtu", "values", "nettedNominations"]

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
    def from_json(cls, json_str: str) -> PublicAggregatedNominationsOverviewResponseMtus:
        """Create an instance of PublicAggregatedNominationsOverviewResponseMtus from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of netted_nominations
        if self.netted_nominations:
            _dict['nettedNominations'] = self.netted_nominations.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PublicAggregatedNominationsOverviewResponseMtus:
        """Create an instance of PublicAggregatedNominationsOverviewResponseMtus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PublicAggregatedNominationsOverviewResponseMtus.parse_obj(obj)

        _obj = PublicAggregatedNominationsOverviewResponseMtus.parse_obj({
            "mtu": obj.get("mtu"),
            "values": [PublicAggregatedNominationsOverviewResponseMtusValues.from_dict(_item) for _item in obj.get("values")] if obj.get("values") is not None else None,
            "netted_nominations": PublicAggregatedNominationsOverviewResponseMtusNettedNominations.from_dict(obj.get("nettedNominations")) if obj.get("nettedNominations") is not None else None
        })
        return _obj


