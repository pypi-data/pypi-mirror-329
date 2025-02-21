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

from empire_platform_api_public_client.models.long_term_auction_bid import LongTermAuctionBid

class TestLongTermAuctionBid(unittest.TestCase):
    """LongTermAuctionBid unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LongTermAuctionBid:
        """Test LongTermAuctionBid
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LongTermAuctionBid`
        """
        model = LongTermAuctionBid()
        if include_optional:
            return LongTermAuctionBid(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                bid_tag = '',
                value = empire_platform_api_public_client.models.bid_value.BidValue(
                    price = 1.337, 
                    capacity = 56, ),
                updated_at = '2022-01-04T00:00:00.000Z',
                status = 'NOT_CLEARED_YET',
                results = empire_platform_api_public_client.models.long_term_auction_bid_results.LongTermAuctionBid_results(
                    allocated_capacity = 56, 
                    marginal_price = 1.337, )
            )
        else:
            return LongTermAuctionBid(
                id = '8d3787bb-b9ce-4d75-9a75-074ddd5d1e09',
                value = empire_platform_api_public_client.models.bid_value.BidValue(
                    price = 1.337, 
                    capacity = 56, ),
                updated_at = '2022-01-04T00:00:00.000Z',
                status = 'NOT_CLEARED_YET',
        )
        """

    def testLongTermAuctionBid(self):
        """Test LongTermAuctionBid"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
