# coding: utf-8

"""
    Compass API

      #### Welcome to the DeFi API from [Compass Labs](https://www.compasslabs.ai)!  Our API allows you to interact and transact in DeFi with ease.  We help you construct your transactions via a **simple REST API**.   You maintain custody at all times and **sign** all transactions **yourself**.  Below is the documentation of our endpoints. It's a great first step to explore.    ---  **Try out our [App](https://api-app.compasslabs.ai/) built on top of the API!**  ---

    The version of the OpenAPI document: 0.0.1
    Contact: contact@compasslabs.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from compass.api_client.models.aero_remove_liquidity_eth_call_data import AeroRemoveLiquidityEthCallData

class TestAeroRemoveLiquidityEthCallData(unittest.TestCase):
    """AeroRemoveLiquidityEthCallData unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AeroRemoveLiquidityEthCallData:
        """Test AeroRemoveLiquidityEthCallData
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AeroRemoveLiquidityEthCallData`
        """
        model = AeroRemoveLiquidityEthCallData()
        if include_optional:
            return AeroRemoveLiquidityEthCallData(
                token = '1INCH',
                stable = True,
                liquidity = None,
                amount_token_min = None,
                amount_eth_min = None,
                to = '',
                deadline = 56
            )
        else:
            return AeroRemoveLiquidityEthCallData(
                token = '1INCH',
                stable = True,
                liquidity = None,
                amount_token_min = None,
                amount_eth_min = None,
                deadline = 56,
        )
        """

    def testAeroRemoveLiquidityEthCallData(self):
        """Test AeroRemoveLiquidityEthCallData"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
