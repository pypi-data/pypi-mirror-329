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

from empire_platform_api_public_client.models.long_term_auction_results_allocated_capacity import LongTermAuctionResultsAllocatedCapacity

class TestLongTermAuctionResultsAllocatedCapacity(unittest.TestCase):
    """LongTermAuctionResultsAllocatedCapacity unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LongTermAuctionResultsAllocatedCapacity:
        """Test LongTermAuctionResultsAllocatedCapacity
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LongTermAuctionResultsAllocatedCapacity`
        """
        model = LongTermAuctionResultsAllocatedCapacity()
        if include_optional:
            return LongTermAuctionResultsAllocatedCapacity(
                participant = empire_platform_api_public_client.models.auction_result_participant.AuctionResultParticipant(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', 
                    eic_code = '---7S--058SL--92', ),
                requested_capacity = 56,
                allocated_trs = 56
            )
        else:
            return LongTermAuctionResultsAllocatedCapacity(
                participant = empire_platform_api_public_client.models.auction_result_participant.AuctionResultParticipant(
                    id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09', 
                    name = '', 
                    eic_code = '---7S--058SL--92', ),
                allocated_trs = 56,
        )
        """

    def testLongTermAuctionResultsAllocatedCapacity(self):
        """Test LongTermAuctionResultsAllocatedCapacity"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
