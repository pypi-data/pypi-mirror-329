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

from empire_platform_api_public_client.models.aggregated_allocated_auction import AggregatedAllocatedAuction

class TestAggregatedAllocatedAuction(unittest.TestCase):
    """AggregatedAllocatedAuction unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AggregatedAllocatedAuction:
        """Test AggregatedAllocatedAuction
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AggregatedAllocatedAuction`
        """
        model = AggregatedAllocatedAuction()
        if include_optional:
            return AggregatedAllocatedAuction(
                timescale = 'LONG_TERM',
                auction_count = 0,
                product_type_count = 0,
                border_direction = 'GB_NL',
                delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                    from_mtu_start = '2022-01-04T10:00:00.000Z', 
                    to_mtu_end = '2022-01-04T11:00:00.000Z', ),
                participant_requested_count = 0,
                participant_allocated_count = 0,
                offered_capacity = 56,
                total_requested_capacity = 56,
                total_allocated_capacity = 56,
                average_clearing_price = 1.337
            )
        else:
            return AggregatedAllocatedAuction(
                timescale = 'LONG_TERM',
                auction_count = 0,
                product_type_count = 0,
                border_direction = 'GB_NL',
                delivery_period = empire_platform_api_public_client.models.mtu_period.MtuPeriod(
                    from_mtu_start = '2022-01-04T10:00:00.000Z', 
                    to_mtu_end = '2022-01-04T11:00:00.000Z', ),
                participant_requested_count = 0,
                participant_allocated_count = 0,
                offered_capacity = 56,
                total_requested_capacity = 56,
                total_allocated_capacity = 56,
                average_clearing_price = 1.337,
        )
        """

    def testAggregatedAllocatedAuction(self):
        """Test AggregatedAllocatedAuction"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
