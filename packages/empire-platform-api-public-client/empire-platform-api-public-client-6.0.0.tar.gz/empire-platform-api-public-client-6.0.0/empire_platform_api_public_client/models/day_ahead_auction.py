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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from empire_platform_api_public_client.models.auction_allocation_resolution import AuctionAllocationResolution
from empire_platform_api_public_client.models.auction_bidding_configuration import AuctionBiddingConfiguration
from empire_platform_api_public_client.models.auction_process_steps_absolute import AuctionProcessStepsAbsolute
from empire_platform_api_public_client.models.auction_product_type import AuctionProductType
from empire_platform_api_public_client.models.auction_status import AuctionStatus
from empire_platform_api_public_client.models.border_direction import BorderDirection
from empire_platform_api_public_client.models.day_ahead_or_intra_day_auction_mtu import DayAheadOrIntraDayAuctionMtu
from empire_platform_api_public_client.models.mtu_period import MtuPeriod
from empire_platform_api_public_client.models.mtu_size import MtuSize
from empire_platform_api_public_client.models.offered_capacity_setup import OfferedCapacitySetup
from typing import Optional, Set
from typing_extensions import Self

class DayAheadAuction(BaseModel):
    """
    DayAheadAuction
    """ # noqa: E501
    id: StrictStr = Field(description="Unique identifier for the record in UUID4 format")
    name: StrictStr = Field(description="Human readable name")
    display_id: StrictStr = Field(description="Generated display identifier", alias="displayId")
    product_type: AuctionProductType = Field(alias="productType")
    border_direction: BorderDirection = Field(alias="borderDirection")
    status: AuctionStatus
    processing: StrictBool
    delivery_period: MtuPeriod = Field(alias="deliveryPeriod")
    allocation_mtu_size: MtuSize = Field(alias="allocationMtuSize")
    allocation_resolution: AuctionAllocationResolution = Field(alias="allocationResolution")
    bidding_configuration: AuctionBiddingConfiguration = Field(alias="biddingConfiguration")
    process_steps: AuctionProcessStepsAbsolute = Field(alias="processSteps")
    offered_capacity_setup: OfferedCapacitySetup = Field(alias="offeredCapacitySetup")
    offered_capacity_manually_updated: StrictBool = Field(alias="offeredCapacityManuallyUpdated")
    mtus: Optional[List[DayAheadOrIntraDayAuctionMtu]] = None
    previous_auction_id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the record in UUID4 format", alias="previousAuctionId")
    next_auction_id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the record in UUID4 format", alias="nextAuctionId")
    __properties: ClassVar[List[str]] = ["id", "name", "displayId", "productType", "borderDirection", "status", "processing", "deliveryPeriod", "allocationMtuSize", "allocationResolution", "biddingConfiguration", "processSteps", "offeredCapacitySetup", "offeredCapacityManuallyUpdated", "mtus", "previousAuctionId", "nextAuctionId"]

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
        """Create an instance of DayAheadAuction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of delivery_period
        if self.delivery_period:
            _dict['deliveryPeriod'] = self.delivery_period.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bidding_configuration
        if self.bidding_configuration:
            _dict['biddingConfiguration'] = self.bidding_configuration.to_dict()
        # override the default output from pydantic by calling `to_dict()` of process_steps
        if self.process_steps:
            _dict['processSteps'] = self.process_steps.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in mtus (list)
        _items = []
        if self.mtus:
            for _item_mtus in self.mtus:
                if _item_mtus:
                    _items.append(_item_mtus.to_dict())
            _dict['mtus'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DayAheadAuction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "displayId": obj.get("displayId"),
            "productType": obj.get("productType"),
            "borderDirection": obj.get("borderDirection"),
            "status": obj.get("status"),
            "processing": obj.get("processing"),
            "deliveryPeriod": MtuPeriod.from_dict(obj["deliveryPeriod"]) if obj.get("deliveryPeriod") is not None else None,
            "allocationMtuSize": obj.get("allocationMtuSize"),
            "allocationResolution": obj.get("allocationResolution"),
            "biddingConfiguration": AuctionBiddingConfiguration.from_dict(obj["biddingConfiguration"]) if obj.get("biddingConfiguration") is not None else None,
            "processSteps": AuctionProcessStepsAbsolute.from_dict(obj["processSteps"]) if obj.get("processSteps") is not None else None,
            "offeredCapacitySetup": obj.get("offeredCapacitySetup"),
            "offeredCapacityManuallyUpdated": obj.get("offeredCapacityManuallyUpdated"),
            "mtus": [DayAheadOrIntraDayAuctionMtu.from_dict(_item) for _item in obj["mtus"]] if obj.get("mtus") is not None else None,
            "previousAuctionId": obj.get("previousAuctionId"),
            "nextAuctionId": obj.get("nextAuctionId")
        })
        return _obj


