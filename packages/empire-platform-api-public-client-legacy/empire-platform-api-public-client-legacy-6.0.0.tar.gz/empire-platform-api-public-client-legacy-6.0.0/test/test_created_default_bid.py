# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest
import datetime

from empire_platform_api_public_client_legacy.models.created_default_bid import CreatedDefaultBid  # noqa: E501

class TestCreatedDefaultBid(unittest.TestCase):
    """CreatedDefaultBid unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreatedDefaultBid:
        """Test CreatedDefaultBid
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreatedDefaultBid`
        """
        model = CreatedDefaultBid()  # noqa: E501
        if include_optional:
            return CreatedDefaultBid(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09'
            )
        else:
            return CreatedDefaultBid(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
        )
        """

    def testCreatedDefaultBid(self):
        """Test CreatedDefaultBid"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
