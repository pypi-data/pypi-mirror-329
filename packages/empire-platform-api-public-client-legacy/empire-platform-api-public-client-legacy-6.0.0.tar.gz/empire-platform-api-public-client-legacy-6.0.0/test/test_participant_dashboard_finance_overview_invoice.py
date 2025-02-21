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

from empire_platform_api_public_client_legacy.models.participant_dashboard_finance_overview_invoice import ParticipantDashboardFinanceOverviewInvoice  # noqa: E501

class TestParticipantDashboardFinanceOverviewInvoice(unittest.TestCase):
    """ParticipantDashboardFinanceOverviewInvoice unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ParticipantDashboardFinanceOverviewInvoice:
        """Test ParticipantDashboardFinanceOverviewInvoice
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ParticipantDashboardFinanceOverviewInvoice`
        """
        model = ParticipantDashboardFinanceOverviewInvoice()  # noqa: E501
        if include_optional:
            return ParticipantDashboardFinanceOverviewInvoice(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                display_id = '',
                status = 'DRAFT',
                attachment = empire_platform_api_public_client_legacy.models.attachment.Attachment(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    file_name = '', 
                    file_size = 0, 
                    mime_type = '', 
                    url = '', ),
                due_date = '2022-01-04',
                payment_date = '2022-01-04'
            )
        else:
            return ParticipantDashboardFinanceOverviewInvoice(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                display_id = '',
                status = 'DRAFT',
        )
        """

    def testParticipantDashboardFinanceOverviewInvoice(self):
        """Test ParticipantDashboardFinanceOverviewInvoice"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
