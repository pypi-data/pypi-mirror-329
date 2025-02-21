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

from empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_mtu_results import DayAheadOrIntraDayAuctionMtuResults

class TestDayAheadOrIntraDayAuctionMtuResults(unittest.TestCase):
    """DayAheadOrIntraDayAuctionMtuResults unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DayAheadOrIntraDayAuctionMtuResults:
        """Test DayAheadOrIntraDayAuctionMtuResults
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DayAheadOrIntraDayAuctionMtuResults`
        """
        model = DayAheadOrIntraDayAuctionMtuResults()
        if include_optional:
            return DayAheadOrIntraDayAuctionMtuResults(
                bids = [
                    empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_mtu_results_bids.DayAheadOrIntraDayAuctionMtuResults_bids(
                        value = empire_platform_api_public_client.models.bid_value.BidValue(
                            price = 1.337, 
                            capacity = 56, ), 
                        allocated_capacity = 56, 
                        status = 'NOT_CLEARED_YET', )
                    ]
            )
        else:
            return DayAheadOrIntraDayAuctionMtuResults(
                bids = [
                    empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_mtu_results_bids.DayAheadOrIntraDayAuctionMtuResults_bids(
                        value = empire_platform_api_public_client.models.bid_value.BidValue(
                            price = 1.337, 
                            capacity = 56, ), 
                        allocated_capacity = 56, 
                        status = 'NOT_CLEARED_YET', )
                    ],
        )
        """

    def testDayAheadOrIntraDayAuctionMtuResults(self):
        """Test DayAheadOrIntraDayAuctionMtuResults"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
