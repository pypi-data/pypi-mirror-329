"""Configuration values."""

import os

import dotenv

dotenv.load_dotenv()
api_key = os.getenv("GAME_API_KEY", "")
ethereum_rpc_url = os.getenv("ETHEREUM_RPC_URL", "")
ethereum_private_key = os.getenv("ETHEREUM_PRIVATE_KEY", "")

assert api_key, "You must set a GAME_API_KEY env var!"
assert ethereum_rpc_url, "You must set a ETHEREUM_RPC_URL env var!"
assert ethereum_private_key, "You must set a ETHEREUM_PRIVATE_KEY env var!"
