# Coin/graphql_queries.py

CREATE_COIN_MUTATION = """
mutation CreateCoin($input: CreateCoinInput!) {
    createCoin(input: $input) {
        coin {
            id
            name
            symbol
            maxSupply
            totalSupply
            decimals
            governanceModel
            consensusType
            transactionFee
            visibility
            coinMetadata
            treasuryWallet
            treasuryAllocationPercentage
            burnable
            mintable
        }
        ok
        message
    }
}
"""


GET_ALL_COINS_QUERY = """
query GetAllCoins {
    getAllCoins {
        id
        name
        symbol
        maxSupply
        totalSupply
        decimals
        governanceModel
        transactionFee
        visibility
        coinMetadata
        createdTime
        price
        priceChangeUsd
        change24h
        volume1hr
        volume24h
        marketCap
        prices7d
        circulatingSupply
        typicalHoldTime
        volumeMarketCapRatio
        trendingActivity
        popularity
        allTimeHigh
        rank
        orderBook
        candlesticks
        historicalData
    }
}
"""



APPROVE_COIN_MUTATION = """
mutation ApproveCoin($input: ApproveCoinInput!) {
    approveCoin(input: $input) {
        ok
        message
    }
}
"""

PREMINE_ALLOCATION_MUTATION = """
mutation PremineAllocation($input: PremineAllocationInput!) {
    premineAllocation(input: $input) {
        ok
        message
    }
}
"""



GET_AUDIT_LOGS_QUERY = """
query GetAuditLogs($input: AuditLogFilterInput) {
    getAuditLogs(input: $input) {
        id
        action
        details
        timestamp
        initiator
    }
}
"""

GET_PREMINE_REPORT_QUERY = """
query GetPremineReport($input: PremineReportInput!) {
  getPremineReport(input: $input) {
    success
    message
    report {
      walletAddress
      amount
    }
  }
}

"""


GET_COIN_STATISTICS_QUERY = """
query GetCoinStatistics($coinId: ID!) {
    getCoinStatistics(coinId: $coinId) {
        ok
        message
        statistics {
            maxTotalSupply
            holders
            totalTransfers
            marketPrice
            onchainMarketCap
            circulatingSupplyMarketCap
        }
    }
}
"""


CREATE_GOVERNANCE_PROPOSAL_MUTATION = """
mutation CreateGovernanceProposal($input: GovernanceProposalInput!) {
    createGovernanceProposal(input: $input) {
        ok
        message
    }
}
"""

GET_COIN_GOVERNANCE_MODEL_QUERY = """
query GetCoinGovernanceModel($coinId: ID!) {
    getGovernanceModel(coinId: $coinId)
}
"""


VOTE_GOVERNANCE_PROPOSAL_MUTATION = """
mutation VoteGovernanceProposal($input: VoteGovernanceProposalInput!) {
    voteGovernanceProposal(input: $input) {
        ok
        message
    }
}
"""

GET_GOVERNANCE_PROPOSALS_QUERY = """
query GetGovernanceProposals($coinId: ID, $status: String, $limit: Int, $offset: Int) {
    getGovernanceProposals(coinId: $coinId, status: $status, limit: $limit, offset: $offset) {
        id
        coinId
        proposalType
        details
        status
        votesApprove
        votesReject
        createdAt
    }
}
"""

GET_GOVERNANCE_VOTES_QUERY = """
query GetGovernanceVotes($proposalId: ID!, $limit: Int, $offset: Int) {
    getGovernanceVotes(proposalId: $proposalId, limit: $limit, offset: $offset) {
        id
        proposalId
        voter
        vote
        voteWeight
        votedAt
    }
}
"""

GET_GOVERNANCE_PROPOSAL_WITH_VOTES_QUERY = """
query GetGovernanceProposalsWithVotes($coinId: ID, $status: String, $limit: Int, $offset: Int) {
    getGovernanceProposalsWithVotes(coinId: $coinId, status: $status, limit: $limit, offset: $offset) {
        id
        coinId
        proposalType
        details
        status
        votesApprove
        votesReject
        createdAt
        votes {
            id
            proposalId
            voter
            vote
            voteWeight
            votedAt
        }
        electionEndTime
        electionScheduledCloseTime
    }
}
"""

