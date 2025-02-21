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



from pydantic import BaseModel, Field, StrictStr
from empire_platform_api_public_client_legacy.models.organisation_document_uploaded_by_user_organisation import OrganisationDocumentUploadedByUserOrganisation

class OrganisationDocumentUploadedByUser(BaseModel):
    """
    OrganisationDocumentUploadedByUser
    """
    id: StrictStr = Field(default=..., description="Unique identifier for the record in UUID4 format")
    name: StrictStr = Field(...)
    organisation: OrganisationDocumentUploadedByUserOrganisation = Field(...)
    __properties = ["id", "name", "organisation"]

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
    def from_json(cls, json_str: str) -> OrganisationDocumentUploadedByUser:
        """Create an instance of OrganisationDocumentUploadedByUser from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of organisation
        if self.organisation:
            _dict['organisation'] = self.organisation.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrganisationDocumentUploadedByUser:
        """Create an instance of OrganisationDocumentUploadedByUser from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrganisationDocumentUploadedByUser.parse_obj(obj)

        _obj = OrganisationDocumentUploadedByUser.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "organisation": OrganisationDocumentUploadedByUserOrganisation.from_dict(obj.get("organisation")) if obj.get("organisation") is not None else None
        })
        return _obj


