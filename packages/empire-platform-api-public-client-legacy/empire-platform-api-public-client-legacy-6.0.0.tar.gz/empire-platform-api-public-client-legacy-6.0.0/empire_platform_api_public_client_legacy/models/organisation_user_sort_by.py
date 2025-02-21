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





class OrganisationUserSortBy(str, Enum):
    """
    OrganisationUserSortBy
    """

    """
    allowed enum values
    """
    NAME_ASC = 'NAME_ASC'
    NAME_DESC = 'NAME_DESC'
    ROLE_ASC = 'ROLE_ASC'
    ROLE_DESC = 'ROLE_DESC'
    LAST_LOGIN_ASC = 'LAST_LOGIN_ASC'
    LAST_LOGIN_DESC = 'LAST_LOGIN_DESC'
    STATUS_ASC = 'STATUS_ASC'
    STATUS_DESC = 'STATUS_DESC'

    @classmethod
    def from_json(cls, json_str: str) -> OrganisationUserSortBy:
        """Create an instance of OrganisationUserSortBy from a JSON string"""
        return OrganisationUserSortBy(json.loads(json_str))


