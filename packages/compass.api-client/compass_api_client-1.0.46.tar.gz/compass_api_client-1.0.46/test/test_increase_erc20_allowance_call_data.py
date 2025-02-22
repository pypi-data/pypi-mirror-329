# coding: utf-8

"""
    Compass API

      #### Welcome to the DeFi API from [Compass Labs](https://www.compasslabs.ai)!  Our API allows you to interact and transact in DeFi with ease.  We help you construct your transactions via a **simple REST API**.   You maintain custody at all times and **sign** all transactions **yourself**.  Below is the documentation of our endpoints. It's a great first step to explore.  

    The version of the OpenAPI document: 0.0.1
    Contact: contact@compasslabs.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from compass.api_client.models.increase_erc20_allowance_call_data import IncreaseErc20AllowanceCallData

class TestIncreaseErc20AllowanceCallData(unittest.TestCase):
    """IncreaseErc20AllowanceCallData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IncreaseErc20AllowanceCallData:
        """Test IncreaseErc20AllowanceCallData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IncreaseErc20AllowanceCallData`
        """
        model = IncreaseErc20AllowanceCallData()
        if include_optional:
            return IncreaseErc20AllowanceCallData(
                token = '1INCH',
                contract_name = 'AaveV3Pool',
                amount = None
            )
        else:
            return IncreaseErc20AllowanceCallData(
                token = '1INCH',
                contract_name = 'AaveV3Pool',
                amount = None,
        )
        """

    def testIncreaseErc20AllowanceCallData(self):
        """Test IncreaseErc20AllowanceCallData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
