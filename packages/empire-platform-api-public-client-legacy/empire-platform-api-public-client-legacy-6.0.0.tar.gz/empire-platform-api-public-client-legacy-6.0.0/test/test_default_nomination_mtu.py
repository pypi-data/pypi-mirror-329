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

from empire_platform_api_public_client_legacy.models.default_nomination_mtu import DefaultNominationMtu  # noqa: E501

class TestDefaultNominationMtu(unittest.TestCase):
    """DefaultNominationMtu unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DefaultNominationMtu:
        """Test DefaultNominationMtu
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DefaultNominationMtu`
        """
        model = DefaultNominationMtu()  # noqa: E501
        if include_optional:
            return DefaultNominationMtu(
                mtu = '10:00',
                type = 'PERCENT_100',
                value = 56
            )
        else:
            return DefaultNominationMtu(
                mtu = '10:00',
                type = 'PERCENT_100',
        )
        """

    def testDefaultNominationMtu(self):
        """Test DefaultNominationMtu"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
