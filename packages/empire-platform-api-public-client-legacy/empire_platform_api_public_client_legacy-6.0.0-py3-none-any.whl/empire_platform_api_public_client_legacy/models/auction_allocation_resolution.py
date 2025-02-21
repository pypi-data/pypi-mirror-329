# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class AuctionAllocationResolution(str, Enum):
    """
    AuctionAllocationResolution
    """

    """
    allowed enum values
    """
    RES_1_KW = 'RES_1_KW'
    RES_100_KW = 'RES_100_KW'
    RES_500_KW = 'RES_500_KW'
    RES_1_MW = 'RES_1_MW'

    @classmethod
    def from_json(cls, json_str: str) -> AuctionAllocationResolution:
        """Create an instance of AuctionAllocationResolution from a JSON string"""
        return AuctionAllocationResolution(json.loads(json_str))


