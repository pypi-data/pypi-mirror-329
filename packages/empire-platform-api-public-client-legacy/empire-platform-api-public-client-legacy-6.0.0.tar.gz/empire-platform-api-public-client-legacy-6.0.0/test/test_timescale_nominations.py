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

from empire_platform_api_public_client_legacy.models.timescale_nominations import TimescaleNominations  # noqa: E501

class TestTimescaleNominations(unittest.TestCase):
    """TimescaleNominations unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TimescaleNominations:
        """Test TimescaleNominations
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TimescaleNominations`
        """
        model = TimescaleNominations()  # noqa: E501
        if include_optional:
            return TimescaleNominations(
                capacity_resolution = 'RES_1_KW',
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.timescale_nominations_mtus.TimescaleNominations_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        mtu_status = 'EDITABLE', 
                        total_trs = 56, 
                        current_nomination = empire_platform_api_public_client_legacy.models.timescale_nominations_mtus_current_nomination.TimescaleNominations_mtus_currentNomination(
                            status = 'PRE', 
                            value = 56, 
                            floored_value = 56, 
                            pre_curtailed_value = 56, ), 
                        not_nominated_trs = 56, )
                    ]
            )
        else:
            return TimescaleNominations(
                capacity_resolution = 'RES_1_KW',
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client_legacy.models.timescale_nominations_mtus.TimescaleNominations_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        mtu_status = 'EDITABLE', 
                        total_trs = 56, 
                        current_nomination = empire_platform_api_public_client_legacy.models.timescale_nominations_mtus_current_nomination.TimescaleNominations_mtus_currentNomination(
                            status = 'PRE', 
                            value = 56, 
                            floored_value = 56, 
                            pre_curtailed_value = 56, ), 
                        not_nominated_trs = 56, )
                    ],
        )
        """

    def testTimescaleNominations(self):
        """Test TimescaleNominations"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
