"""Simple workers that can be used for experimenting with the Dojo API Virtuals
plugin."""

from game_sdk.game.worker import Worker

from compass.virtuals_sdk.api_wrapper import (
    AaveV3,
    AerodromeBasic,
    AerodromeSlipstream,
    Others,
    UniswapV3,
)
from compass.virtuals_sdk.config import api_key
from compass.virtuals_sdk.shared_defaults import get_state_fn
from compass.virtuals_sdk.wallet import Wallet

others_compass_api_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=Others.worker_description,
    get_state_fn=get_state_fn,
    action_space=Others.action_space,
)
aave_compass_api_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=AaveV3.worker_description,
    get_state_fn=get_state_fn,
    action_space=AaveV3.action_space,
)
aerodrome_basic_compass_api_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=AerodromeBasic.worker_description,
    get_state_fn=get_state_fn,
    action_space=AerodromeBasic.action_space,
)
aerodrome_slipstream_compass_api_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=AerodromeSlipstream.worker_description,
    get_state_fn=get_state_fn,
    action_space=AerodromeSlipstream.action_space,
)
uniswap_compass_api_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=UniswapV3.worker_description,
    get_state_fn=get_state_fn,
    action_space=UniswapV3.action_space,
)
wallet_worker = lambda: Worker(  # noqa: E731
    api_key=api_key,
    description=Wallet.worker_description,
    get_state_fn=get_state_fn,
    action_space=Wallet.action_space,
)


# example usage:
"""
others_compass_api_worker().run(
    "create an unsigned transaction to give an allowance of 100 USDC to the UniswapV3Router contract, sent from address 0x8A2c9eD8F6B9aD09036Cc0F5AAcaE7E6708f3D0c. Use the `set` endpoint, not the `set_any` endpoint."
)
"""
