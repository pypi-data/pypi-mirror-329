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

from empire_platform_api_public_client_legacy.models.aggregated_nominations_mns_or_gb import AggregatedNominationsMnsOrGb  # noqa: E501

class TestAggregatedNominationsMnsOrGb(unittest.TestCase):
    """AggregatedNominationsMnsOrGb unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AggregatedNominationsMnsOrGb:
        """Test AggregatedNominationsMnsOrGb
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AggregatedNominationsMnsOrGb`
        """
        model = AggregatedNominationsMnsOrGb()  # noqa: E501
        if include_optional:
            return AggregatedNominationsMnsOrGb(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client_legacy.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                direction = 'GB_NL', 
                                value = 56, )
                            ], 
                        netted_nominations = empire_platform_api_public_client_legacy.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                            direction = 'GB_NL', 
                            flow = 56, ), )
                    ]
            )
        else:
            return AggregatedNominationsMnsOrGb(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.aggregated_nominations_mns_or_gb_mtus.AggregatedNominationsMnsOrGb_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client_legacy.models.aggregated_nominations_mtu_value.AggregatedNominationsMtuValue(
                                direction = 'GB_NL', 
                                value = 56, )
                            ], 
                        netted_nominations = empire_platform_api_public_client_legacy.models.aggregated_nominations_mtu_netted_nominations.AggregatedNominationsMtuNettedNominations(
                            direction = 'GB_NL', 
                            flow = 56, ), )
                    ],
        )
        """

    def testAggregatedNominationsMnsOrGb(self):
        """Test AggregatedNominationsMnsOrGb"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
