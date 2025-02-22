# coding: utf-8

"""
    Phoenix API

    Base API for Glumanda and other services.

    The version of the OpenAPI document: Alpha
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class OrderStatus(str, Enum):
    """
    OrderStatus
    """

    """
    allowed enum values
    """
    IN_PROGRESS = 'in_progress'
    OFFER_ISSUED = 'offer_issued'
    INVOICE_FINALIZED = 'invoice_finalized'
    COMPLETED = 'completed'
    OFFER_ACCEPTED = 'offer_accepted'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of OrderStatus from a JSON string"""
        return cls(json.loads(json_str))


