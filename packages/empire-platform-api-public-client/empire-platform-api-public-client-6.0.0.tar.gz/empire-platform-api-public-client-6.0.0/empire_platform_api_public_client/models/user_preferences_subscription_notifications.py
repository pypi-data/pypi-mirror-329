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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from empire_platform_api_public_client.models.subscription_notification_preference import SubscriptionNotificationPreference
from empire_platform_api_public_client.models.subscription_notification_preference_with_email import SubscriptionNotificationPreferenceWithEmail
from typing import Optional, Set
from typing_extensions import Self

class UserPreferencesSubscriptionNotifications(BaseModel):
    """
    UserPreferencesSubscriptionNotifications
    """ # noqa: E501
    long_term_auction_updates: SubscriptionNotificationPreferenceWithEmail = Field(alias="longTermAuctionUpdates")
    day_ahead_auction_updates: SubscriptionNotificationPreference = Field(alias="dayAheadAuctionUpdates")
    intraday_auction_updates: SubscriptionNotificationPreference = Field(alias="intradayAuctionUpdates")
    buy_now_transmission_rights_offers: SubscriptionNotificationPreferenceWithEmail = Field(alias="buyNowTransmissionRightsOffers")
    unplanned_outage_updates: SubscriptionNotificationPreferenceWithEmail = Field(alias="unplannedOutageUpdates")
    curtailment: SubscriptionNotificationPreferenceWithEmail
    __properties: ClassVar[List[str]] = ["longTermAuctionUpdates", "dayAheadAuctionUpdates", "intradayAuctionUpdates", "buyNowTransmissionRightsOffers", "unplannedOutageUpdates", "curtailment"]

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
        """Create an instance of UserPreferencesSubscriptionNotifications from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of long_term_auction_updates
        if self.long_term_auction_updates:
            _dict['longTermAuctionUpdates'] = self.long_term_auction_updates.to_dict()
        # override the default output from pydantic by calling `to_dict()` of day_ahead_auction_updates
        if self.day_ahead_auction_updates:
            _dict['dayAheadAuctionUpdates'] = self.day_ahead_auction_updates.to_dict()
        # override the default output from pydantic by calling `to_dict()` of intraday_auction_updates
        if self.intraday_auction_updates:
            _dict['intradayAuctionUpdates'] = self.intraday_auction_updates.to_dict()
        # override the default output from pydantic by calling `to_dict()` of buy_now_transmission_rights_offers
        if self.buy_now_transmission_rights_offers:
            _dict['buyNowTransmissionRightsOffers'] = self.buy_now_transmission_rights_offers.to_dict()
        # override the default output from pydantic by calling `to_dict()` of unplanned_outage_updates
        if self.unplanned_outage_updates:
            _dict['unplannedOutageUpdates'] = self.unplanned_outage_updates.to_dict()
        # override the default output from pydantic by calling `to_dict()` of curtailment
        if self.curtailment:
            _dict['curtailment'] = self.curtailment.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserPreferencesSubscriptionNotifications from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "longTermAuctionUpdates": SubscriptionNotificationPreferenceWithEmail.from_dict(obj["longTermAuctionUpdates"]) if obj.get("longTermAuctionUpdates") is not None else None,
            "dayAheadAuctionUpdates": SubscriptionNotificationPreference.from_dict(obj["dayAheadAuctionUpdates"]) if obj.get("dayAheadAuctionUpdates") is not None else None,
            "intradayAuctionUpdates": SubscriptionNotificationPreference.from_dict(obj["intradayAuctionUpdates"]) if obj.get("intradayAuctionUpdates") is not None else None,
            "buyNowTransmissionRightsOffers": SubscriptionNotificationPreferenceWithEmail.from_dict(obj["buyNowTransmissionRightsOffers"]) if obj.get("buyNowTransmissionRightsOffers") is not None else None,
            "unplannedOutageUpdates": SubscriptionNotificationPreferenceWithEmail.from_dict(obj["unplannedOutageUpdates"]) if obj.get("unplannedOutageUpdates") is not None else None,
            "curtailment": SubscriptionNotificationPreferenceWithEmail.from_dict(obj["curtailment"]) if obj.get("curtailment") is not None else None
        })
        return _obj


