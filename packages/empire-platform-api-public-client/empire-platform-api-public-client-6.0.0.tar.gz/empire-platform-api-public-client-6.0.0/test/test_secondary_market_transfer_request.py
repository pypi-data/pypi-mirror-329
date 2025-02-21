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

from empire_platform_api_public_client.models.secondary_market_transfer_request import SecondaryMarketTransferRequest

class TestSecondaryMarketTransferRequest(unittest.TestCase):
    """SecondaryMarketTransferRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SecondaryMarketTransferRequest:
        """Test SecondaryMarketTransferRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SecondaryMarketTransferRequest`
        """
        model = SecondaryMarketTransferRequest()
        if include_optional:
            return SecondaryMarketTransferRequest(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                timescale = 'LONG_TERM',
                delivery_period = empire_platform_api_public_client.models.date_period.DatePeriod(
                    start = '2022-01-04', 
                    end = '2022-01-04', ),
                direction = 'GB_NL',
                transferred_capacity = 56,
                requested_at = '2022-01-04T00:00:00.000Z',
                updated_at = '2022-01-04T00:00:00.000Z',
                completed_at = '2022-01-04T00:00:00.000Z',
                expires_at = '2022-01-04T00:00:00.000Z',
                sender = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
                receiver = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
                status = 'PENDING'
            )
        else:
            return SecondaryMarketTransferRequest(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                timescale = 'LONG_TERM',
                delivery_period = empire_platform_api_public_client.models.date_period.DatePeriod(
                    start = '2022-01-04', 
                    end = '2022-01-04', ),
                direction = 'GB_NL',
                transferred_capacity = 56,
                requested_at = '2022-01-04T00:00:00.000Z',
                updated_at = '2022-01-04T00:00:00.000Z',
                expires_at = '2022-01-04T00:00:00.000Z',
                sender = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
                receiver = empire_platform_api_public_client.models.invoice_participant_details.InvoiceParticipantDetails(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', ),
                status = 'PENDING',
        )
        """

    def testSecondaryMarketTransferRequest(self):
        """Test SecondaryMarketTransferRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
