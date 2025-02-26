import json
import logging

from gql import (
    Client,
    gql,
)
from gql.transport.requests import RequestsHTTPTransport

from dnet.Api.graphql_queries import (
    CHECK_API_KEY_USAGE_QUERY,
    CREATE_API_KEY_MUTATION,
    CREATE_COMPANY_MUTATION,
    CREATE_USER_MUTATION,
    GET_API_KEYS_QUERY,
    REVOKE_API_KEY_MUTATION,
    ROTATE_API_KEY_MUTATION,
)

# Set the logging level for gql.transport.requests
logging.getLogger("gql.transport.requests").setLevel(logging.WARNING)


class ApiManager:
    """
    A library to interact with the network API for managing users, companies, and API keys using GraphQL.
    """

    def __init__(self, base_url: str, api_key: str = None):
        """
        Initialize the ApiManager with the network URL and optional API key.
        :param base_url: Base URL of the network API.
        :param api_key: API key for authentication (optional).
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = None
        #self.client = self._initialize_client()
        

    @property
    def client(self):
        """
        Create the GQL client on-demand (lazily), but only once.
        """
        if self._client is None:
            transport = RequestsHTTPTransport(
                url=f"{self.base_url}/graphql",
                headers={"X-API-Key": self.api_key} if self.api_key else {},
                verify=True,
            )
            self._client = Client(transport=transport, fetch_schema_from_transport=False)
        return self._client


    def _execute_graphql(self, query: str, variables: dict = None):
        """
        Execute a GraphQL query or mutation with error handling and structured output.
        :param query: GraphQL query or mutation as a string.
        :param variables: Variables for the query/mutation.
        :return: Parsed JSON response.
        """
        try:
            gql_query = gql(query)
            response = self.client.execute(gql_query, variable_values=variables)

            # Use print with json.dumps for readable output
            logging.info("GraphQL operation successful. Response:")
            json.dumps(response, indent=4)

            return response
        except Exception as e:
            # Use print with json.dumps for error output
            error_message = {"error": str(e)}
            logging.info("Error executing GraphQL operation:")
            json.dumps(error_message, indent=4)
            raise RuntimeError(f"Failed GraphQL operation: {e}")

    def create_user(self, email: str, password: str, organization: str = None):
        """
        Create a new user on the network.
        :param email: Email of the user.
        :param password: Password for the user.
        :param organization: Organization name (optional).
        :return: User creation response.
        """
        return self._execute_graphql(
            CREATE_USER_MUTATION,
            {"email": email, "password": password, "organization": organization},
        )

    def create_company(self, name: str):
        """
        Create a new company on the network.
        :param name: Name of the company.
        :return: Company creation response.
        """
        return self._execute_graphql(CREATE_COMPANY_MUTATION, {"name": name})

    def get_api_keys(self, entity_type: str, entity_identifier: str):
        """
        Fetch all API keys for the specified entity.
        :param entity_type: Type of the entity (e.g., "user" or "company").
        :param entity_identifier: Identifier of the entity (e.g., email or company name).
        :return: List of API keys.
        """
        return self._execute_graphql(
            GET_API_KEYS_QUERY,
            {"entityType": entity_type, "entityIdentifier": entity_identifier},
        )

    def create_api_key(self, entity_type: str, entity_identifier: str, scopes=None):
        """
        Create a new API key for the specified entity.
        :param entity_type: Type of the entity (e.g., "user" or "company").
        :param entity_identifier: Identifier of the entity (e.g., email or company name).
        :param scopes: List of scopes (default is ["read"]).
        :return: New API key details.
        """
        return self._execute_graphql(
            CREATE_API_KEY_MUTATION,
            {
                "entityType": entity_type,
                "entityIdentifier": entity_identifier,
                "scopes": scopes or ["read"],
            },
        )

    def check_api_key_usage(self, api_key: str):
        """
        Check the usage of a specific API key.
        :param api_key: The API key to check.
        :return: Usage details.
        """
        return self._execute_graphql(CHECK_API_KEY_USAGE_QUERY, {"apiKey": api_key})
    
    
    def rotate_api_key(self, api_key_id: str):
        """
        Rotate (regenerate) an API key, revoking the old one.
        :param api_key_id: ID of the API key to rotate.
        :return: New API key details.
        """
        return self._execute_graphql(
            ROTATE_API_KEY_MUTATION,
            {"apiKeyId": api_key_id},
        )

    def revoke_api_key(self, api_key_id: str):
        """
        Revoke an API key.
        :param api_key_id: ID of the API key to revoke.
        :return: Confirmation message.
        """
        return self._execute_graphql(
            REVOKE_API_KEY_MUTATION,
            {"apiKeyId": api_key_id},
        )

    
    
