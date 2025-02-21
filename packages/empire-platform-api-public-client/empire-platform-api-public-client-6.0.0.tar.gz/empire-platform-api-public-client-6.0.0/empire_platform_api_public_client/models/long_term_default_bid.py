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
from empire_platform_api_public_client.models.auction_product_type import AuctionProductType
from empire_platform_api_public_client.models.bid_value import BidValue
from empire_platform_api_public_client.models.border_direction import BorderDirection
from empire_platform_api_public_client.models.mtu_size import MtuSize
from typing import Optional, Set
from typing_extensions import Self

class LongTermDefaultBid(BaseModel):
    """
    LongTermDefaultBid
    """ # noqa: E501
    id: StrictStr = Field(description="Unique identifier for the record in UUID4 format")
    auction_product_type: AuctionProductType = Field(alias="auctionProductType")
    border_direction: BorderDirection = Field(alias="borderDirection")
    delivery_period_start: datetime = Field(description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ", alias="deliveryPeriodStart")
    delivery_period_end: Optional[datetime] = Field(default=None, description="The last moment (exclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ", alias="deliveryPeriodEnd")
    validity_period_start: datetime = Field(description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ", alias="validityPeriodStart")
    validity_period_end: Optional[datetime] = Field(default=None, description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ", alias="validityPeriodEnd")
    mtu_size: MtuSize = Field(alias="mtuSize")
    bids: List[BidValue]
    __properties: ClassVar[List[str]] = ["id", "auctionProductType", "borderDirection", "deliveryPeriodStart", "deliveryPeriodEnd", "validityPeriodStart", "validityPeriodEnd", "mtuSize", "bids"]

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
        """Create an instance of LongTermDefaultBid from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in bids (list)
        _items = []
        if self.bids:
            for _item_bids in self.bids:
                if _item_bids:
                    _items.append(_item_bids.to_dict())
            _dict['bids'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of LongTermDefaultBid from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "auctionProductType": obj.get("auctionProductType"),
            "borderDirection": obj.get("borderDirection"),
            "deliveryPeriodStart": obj.get("deliveryPeriodStart"),
            "deliveryPeriodEnd": obj.get("deliveryPeriodEnd"),
            "validityPeriodStart": obj.get("validityPeriodStart"),
            "validityPeriodEnd": obj.get("validityPeriodEnd"),
            "mtuSize": obj.get("mtuSize"),
            "bids": [BidValue.from_dict(_item) for _item in obj["bids"]] if obj.get("bids") is not None else None
        })
        return _obj


