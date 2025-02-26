# Wallet/wallet_manager.py

import logging

from gql import gql

from dnet.Api.api_manager import ApiManager
from dnet.Wallet.graphql_queries import (CHECK_WALLET_BALANCE_QUERY,
                                         CREATE_MULTIPLE_WALLETS_MUTATION,
                                         CREATE_WALLET_MUTATION,
                                         DELETE_WALLET_MUTATION,
                                         DELETE_WALLETS_MUTATION,
                                         GET_ALL_WALLETS_QUERY)


class WalletManager:
    """
    A class to manage wallet-related operations via the network API using GraphQL.
    """

    def __init__(self, api_manager: ApiManager):
        """
        Initialize the WalletManager with an instance of ApiManager.
        :param api_manager: An instance of ApiManager for executing GraphQL operations.
        """
        self.api_manager = api_manager

    def create_wallet(self, coin_id: int):
        """
        Create a new wallet with the specified coin ID.
        :param coin_id: The ID of the coin for which to create the wallet.
        :return: Wallet creation response.
        """
        input_data = {"coinId": coin_id}
        variables = {"input": input_data}
        response = self.api_manager._execute_graphql(
            CREATE_WALLET_MUTATION,
            variables,
        )
        return response

    # Additional wallet-related methods can be added here
    
    
    
    def create_multiple_wallets(self, coin_id: int, count: int):
        """
        Create multiple wallets for the specified coin ID.
        :param coin_id: The ID of the coin for which to create wallets.
        :param count: The number of wallets to create.
        :return: Response for multiple wallet creation.
        """
        input_data = {"coinId": coin_id, "count": count}
        variables = {"input": input_data}
        response = self.api_manager._execute_graphql(
            CREATE_MULTIPLE_WALLETS_MUTATION,
            variables,
        )
        return response
    
    
    def get_all_wallets(self):
        """
        Get all wallets associated with the current API key.
        :return: List of wallets and their details.
        """
        response = self.api_manager._execute_graphql(GET_ALL_WALLETS_QUERY)
        return response

    def delete_wallet(self, public_address: str):
        """
        Delete a single wallet by its public address.
        """
        input_data = {"publicAddress": public_address}
        variables = {"input": input_data}
        response = self.api_manager._execute_graphql(DELETE_WALLET_MUTATION, variables)
        return response


    def delete_wallets(self, public_addresses: list):
        """
        Delete multiple wallets by their public addresses.
        """
        input_data = {"publicAddresses": public_addresses}
        variables = {"input": input_data}
        response = self.api_manager._execute_graphql(DELETE_WALLETS_MUTATION, variables)
        return response

    
    
    def check_wallet_balance(self, public_address: str):
        """
        Check the balance of a wallet by its public address.
        :param public_address: The public address of the wallet to check.
        :return: Wallet balance response.
        """
        variables = {"publicAddress": public_address}
        response = self.api_manager._execute_graphql(
            CHECK_WALLET_BALANCE_QUERY,
            variables,
        )
        return response

