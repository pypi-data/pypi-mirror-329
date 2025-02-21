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

from empire_platform_api_public_client_legacy.models.secondary_market_day_ahead_or_intra_day_noticeboard_entry_details import SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails  # noqa: E501

class TestSecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails(unittest.TestCase):
    """SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails:
        """Test SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails`
        """
        model = SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails()  # noqa: E501
        if include_optional:
            return SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails(
                type = 'BUY',
                timescale = 'LONG_TERM',
                mtu_size = 'MTU_15_MINS',
                delivery_day = '2022-01-04',
                direction = 'GB_NL',
                expires_at = '2022-01-04T00:00:00.000Z',
                mtus = [
                    empire_platform_api_public_client_legacy.models.secondary_market_capacity_price_mtu.SecondaryMarketCapacityPriceMtu(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        capacity = 56, 
                        price = 1.337, )
                    ],
                is_own = True
            )
        else:
            return SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails(
                type = 'BUY',
                timescale = 'LONG_TERM',
                mtu_size = 'MTU_15_MINS',
                delivery_day = '2022-01-04',
                direction = 'GB_NL',
                expires_at = '2022-01-04T00:00:00.000Z',
                mtus = [
                    empire_platform_api_public_client_legacy.models.secondary_market_capacity_price_mtu.SecondaryMarketCapacityPriceMtu(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        capacity = 56, 
                        price = 1.337, )
                    ],
                is_own = True,
        )
        """

    def testSecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails(self):
        """Test SecondaryMarketDayAheadOrIntraDayNoticeboardEntryDetails"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
