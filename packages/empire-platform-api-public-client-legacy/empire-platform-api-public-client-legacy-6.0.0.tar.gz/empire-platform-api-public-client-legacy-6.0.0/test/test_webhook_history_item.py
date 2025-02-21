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

from empire_platform_api_public_client_legacy.models.webhook_history_item import WebhookHistoryItem  # noqa: E501

class TestWebhookHistoryItem(unittest.TestCase):
    """WebhookHistoryItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WebhookHistoryItem:
        """Test WebhookHistoryItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WebhookHistoryItem`
        """
        model = WebhookHistoryItem()  # noqa: E501
        if include_optional:
            return WebhookHistoryItem(
                status = 'IN_PROGRESS',
                event_type = 'LONG_TERM_AUCTION_SPECIFICATION_UPDATED',
                sent_at = '2022-01-04T00:00:00.000Z',
                request_headers = '',
                request_body = '',
                error_message = '',
                response_code = '',
                response_headers = '',
                response_body = ''
            )
        else:
            return WebhookHistoryItem(
                status = 'IN_PROGRESS',
                event_type = 'LONG_TERM_AUCTION_SPECIFICATION_UPDATED',
                request_headers = '',
                request_body = '',
        )
        """

    def testWebhookHistoryItem(self):
        """Test WebhookHistoryItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
