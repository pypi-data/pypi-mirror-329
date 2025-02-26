# Mutation for creating a wallet
CREATE_WALLET_MUTATION = """
mutation CreateWallet($input: CreateWalletInput!) {
    createWallet(input: $input) {
        success
        message
        wallet {
            coinId
            balance
            symbol
            publicAddress

        }
    }
}
"""

# Mutation for creating multiple wallets
CREATE_MULTIPLE_WALLETS_MUTATION = """
mutation CreateMultipleWallets($input: CreateMultipleWalletsInput!) {
    createMultipleWallets(input: $input) {
        success
        message
        wallets {
            coinId
            balance
            symbol
            publicAddress
            label
        }
        details
    }
}
"""


GET_ALL_WALLETS_QUERY = """
query GetAllWallets {
    getAllWallets {
        success
        message
        wallets {
            coinId
            balance
            symbol
            publicAddress
            label
            owner
        }
    }
}
"""


DELETE_WALLET_MUTATION = """
mutation DeleteWallet($input: DeleteWalletInput!) {
    deleteWallet(input: $input) {
        success
        message
    }
}
"""

DELETE_WALLETS_MUTATION = """
mutation DeleteWallets($input: DeleteWalletsInput!) {
    deleteWallets(input: $input) {
        success
        message
        deletedWallets
        notFoundWallets
    }
}
"""



CHECK_WALLET_BALANCE_QUERY = """
query CheckWalletBalance($publicAddress: String!) {
    checkWalletBalance(publicAddress: $publicAddress) {
        success
        message
        publicAddress
        rawBalance
        scaledBalance
        symbol
        label
     
    }
}
"""

GET_TRANSACTION_DETAILS_QUERY = """
query GetTransactionDetails($transactionId: String!) {
    getTransactionDetails(transactionId: $transactionId) {
        transactionId
        blockId
        isCoinbase
        fee
        coinId
        status
    }
}
"""
