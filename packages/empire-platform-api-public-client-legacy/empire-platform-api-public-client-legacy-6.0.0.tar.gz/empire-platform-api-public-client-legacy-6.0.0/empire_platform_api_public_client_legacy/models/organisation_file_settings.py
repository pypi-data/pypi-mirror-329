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



from pydantic import BaseModel, Field, StrictBool

class OrganisationFileSettings(BaseModel):
    """
    OrganisationFileSettings
    """
    include_in_fpn: StrictBool = Field(default=..., alias="includeInFpn")
    include_in_dmv: StrictBool = Field(default=..., alias="includeInDmv")
    __properties = ["includeInFpn", "includeInDmv"]

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
    def from_json(cls, json_str: str) -> OrganisationFileSettings:
        """Create an instance of OrganisationFileSettings from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrganisationFileSettings:
        """Create an instance of OrganisationFileSettings from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrganisationFileSettings.parse_obj(obj)

        _obj = OrganisationFileSettings.parse_obj({
            "include_in_fpn": obj.get("includeInFpn"),
            "include_in_dmv": obj.get("includeInDmv")
        })
        return _obj


