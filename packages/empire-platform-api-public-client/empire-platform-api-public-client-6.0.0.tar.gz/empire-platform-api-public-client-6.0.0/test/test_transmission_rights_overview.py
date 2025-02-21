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

from empire_platform_api_public_client.models.transmission_rights_overview import TransmissionRightsOverview

class TestTransmissionRightsOverview(unittest.TestCase):
    """TransmissionRightsOverview unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TransmissionRightsOverview:
        """Test TransmissionRightsOverview
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TransmissionRightsOverview`
        """
        model = TransmissionRightsOverview()
        if include_optional:
            return TransmissionRightsOverview(
                mtus = [
                    empire_platform_api_public_client.models.transmission_rights_overview_mtus.TransmissionRightsOverview_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client.models.transmission_rights_overview_mtus_values.TransmissionRightsOverview_mtus_values(
                                direction = 'GB_NL', 
                                timescales = [
                                    empire_platform_api_public_client.models.transmission_rights_overview_mtus_values_timescales.TransmissionRightsOverview_mtus_values_timescales(
                                        timescale = 'LONG_TERM', 
                                        value = 56, )
                                    ], 
                                total = 56, 
                                curtailed = 56, 
                                remaining = 56, )
                            ], )
                    ]
            )
        else:
            return TransmissionRightsOverview(
                mtus = [
                    empire_platform_api_public_client.models.transmission_rights_overview_mtus.TransmissionRightsOverview_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client.models.transmission_rights_overview_mtus_values.TransmissionRightsOverview_mtus_values(
                                direction = 'GB_NL', 
                                timescales = [
                                    empire_platform_api_public_client.models.transmission_rights_overview_mtus_values_timescales.TransmissionRightsOverview_mtus_values_timescales(
                                        timescale = 'LONG_TERM', 
                                        value = 56, )
                                    ], 
                                total = 56, 
                                curtailed = 56, 
                                remaining = 56, )
                            ], )
                    ],
        )
        """

    def testTransmissionRightsOverview(self):
        """Test TransmissionRightsOverview"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
