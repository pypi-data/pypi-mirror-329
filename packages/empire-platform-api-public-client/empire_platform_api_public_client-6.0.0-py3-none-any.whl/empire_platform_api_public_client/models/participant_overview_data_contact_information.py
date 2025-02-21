# coding: utf-8

"""
    Platform API

    _OpenAPI specification for the **Platform API** of **Empire**, the allocation and nomination platform of BritNed_  ---  Additional documentation available in the API's [GitHub repository](https://github.com/britned/empire-platform-api) 

    The version of the OpenAPI document: 6.0.0
    Contact: britned.info@britned.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Any, ClassVar, Dict, List
from typing_extensions import Annotated
from empire_platform_api_public_client.models.organisation_contact import OrganisationContact
from typing import Optional, Set
from typing_extensions import Self

class ParticipantOverviewDataContactInformation(BaseModel):
    """
    ParticipantOverviewDataContactInformation
    """ # noqa: E501
    primary_contact: OrganisationContact = Field(alias="primaryContact")
    operational_emergency_contact: OrganisationContact = Field(alias="operationalEmergencyContact")
    helpdesk_pin: Annotated[str, Field(strict=True)] = Field(alias="helpdeskPin")
    __properties: ClassVar[List[str]] = ["primaryContact", "operationalEmergencyContact", "helpdeskPin"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ParticipantOverviewDataContactInformation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of primary_contact
        if self.primary_contact:
            _dict['primaryContact'] = self.primary_contact.to_dict()
        # override the default output from pydantic by calling `to_dict()` of operational_emergency_contact
        if self.operational_emergency_contact:
            _dict['operationalEmergencyContact'] = self.operational_emergency_contact.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ParticipantOverviewDataContactInformation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "primaryContact": OrganisationContact.from_dict(obj["primaryContact"]) if obj.get("primaryContact") is not None else None,
            "operationalEmergencyContact": OrganisationContact.from_dict(obj["operationalEmergencyContact"]) if obj.get("operationalEmergencyContact") is not None else None,
            "helpdeskPin": obj.get("helpdeskPin")
        })
        return _obj


