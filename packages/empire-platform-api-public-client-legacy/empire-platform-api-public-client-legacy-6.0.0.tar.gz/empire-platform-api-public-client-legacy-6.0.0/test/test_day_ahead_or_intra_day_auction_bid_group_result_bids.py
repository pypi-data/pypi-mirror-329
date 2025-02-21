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

from empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_bid_group_result_bids import DayAheadOrIntraDayAuctionBidGroupResultBids  # noqa: E501

class TestDayAheadOrIntraDayAuctionBidGroupResultBids(unittest.TestCase):
    """DayAheadOrIntraDayAuctionBidGroupResultBids unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DayAheadOrIntraDayAuctionBidGroupResultBids:
        """Test DayAheadOrIntraDayAuctionBidGroupResultBids
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DayAheadOrIntraDayAuctionBidGroupResultBids`
        """
        model = DayAheadOrIntraDayAuctionBidGroupResultBids()  # noqa: E501
        if include_optional:
            return DayAheadOrIntraDayAuctionBidGroupResultBids(
                mtu = '2022-01-04T10:00:00.000Z',
                bid = empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_bid_group_result_bids_bid.DayAheadOrIntraDayAuctionBidGroupResult_bids_bid(
                    value = empire_platform_api_public_client_legacy.models.bid_value.BidValue(
                        price = 1.337, 
                        capacity = 56, ), 
                    updated_at = '2022-01-04T00:00:00.000Z', 
                    status = 'NOT_CLEARED_YET', )
            )
        else:
            return DayAheadOrIntraDayAuctionBidGroupResultBids(
                mtu = '2022-01-04T10:00:00.000Z',
        )
        """

    def testDayAheadOrIntraDayAuctionBidGroupResultBids(self):
        """Test DayAheadOrIntraDayAuctionBidGroupResultBids"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
