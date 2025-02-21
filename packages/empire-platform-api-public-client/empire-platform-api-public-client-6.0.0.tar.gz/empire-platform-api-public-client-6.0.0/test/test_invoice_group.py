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

from empire_platform_api_public_client.models.invoice_group import InvoiceGroup

class TestInvoiceGroup(unittest.TestCase):
    """InvoiceGroup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> InvoiceGroup:
        """Test InvoiceGroup
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `InvoiceGroup`
        """
        model = InvoiceGroup()
        if include_optional:
            return InvoiceGroup(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                display_id = '',
                attachment = empire_platform_api_public_client.models.attachment.Attachment(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    file_name = '', 
                    file_size = 0, 
                    mime_type = '', 
                    url = '', ),
                invoices = [
                    empire_platform_api_public_client.models.invoice.Invoice(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        display_id = '', 
                        participant = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                            id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                            name = '', ), 
                        net_amount = 1.337, 
                        gross_amount = 1.337, 
                        due_date = '2022-01-04', 
                        status = 'DRAFT', 
                        last_status_change = '2022-01-04T00:00:00.000Z', 
                        attachment = empire_platform_api_public_client.models.attachment.Attachment(
                            id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                            file_name = '', 
                            file_size = 0, 
                            mime_type = '', 
                            url = '', ), 
                        type = 'SB', )
                    ],
                net_amount = 1.337,
                gross_amount = 1.337,
                status = 'DRAFT',
                due_date = '2022-01-04',
                last_status_change = '2022-01-04T00:00:00.000Z',
                participant = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', )
            )
        else:
            return InvoiceGroup(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                display_id = '',
                invoices = [
                    empire_platform_api_public_client.models.invoice.Invoice(
                        id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                        display_id = '', 
                        participant = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                            id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                            name = '', ), 
                        net_amount = 1.337, 
                        gross_amount = 1.337, 
                        due_date = '2022-01-04', 
                        status = 'DRAFT', 
                        last_status_change = '2022-01-04T00:00:00.000Z', 
                        attachment = empire_platform_api_public_client.models.attachment.Attachment(
                            id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                            file_name = '', 
                            file_size = 0, 
                            mime_type = '', 
                            url = '', ), 
                        type = 'SB', )
                    ],
                net_amount = 1.337,
                gross_amount = 1.337,
                status = 'DRAFT',
                last_status_change = '2022-01-04T00:00:00.000Z',
                participant = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
        )
        """

    def testInvoiceGroup(self):
        """Test InvoiceGroup"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
