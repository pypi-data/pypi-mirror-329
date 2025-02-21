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

from empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response import PublicAggregatedNominationsOverviewResponse  # noqa: E501

class TestPublicAggregatedNominationsOverviewResponse(unittest.TestCase):
    """PublicAggregatedNominationsOverviewResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PublicAggregatedNominationsOverviewResponse:
        """Test PublicAggregatedNominationsOverviewResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PublicAggregatedNominationsOverviewResponse`
        """
        model = PublicAggregatedNominationsOverviewResponse()  # noqa: E501
        if include_optional:
            return PublicAggregatedNominationsOverviewResponse(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus.PublicAggregatedNominationsOverviewResponse_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_values.PublicAggregatedNominationsOverviewResponse_mtus_values(
                                direction = 'GB_NL', 
                                ntc = 56, 
                                aggregated_nominations = 56, )
                            ], 
                        netted_nominations = empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_netted_nominations.PublicAggregatedNominationsOverviewResponse_mtus_nettedNominations(
                            direction = 'GB_NL', 
                            flow = 56, ), )
                    ]
            )
        else:
            return PublicAggregatedNominationsOverviewResponse(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus.PublicAggregatedNominationsOverviewResponse_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_values.PublicAggregatedNominationsOverviewResponse_mtus_values(
                                direction = 'GB_NL', 
                                ntc = 56, 
                                aggregated_nominations = 56, )
                            ], 
                        netted_nominations = empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_netted_nominations.PublicAggregatedNominationsOverviewResponse_mtus_nettedNominations(
                            direction = 'GB_NL', 
                            flow = 56, ), )
                    ],
        )
        """

    def testPublicAggregatedNominationsOverviewResponse(self):
        """Test PublicAggregatedNominationsOverviewResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
