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

from empire_platform_api_public_client_legacy.api.webhook_api import WebhookApi  # noqa: E501


class TestWebhookApi(unittest.TestCase):
    """WebhookApi unit test stubs"""

    def setUp(self) -> None:
        self.api = WebhookApi()

    def tearDown(self) -> None:
        self.api.api_client.close()

    def test_create_webhook(self) -> None:
        """Test case for create_webhook

        """
        pass

    def test_delete_webhook(self) -> None:
        """Test case for delete_webhook

        """
        pass

    def test_get_webhook(self) -> None:
        """Test case for get_webhook

        """
        pass

    def test_get_webhook_history(self) -> None:
        """Test case for get_webhook_history

        """
        pass

    def test_get_webhooks(self) -> None:
        """Test case for get_webhooks

        """
        pass

    def test_test_webhook(self) -> None:
        """Test case for test_webhook

        """
        pass

    def test_update_webhook(self) -> None:
        """Test case for update_webhook

        """
        pass


if __name__ == '__main__':
    unittest.main()
