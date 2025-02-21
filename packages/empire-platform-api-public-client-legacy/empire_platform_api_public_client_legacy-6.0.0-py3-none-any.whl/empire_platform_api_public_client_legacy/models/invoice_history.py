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
from typing import Optional
from pydantic import BaseModel, Field
from empire_platform_api_public_client_legacy.models.invoice_action_type import InvoiceActionType
from empire_platform_api_public_client_legacy.models.invoice_participant_details import InvoiceParticipantDetails

class InvoiceHistory(BaseModel):
    """
    Participant basic information  # noqa: E501
    """
    user: Optional[InvoiceParticipantDetails] = None
    action: InvoiceActionType = Field(...)
    actioned_at: datetime = Field(default=..., alias="actionedAt", description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ")
    __properties = ["user", "action", "actionedAt"]

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
    def from_json(cls, json_str: str) -> InvoiceHistory:
        """Create an instance of InvoiceHistory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of user
        if self.user:
            _dict['user'] = self.user.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InvoiceHistory:
        """Create an instance of InvoiceHistory from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InvoiceHistory.parse_obj(obj)

        _obj = InvoiceHistory.parse_obj({
            "user": InvoiceParticipantDetails.from_dict(obj.get("user")) if obj.get("user") is not None else None,
            "action": obj.get("action"),
            "actioned_at": obj.get("actionedAt")
        })
        return _obj