REGISTER_DELEGATE_MUTATION = """
mutation RegisterDelegate($input: RegisterDelegateInput!) {
  registerDelegate(input: $input) {
    ok
    message
    delegate {
      id
      name
      votesReceived
      isActive
      createdAt
    }
  }
}
"""

DELEGATE_VOTE_MUTATION = """
mutation DelegateVote($input: DelegatedVoteInput!) {
  delegateVote(input: $input) {
    ok
    message
  }
}
"""


REVOKE_DELEGATION_MUTATION = """
        mutation RevokeDelegation($input: DelegatedVoteInput!) {
            revokeDelegation(input: $input) {
                ok
                message
            }
        }
        """

GET_ACTIVE_DELEGATES_QUERY = """
query GetActiveDelegates($coinId: ID!, $limit: Int) {
    getActiveDelegates(coinId: $coinId, limit: $limit) {
        ok
        message
        delegates {
            id
            name
            walletAddress
            votesReceived
            isActive
            createdAt
        }
    }
}
"""


GET_ALL_DELEGATES_QUERY = """
query GetAllDelegates($coinId: Int!, $status: String, $limit: Int, $offset: Int) {
    getAllDelegates(coinId: $coinId, status: $status, limit: $limit, offset: $offset) {
        ok
        message
        delegates {
            id
            name
            walletAddress
            votesReceived
            isActive
            createdAt
        }
    }
}

"""

GET_ELECTION_RESULTS_QUERY = """
query GetElectionResults($coinId: ID!) {
  getElectionResults(coinId: $coinId) {
    coinId
    coinName
    totalDelegates
    activeDelegateCount
    totalVotes
    quorum
    electionEndTime
    electionScheduledCloseTime
    electionMethodology
    elections {
      electionId
      startTime
      scheduledCloseTime
      endTime
      status
      proposals {
        proposalId
        proposalType
        status
        votesApprove
        votesReject
        createdAt
      }
    }
    delegates {
      delegateId
      name
      walletAddress
      votesReceived
      isActive
    }
  }
}
"""

REPORT_DELEGATE_MISCONDUCT_MUTATION = """
mutation ReportDelegateMisconduct($input: ReportDelegateMisconductInput!) {
    reportDelegateMisconduct(input: $input) {
        ok
        message
    }
}
"""

GET_DELEGATE_MISCONDUCT_REPORTS_QUERY = """
query GetDelegateMisconductReports(
    $delegateId: Int,
    $walletId: Int,
    $status: String,
    $startDate: DateTime,
    $endDate: DateTime
) {
    getDelegateMisconductReports(
        delegateId: $delegateId,
        walletId: $walletId,
        status: $status,
        startDate: $startDate,
        endDate: $endDate
    ) {
        id
        delegateId
        walletId
        reason
        evidence
        status
        createdAt
    }
}

"""

SWITCH_GOVERNANCE_MODEL_MUTATION = """
mutation SwitchGovernanceModel($coinId: ID!, $newModel: GovernanceModelEnum!) {
    switchGovernanceModel(input: {coinId: $coinId, newModel: $newModel}) {
        ok
        message
    }
}
"""



CREATE_AIRDROP_MUTATION = """
mutation CreateAirdrop($input: CreateAirdropInput!) {
    createAirdrop(input: $input) {
        ok
        message
        airdrop {
            id
            coinId
            description
            criteria
            totalTokens
            tokensDistributed
            status
            createdAt
        }
    }
}
"""

CLAIM_AIRDROP_MUTATION = """
mutation ClaimAirdrop($input: ClaimAirdropInput!) {
    claimAirdrop(input: $input) {
        ok
        message
        tokensClaimed
    }
}
"""


