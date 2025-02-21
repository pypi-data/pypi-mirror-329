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

from empire_platform_api_public_client_legacy.models.error_response import ErrorResponse  # noqa: E501

class TestErrorResponse(unittest.TestCase):
    """ErrorResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ErrorResponse:
        """Test ErrorResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ErrorResponse`
        """
        model = ErrorResponse()  # noqa: E501
        if include_optional:
            return ErrorResponse(
                code = 'ACTIVE_UNPLANNED_OUTAGE_EXISTS',
                message = '',
                nested_errors = [
                    empire_platform_api_public_client_legacy.models.nested_error.NestedError(
                        field_name = '', 
                        code = '', 
                        message = '', )
                    ],
                params = {
                    'key' : ''
                    },
                request_id = '',
                debug_error = ''
            )
        else:
            return ErrorResponse(
                code = 'ACTIVE_UNPLANNED_OUTAGE_EXISTS',
        )
        """

    def testErrorResponse(self):
        """Test ErrorResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
