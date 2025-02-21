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

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Union
from typing_extensions import Annotated
from empire_platform_api_public_client.models.auction_timescale import AuctionTimescale
from empire_platform_api_public_client.models.border_direction import BorderDirection
from empire_platform_api_public_client.models.mtu_period import MtuPeriod
from typing import Optional, Set
from typing_extensions import Self

class AggregatedAllocatedAuction(BaseModel):
    """
    AggregatedAllocatedAuction
    """ # noqa: E501
    timescale: AuctionTimescale
    auction_count: Annotated[int, Field(strict=True, ge=0)] = Field(description="Natural numbers {0, 1, 2, 3, ...} used for counting elements", alias="auctionCount")
    product_type_count: Annotated[int, Field(strict=True, ge=0)] = Field(description="Natural numbers {0, 1, 2, 3, ...} used for counting elements", alias="productTypeCount")
    border_direction: BorderDirection = Field(alias="borderDirection")
    delivery_period: MtuPeriod = Field(alias="deliveryPeriod")
    participant_requested_count: Annotated[int, Field(strict=True, ge=0)] = Field(description="Natural numbers {0, 1, 2, 3, ...} used for counting elements", alias="participantRequestedCount")
    participant_allocated_count: Annotated[int, Field(strict=True, ge=0)] = Field(description="Natural numbers {0, 1, 2, 3, ...} used for counting elements", alias="participantAllocatedCount")
    offered_capacity: StrictInt = Field(description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="offeredCapacity")
    total_requested_capacity: StrictInt = Field(description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="totalRequestedCapacity")
    total_allocated_capacity: StrictInt = Field(description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="totalAllocatedCapacity")
    average_clearing_price: Union[Annotated[float, Field(multiple_of=0.01, strict=True)], Annotated[int, Field(strict=True)]] = Field(description="Currency value in Euros (€), accepted with a precision of maximum 2 decimal places", alias="averageClearingPrice")
    __properties: ClassVar[List[str]] = ["timescale", "auctionCount", "productTypeCount", "borderDirection", "deliveryPeriod", "participantRequestedCount", "participantAllocatedCount", "offeredCapacity", "totalRequestedCapacity", "totalAllocatedCapacity", "averageClearingPrice"]

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
        """Create an instance of AggregatedAllocatedAuction from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AggregatedAllocatedAuction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "timescale": obj.get("timescale"),
            "auctionCount": obj.get("auctionCount"),
            "productTypeCount": obj.get("productTypeCount"),
            "borderDirection": obj.get("borderDirection"),
            "deliveryPeriod": MtuPeriod.from_dict(obj["deliveryPeriod"]) if obj.get("deliveryPeriod") is not None else None,
            "participantRequestedCount": obj.get("participantRequestedCount"),
            "participantAllocatedCount": obj.get("participantAllocatedCount"),
            "offeredCapacity": obj.get("offeredCapacity"),
            "totalRequestedCapacity": obj.get("totalRequestedCapacity"),
            "totalAllocatedCapacity": obj.get("totalAllocatedCapacity"),
            "averageClearingPrice": obj.get("averageClearingPrice")
        })
        return _obj


