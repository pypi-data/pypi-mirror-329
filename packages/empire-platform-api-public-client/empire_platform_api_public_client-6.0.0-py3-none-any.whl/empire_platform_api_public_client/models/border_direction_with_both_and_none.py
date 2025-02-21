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


class BorderDirectionWithBothAndNone(str, Enum):
    """
    Same as BorderDirection, but with both and none option added
    """

    """
    allowed enum values
    """
    GB_NL = 'GB_NL'
    NL_GB = 'NL_GB'
    BOTH = 'BOTH'
    NONE = 'NONE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of BorderDirectionWithBothAndNone from a JSON string"""
        return cls(json.loads(json_str))