GET_ALL_AIRDROPS_QUERY = """
query GetAirdrops($coinId: ID!) {
    getAirdrops(coinId: $coinId) {
        id
        coinId
        description
        criteria
        totalTokens
        tokensDistributed
        status
        createdAt
    }
}
"""


# Staking
STAKE_TOKENS_MUTATION = """
mutation StakeTokens($input: StakeInput!) {
    stakeTokens(input: $input) {
        ok
        message
    }
}
"""

WITHDRAW_STAKE_MUTATION = """
mutation WithdrawStake($input: WithdrawStakeInput!) {
    withdrawStake(input: $input) {
        ok
        message
        stakedAmount
        rewardsEarned
    }
}
"""

GET_STAKES_QUERY = """
query GetStakes($walletAddress: String!, $coinId: ID!) {
    getStakes(walletAddress: $walletAddress, coinId: $coinId) {
        id
        stakedAmount
        rewardRate
        lockPeriod
        stakedAt
        unlockAt
        rewardsEarned
        status
    }
}
"""



CREATE_LIQUIDITY_POOL_MUTATION = """
mutation CreateLiquidityPool($input: CreateLiquidityPoolInput!) {
    createLiquidityPool(input: $input) {
        ok
        message
        poolId
    }
}
"""


GET_LIQUIDITY_POOLS_QUERY = """
query GetLiquidityPools($filters: LiquidityPoolFilterInput) {
    getLiquidityPools(filters: $filters) {
        totalCount
        pools {
            id
            tokens
            tokenPair
            totalLiquidity
            totalLiquidityTokens
            volume24h
            averageDeposit
            rewardTokens
            currentApr
            aprStrategy
            aprImpact
            dynamicApr
            aprParameters
            penaltyRate
            lastActivityAt
            totalDeposits
            totalWithdrawals
            createdAt
            description
            updatedAt
            deposits {
                id
                poolId
                walletId
                eventType
                tokenAAmount
                tokenBAmount
                tokenAmount
                timestamp
                txId
            }
            withdrawals {
                id
                poolId
                walletId
                eventType
                tokenAAmount
                tokenBAmount
                tokenAmount
                timestamp
                txId
            }
        }
    }
}


"""

ADD_LIQUIDITY_MUTATION = """
mutation AddLiquidity($input: AddLiquidityInput!) {
    addLiquidity(input: $input) {
        ok
        message
        lpTokensIssued
    }
}
"""

GET_TRANSACTIONS_IN_POOL_QUERY = """
query GetTransactionsInPool($poolId: Int!, $limit: Int, $offset: Int) {
  getTransactionsInPool(poolId: $poolId, limit: $limit, offset: $offset) {
    totalCount
    transactions {
      id
      poolId
      walletId
      eventType
      tokenAAmount
      tokenBAmount
      tokenAmount
      timestamp
      txId
    }
    ok
    message
  }
}
"""

REMOVE_TRANSACTION_LIQUIDITY_MUTATION = """
mutation RemoveLiquidity($input: RemoveTransactionLiquidityInput!) {
  removeLiquidity(input: $input) {
    ok
    message
  }
}
"""



# REMOVE_LIQUIDITY_MUTATION = """
# mutation RemoveLiquidity($input: RemoveLiquidityInput!) {
#     removeLiquidity(input: $input) {
#         ok
#         message
#         redeemedTokens
#     }
# }
# """



# Farming Queries and Mutations
CREATE_FARM_MUTATION = """
mutation CreateFarm($input: CreateFarmInput!) {
    createFarm(input: $input) {
        ok
        message
        governancePower
        lpTokensUsed
        farmId
    }
}
"""

GET_FARM_TXS_IN_POOL_QUERY = """
query GetFarmTx($poolId: Int!, $limit: Int, $offset: Int) {
  getFarmTransactions(poolId: $poolId, limit: $limit, offset: $offset) {
    totalCount
    ok
    message
    transactions {
      id
      eventType
      tokenAmount
      governancePower
      txId
      timestamp
    }
  }
}

"""


