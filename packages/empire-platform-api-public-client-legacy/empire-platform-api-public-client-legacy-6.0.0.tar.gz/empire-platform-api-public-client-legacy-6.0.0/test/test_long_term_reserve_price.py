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

from empire_platform_api_public_client_legacy.models.long_term_reserve_price import LongTermReservePrice  # noqa: E501

class TestLongTermReservePrice(unittest.TestCase):
    """LongTermReservePrice unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LongTermReservePrice:
        """Test LongTermReservePrice
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LongTermReservePrice`
        """
        model = LongTermReservePrice()  # noqa: E501
        if include_optional:
            return LongTermReservePrice(
                steps = [
                    empire_platform_api_public_client_legacy.models.long_term_reserve_price_steps.LongTermReservePrice_steps(
                        from = 56, 
                        to = 56, 
                        reserve_price = 1.337, )
                    ],
                publish = 'PRELIMINARY_SPEC_PUBLISHED'
            )
        else:
            return LongTermReservePrice(
                steps = [
                    empire_platform_api_public_client_legacy.models.long_term_reserve_price_steps.LongTermReservePrice_steps(
                        from = 56, 
                        to = 56, 
                        reserve_price = 1.337, )
                    ],
                publish = 'PRELIMINARY_SPEC_PUBLISHED',
        )
        """

    def testLongTermReservePrice(self):
        """Test LongTermReservePrice"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
