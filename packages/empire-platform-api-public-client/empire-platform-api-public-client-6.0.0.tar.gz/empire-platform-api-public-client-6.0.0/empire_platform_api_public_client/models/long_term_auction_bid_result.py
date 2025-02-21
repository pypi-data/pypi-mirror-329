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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from empire_platform_api_public_client.models.auction_bid_participant import AuctionBidParticipant
from empire_platform_api_public_client.models.auction_bid_status import AuctionBidStatus
from empire_platform_api_public_client.models.bid_value import BidValue
from typing import Optional, Set
from typing_extensions import Self

class LongTermAuctionBidResult(BaseModel):
    """
    LongTermAuctionBidResult
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the record in UUID4 format")
    participant: Optional[AuctionBidParticipant] = None
    value: BidValue
    updated_at: Optional[datetime] = Field(default=None, description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ", alias="updatedAt")
    status: AuctionBidStatus
    __properties: ClassVar[List[str]] = ["id", "participant", "value", "updatedAt", "status"]

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
        """Create an instance of LongTermAuctionBidResult from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of participant
        if self.participant:
            _dict['participant'] = self.participant.to_dict()
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of LongTermAuctionBidResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "participant": AuctionBidParticipant.from_dict(obj["participant"]) if obj.get("participant") is not None else None,
            "value": BidValue.from_dict(obj["value"]) if obj.get("value") is not None else None,
            "updatedAt": obj.get("updatedAt"),
            "status": obj.get("status")
        })
        return _obj


