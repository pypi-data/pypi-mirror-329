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
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from empire_platform_api_public_client.models.secondary_market_day_ahead_or_intra_day_noticeboard_entry_response_mtus import SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus
from typing import Optional, Set
from typing_extensions import Self

class SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse(BaseModel):
    """
    SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse
    """ # noqa: E501
    mtus: List[SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus]
    contact_name: StrictStr = Field(alias="contactName")
    phone_number: Annotated[str, Field(strict=True)] = Field(alias="phoneNumber")
    email: Annotated[str, Field(strict=True)]
    comment: Optional[StrictStr] = None
    responded_at: datetime = Field(description="Date and time with zone information, marks an **absolute point** on the timeline  - theoretically can be sent and received with any zone offset (until it marks the desired **absolute point** on the timeline) - in practice it is advised to transfer it in UTC timezone (with Z offset, \"Zulu time\") - ISO 8601 compliant string in `yyyy-mm-ddThh:mm:ss.SSSZ` format ", alias="respondedAt")
    __properties: ClassVar[List[str]] = ["mtus", "contactName", "phoneNumber", "email", "comment", "respondedAt"]

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
        """Create an instance of SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse from a JSON string"""
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
        """Create an instance of SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "mtus": [SecondaryMarketDayAheadOrIntraDayNoticeboardEntryResponseMtus.from_dict(_item) for _item in obj["mtus"]] if obj.get("mtus") is not None else None,
            "contactName": obj.get("contactName"),
            "phoneNumber": obj.get("phoneNumber"),
            "email": obj.get("email"),
            "comment": obj.get("comment"),
            "respondedAt": obj.get("respondedAt")
        })
        return _obj


