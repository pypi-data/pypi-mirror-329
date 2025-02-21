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





class TimescaleNominationWindowStatus(str, Enum):
    """
    TimescaleNominationWindowStatus
    """

    """
    allowed enum values
    """
    NOT_YET_OPEN = 'NOT_YET_OPEN'
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'

    @classmethod
    def from_json(cls, json_str: str) -> TimescaleNominationWindowStatus:
        """Create an instance of TimescaleNominationWindowStatus from a JSON string"""
        return TimescaleNominationWindowStatus(json.loads(json_str))


