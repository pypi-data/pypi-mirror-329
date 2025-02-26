# tests/test_wallet_manager.py

from unittest.mock import MagicMock

import pytest
from gql import gql

from Api.api_manager import ApiManager
from Wallet.graphql_queries import (CHECK_WALLET_BALANCE_QUERY,
                                    CREATE_MULTIPLE_WALLETS_MUTATION,
                                    CREATE_WALLET_MUTATION,
                                    DELETE_WALLET_MUTATION,
                                    DELETE_WALLETS_MUTATION,
                                    GET_ALL_WALLETS_QUERY)
from Wallet.wallet_manager import WalletManager

# Sample mock responses
MOCK_CREATE_WALLET_RESPONSE = {
    "createWallet": {
        "success": True,
        "message": "Wallet created successfully.",
        "wallet": {
            "coinId": 1,
            "balance": 0.0,
            "symbol": "BTC",
            "publicAddress": "0xabc123..."
        }
    }
}

MOCK_CREATE_WALLETS_RESPONSE = {
    "createMultipleWallets": {
        "success": True,
        "message": "Multiple wallets processed.",
        "wallets": [
            {
                "coinId": 1,
                "balance": 0.0,
                "symbol": "BTC",
                "publicAddress": "0xabc123...",
                "label": "user@example.com-wallet"
            },
            {
                "coinId": 1,
                "balance": 0.0,
                "symbol": "BTC",
                "publicAddress": "0xdef456...",
                "label": "user@example.com-wallet-1"
            }
        ],
        "details": [
            "Created wallet for coin 1.",
            "Created wallet for coin 1."
        ]
    }
}

MOCK_GET_ALL_WALLETS_RESPONSE = {
    "getAllWallets": {
        "success": True,
        "message": "Retrieved 2 wallet(s).",
        "wallets": [
            {
                "coinId": 1,
                "balance": 0.0,
                "symbol": "BTC",
                "publicAddress": "0xabc123...",
                "label": "user@example.com-wallet",
                "owner": "user@example.com"
            },
            {
                "coinId": 1,
                "balance": 0.0,
                "symbol": "BTC",
                "publicAddress": "0xdef456...",
                "label": "user@example.com-wallet-1",
                "owner": "user@example.com"
            }
        ]
    }
}

MOCK_DELETE_WALLET_RESPONSE = {
    "deleteWallet": {
        "success": True,
        "message": "Wallet with public address 0xabc123... deleted successfully."
    }
}

MOCK_DELETE_WALLETS_RESPONSE = {
    "deleteWallets": {
        "success": True,
        "message": "Wallet deletion processed.",
        "deletedWallets": ["0xabc123...", "0xdef456..."],
        "notFoundWallets": []
    }
}

MOCK_CHECK_BALANCE_RESPONSE = {
    "checkWalletBalance": {
        "success": True,
        "message": "Wallet balance retrieved successfully.",
        "balance": 150.75,
        "symbol": "BTC",
        "label": "user@example.com-wallet"
    }
}

# Error mock responses
MOCK_WALLET_NOT_FOUND_RESPONSE = {
    "checkWalletBalance": {
        "success": False,
        "message": "Wallet with public address 0xnonexistent does not exist or does not belong to the requester.",
        "balance": None,
        "symbol": None,
        "label": None
    }
}

@pytest.fixture
def wallet_manager():
    base_url = "https://api.example.com"
    api_key = "test_wallet_api_key"
    api_manager = ApiManager(base_url, api_key)
    return WalletManager(api_manager)

@pytest.fixture
def mock_client(monkeypatch, wallet_manager):
    mock_execute = MagicMock()
    monkeypatch.setattr(wallet_manager.api_manager.client, 'execute', mock_execute)
    return mock_execute

