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

from empire_platform_api_public_client_legacy.models.create_default_nomination_request import CreateDefaultNominationRequest  # noqa: E501

class TestCreateDefaultNominationRequest(unittest.TestCase):
    """CreateDefaultNominationRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateDefaultNominationRequest:
        """Test CreateDefaultNominationRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateDefaultNominationRequest`
        """
        model = CreateDefaultNominationRequest()  # noqa: E501
        if include_optional:
            return CreateDefaultNominationRequest(
                timescale = 'LONG_TERM',
                border_direction = 'GB_NL',
                delivery_period_start = '2022-01-04',
                delivery_period_end = '2022-01-04',
                mtus = [
                    empire_platform_api_public_client_legacy.models.default_nomination_mtu.DefaultNominationMtu(
                        mtu = '10:00', 
                        type = 'PERCENT_100', 
                        value = 56, )
                    ]
            )
        else:
            return CreateDefaultNominationRequest(
                timescale = 'LONG_TERM',
                border_direction = 'GB_NL',
                delivery_period_start = '2022-01-04',
                mtus = [
                    empire_platform_api_public_client_legacy.models.default_nomination_mtu.DefaultNominationMtu(
                        mtu = '10:00', 
                        type = 'PERCENT_100', 
                        value = 56, )
                    ],
        )
        """

    def testCreateDefaultNominationRequest(self):
        """Test CreateDefaultNominationRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
