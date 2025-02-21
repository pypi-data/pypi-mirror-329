# coding: utf-8

"""
    FastAPI

    An API for our smart search engine that provides the agent that best fits your needs.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from agentverse_client.search.models.search_term_percentage import SearchTermPercentage
from typing import Optional, Set
from typing_extensions import Self

class AgentSearchTermAnalyticsResponse(BaseModel):
    """
    The agent search term analytics response object
    """ # noqa: E501
    address: StrictStr = Field(description="The address of the agent that we are retrieving search analytics for")
    term_percentages: List[SearchTermPercentage] = Field(description="Percentage of searches with different terms when this agent was retrieved")
    __properties: ClassVar[List[str]] = ["address", "term_percentages"]

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
        """Create an instance of AgentSearchTermAnalyticsResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in term_percentages (list)
        _items = []
        if self.term_percentages:
            for _item_term_percentages in self.term_percentages:
                if _item_term_percentages:
                    _items.append(_item_term_percentages.to_dict())
            _dict['term_percentages'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AgentSearchTermAnalyticsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "address": obj.get("address"),
            "term_percentages": [SearchTermPercentage.from_dict(_item) for _item in obj["term_percentages"]] if obj.get("term_percentages") is not None else None
        })
        return _obj


