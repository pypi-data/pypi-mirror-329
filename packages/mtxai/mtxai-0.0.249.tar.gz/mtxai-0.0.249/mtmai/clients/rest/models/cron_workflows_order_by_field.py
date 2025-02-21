# coding: utf-8

"""
    Mtmai API

    The Mtmai API

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class CronWorkflowsOrderByField(str, Enum):
    """
    CronWorkflowsOrderByField
    """

    """
    allowed enum values
    """
    NAME = 'name'
    CREATEDAT = 'createdAt'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CronWorkflowsOrderByField from a JSON string"""
        return cls(json.loads(json_str))


