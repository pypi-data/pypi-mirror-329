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

from empire_platform_api_public_client_legacy.api.transmission_right_api import TransmissionRightApi  # noqa: E501


class TestTransmissionRightApi(unittest.TestCase):
    """TransmissionRightApi unit test stubs"""

    def setUp(self) -> None:
        self.api = TransmissionRightApi()

    def tearDown(self) -> None:
        self.api.api_client.close()

    def test_get_transmission_rights_overview(self) -> None:
        """Test case for get_transmission_rights_overview

        """
        pass


if __name__ == '__main__':
    unittest.main()
