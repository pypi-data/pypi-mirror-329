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

from empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results_mtus_value import DayAheadOrIntraDayAuctionParticipantResultsMtusValue  # noqa: E501

class TestDayAheadOrIntraDayAuctionParticipantResultsMtusValue(unittest.TestCase):
    """DayAheadOrIntraDayAuctionParticipantResultsMtusValue unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DayAheadOrIntraDayAuctionParticipantResultsMtusValue:
        """Test DayAheadOrIntraDayAuctionParticipantResultsMtusValue
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DayAheadOrIntraDayAuctionParticipantResultsMtusValue`
        """
        model = DayAheadOrIntraDayAuctionParticipantResultsMtusValue()  # noqa: E501
        if include_optional:
            return DayAheadOrIntraDayAuctionParticipantResultsMtusValue(
                requested_capacity = 56,
                allocated_trs = 56
            )
        else:
            return DayAheadOrIntraDayAuctionParticipantResultsMtusValue(
                requested_capacity = 56,
                allocated_trs = 56,
        )
        """

    def testDayAheadOrIntraDayAuctionParticipantResultsMtusValue(self):
        """Test DayAheadOrIntraDayAuctionParticipantResultsMtusValue"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
