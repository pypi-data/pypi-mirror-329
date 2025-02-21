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

from empire_platform_api_public_client.models.uiosi_overview import UiosiOverview

class TestUiosiOverview(unittest.TestCase):
    """UiosiOverview unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> UiosiOverview:
        """Test UiosiOverview
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `UiosiOverview`
        """
        model = UiosiOverview()
        if include_optional:
            return UiosiOverview(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client.models.uiosi_overview_per_mtu.UiosiOverviewPerMtu(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        allocated_capacity = 56, 
                        unnominated_capacity = 56, 
                        resold = empire_platform_api_public_client.models.uiosi_resold.UiosiResold(
                            transmission_right = 56, 
                            compensation_price = 1.337, 
                            revenue = 1.337, ), 
                        not_resold = empire_platform_api_public_client.models.uiosi_not_resold.UiosiNotResold(
                            transmission_right = 56, 
                            reason = '', ), )
                    ]
            )
        else:
            return UiosiOverview(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client.models.uiosi_overview_per_mtu.UiosiOverviewPerMtu(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        allocated_capacity = 56, 
                        unnominated_capacity = 56, 
                        resold = empire_platform_api_public_client.models.uiosi_resold.UiosiResold(
                            transmission_right = 56, 
                            compensation_price = 1.337, 
                            revenue = 1.337, ), 
                        not_resold = empire_platform_api_public_client.models.uiosi_not_resold.UiosiNotResold(
                            transmission_right = 56, 
                            reason = '', ), )
                    ],
        )
        """

    def testUiosiOverview(self):
        """Test UiosiOverview"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
