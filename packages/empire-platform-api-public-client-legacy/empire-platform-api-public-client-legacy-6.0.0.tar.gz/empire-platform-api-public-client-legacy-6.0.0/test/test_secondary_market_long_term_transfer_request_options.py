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

from empire_platform_api_public_client_legacy.models.secondary_market_long_term_transfer_request_options import SecondaryMarketLongTermTransferRequestOptions  # noqa: E501

class TestSecondaryMarketLongTermTransferRequestOptions(unittest.TestCase):
    """SecondaryMarketLongTermTransferRequestOptions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SecondaryMarketLongTermTransferRequestOptions:
        """Test SecondaryMarketLongTermTransferRequestOptions
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SecondaryMarketLongTermTransferRequestOptions`
        """
        model = SecondaryMarketLongTermTransferRequestOptions()  # noqa: E501
        if include_optional:
            return SecondaryMarketLongTermTransferRequestOptions(
                available_capacity = 56
            )
        else:
            return SecondaryMarketLongTermTransferRequestOptions(
                available_capacity = 56,
        )
        """

    def testSecondaryMarketLongTermTransferRequestOptions(self):
        """Test SecondaryMarketLongTermTransferRequestOptions"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
