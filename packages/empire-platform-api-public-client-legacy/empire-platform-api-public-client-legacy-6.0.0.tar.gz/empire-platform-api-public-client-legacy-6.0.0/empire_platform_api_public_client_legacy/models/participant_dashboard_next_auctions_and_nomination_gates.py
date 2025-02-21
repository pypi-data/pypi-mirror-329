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
from empire_platform_api_public_client_legacy.models.dashboard_next_nomination_gate import DashboardNextNominationGate
from empire_platform_api_public_client_legacy.models.participant_dashboard_next_auction import ParticipantDashboardNextAuction

class ParticipantDashboardNextAuctionsAndNominationGates(BaseModel):
    """
    ParticipantDashboardNextAuctionsAndNominationGates
    """
    nomination_gates: conlist(DashboardNextNominationGate) = Field(default=..., alias="nominationGates")
    day_ahead_auctions: conlist(ParticipantDashboardNextAuction) = Field(default=..., alias="dayAheadAuctions")
    intra_day_auctions: conlist(ParticipantDashboardNextAuction) = Field(default=..., alias="intraDayAuctions")
    __properties = ["nominationGates", "dayAheadAuctions", "intraDayAuctions"]

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
    def from_json(cls, json_str: str) -> ParticipantDashboardNextAuctionsAndNominationGates:
        """Create an instance of ParticipantDashboardNextAuctionsAndNominationGates from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in nomination_gates (list)
        _items = []
        if self.nomination_gates:
            for _item in self.nomination_gates:
                if _item:
                    _items.append(_item.to_dict())
            _dict['nominationGates'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in day_ahead_auctions (list)
        _items = []
        if self.day_ahead_auctions:
            for _item in self.day_ahead_auctions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['dayAheadAuctions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in intra_day_auctions (list)
        _items = []
        if self.intra_day_auctions:
            for _item in self.intra_day_auctions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['intraDayAuctions'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ParticipantDashboardNextAuctionsAndNominationGates:
        """Create an instance of ParticipantDashboardNextAuctionsAndNominationGates from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ParticipantDashboardNextAuctionsAndNominationGates.parse_obj(obj)

        _obj = ParticipantDashboardNextAuctionsAndNominationGates.parse_obj({
            "nomination_gates": [DashboardNextNominationGate.from_dict(_item) for _item in obj.get("nominationGates")] if obj.get("nominationGates") is not None else None,
            "day_ahead_auctions": [ParticipantDashboardNextAuction.from_dict(_item) for _item in obj.get("dayAheadAuctions")] if obj.get("dayAheadAuctions") is not None else None,
            "intra_day_auctions": [ParticipantDashboardNextAuction.from_dict(_item) for _item in obj.get("intraDayAuctions")] if obj.get("intraDayAuctions") is not None else None
        })
        return _obj