GET_FARM_EVENTS_QUERY = """
query FetchFarmEvents($farmId: Int!, $limit: Int, $offset: Int) {
  getFarmEvents(farmId: $farmId, limit: $limit, offset: $offset) {
    totalCount
    ok
    message
    events {
      id
      eventType
      tokenAmount
      rewardsClaimed
      timestamp
    }
  }
}

"""

ADD_FARM_TRANSACTION_MUTATION = """
mutation addTransactionFarm($input: AddFarmTransactionInput!) {
    addTransactionFarm(input: $input) {
        ok
        message
        farmId
        eventId
    }
}
"""

CLAIM_FARM_REWARDS_MUTATION = """
mutation ClaimFarmRewards($input: ClaimFarmRewardsInput!) {
    claimFarmRewards(input: $input) {
        ok
        message
        rewardsClaimed
    }
}
"""

WITHDRAW_FARM_MUTATION = """
mutation WithdrawFarm($input: WithdrawFarmInput!) {
    withdrawFarm(input: $input) {
        ok
        message
        stakedAmount
        rewardsEarned
    }
}
"""

GET_USER_FARMS_QUERY = """
query GetUserFarms($userId: ID!) {
    getUserFarms(userId: $userId) {
        id
        userId
        poolId
        stakedTokens
        rewardsEarned
        boosters
        stakedAt
        lastRewardClaim
        lockPeriod
        unlockAt
        penaltyApplied
        status
        governancePower
    }
}
"""

# CLAIM_FARM_REWARDS_MUTATION = """
# mutation ClaimFarmRewards($input: ClaimFarmRewardsInput!) {
#     claimFarmRewards(input: $input) {
#         ok
#         message
#         rewardsClaimed
#     }
# }
# """




GET_LEADERBOARD_QUERY = """
query GetLeaderboard($coinId: ID!, $limit: Int!) {
    getLeaderboard(coinId: $coinId, limit: $limit) {
        userId
        walletAddress
        stakedAmount
        rewardsEarned
        governancePower
    }
}
"""







GET_GOVERNANCE_LEADERBOARD_QUERY = """
query GetGovernanceLeaderboard($coinId: ID!, $limit: Int!) {
    getGovernanceLeaderboard(coinId: $coinId, limit: $limit) {
        userId
        walletAddress
        stakedAmount
        rewardsEarned
        governancePower
        loyaltyScore
    }
}
"""

GET_REWARDS_LEADERBOARD_QUERY = """
query GetRewardsLeaderboard($coinId: ID!, $limit: Int!) {
    getRewardsLeaderboard(coinId: $coinId, limit: $limit) {
        userId
        walletAddress
        stakedAmount
        rewardsEarned
        governancePower
        loyaltyScore
    }
}
"""

GET_STAKED_AMOUNT_LEADERBOARD_QUERY = """
query GetStakedAmountLeaderboard($coinId: ID!, $limit: Int!) {
    getStakedAmountLeaderboard(coinId: $coinId, limit: $limit) {
        userId
        walletAddress
        stakedAmount
        rewardsEarned
        governancePower
        loyaltyScore
    }
}
"""

GET_LOYALTY_LEADERBOARD_QUERY = """
query GetLoyaltyLeaderboard($coinId: ID!, $limit: Int!) {
    getLoyaltyLeaderboard(coinId: $coinId, limit: $limit) {
        userId
        walletAddress
        stakedAmount
        rewardsEarned
        governancePower
        loyaltyScore
    }
}
"""


UPDATE_APR_STRATEGY_MUTATION = """
mutation UpdateAprStrategy($input: UpdateAprStrategyInput!) {
    updateAprStrategy(input: $input) {
        ok
        message
        pool {
            id
            currentApr
            aprStrategy
            aprParameters
        }
    }
}
"""

# Analytics Query
GET_COIN_ANALYTICS_QUERY = """
query GetCoinAnalytics($coinId: ID!) {
    getCoinAnalytics(coinId: $coinId) {
        ok
        message
        statistics {
            totalStaked
            totalRewardsDistributed
            activeFarms
            activeStakes
            userParticipation
            governanceProposals
        }
    }
}
"""