def test_create_wallet_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_CREATE_WALLET_RESPONSE

    response = wallet_manager.create_wallet(coin_id=1)
    
    assert response == MOCK_CREATE_WALLET_RESPONSE
    mock_client.assert_called_once_with(
        gql(CREATE_WALLET_MUTATION),
        variable_values={"input": {"coinId": 1}},
    )

def test_create_wallet_failure(wallet_manager, mock_client):
    mock_client.side_effect = Exception("GraphQL Error: Wallet creation failed.")

    with pytest.raises(RuntimeError) as exc_info:
        wallet_manager.create_wallet(coin_id=1)
    
    assert "Failed GraphQL operation: GraphQL Error: Wallet creation failed." in str(exc_info.value)
    mock_client.assert_called_once_with(
        gql(CREATE_WALLET_MUTATION),
        variable_values={"input": {"coinId": 1}},
    )

def test_create_multiple_wallets_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_CREATE_WALLETS_RESPONSE

    response = wallet_manager.create_multiple_wallets(coin_id=1, count=2)
    
    assert response == MOCK_CREATE_WALLETS_RESPONSE
    mock_client.assert_called_once_with(
        gql(CREATE_MULTIPLE_WALLETS_MUTATION),
        variable_values={"input": {"coinId": 1, "count": 2}},
    )

def test_get_all_wallets_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_GET_ALL_WALLETS_RESPONSE

    response = wallet_manager.get_all_wallets()
    
    assert response == MOCK_GET_ALL_WALLETS_RESPONSE
    mock_client.assert_called_once_with(
        gql(GET_ALL_WALLETS_QUERY),
        variable_values=None,
    )

def test_delete_wallet_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_DELETE_WALLET_RESPONSE

    response = wallet_manager.delete_wallet(public_address="0xabc123...")
    
    assert response == MOCK_DELETE_WALLET_RESPONSE
    mock_client.assert_called_once_with(
        gql(DELETE_WALLET_MUTATION),
        variable_values={"input": {"publicAddress": "0xabc123..."}},
    )

def test_delete_wallets_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_DELETE_WALLETS_RESPONSE

    public_addresses = ["0xabc123...", "0xdef456..."]
    response = wallet_manager.delete_wallets(public_addresses=public_addresses)
    
    assert response == MOCK_DELETE_WALLETS_RESPONSE
    mock_client.assert_called_once_with(
        gql(DELETE_WALLETS_MUTATION),
        variable_values={"input": {"publicAddresses": public_addresses}},
    )

def test_check_wallet_balance_success(wallet_manager, mock_client):
    mock_client.return_value = MOCK_CHECK_BALANCE_RESPONSE

    response = wallet_manager.check_wallet_balance(public_address="0xabc123...")
    
    assert response == MOCK_CHECK_BALANCE_RESPONSE
    mock_client.assert_called_once_with(
        gql(CHECK_WALLET_BALANCE_QUERY),
        variable_values={"publicAddress": "0xabc123..."},
    )

def test_check_wallet_balance_wallet_not_found(wallet_manager, mock_client):
    mock_client.return_value = MOCK_WALLET_NOT_FOUND_RESPONSE

    response = wallet_manager.check_wallet_balance(public_address="0xnonexistent")
    
    assert response == MOCK_WALLET_NOT_FOUND_RESPONSE
    mock_client.assert_called_once_with(
        gql(CHECK_WALLET_BALANCE_QUERY),
        variable_values={"publicAddress": "0xnonexistent"},
    )

def test_check_wallet_balance_failure(wallet_manager, mock_client):
    mock_client.side_effect = Exception("Network Error")

    with pytest.raises(RuntimeError) as exc_info:
        wallet_manager.check_wallet_balance(public_address="0xabc123...")
    
    assert "Failed GraphQL operation: Network Error" in str(exc_info.value)
    mock_client.assert_called_once_with(
        gql(CHECK_WALLET_BALANCE_QUERY),
        variable_values={"publicAddress": "0xabc123..."},
    )
