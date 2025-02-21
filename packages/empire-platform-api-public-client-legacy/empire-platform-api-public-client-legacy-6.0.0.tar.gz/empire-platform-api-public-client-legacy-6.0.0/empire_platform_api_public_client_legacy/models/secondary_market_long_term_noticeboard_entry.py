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


from typing import List
from pydantic import BaseModel, Field, conlist
from empire_platform_api_public_client_legacy.models.secondary_market_long_term_noticeboard_entry_details import SecondaryMarketLongTermNoticeboardEntryDetails
from empire_platform_api_public_client_legacy.models.secondary_market_long_term_noticeboard_entry_response import SecondaryMarketLongTermNoticeboardEntryResponse

class SecondaryMarketLongTermNoticeboardEntry(BaseModel):
    """
    SecondaryMarketLongTermNoticeboardEntry
    """
    notice_details: SecondaryMarketLongTermNoticeboardEntryDetails = Field(default=..., alias="noticeDetails")
    responses: conlist(SecondaryMarketLongTermNoticeboardEntryResponse) = Field(...)
    __properties = ["noticeDetails", "responses"]

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
    def from_json(cls, json_str: str) -> SecondaryMarketLongTermNoticeboardEntry:
        """Create an instance of SecondaryMarketLongTermNoticeboardEntry from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of notice_details
        if self.notice_details:
            _dict['noticeDetails'] = self.notice_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in responses (list)
        _items = []
        if self.responses:
            for _item in self.responses:
                if _item:
                    _items.append(_item.to_dict())
            _dict['responses'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SecondaryMarketLongTermNoticeboardEntry:
        """Create an instance of SecondaryMarketLongTermNoticeboardEntry from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SecondaryMarketLongTermNoticeboardEntry.parse_obj(obj)

        _obj = SecondaryMarketLongTermNoticeboardEntry.parse_obj({
            "notice_details": SecondaryMarketLongTermNoticeboardEntryDetails.from_dict(obj.get("noticeDetails")) if obj.get("noticeDetails") is not None else None,
            "responses": [SecondaryMarketLongTermNoticeboardEntryResponse.from_dict(_item) for _item in obj.get("responses")] if obj.get("responses") is not None else None
        })
        return _obj


