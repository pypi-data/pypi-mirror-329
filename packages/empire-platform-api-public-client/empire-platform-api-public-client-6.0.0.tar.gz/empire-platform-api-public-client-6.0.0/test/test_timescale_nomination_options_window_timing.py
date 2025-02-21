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

from empire_platform_api_public_client.models.timescale_nomination_options_window_timing import TimescaleNominationOptionsWindowTiming

class TestTimescaleNominationOptionsWindowTiming(unittest.TestCase):
    """TimescaleNominationOptionsWindowTiming unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TimescaleNominationOptionsWindowTiming:
        """Test TimescaleNominationOptionsWindowTiming
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TimescaleNominationOptionsWindowTiming`
        """
        model = TimescaleNominationOptionsWindowTiming()
        if include_optional:
            return TimescaleNominationOptionsWindowTiming(
                open_at = '2022-01-04T00:00:00.000Z',
                close_at = '2022-01-04T00:00:00.000Z'
            )
        else:
            return TimescaleNominationOptionsWindowTiming(
                open_at = '2022-01-04T00:00:00.000Z',
                close_at = '2022-01-04T00:00:00.000Z',
        )
        """

    def testTimescaleNominationOptionsWindowTiming(self):
        """Test TimescaleNominationOptionsWindowTiming"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
