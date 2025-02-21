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

from empire_platform_api_public_client_legacy.models.finance_information_lockable_date import FinanceInformationLockableDate  # noqa: E501

class TestFinanceInformationLockableDate(unittest.TestCase):
    """FinanceInformationLockableDate unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FinanceInformationLockableDate:
        """Test FinanceInformationLockableDate
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FinanceInformationLockableDate`
        """
        model = FinanceInformationLockableDate()  # noqa: E501
        if include_optional:
            return FinanceInformationLockableDate(
                var_date = '2022-01-04',
                locked = True
            )
        else:
            return FinanceInformationLockableDate(
                var_date = '2022-01-04',
                locked = True,
        )
        """

    def testFinanceInformationLockableDate(self):
        """Test FinanceInformationLockableDate"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
