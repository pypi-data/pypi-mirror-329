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

from datetime import date, datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictStr, confloat, conint, conlist
from empire_platform_api_public_client_legacy.models.attachment import Attachment
from empire_platform_api_public_client_legacy.models.invoice import Invoice
from empire_platform_api_public_client_legacy.models.invoice_participant_details import InvoiceParticipantDetails
from empire_platform_api_public_client_legacy.models.invoice_status import InvoiceStatus

class InvoiceGroup(BaseModel):
    """
    InvoiceGroup
    """
    id: StrictStr = Field(default=..., description="Unique identifier for the record in UUID4 format")
    display_id: StrictStr = Field(default=..., alias="displayId")
    attachment: Optional[Attachment] = None
    invoices: conlist(Invoice) = Field(...)
    net_amount: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="netAmount", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    gross_amount: Union[confloat(multiple_of=0.01, strict=True), conint(strict=True)] = Field(default=..., alias="grossAmount", description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places")
    status: InvoiceStatus = Field(...)
    due_date: Optional[date] = Field(default=None, alias="dueDate", description="One single calendar day, interpreted in **System Time**  - ISO 8601 compliant string in `yyyy-mm-dd` format ")
    last_status_change: datetime = Field(default=..., alias="lastStatusChange", description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ")
    participant: InvoiceParticipantDetails = Field(...)
    __properties = ["id", "displayId", "attachment", "invoices", "netAmount", "grossAmount", "status", "dueDate", "lastStatusChange", "participant"]

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
    def from_json(cls, json_str: str) -> InvoiceGroup:
        """Create an instance of InvoiceGroup from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of attachment
        if self.attachment:
            _dict['attachment'] = self.attachment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in invoices (list)
        _items = []
        if self.invoices:
            for _item in self.invoices:
                if _item:
                    _items.append(_item.to_dict())
            _dict['invoices'] = _items
        # override the default output from pydantic by calling `to_dict()` of participant
        if self.participant:
            _dict['participant'] = self.participant.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> InvoiceGroup:
        """Create an instance of InvoiceGroup from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return InvoiceGroup.parse_obj(obj)

        _obj = InvoiceGroup.parse_obj({
            "id": obj.get("id"),
            "display_id": obj.get("displayId"),
            "attachment": Attachment.from_dict(obj.get("attachment")) if obj.get("attachment") is not None else None,
            "invoices": [Invoice.from_dict(_item) for _item in obj.get("invoices")] if obj.get("invoices") is not None else None,
            "net_amount": obj.get("netAmount"),
            "gross_amount": obj.get("grossAmount"),
            "status": obj.get("status"),
            "due_date": obj.get("dueDate"),
            "last_status_change": obj.get("lastStatusChange"),
            "participant": InvoiceParticipantDetails.from_dict(obj.get("participant")) if obj.get("participant") is not None else None
        })
        return _obj


