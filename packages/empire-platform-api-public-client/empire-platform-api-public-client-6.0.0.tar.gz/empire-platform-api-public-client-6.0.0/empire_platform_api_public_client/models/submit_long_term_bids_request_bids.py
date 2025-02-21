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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from empire_platform_api_public_client.models.bid_value import BidValue
from typing import Optional, Set
from typing_extensions import Self

class SubmitLongTermBidsRequestBids(BaseModel):
    """
    SubmitLongTermBidsRequestBids
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique (at least locally) identifier for the record in UUID4 format  * records received nullable identifiers through GET requests should have the property filled out * records sent to PUT endpoints:   - if property is filled out => backend is expected to update the record   - if property is null or missing => backend is expected to create a new record   - if list of records does not contain the record identifier => backend is expected to delete the record ")
    bid_tag: Optional[StrictStr] = Field(default=None, description="Optional external identifier for the bid, for example to differentiate between traders ", alias="bidTag")
    value: BidValue
    __properties: ClassVar[List[str]] = ["id", "bidTag", "value"]

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
        """Create an instance of SubmitLongTermBidsRequestBids from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SubmitLongTermBidsRequestBids from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "bidTag": obj.get("bidTag"),
            "value": BidValue.from_dict(obj["value"]) if obj.get("value") is not None else None
        })
        return _obj


