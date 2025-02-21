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

from empire_platform_api_public_client.models.submit_day_ahead_or_intra_day_bids_request_bid_groups_bids import SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids

class TestSubmitDayAheadOrIntraDayBidsRequestBidGroupsBids(unittest.TestCase):
    """SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids:
        """Test SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids`
        """
        model = SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids()
        if include_optional:
            return SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids(
                mtu = '2022-01-04T10:00:00.000Z',
                value = empire_platform_api_public_client.models.bid_value.BidValue(
                    price = 1.337, 
                    capacity = 56, )
            )
        else:
            return SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids(
                mtu = '2022-01-04T10:00:00.000Z',
        )
        """

    def testSubmitDayAheadOrIntraDayBidsRequestBidGroupsBids(self):
        """Test SubmitDayAheadOrIntraDayBidsRequestBidGroupsBids"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
