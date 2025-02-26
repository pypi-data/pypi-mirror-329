

import logging

from dnet.Api.api_manager import ApiManager
from dnet.Transaction.graphql_queries import (CONVERT_COIN_MUTATION,
                                              GET_TRANSACTION_DETAILS_QUERY,
                                              GET_TRANSACTIONS_QUERY,
                                              SEND_DCOIN_MUTATION)


class TransactionManager:
    def __init__(self, api_manager: ApiManager):
        """
        Initialize the TransactionManager with an instance of ApiManager.
        :param api_manager: Instance of ApiManager for executing GraphQL operations.
        """
        self.api_manager = api_manager

    def create_transaction(self, sender_address, recipient_address, fee_payer_address, amount):
        """
        Send Dcoin from one wallet to another.
        :param sender_address: Address of the sender's wallet.
        :param recipient_address: Address of the recipient's wallet.
        :param fee_payer_address: Address of the fee payer's wallet.
        :param amount: Amount to send.
        :return: Response from the GraphQL API.
        """
        variables = {
            "senderAddress": sender_address,
            "recipientAddress": recipient_address,
            "feePayerAddress": fee_payer_address,
            "amount": amount
        }
        logging.info(f"Sending {amount} Dcoin from {sender_address} to {recipient_address}. Fee payer: {fee_payer_address}")
        response = self.api_manager._execute_graphql(SEND_DCOIN_MUTATION, variables)
        return response
    
    def convert_coin(self, sender_address,  recipient_address, fee_payer_address, amount):
        """
        Convert one coin to another.
        :param sender_address: Address of the sender's wallet.
        :param source_coin_id: ID of the source coin being converted.
        :param destination_coin_id: ID of the destination coin.
        :param recipient_address: Address of the recipient's wallet.
        :param amount: Amount to convert.
        :return: Response from the GraphQL API.
        """
        variables = {
            "senderAddress": sender_address,
            "recipientAddress": recipient_address,
            "feePayerAddress": fee_payer_address,
            "amount": amount
        }
        
        response = self.api_manager._execute_graphql(CONVERT_COIN_MUTATION, variables)
        
        return response

    def get_transactions(self, wallet_address):
        """
        Get transactions for a specific wallet address.
        :param wallet_address: Address of the wallet.
        :return: Response from the GraphQL API.
        """
        variables = {"walletAddress": wallet_address}
        response = self.api_manager._execute_graphql(GET_TRANSACTIONS_QUERY, variables)
        return response
    
    def get_transaction_details(self, transaction_id):
        """
        Get detailed information about a specific transaction.
        :param transaction_id: ID of the transaction.
        :return: Response from the GraphQL API.
        """
        variables = {"transactionId": transaction_id}
        logging.info(f"Fetching details for transaction ID: {transaction_id}")
        response = self.api_manager._execute_graphql(GET_TRANSACTION_DETAILS_QUERY, variables)
        return response