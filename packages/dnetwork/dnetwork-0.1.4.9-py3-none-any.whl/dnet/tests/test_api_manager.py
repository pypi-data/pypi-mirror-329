# tests/test_api_manager.py

from unittest.mock import MagicMock

import pytest

from Api.api_manager import ApiManager
from Api.graphql_queries import (CHECK_API_KEY_USAGE_QUERY,
                                 CREATE_API_KEY_MUTATION,
                                 CREATE_COMPANY_MUTATION, CREATE_USER_MUTATION,
                                 GET_API_KEYS_QUERY, REVOKE_API_KEY_MUTATION,
                                 ROTATE_API_KEY_MUTATION)

# Sample mock responses
MOCK_USER_RESPONSE = {
    "createUser": {
        "success": True,
        "message": "User created successfully.",
        "user": {
            "id": "user123",
            "email": "test@example.com",
            "organization": "TestOrg",
            "createdAt": "2024-01-01T00:00:00Z"
        }
    }
}

MOCK_COMPANY_RESPONSE = {
    "createCompany": {
        "success": True,
        "message": "Company created successfully.",
        "company": {
            "id": "company123",
            "name": "TestCompany",
            "createdAt": "2024-01-01T00:00:00Z"
        }
    }
}

MOCK_API_KEYS_RESPONSE = {
    "getApiKeys": [
        {
            "key": "api_key_1",
            "createdAt": "2024-01-01T00:00:00Z",
            "entityType": "user",
            "entityName": "test@example.com"
        },
        {
            "key": "api_key_2",
            "createdAt": "2024-02-01T00:00:00Z",
            "entityType": "user",
            "entityName": "test@example.com"
        }
    ]
}

MOCK_CREATE_API_KEY_RESPONSE = {
    "createApiKey": {
        "success": True,
        "message": "API key created successfully.",
        "apiKey": {
            "key": "new_api_key",
            "createdAt": "2024-03-01T00:00:00Z",
            "entityType": "user",
            "entityName": "test@example.com"
        }
    }
}

MOCK_CHECK_API_KEY_USAGE_RESPONSE = {
    "getApiKeyUsage": {
        "usageCount": 100,
        "rateLimit": 1000,
        "remainingRequests": 900,
        "isWithinLimit": True
    }
}

MOCK_ROTATE_API_KEY_RESPONSE = {
    "rotateApiKey": {
        "success": True,
        "message": "API key rotated successfully.",
        "apiKey": {
            "key": "rotated_api_key",
            "createdAt": "2024-04-01T00:00:00Z",
            "entityType": "user",
            "entityName": "test@example.com"
        }
    }
}

MOCK_REVOKE_API_KEY_RESPONSE = {
    "revokeApiKey": {
        "success": True,
        "message": "API key revoked successfully."
    }
}

@pytest.fixture
def api_manager():
    base_url = "https://api.example.com"
    api_key = "test_api_key"
    manager = ApiManager(base_url, api_key)
    return manager

@pytest.fixture
def mock_client(monkeypatch, api_manager):
    mock_execute = MagicMock()
    monkeypatch.setattr(api_manager.client, 'execute', mock_execute)
    return mock_execute

def test_create_user_success(api_manager, mock_client):
    mock_client.return_value = MOCK_USER_RESPONSE

    response = api_manager.create_user(email="test@example.com", password="securepassword", organization="TestOrg")
    
    assert response == MOCK_USER_RESPONSE
    mock_client.assert_called_once()

def test_create_user_failure(api_manager, mock_client):
    mock_client.side_effect = Exception("GraphQL Error: User creation failed.")

    with pytest.raises(RuntimeError) as exc_info:
        api_manager.create_user(email="test@example.com", password="securepassword")
    
    assert "Failed GraphQL operation: GraphQL Error: User creation failed." in str(exc_info.value)
    mock_client.assert_called_once()

def test_create_company_success(api_manager, mock_client):
    mock_client.return_value = MOCK_COMPANY_RESPONSE

    response = api_manager.create_company(name="TestCompany")
    
    assert response == MOCK_COMPANY_RESPONSE
    mock_client.assert_called_once()

def test_get_api_keys_success(api_manager, mock_client):
    mock_client.return_value = MOCK_API_KEYS_RESPONSE

    response = api_manager.get_api_keys(entity_type="user", entity_identifier="test@example.com")
    
    assert response == MOCK_API_KEYS_RESPONSE
    mock_client.assert_called_once()

def test_create_api_key_success(api_manager, mock_client):
    mock_client.return_value = MOCK_CREATE_API_KEY_RESPONSE

    response = api_manager.create_api_key(entity_type="user", entity_identifier="test@example.com", scopes=["read", "write"])
    
    assert response == MOCK_CREATE_API_KEY_RESPONSE
    mock_client.assert_called_once()

def test_check_api_key_usage_success(api_manager, mock_client):
    mock_client.return_value = MOCK_CHECK_API_KEY_USAGE_RESPONSE

    response = api_manager.check_api_key_usage(api_key="api_key_1")
    
    assert response == MOCK_CHECK_API_KEY_USAGE_RESPONSE
    mock_client.assert_called_once()

def test_rotate_api_key_success(api_manager, mock_client):
    mock_client.return_value = MOCK_ROTATE_API_KEY_RESPONSE

    response = api_manager.rotate_api_key(api_key_id="api_key_id_1")
    
    assert response == MOCK_ROTATE_API_KEY_RESPONSE
    mock_client.assert_called_once()

def test_revoke_api_key_success(api_manager, mock_client):
    mock_client.return_value = MOCK_REVOKE_API_KEY_RESPONSE

    response = api_manager.revoke_api_key(api_key_id="api_key_id_1")
    
    assert response == MOCK_REVOKE_API_KEY_RESPONSE
    mock_client.assert_called_once()

def test_create_api_key_default_scopes(api_manager, mock_client):
    mock_client.return_value = MOCK_CREATE_API_KEY_RESPONSE

    response = api_manager.create_api_key(entity_type="user", entity_identifier="test@example.com")
    
    assert response == MOCK_CREATE_API_KEY_RESPONSE
    mock_client.assert_called_once()
    variables = mock_client.call_args[1].get('variable_values', {})
    assert variables.get("scopes") == ["read"]

def test_graphql_error_handling(api_manager, mock_client):
    mock_client.side_effect = Exception("Network Error")

    with pytest.raises(RuntimeError) as exc_info:
        api_manager.get_api_keys(entity_type="user", entity_identifier="test@example.com")
    
    assert "Failed GraphQL operation: Network Error" in str(exc_info.value)
    mock_client.assert_called_once()
