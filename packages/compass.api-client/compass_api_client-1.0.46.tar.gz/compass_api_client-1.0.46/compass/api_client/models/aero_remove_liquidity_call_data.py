# coding: utf-8

"""
    Compass API

      #### Welcome to the DeFi API from [Compass Labs](https://www.compasslabs.ai)!  Our API allows you to interact and transact in DeFi with ease.  We help you construct your transactions via a **simple REST API**.   You maintain custody at all times and **sign** all transactions **yourself**.  Below is the documentation of our endpoints. It's a great first step to explore.    ---  **Try out our [App](https://api-app.compasslabs.ai/) built on top of the API!**  ---

    The version of the OpenAPI document: 0.0.1
    Contact: contact@compasslabs.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from compass.api_client.models.amount_a_min1 import AmountAMin1
from compass.api_client.models.amount_b_min1 import AmountBMin1
from compass.api_client.models.liquidity import Liquidity
from compass.api_client.models.token import Token
from typing import Optional, Set
from typing_extensions import Self

class AeroRemoveLiquidityCallData(BaseModel):
    """
    AeroRemoveLiquidityCallData
    """ # noqa: E501
    token_a: Token = Field(description="The symbol of the token to remove liquidity for<br> Note the supported tokens per chain:<br>**ethereum:mainnet**: ['1INCH', 'AAVE', 'BAL', 'cbBTC', 'cbETH', 'CRV', 'crvUSD', 'DAI', 'ENS', 'ETHx', 'FRAX', 'FXS', 'GHO', 'KNC', 'LDO', 'LINK', 'LUSD', 'MKR', 'osETH', 'PYUSD', 'rETH', 'RPL', 'rsETH', 'sDAI', 'SNX', 'STG', 'sUSDe', 'tBTC', 'UNI', 'USDC', 'USDe', 'USDS', 'USDT', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>**arbitrum:mainnet**: ['AAVE', 'ARB', 'DAI', 'EURS', 'FRAX', 'GHO', 'LINK', 'LUSD', 'MAI', 'rETH', 'USDC', 'USDCe', 'USDT', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>**base:mainnet**: ['1INCH', 'AERO', 'ARB', 'BAL', 'cbBTC', 'cbETH', 'CRV', 'crvUSD', 'DAI', 'EUR', 'LUSD', 'MKR', 'osETH', 'rETH', 'SNX', 'STG', 'tBTC', 'USDC', 'UNI', 'USDT', 'VIRTUAL', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>")
    token_b: Token = Field(description="The symbol of the token to remove liquidity for<br> Note the supported tokens per chain:<br>**ethereum:mainnet**: ['1INCH', 'AAVE', 'BAL', 'cbBTC', 'cbETH', 'CRV', 'crvUSD', 'DAI', 'ENS', 'ETHx', 'FRAX', 'FXS', 'GHO', 'KNC', 'LDO', 'LINK', 'LUSD', 'MKR', 'osETH', 'PYUSD', 'rETH', 'RPL', 'rsETH', 'sDAI', 'SNX', 'STG', 'sUSDe', 'tBTC', 'UNI', 'USDC', 'USDe', 'USDS', 'USDT', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>**arbitrum:mainnet**: ['AAVE', 'ARB', 'DAI', 'EURS', 'FRAX', 'GHO', 'LINK', 'LUSD', 'MAI', 'rETH', 'USDC', 'USDCe', 'USDT', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>**base:mainnet**: ['1INCH', 'AERO', 'ARB', 'BAL', 'cbBTC', 'cbETH', 'CRV', 'crvUSD', 'DAI', 'EUR', 'LUSD', 'MKR', 'osETH', 'rETH', 'SNX', 'STG', 'tBTC', 'USDC', 'UNI', 'USDT', 'VIRTUAL', 'WBTC', 'weETH', 'WETH', 'wstETH']<br>")
    stable: StrictBool = Field(description="If true, try to remove liquidity from a stable pool with a bonding curve of K=x^3y+y^3x. If false, try to remove liquidity from a volatile pool with a bonding curve of K=xy")
    liquidity: Liquidity
    amount_a_min: AmountAMin1
    amount_b_min: AmountBMin1
    to: Optional[StrictStr] = None
    deadline: Optional[StrictInt]
    __properties: ClassVar[List[str]] = ["token_a", "token_b", "stable", "liquidity", "amount_a_min", "amount_b_min", "to", "deadline"]

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
        """Create an instance of AeroRemoveLiquidityCallData from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of liquidity
        if self.liquidity:
            _dict['liquidity'] = self.liquidity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of amount_a_min
        if self.amount_a_min:
            _dict['amount_a_min'] = self.amount_a_min.to_dict()
        # override the default output from pydantic by calling `to_dict()` of amount_b_min
        if self.amount_b_min:
            _dict['amount_b_min'] = self.amount_b_min.to_dict()
        # set to None if to (nullable) is None
        # and model_fields_set contains the field
        if self.to is None and "to" in self.model_fields_set:
            _dict['to'] = None

        # set to None if deadline (nullable) is None
        # and model_fields_set contains the field
        if self.deadline is None and "deadline" in self.model_fields_set:
            _dict['deadline'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AeroRemoveLiquidityCallData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "token_a": obj.get("token_a"),
            "token_b": obj.get("token_b"),
            "stable": obj.get("stable"),
            "liquidity": Liquidity.from_dict(obj["liquidity"]) if obj.get("liquidity") is not None else None,
            "amount_a_min": AmountAMin1.from_dict(obj["amount_a_min"]) if obj.get("amount_a_min") is not None else None,
            "amount_b_min": AmountBMin1.from_dict(obj["amount_b_min"]) if obj.get("amount_b_min") is not None else None,
            "to": obj.get("to"),
            "deadline": obj.get("deadline")
        })
        return _obj


