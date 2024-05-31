from solders.pubkey import Pubkey # type: ignore


WSOL: Pubkey = Pubkey.from_string("So11111111111111111111111111111111111111112")
ASSOCIATED_TOKEN_PROGRAM_ID: Pubkey = Pubkey.from_string("ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL")

# Data length of a token mint account.
MINT_LEN: int = 82

# Data length of a token account
ACCOUNT_LEN: int = 165

# Data length of a multisig token account
MULTISIG_LEN: int = 355

# New token mint program ID
TOKEN_PROGRAM_ID: Pubkey = Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")

# Associated token Program ID
TOKEN_PROGRAM_ID_2022: Pubkey = Pubkey.from_string("TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb")

# New pool creation Program ID
RAY_V4_AMM_ID: Pubkey = Pubkey.from_string("675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8")

# Owner of RAY_V4
RAY_AUTHORITY_V4: Pubkey = Pubkey.from_string("5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1") #AMM_PROGRAM_ID

OPEN_BOOK_PROGRAM: Pubkey = Pubkey.from_string("srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX") #SERUM_PROGRAM_ID

LAMPORTS_PER_SOL: int = 1000000000
