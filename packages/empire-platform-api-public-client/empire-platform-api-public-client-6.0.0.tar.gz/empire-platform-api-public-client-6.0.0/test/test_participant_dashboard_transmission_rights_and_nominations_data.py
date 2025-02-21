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

from empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data import ParticipantDashboardTransmissionRightsAndNominationsData

class TestParticipantDashboardTransmissionRightsAndNominationsData(unittest.TestCase):
    """ParticipantDashboardTransmissionRightsAndNominationsData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ParticipantDashboardTransmissionRightsAndNominationsData:
        """Test ParticipantDashboardTransmissionRightsAndNominationsData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ParticipantDashboardTransmissionRightsAndNominationsData`
        """
        model = ParticipantDashboardTransmissionRightsAndNominationsData()
        if include_optional:
            return ParticipantDashboardTransmissionRightsAndNominationsData(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus.ParticipantDashboardTransmissionRightsAndNominationsData_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus_values.ParticipantDashboardTransmissionRightsAndNominationsData_mtus_values(
                                direction = 'GB_NL', 
                                allocated_trs = 56, 
                                nominated_capacity = 56, 
                                nomination_restriction = empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus_values_nomination_restriction.ParticipantDashboardTransmissionRightsAndNominationsData_mtus_values_nominationRestriction(
                                    type = 'FLOORED', 
                                    value = 56, ), )
                            ], )
                    ]
            )
        else:
            return ParticipantDashboardTransmissionRightsAndNominationsData(
                mtu_size = 'MTU_15_MINS',
                mtus = [
                    empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus.ParticipantDashboardTransmissionRightsAndNominationsData_mtus(
                        mtu = '2022-01-04T10:00:00.000Z', 
                        values = [
                            empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus_values.ParticipantDashboardTransmissionRightsAndNominationsData_mtus_values(
                                direction = 'GB_NL', 
                                allocated_trs = 56, 
                                nominated_capacity = 56, 
                                nomination_restriction = empire_platform_api_public_client.models.participant_dashboard_transmission_rights_and_nominations_data_mtus_values_nomination_restriction.ParticipantDashboardTransmissionRightsAndNominationsData_mtus_values_nominationRestriction(
                                    type = 'FLOORED', 
                                    value = 56, ), )
                            ], )
                    ],
        )
        """

    def testParticipantDashboardTransmissionRightsAndNominationsData(self):
        """Test ParticipantDashboardTransmissionRightsAndNominationsData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
