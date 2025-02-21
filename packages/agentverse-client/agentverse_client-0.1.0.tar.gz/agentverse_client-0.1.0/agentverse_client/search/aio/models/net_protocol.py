# coding: utf-8

"""
    FastAPI

    An API for our smart search engine that provides the agent that best fits your needs.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class NetProtocol(str, Enum):
    """
    NetProtocol
    """

    """
    allowed enum values
    """
    AGENT = 'agent'
    TEST_MINUS_AGENT = 'test-agent'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of NetProtocol from a JSON string"""
        return cls(json.loads(json_str))


