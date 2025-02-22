# coding: utf-8

"""
    Mtmai API

    The Mtmai API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.clients.rest.models.team_config import TeamConfig
from typing import Optional, Set
from typing_extensions import Self

class TeamComponent(BaseModel):
    """
    TeamComponent
    """ # noqa: E501
    provider: StrictStr = Field(description="Describes how the component can be instantiated.")
    component_type: StrictStr = Field(description="Logical type of the component. If missing, the component assumes the default type of the provider.")
    version: Optional[StrictInt] = Field(default=None, description="Version of the component specification. If missing, the component assumes whatever is the current version of the library used to load it. This is obviously dangerous and should be used for user authored ephmeral config. For all other configs version should be specified.")
    component_version: Optional[StrictInt] = Field(default=None, description="Version of the component. If missing, the component assumes the default version of the provider.")
    description: Optional[StrictStr] = Field(default=None, description="Description of the component.")
    label: Optional[StrictStr] = Field(default=None, description="Human readable label for the component. If missing the component assumes the class name of the provider.")
    config: TeamConfig
    __properties: ClassVar[List[str]] = ["provider", "component_type", "version", "component_version", "description", "label", "config"]

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
        """Create an instance of TeamComponent from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of config
        if self.config:
            _dict['config'] = self.config.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TeamComponent from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "provider": obj.get("provider"),
            "component_type": obj.get("component_type"),
            "version": obj.get("version"),
            "component_version": obj.get("component_version"),
            "description": obj.get("description"),
            "label": obj.get("label"),
            "config": TeamConfig.from_dict(obj["config"]) if obj.get("config") is not None else None
        })
        return _obj


