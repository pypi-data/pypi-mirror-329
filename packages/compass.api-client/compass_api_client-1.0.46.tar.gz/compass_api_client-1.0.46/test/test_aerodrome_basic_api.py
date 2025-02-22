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

from compass.api_client.api.aerodrome_basic_api import AerodromeBasicApi


class TestAerodromeBasicApi(unittest.TestCase):
    """AerodromeBasicApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AerodromeBasicApi()

    def tearDown(self) -> None:
        pass

    def test_process_request_v0_aerodrome_basic_liquidity_provision_add_liquidity_eth_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_liquidity_provision_add_liquidity_eth_post

        Provide liquidity to a pool on Aerodrome using WETH and another token
        """
        pass

    def test_process_request_v0_aerodrome_basic_liquidity_provision_add_liquidity_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_liquidity_provision_add_liquidity_post

        Provide liquidity to a pool on Aerodrome
        """
        pass

    def test_process_request_v0_aerodrome_basic_liquidity_provision_remove_liquidity_eth_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_liquidity_provision_remove_liquidity_eth_post

        Remove liquidity from a pool on Aerodrome using WETH and another token
        """
        pass

    def test_process_request_v0_aerodrome_basic_liquidity_provision_remove_liquidity_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_liquidity_provision_remove_liquidity_post

        Remove liquidity from a pool on Aerodrome
        """
        pass

    def test_process_request_v0_aerodrome_basic_swap_eth_for_token_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_swap_eth_for_token_post

        Swap ETH for some of a token on Aerodrome
        """
        pass

    def test_process_request_v0_aerodrome_basic_swap_token_for_eth_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_swap_token_for_eth_post

        Swap a token for ETH on Aerodrome
        """
        pass

    def test_process_request_v0_aerodrome_basic_swap_tokens_post(self) -> None:
        """Test case for process_request_v0_aerodrome_basic_swap_tokens_post

        Swap one token for another token on Aerodrome
        """
        pass


if __name__ == '__main__':
    unittest.main()
