

import json
import logging

from dnet.Api.api_manager import ApiManager
from dnet.Coin.graphql_queries import (ADD_FARM_TRANSACTION_MUTATION,
                                       ADD_LIQUIDITY_MUTATION,
                                       APPROVE_COIN_MUTATION,
                                       CLAIM_AIRDROP_MUTATION,
                                       CLAIM_FARM_REWARDS_MUTATION,
                                       CREATE_AIRDROP_MUTATION,
                                       CREATE_COIN_MUTATION,
                                       CREATE_FARM_MUTATION,
                                       CREATE_GOVERNANCE_PROPOSAL_MUTATION,
                                       CREATE_LIQUIDITY_POOL_MUTATION,
                                       DELEGATE_VOTE_MUTATION,
                                       GET_ACTIVE_DELEGATES_QUERY,
                                       GET_ALL_AIRDROPS_QUERY,
                                       GET_ALL_COINS_QUERY,
                                       GET_ALL_DELEGATES_QUERY,
                                       GET_AUDIT_LOGS_QUERY,
                                       GET_COIN_ANALYTICS_QUERY,
                                       GET_COIN_GOVERNANCE_MODEL_QUERY,
                                       GET_COIN_STATISTICS_QUERY,
                                       GET_DELEGATE_MISCONDUCT_REPORTS_QUERY,
                                       GET_ELECTION_RESULTS_QUERY,
                                       GET_FARM_EVENTS_QUERY,
                                       GET_FARM_TXS_IN_POOL_QUERY,
                                       GET_GOVERNANCE_LEADERBOARD_QUERY,
                                       GET_GOVERNANCE_PROPOSALS_QUERY,
                                       GET_GOVERNANCE_VOTES_QUERY,
                                       GET_LEADERBOARD_QUERY,
                                       GET_LIQUIDITY_POOLS_QUERY,
                                       GET_LOYALTY_LEADERBOARD_QUERY,
                                       GET_PREMINE_REPORT_QUERY,
                                       GET_REWARDS_LEADERBOARD_QUERY,
                                       GET_STAKED_AMOUNT_LEADERBOARD_QUERY,
                                       GET_STAKES_QUERY,
                                       GET_TRANSACTIONS_IN_POOL_QUERY,
                                       GET_USER_FARMS_QUERY,
                                       PREMINE_ALLOCATION_MUTATION,
                                       REGISTER_DELEGATE_MUTATION,
                                       REMOVE_TRANSACTION_LIQUIDITY_MUTATION,
                                       REPORT_DELEGATE_MISCONDUCT_MUTATION,
                                       REVOKE_DELEGATION_MUTATION,
                                       STAKE_TOKENS_MUTATION,
                                       SWITCH_GOVERNANCE_MODEL_MUTATION,
                                       UPDATE_APR_STRATEGY_MUTATION,
                                       VOTE_GOVERNANCE_PROPOSAL_MUTATION,
                                       WITHDRAW_FARM_MUTATION,GET_GOVERNANCE_PROPOSAL_WITH_VOTES_QUERY,
                                       WITHDRAW_STAKE_MUTATION)


