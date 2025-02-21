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
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DayAheadOrIntraDayAuctionMtu(BaseModel):
    """
    MTU values for DA / ID auctions  * `atc` - ATC (Available Transfer Capacity) for the given MTU in kilowatts * `preliminaryOc` - The OC that was initially reserved at the auction creation - not including any un nominated capacity in the LT nomination window from participants in kilowatts * `unNominatedCapacity` - The un nominated capacity for this auction from the LT nomination window. This can be put up either as UIoSI or UIoLI and returned in kilowatts * `finalOc` - The final OC of the auction taking into account the preliminary OC and the un-nominated capacity in kilowatts 
    """ # noqa: E501
    mtu: datetime = Field(description="The first moment (inclusive) of an MTU period  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute MTU start point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format - only with `XX:00:00`, `XX:15:00`, `XX:30:00` and `XX:45:00` time parts are valid values (depending on MTU size) ")
    atc: Optional[StrictInt] = Field(default=None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers")
    preliminary_oc: Optional[StrictInt] = Field(default=None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="preliminaryOc")
    un_nominated_capacity: Optional[StrictInt] = Field(default=None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="unNominatedCapacity")
    final_oc: Optional[StrictInt] = Field(default=None, description="Capacity value in kilowatts (kW) - the required system precision allows for handling capacity values as integers", alias="finalOc")
    __properties: ClassVar[List[str]] = ["mtu", "atc", "preliminaryOc", "unNominatedCapacity", "finalOc"]

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
        """Create an instance of DayAheadOrIntraDayAuctionMtu from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DayAheadOrIntraDayAuctionMtu from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "mtu": obj.get("mtu"),
            "atc": obj.get("atc"),
            "preliminaryOc": obj.get("preliminaryOc"),
            "unNominatedCapacity": obj.get("unNominatedCapacity"),
            "finalOc": obj.get("finalOc")
        })
        return _obj


