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

from empire_platform_api_public_client_legacy.models.public_aggregated_nominations_overview_response_mtus_values import PublicAggregatedNominationsOverviewResponseMtusValues  # noqa: E501

class TestPublicAggregatedNominationsOverviewResponseMtusValues(unittest.TestCase):
    """PublicAggregatedNominationsOverviewResponseMtusValues unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PublicAggregatedNominationsOverviewResponseMtusValues:
        """Test PublicAggregatedNominationsOverviewResponseMtusValues
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PublicAggregatedNominationsOverviewResponseMtusValues`
        """
        model = PublicAggregatedNominationsOverviewResponseMtusValues()  # noqa: E501
        if include_optional:
            return PublicAggregatedNominationsOverviewResponseMtusValues(
                direction = 'GB_NL',
                ntc = 56,
                aggregated_nominations = 56
            )
        else:
            return PublicAggregatedNominationsOverviewResponseMtusValues(
                direction = 'GB_NL',
                ntc = 56,
                aggregated_nominations = 56,
        )
        """

    def testPublicAggregatedNominationsOverviewResponseMtusValues(self):
        """Test PublicAggregatedNominationsOverviewResponseMtusValues"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
