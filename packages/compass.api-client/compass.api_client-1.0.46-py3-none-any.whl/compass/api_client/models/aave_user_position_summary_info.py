# coding: utf-8

"""
    Compass API

      #### Welcome to the DeFi API from [Compass Labs](https://www.compasslabs.ai)!  Our API allows you to interact and transact in DeFi with ease.  We help you construct your transactions via a **simple REST API**.   You maintain custody at all times and **sign** all transactions **yourself**.  Below is the documentation of our endpoints. It's a great first step to explore.  

    The version of the OpenAPI document: 0.0.1
    Contact: contact@compasslabs.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class AaveUserPositionSummaryInfo(BaseModel):
    """
    AaveUserPositionSummaryInfo
    """ # noqa: E501
    maximum_loan_to_value_ratio: StrictStr = Field(description="The loan to value ratio of a user.")
    health_factor: StrictStr = Field(description="The health factor of a user. If this is above 1 it is safe; below 1 and the user is in risk of liquidation. This number might be very high (which would mean the user is safe!)")
    total_collateral: StrictStr = Field(description="The total collateral (in USD) of a user.")
    total_debt: StrictStr = Field(description="The total debt (in USD) of a user.")
    available_borrows: StrictStr = Field(description="The available borrows (in USD) of a user.")
    liquidation_threshold: StrictStr = Field(description="The liquidation threshold of a user. A user might exceed this due to changing asset values.")
    __properties: ClassVar[List[str]] = ["maximum_loan_to_value_ratio", "health_factor", "total_collateral", "total_debt", "available_borrows", "liquidation_threshold"]

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
        """Create an instance of AaveUserPositionSummaryInfo from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AaveUserPositionSummaryInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "maximum_loan_to_value_ratio": obj.get("maximum_loan_to_value_ratio"),
            "health_factor": obj.get("health_factor"),
            "total_collateral": obj.get("total_collateral"),
            "total_debt": obj.get("total_debt"),
            "available_borrows": obj.get("available_borrows"),
            "liquidation_threshold": obj.get("liquidation_threshold")
        })
        return _obj