class CoinManager:
    def __init__(self, api_manager: ApiManager):
        """
        Initialize the CoinManager with an instance of ApiManager.
        :param api_manager: Instance of ApiManager for executing GraphQL operations.
        """
        self.api_manager = api_manager

    def create_coin(self, name, symbol, max_supply, total_supply, decimals, consensus_type, governance_model, transaction_fee, visibility, metadata=None, treasury_wallet=None, treasury_allocation_percentage=0.0, burnable=True, mintable=False):
        """
        Create a new coin.
        :param name: Name of the coin.
        :param symbol: Symbol of the coin.
        :param max_supply: Maximum supply of the coin.
        :param total_supply: Total supply of the coin.
        :param decimals: Number of decimals for the coin.
        :param governance_type: Governance type (e.g., PoW, PoS).
        :param transaction_fee: Default transaction fee.
        :param visibility: Visibility of the coin ("public" or "private").
        :param metadata: Optional metadata (e.g., logo URL, description).
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "name": name,
                "symbol": symbol,
                "maxSupply": max_supply,
                "totalSupply": total_supply,
                "decimals": decimals,
                "consensusType": consensus_type,
                "governanceModel": governance_model,
                "transactionFee": transaction_fee,
                "visibility": visibility,
                "metadata": metadata or {},
                "treasuryWallet": treasury_wallet,
                "treasuryAllocationPercentage": treasury_allocation_percentage,
                "burnable": burnable,
                "mintable": mintable,
            }
        }
        response = self.api_manager._execute_graphql(CREATE_COIN_MUTATION, variables)
        return response

    def get_all_coins(self):
        """
        Fetch all coins from the blockchain.
        :return: Response from the GraphQL API.
        """
        response = self.api_manager._execute_graphql(GET_ALL_COINS_QUERY, {})
        return response


    def approve_coin(self, coin_id):
        """
        Approve a registered coin.
        :param coin_id: ID of the coin to be approved.
        :return: Response from the GraphQL API.
        """
        variables = {"input": {"coinId": coin_id}}
        response = self.api_manager._execute_graphql(APPROVE_COIN_MUTATION, variables)
        return response

    def premine_allocation(self, coin_id, allocation):
        """
        Allocate premine for an approved coin.
        :param coin_id: ID of the coin.
        :param allocation: JSON representing the wallet allocations.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "allocation": allocation,
            }
        }
        response = self.api_manager._execute_graphql(
            PREMINE_ALLOCATION_MUTATION, variables
        )
        return response
    
    def get_audit_logs(self, filters=None):
        """
        Fetch audit logs with optional filters.
        :param filters: Dictionary of filters (e.g., action, initiator, timestamp range).
        :return: Response from the GraphQL API.
        """
        variables = {"input": filters or {}}
        return self.api_manager._execute_graphql(GET_AUDIT_LOGS_QUERY, variables)

    def get_premine_report(self, coin_id=None, start_date=None, end_date=None):
        """
        Generate a premine allocation report.
        :param coin_id: ID of the coin to filter by.
        :param start_date: Start date for the report.
        :param end_date: End date for the report.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "startDate": start_date,
                "endDate": end_date,
            }
        }
        return self.api_manager._execute_graphql(GET_PREMINE_REPORT_QUERY, variables)
    
    def get_coin_statistics(self, coin_id):
        """
        Fetch aggregate statistics for a specific coin.
        :param coin_id: ID of the coin.
        :return: Response from the GraphQL API.
        """
        variables = {"coinId": coin_id}
        response = self.api_manager._execute_graphql(GET_COIN_STATISTICS_QUERY, variables)
        return response
    
    
    def create_governance_proposal(self, coin_id, proposal_type, wallet_address, details):
        """
        Create a governance proposal with wallet-based tracking.
        :param coin_id: ID of the coin for which the proposal is being created.
        :param proposal_type: Type of the proposal (e.g., "burn", "mint").
        :param wallet_address: Wallet address initiating the proposal.
        :param details: Proposal details in JSON format.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "proposalType": proposal_type,
                "walletAddress": wallet_address,
                "details": json.dumps(details) if isinstance(details, dict) else details
            }
        }
        return self.api_manager._execute_graphql(CREATE_GOVERNANCE_PROPOSAL_MUTATION, variables)

    
    def get_governance_model(self, coin_id):
        """
        Fetch the governance model of a specific coin.
        :param coin_id: ID of the coin.
        :return: Governance model as a string.
        """
        
        variables = {
            "coinId": coin_id
        }
        response = self.api_manager._execute_graphql(GET_COIN_GOVERNANCE_MODEL_QUERY, variables)
        return response.get("getCoin", {}).get("governanceModel", "stake_weighted")
    
    def vote_governance_proposal(self, proposal_id, vote, wallet_address):
        """
        Vote on a governance proposal.
        :param proposal_id: ID of the proposal.
        :param vote: Vote type ("approve" or "reject").
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "proposalId": proposal_id,
                "vote": vote,
                "walletAddress": wallet_address
            }
        }
        response = self.api_manager._execute_graphql(VOTE_GOVERNANCE_PROPOSAL_MUTATION, variables)
        return response
    
    
    def get_governance_proposals(self, coin_id=None, status=None, limit=10, offset=0):
        """
        Fetch governance proposals with optional filters and pagination.
        :param coin_id: ID of the coin to filter by (optional).
        :param status: Status of proposals to filter by (optional).
        :param limit: Maximum number of results to return (default: 10).
        :param offset: Offset for pagination (default: 0).
        :return: List of governance proposals.
        """
        variables = {
            "coinId": coin_id,
            "status": status,
            "limit": limit,
            "offset": offset
        }
        response = self.api_manager._execute_graphql(GET_GOVERNANCE_PROPOSALS_QUERY, variables)
        return response
    
    def get_governance_votes(self, proposal_id, limit=10, offset=0):
        """
        Fetch votes for a specific governance proposal with pagination.
        :param proposal_id: ID of the governance proposal.
        :param limit: Maximum number of votes to return.
        :param offset: Number of votes to skip for pagination.
        :return: Response from the GraphQL API.
        """
        
        variables = {
            "proposalId": proposal_id,
            "limit": limit,
            "offset": offset,
        }
        return self.api_manager._execute_graphql(GET_GOVERNANCE_VOTES_QUERY, variables)
    
    
    def get_governance_proposal_with_votes(self, coin_id, status=None, limit=10, offset=0):
        """
        Fetch governance proposals with votes and pagination.
        :param coin_id: ID of the coin to filter by.
        :param limit: Maximum number of results to return.
        :param offset: Number of results to skip for pagination.
        :return: Response from the GraphQL API.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit,
            "status": status,
            "offset": offset
        }
        return self.api_manager._execute_graphql(GET_GOVERNANCE_PROPOSAL_WITH_VOTES_QUERY, variables)


    def register_delegate(self, coin_id, wallet_address, delegate_name):
        """
        Register a delegate for a specific coin.
        :param coin_id: ID of the coin.
        :param wallet_address: Wallet address of the delegate.
        :param delegate_name: Name of the delegate.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "walletAddress": wallet_address,
                "name": delegate_name
            }
        }
        return self.api_manager._execute_graphql(REGISTER_DELEGATE_MUTATION, variables)
    
    def delegate_vote(self, delegator_wallet_address, coin_id, delegate_id=None, delegatee_wallet_address=None):
        """
        Delegate voting power to another wallet or delegate by ID.
        :param delegator_wallet_address: Wallet address of the delegator.
        :param coin_id: ID of the coin for which voting power is delegated.
        :param delegate_id: ID of the delegate (optional).
        :param delegatee_wallet_address: Wallet address of the delegatee (optional).
        :return: Response from the GraphQL API.
        """
        if not delegate_id and not delegatee_wallet_address:
            raise ValueError("Either delegate_id or delegatee_wallet_address must be provided.")

        input_data = {
            "delegatorWalletAddress": delegator_wallet_address,
            "coinId": coin_id,
        }

        if delegate_id:
            input_data["delegateId"] = delegate_id
        if delegatee_wallet_address:
            input_data["delegateeWalletAddress"] = delegatee_wallet_address

        variables = {"input": input_data}

        return self.api_manager._execute_graphql(DELEGATE_VOTE_MUTATION, variables)


    def revoke_delegation(self, delegator_wallet_address, coin_id, delegate_id=None, delegatee_wallet_address=None):
        """
        Revoke delegated voting power.
        :param delegator_wallet_address: Wallet address of the delegator.
        :param coin_id: ID of the coin for which delegation is being revoked.
        :param delegate_id: ID of the delegate (optional).
        :param delegatee_wallet_address: Wallet address of the delegatee (optional).
        :return: Response from the GraphQL API.
        """
        if not delegate_id and not delegatee_wallet_address:
            raise ValueError("Either delegate_id or delegatee_wallet_address must be provided.")

        input_data = {
            "delegatorWalletAddress": delegator_wallet_address,
            "coinId": coin_id,
        }

        if delegate_id:
            input_data["delegateId"] = delegate_id
        if delegatee_wallet_address:
            input_data["delegateeWalletAddress"] = delegatee_wallet_address

        variables = {"input": input_data}

        return self.api_manager._execute_graphql(REVOKE_DELEGATION_MUTATION, variables)

    
    
    def get_active_delegates(self, coin_id, status=None, limit=100):
        
        variables = {"coinId": str(coin_id),
                     "status": status,
                     "limit": limit
                     }
        
        return self.api_manager._execute_graphql(GET_ACTIVE_DELEGATES_QUERY, variables)

    def get_all_delegates(self, coin_id, status=None, limit=100, offset=0):
        """
        Fetch all delegates for a specific coin with optional filters and pagination.
        """
        variables = {
            "coinId": coin_id,
            "status": status,
            "limit": limit,
            "offset": offset
        }
        return self.api_manager._execute_graphql(GET_ALL_DELEGATES_QUERY, variables)
    
    
    def report_delegate_misconduct(self, delegate_id, reason, wallet_address, evidence=None):
        """
        Report misconduct by a delegate.
        :param delegate_id: ID of the delegate being reported.
        :param reason: Reason for the misconduct report.
        :param wallet_address: Wallet address of the user submitting the report.
        :param evidence: Optional evidence supporting the report.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "delegateId": delegate_id,
                "reason": reason,
                "walletAddress": wallet_address,
                "evidence": evidence or "No evidence provided."
            }
        }
        response = self.api_manager._execute_graphql(REPORT_DELEGATE_MISCONDUCT_MUTATION, variables)
        return response
    
    
    def get_delegate_misconduct_reports(self, delegate_id=None, wallet_id=None, status=None, start_date=None, end_date=None):
        """
        Fetch misconduct reports for delegates with optional filters.
        :param delegate_id: Filter by delegate ID.
        :param wallet_id: Filter by wallet ID.
        :param status: Filter by report status (e.g., "pending", "resolved").
        :param start_date: Start date for filtering reports.
        :param end_date: End date for filtering reports.
        :return: Response from the GraphQL API.
        """
        variables = {
        "delegateId": delegate_id,
        "walletId": wallet_id,
        "status": status,
        "startDate": start_date,
        "endDate": end_date,
            }
        #response = self.api_manager._execute_graphql(GET_DELEGATE_MISCONDUCT_REPORTS_QUERY, filters)

        response = self.api_manager._execute_graphql(GET_DELEGATE_MISCONDUCT_REPORTS_QUERY, variables)
        return response
    
    def get_election_results(self, coin_id):
        """
        Fetch election results for a specific coin.
        :param coin_id: ID of the coin.
        :return: Response from the GraphQL API.
        """
        variables = {
            "coinId": coin_id
        }
        return self.api_manager._execute_graphql(GET_ELECTION_RESULTS_QUERY, variables)
    
        
    def switch_governance_model(self, coin_id, new_model):
        """
        Switch governance model for a coin.
        :param coin_id: ID of the coin.
        :param new_model: New governance model ("STAKE_WEIGHTED" or "OPEN").
        :return: Response from the GraphQL API.
        """
        if new_model.lower() not in {"stake_weighted", "open"}:
            raise ValueError("Invalid governance model. Use 'stake_weighted' or 'open'.")
        
        # Convert to uppercase enum value as expected by the API
        enum_value = new_model.upper()
        
        variables = {
            "coinId": coin_id,
            "newModel": enum_value
        }
        return self.api_manager._execute_graphql(SWITCH_GOVERNANCE_MODEL_MUTATION, variables)
    
    # Stake Management
    
    def stake_tokens(self, coin_id, staked_amount, lock_period, wallet_address):
        """
        Stake tokens for a specific coin.
        :param coin_id: ID of the coin.
        :param staked_amount: Amount of tokens to stake.
        :param lock_period: Lock period in days.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "stakedAmount": staked_amount,
                "lockPeriod": lock_period,
                "walletAddress": wallet_address
            }
        }
        return self.api_manager._execute_graphql(STAKE_TOKENS_MUTATION, variables)

    def withdraw_stake(self, stake_id, wallet_address):
        """
        Withdraw staked tokens and rewards.
        :param stake_id: ID of the stake.
        :return: Response from the GraphQL API.
        """
        variables = {
        "input": {
            "stakeId": stake_id,
            "walletAddress": wallet_address 
        }
        }
        return self.api_manager._execute_graphql(WITHDRAW_STAKE_MUTATION, variables)

    def get_stakes(self, wallet_address, coin_id):
        """
        Fetch all stakes for a specific user and coin.
        :param user_id: ID of the user.
        :param coin_id: ID of the coin.
        :return: Response from the GraphQL API.
        """
        variables = {"walletAddress": wallet_address, "coinId": coin_id}
        return self.api_manager._execute_graphql(GET_STAKES_QUERY, variables)

    
    
    
    def create_airdrop(self, coin_id, description, total_tokens, criteria=None):
        """
        Create a new airdrop campaign.
        :param coin_id: ID of the coin associated with the airdrop.
        :param description: Description of the airdrop.
        :param total_tokens: Total tokens allocated for the airdrop.
        :param criteria: Eligibility criteria for the airdrop (optional).
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "coinId": coin_id,
                "description": description,
                "totalTokens": total_tokens,
                "criteria": json.dumps(criteria) if criteria else "{}"  # Convert dict to JSON string
            }
        }
        response = self.api_manager._execute_graphql(CREATE_AIRDROP_MUTATION, variables)
        return response

    def claim_airdrop(self, airdrop_id, wallet_address):
        """
        Claim tokens from an airdrop.
        :param airdrop_id: ID of the airdrop.
        :param wallet_address: The wallet address claiming the airdrop.
        :return: Response from the GraphQL API.
        """
        variables = {
            "input": {
                "airdropId": airdrop_id,
                "walletAddress": wallet_address
            }
        }
        response = self.api_manager._execute_graphql(CLAIM_AIRDROP_MUTATION, variables)
        return response

    def get_airdrops(self, coin_id):
        """
        Fetch all airdrops for a specific coin.
        :param coin_id: ID of the coin.
        :return: List of airdrops from the GraphQL API.
        """
        variables = {
            "coinId": coin_id
        }
        response = self.api_manager._execute_graphql(GET_ALL_AIRDROPS_QUERY, variables)
        return response


    
    # Liquidity Pool Management
    


    def create_liquidity_pool(
        self,
        token_id: dict,
        reward_tokens: dict,
        description: str,
        apr_strategy: str,
        apr_parameters: dict,
        penalty_rate: float = 0.1,
        coin_inputs: dict = None  # <-- new parameter
    ):
        """
        Create a new liquidity pool with the given parameters, including initial liquidity.

        Args:
            token_id (dict): e.g. {"TOKEN_A": "address_A", "TOKEN_B": "address_B"}.
            reward_tokens (dict): e.g. {"DVC": 0.002, "DCX": 0.000005}.
            description (str): Pool description.
            apr_strategy (str): e.g., "linear", "exponential".
            apr_parameters (dict): e.g. {"max_liquidity": 1000000, "min_apr": 1.0}.
            penalty_rate (float): Penalty for early withdrawal (default 0.1).
            coin_inputs (dict, optional): The initial deposit amounts & wallet addrs for each token.
                e.g. {
                    "DVC": {"publicAddress": "...", "amount": 0.05},
                    "DCX": {"publicAddress": "...", "amount": 0.005}
                }

        Returns:
            dict: Result of the GraphQL mutation.
        """
        # Serialize dictionaries to JSON strings
        serialized_tokens = json.dumps(token_id)
        serialized_reward_tokens = json.dumps(reward_tokens)
        serialized_apr_parameters = json.dumps(apr_parameters)

        # Prepare the GraphQL variables
        variables = {
            "input": {
                "tokens": serialized_tokens,
                "rewardTokens": serialized_reward_tokens,
                "aprStrategy": apr_strategy,
                "aprParameters": serialized_apr_parameters,
                "penaltyRate": penalty_rate,
                "description": description
            }
        }

        # If coin_inputs is provided, serialize and include it
        if coin_inputs:
            serialized_coin_inputs = json.dumps(coin_inputs)
            variables["input"]["coinInputs"] = serialized_coin_inputs

        # Execute the GraphQL mutation (assuming CREATE_LIQUIDITY_POOL_MUTATION includes coinInputs in the schema)
        return self.api_manager._execute_graphql(CREATE_LIQUIDITY_POOL_MUTATION, variables)


    
    def get_liquidity_pools(self, filters=None):
        """
        Fetch all liquidity pools with optional filters.

        Args:
            filters (dict, optional): A dictionary of filters to apply. Possible keys include:
                - token_filter (str): Filter pools by a specific token (e.g., "TOKEN_A").
                - min_apr (float): Minimum APR to filter pools.
                - max_apr (float): Maximum APR to filter pools.
                - limit (int): The maximum number of results to return.
                - offset (int): The starting point for the results (used for pagination).

        Returns:
            list: A list of liquidity pools matching the filters.
        """
        # Default to an empty filters object if none are provided
        filters = filters or {}

        # Prepare GraphQL variables
        variables = {
            "filters": {
                "tokenFilter": filters.get("token_filter"),
                "minApr": filters.get("min_apr"),
                "maxApr": filters.get("max_apr"),
                "limit": filters.get("limit"),
                "offset": filters.get("offset"),
            }
        }

        # Execute the GraphQL query
        response = self.api_manager._execute_graphql(GET_LIQUIDITY_POOLS_QUERY, variables)

        return response
    
    
    def add_liquidity(self, pool_id, coin_inputs):
        """
        Add liquidity to a pool using one or two coins.

        Args:
            pool_id (str): ID of the liquidity pool to add liquidity to.
            coin_inputs (dict): Dictionary of coin inputs, e.g.,
                                {"coinA": {"publicAddress": "addr1", "amount": 100},
                                "coinB": {"publicAddress": "addr2", "amount": 50}}.

        Returns:
            dict: Response from the GraphQL mutation.
        """
        variables = {
            "input": {
                "poolId": str(pool_id),  # Ensure it's a string
                "coinInputs": json.dumps(coin_inputs)  # Serialize the coin inputs dictionary
            }
        }
        response = self.api_manager._execute_graphql(ADD_LIQUIDITY_MUTATION, variables)
        return response
    
    def get_transactions_in_pool(self, pool_id, limit=50, offset=0):
        """
        Fetch all transactions for a specific liquidity pool.

        Args:
            pool_id (int): ID of the liquidity pool to fetch transactions for.
            limit (int): Maximum number of results to return (default is 50).
            offset (int): Number of results to skip for pagination (default is 0).

        Returns:
            dict: Response from the GraphQL query.
        """
        variables = {
            "poolId": pool_id,  # Pass the pool ID as an integer
            "limit": limit,  # Apply pagination limit
            "offset": offset  # Apply pagination offset
        }
        response = self.api_manager._execute_graphql(GET_TRANSACTIONS_IN_POOL_QUERY, variables)
        return response
    
    def remove_transaction_from_liquidity(self, pool_id, wallet_id, transaction_id):
        """
        Remove liquidity from a pool by transaction ID.

        Args:
            pool_id (int): ID of the liquidity pool to remove liquidity from.
            transaction_id (int): ID of the transaction to be removed.

        Returns:
            dict: Response from the GraphQL mutation.
        """
        try:
            variables = {
                "input": {
                    "poolId": str(pool_id),  # Ensure the pool ID is passed as a string
                    "walletId": str(wallet_id),  # Ensure the wallet ID is passed as a string
                    "transactionId": str(transaction_id)
                }
            }
            response = self.api_manager._execute_graphql(REMOVE_TRANSACTION_LIQUIDITY_MUTATION, variables)
            if response.get("errors"):
                raise ValueError(f"GraphQL Errors: {response['errors']}")
            return response
        except Exception as e:
            logging.error(f"Error removing transaction from liquidity: {e}")
            return {
                "ok": False,
                "message": f"Failed to remove transaction {wallet_id} from pool {pool_id}. Reason: {str(e)}"
            }






    
    
    
    # def remove_liquidity(self, pool_id, lp_token_amount, wallet_id):
    #     """
    #     Remove liquidity from a pool.

    #     Args:
    #         pool_id (str): ID of the liquidity pool to remove liquidity from.
    #         lp_token_amount (float): Amount of LP tokens to redeem for liquidity removal.
    #         wallet_id (str): Wallet ID to associate with the removal.

    #     Returns:
    #         dict: Response from the GraphQL mutation.
    #     """
    #     variables = {
    #         "input": {
    #             "poolId": pool_id,
    #             "lpTokenAmount": lp_token_amount,
    #             "walletId": wallet_id
    #         }
    #     }
    #     return self.api_manager._execute_graphql(REMOVE_LIQUIDITY_MUTATION, variables)



    
    
    # Farming Management
    # Multi-Token Farming Management

    def create_farm(
        self,
        pool_id: int,
        farmed_amount: float,
        lock_period: int,
        wallet_address: str,
        use_lp_tokens: bool = False,
        lp_wallet_id: int = None,  # Optional, only required if use_lp_tokens=True
        coin_inputs: dict = None  # Optional, only required if minting new LP
    ) -> dict:
        """
        Create a farm in a liquidity pool via GraphQL mutation.

        Args:
            pool_id (int): ID of the liquidity pool to farm in.
            farmed_amount (float): Amount to farm (in LP tokens or coins).
            lock_period (int): Lock period in days for farming.
            wallet_address (str): Address of the wallet associated with the farm.
            use_lp_tokens (bool): Whether to use existing LP tokens (default: False).
            lp_wallet_id (int): Wallet ID holding LP tokens (required if use_lp_tokens=True).
            coin_inputs (dict): Coin deposit details for minting LP tokens.
                Example:
                {
                    "TOKEN_A": {
                    "publicAddress": "0xWalletA",
                    "amount": 60.0
                    },
                    "TOKEN_B": {
                    "publicAddress": "0xWalletB",
                    "amount": 40.0
                    }
                }

        Returns:
            dict: Response from the server. Example:
                {
                    "ok": True,
                    "message": "Farm created successfully.",
                    "governancePower": 123.45,
                    "lpTokensUsed": 100.0,
                    "farmId": "10"
                }
        """

        # Step 1: Build the base input payload
        variables = {
            "input": {
                "poolId": str(pool_id),
                "farmedAmount": float(farmed_amount),
                "lockPeriod": int(lock_period),
                "walletAddress": str(wallet_address),
                "useLpTokens": bool(use_lp_tokens),
            }
        }

        # Step 2: Add lpWalletId if using existing LP tokens
        if use_lp_tokens:
            if lp_wallet_id is None:
                raise ValueError("lp_wallet_id is required when use_lp_tokens=True.")
            variables["input"]["lpWalletId"] = int(lp_wallet_id)

        # Step 3: Add coinInputs if provided (for minting LP tokens)
        if coin_inputs:
            if not isinstance(coin_inputs, dict):
                raise ValueError("coin_inputs must be a dictionary.")
            # Convert the coin_inputs dictionary to a JSON string
            variables["input"]["coinInputs"] = json.dumps(coin_inputs)

        # Step 4: Execute the GraphQL mutation
        try:
            response = self.api_manager._execute_graphql(CREATE_FARM_MUTATION, variables)
        except Exception as e:
            raise RuntimeError(f"Error executing GraphQL operation: {e}")

        # Step 5: Return the server response
        return response


    
    def get_farm_txs_in_pool(self, pool_id, limit=10, offset=0):
        """
        Fetch all transactions for a specific pool.
        """
        variables = {"poolId": pool_id}
        return self.api_manager._execute_graphql(GET_FARM_TXS_IN_POOL_QUERY, variables)
    
    def get_farm_events_in_pool(self, farm_id, limit=10, offset=0):
        """
        Fetch all events for a specific pool.
        """
        variables = {"farmId": farm_id}
        return self.api_manager._execute_graphql(GET_FARM_EVENTS_QUERY, variables)
    
    def add_farm_transaction(self, farm_id, token_amount, wallet_address, lp_wallet_id=None, use_lp_tokens=False, coin_inputs=None):
        variables = {
            "input": {
                "farmId": str(farm_id),
                "tokenAmount": float(token_amount),
                "walletAddress": str(wallet_address),
                "useLpTokens": bool(use_lp_tokens),
            }
        }
        if lp_wallet_id is not None:
            variables["input"]["lpWalletId"] = str(lp_wallet_id)
        if coin_inputs:
            import json
            variables["input"]["coinInputs"] = json.dumps(coin_inputs)

        return self.api_manager._execute_graphql(ADD_FARM_TRANSACTION_MUTATION, variables)



    def claim_farm_rewards(self, farm_id: int)  -> dict:
        """
        Claim farming rewards with dynamic calculations.
        """
        variables = {
            "input": {
                "farmId": farm_id
            }
        }
        return self.api_manager._execute_graphql(CLAIM_FARM_REWARDS_MUTATION, variables)

    def withdraw_farm(self, farm_id, withdraw_amount, force_withdraw=False):
        """
        Withdraw staked tokens and rewards with penalties if applicable.
        """
        variables = {
            "input": {
                "farmId": farm_id,
                "withdrawAmount": withdraw_amount,
                "forceWithdraw": force_withdraw,
            }
        }
        return self.api_manager._execute_graphql(WITHDRAW_FARM_MUTATION, variables)
    
    def get_user_farms(self, user_id):
        """
        Fetch all farms for a specific user.
        """
        variables = {"userId": user_id}
        return self.api_manager._execute_graphql(GET_USER_FARMS_QUERY, variables)
    
    
    
    
    
    
    # Leaderboard Management
    def get_leaderboard(self, coin_id, limit=10):
        """
        Fetch the leaderboard for a specific coin.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit
        }
        return self.api_manager._execute_graphql(GET_LEADERBOARD_QUERY, variables)
    
    
    # Tiered Leaderboard Management
    def get_governance_leaderboard(self, coin_id, limit=10):
        """
        Fetch the governance power leaderboard for a specific coin.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit
        }
        return self.api_manager._execute_graphql(GET_GOVERNANCE_LEADERBOARD_QUERY, variables)

    def get_rewards_leaderboard(self, coin_id, limit=10):
        """
        Fetch the rewards earned leaderboard for a specific coin.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit
        }
        return self.api_manager._execute_graphql(GET_REWARDS_LEADERBOARD_QUERY, variables)

    def get_staked_amount_leaderboard(self, coin_id, limit=10):
        """
        Fetch the staked amount leaderboard for a specific coin.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit
        }
        return self.api_manager._execute_graphql(GET_STAKED_AMOUNT_LEADERBOARD_QUERY, variables)
    

    def get_loyalty_leaderboard(self, coin_id, limit=10):
        """
        Fetch the loyalty leaderboard for a specific coin.
        """
        variables = {
            "coinId": coin_id,
            "limit": limit
        }
        return self.api_manager._execute_graphql(GET_LOYALTY_LEADERBOARD_QUERY, variables)


    # APR Strategy Management
    def update_apr_strategy(self, pool_id, apr_strategy, apr_parameters):
        """
        Update the APR strategy and parameters for a liquidity pool.
        """
        variables = {
            "input": {
                "poolId": pool_id,
                "aprStrategy": apr_strategy,
                "aprParameters": apr_parameters
            }
        }
        response = self.api_manager._execute_graphql(UPDATE_APR_STRATEGY_MUTATION, variables)
        return response
    
    # Analytics Management
    def get_coin_analytics(self, coin_id):
        """
        Fetch analytics for a specific coin.
        """
        variables = {
            "coinId": coin_id
        }
        return self.api_manager._execute_graphql(GET_COIN_ANALYTICS_QUERY, variables)

    

    