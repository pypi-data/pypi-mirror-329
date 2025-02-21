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

from empire_platform_api_public_client_legacy.api.public_auction_api import PublicAuctionApi  # noqa: E501


class TestPublicAuctionApi(unittest.TestCase):
    """PublicAuctionApi unit test stubs"""

    def setUp(self) -> None:
        self.api = PublicAuctionApi()

    def tearDown(self) -> None:
        self.api.api_client.close()

    def test_get_public_auction_reduction_periods(self) -> None:
        """Test case for get_public_auction_reduction_periods

        """
        pass

    def test_get_public_auctions(self) -> None:
        """Test case for get_public_auctions

        """
        pass

    def test_get_public_day_ahead_auction(self) -> None:
        """Test case for get_public_day_ahead_auction

        """
        pass

    def test_get_public_day_ahead_or_intra_day_auction_mtu_results(self) -> None:
        """Test case for get_public_day_ahead_or_intra_day_auction_mtu_results

        """
        pass

    def test_get_public_day_ahead_or_intra_day_auction_results(self) -> None:
        """Test case for get_public_day_ahead_or_intra_day_auction_results

        """
        pass

    def test_get_public_intra_day_auction(self) -> None:
        """Test case for get_public_intra_day_auction

        """
        pass

    def test_get_public_long_term_auction(self) -> None:
        """Test case for get_public_long_term_auction

        """
        pass

    def test_get_public_long_term_auction_calendar(self) -> None:
        """Test case for get_public_long_term_auction_calendar

        """
        pass

    def test_get_public_long_term_auction_results(self) -> None:
        """Test case for get_public_long_term_auction_results

        """
        pass


if __name__ == '__main__':
    unittest.main()
