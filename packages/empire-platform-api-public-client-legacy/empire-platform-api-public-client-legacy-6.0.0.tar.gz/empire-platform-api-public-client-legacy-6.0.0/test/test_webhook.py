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

from empire_platform_api_public_client_legacy.models.webhook import Webhook  # noqa: E501

class TestWebhook(unittest.TestCase):
    """Webhook unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Webhook:
        """Test Webhook
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Webhook`
        """
        model = Webhook()  # noqa: E501
        if include_optional:
            return Webhook(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                url = 'https://WzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyvKX7HzK.ul80FcVjSkp5IHYCm6w-v0dZfUofvKERjsmInY9s-EmM.6kw8gsnXv2Z7jRPK542XGp8ZohR8pb-ziKqEde8fXg9wdp.xa2-zRi2iAxU4NCUavTrirUe4ba7Jn.rgEdBCJE-ArE6U3CZ-Vnrj9Rm.DJnzkccYEcEziPbHZkRTSxklvbNrZ:249',
                event_types = [
                    'LONG_TERM_AUCTION_SPECIFICATION_UPDATED'
                    ]
            )
        else:
            return Webhook(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                url = 'https://WzyBAw2ZuufUOHOEhA8IcFQXnuaZcdyyvKX7HzK.ul80FcVjSkp5IHYCm6w-v0dZfUofvKERjsmInY9s-EmM.6kw8gsnXv2Z7jRPK542XGp8ZohR8pb-ziKqEde8fXg9wdp.xa2-zRi2iAxU4NCUavTrirUe4ba7Jn.rgEdBCJE-ArE6U3CZ-Vnrj9Rm.DJnzkccYEcEziPbHZkRTSxklvbNrZ:249',
                event_types = [
                    'LONG_TERM_AUCTION_SPECIFICATION_UPDATED'
                    ],
        )
        """

    def testWebhook(self):
        """Test Webhook"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
