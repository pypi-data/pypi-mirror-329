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

from empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results import DayAheadOrIntraDayAuctionParticipantResults  # noqa: E501

class TestDayAheadOrIntraDayAuctionParticipantResults(unittest.TestCase):
    """DayAheadOrIntraDayAuctionParticipantResults unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DayAheadOrIntraDayAuctionParticipantResults:
        """Test DayAheadOrIntraDayAuctionParticipantResults
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DayAheadOrIntraDayAuctionParticipantResults`
        """
        model = DayAheadOrIntraDayAuctionParticipantResults()  # noqa: E501
        if include_optional:
            return DayAheadOrIntraDayAuctionParticipantResults(
                mtus = [
                    empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results_mtus.DayAheadOrIntraDayAuctionParticipantResults_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        value = empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results_mtus_value.DayAheadOrIntraDayAuctionParticipantResults_mtus_value(
                            requested_capacity = 56, 
                            allocated_trs = 56, ), )
                    ]
            )
        else:
            return DayAheadOrIntraDayAuctionParticipantResults(
                mtus = [
                    empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results_mtus.DayAheadOrIntraDayAuctionParticipantResults_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        value = empire_platform_api_public_client_legacy.models.day_ahead_or_intra_day_auction_participant_results_mtus_value.DayAheadOrIntraDayAuctionParticipantResults_mtus_value(
                            requested_capacity = 56, 
                            allocated_trs = 56, ), )
                    ],
        )
        """

    def testDayAheadOrIntraDayAuctionParticipantResults(self):
        """Test DayAheadOrIntraDayAuctionParticipantResults"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
