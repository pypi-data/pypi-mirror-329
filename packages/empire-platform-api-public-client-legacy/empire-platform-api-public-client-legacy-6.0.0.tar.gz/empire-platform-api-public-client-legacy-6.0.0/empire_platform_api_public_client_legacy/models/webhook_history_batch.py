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
from pydantic import BaseModel, Field, conint, conlist
from empire_platform_api_public_client_legacy.models.webhook_history_item import WebhookHistoryItem

class WebhookHistoryBatch(BaseModel):
    """
    WebhookHistoryBatch
    """
    entries: conlist(WebhookHistoryItem) = Field(...)
    total_count: conint(strict=True, ge=0) = Field(default=..., alias="totalCount", description="Natural numbers {0, 1, 2, 3, ...} used for counting elements")
    __properties = ["entries", "totalCount"]

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
    def from_json(cls, json_str: str) -> WebhookHistoryBatch:
        """Create an instance of WebhookHistoryBatch from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in entries (list)
        _items = []
        if self.entries:
            for _item in self.entries:
                if _item:
                    _items.append(_item.to_dict())
            _dict['entries'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> WebhookHistoryBatch:
        """Create an instance of WebhookHistoryBatch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return WebhookHistoryBatch.parse_obj(obj)

        _obj = WebhookHistoryBatch.parse_obj({
            "entries": [WebhookHistoryItem.from_dict(_item) for _item in obj.get("entries")] if obj.get("entries") is not None else None,
            "total_count": obj.get("totalCount")
        })
        return _obj


