# graphql_queries.py

# Mutation for creating a user
CREATE_USER_MUTATION = """
mutation CreateUser($email: String!, $password: String!, $organization: String) {
    createUser(email: $email, password: $password, organization: $organization) {
        success
        message
        user {
            id
            email
            organization
            createdAt
        }
    }
}
"""

# Mutation for creating a company
CREATE_COMPANY_MUTATION = """
mutation CreateCompany($name: String!) {
    createCompany(name: $name) {
        success
        message
        company {
            id
            name
            createdAt
        }
    }
}
"""

# Query for fetching API keys
GET_API_KEYS_QUERY = """
query GetApiKeys($entityType: String!, $entityIdentifier: String!) {
    getApiKeys(entityType: $entityType, entityIdentifier: $entityIdentifier) {
        key
        createdAt
        entityType
        entityName
    }
}
"""

# Mutation for creating an API key
CREATE_API_KEY_MUTATION = """
mutation CreateApiKey($entityType: String!, $entityIdentifier: String!, $scopes: [String!]) {
    createApiKey(entityType: $entityType, entityIdentifier: $entityIdentifier, scopes: $scopes) {
        success
        message
        apiKey {
            key
            createdAt
            entityType
            entityName
        }
    }
}
"""

# Query for checking API key usage
CHECK_API_KEY_USAGE_QUERY = """
query CheckApiKeyUsage($apiKey: String!) {
    getApiKeyUsage(apiKey: $apiKey) {
        usageCount
        rateLimit
        remainingRequests
        isWithinLimit
    }
}
"""


# Mutation for rotating an API key
ROTATE_API_KEY_MUTATION = """
mutation RotateApiKey($apiKeyId: String!) {
    rotateApiKey(apiKeyId: $apiKeyId) {
        success
        message
        apiKey {
            key
            createdAt
            entityType
            entityName
        }
    }
}
"""

# Mutation for revoking an API key
REVOKE_API_KEY_MUTATION = """
mutation RevokeApiKey($apiKeyId: String!) {
    revokeApiKey(apiKeyId: $apiKeyId) {
        success
        message
    }
}
"""
