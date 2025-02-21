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
import json
from enum import Enum
from typing_extensions import Self


class AuctionStatus(str, Enum):
    """
    Complete list of Auction statuses 
    """

    """
    allowed enum values
    """
    CREATED = 'CREATED'
    INITIALISED = 'INITIALISED'
    PRELIMINARY_SPEC_PUBLISHED = 'PRELIMINARY_SPEC_PUBLISHED'
    FINAL_SPEC_PUBLISHED = 'FINAL_SPEC_PUBLISHED'
    BIDDING_OPEN = 'BIDDING_OPEN'
    BIDDING_CLOSED = 'BIDDING_CLOSED'
    PROVISIONAL_RESULTS_PUBLISHED = 'PROVISIONAL_RESULTS_PUBLISHED'
    FINAL_RESULTS_PUBLISHED = 'FINAL_RESULTS_PUBLISHED'
    CANCELLED = 'CANCELLED'
    DELETED = 'DELETED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AuctionStatus from a JSON string"""
        return cls(json.loads(json_str))


