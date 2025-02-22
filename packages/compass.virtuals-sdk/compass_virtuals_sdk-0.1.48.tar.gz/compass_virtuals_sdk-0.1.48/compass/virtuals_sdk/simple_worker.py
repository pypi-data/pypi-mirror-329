"""Simple workers that can be used for experimenting with the Dojo API Virtuals
plugin."""

from game_sdk.game.worker import Worker

from compass.virtuals_sdk.api_wrapper import AaveV3, Aerodrome, Others, UniswapV3
from compass.virtuals_sdk.config import api_key
from compass.virtuals_sdk.shared_defaults import get_state_fn
from compass.virtuals_sdk.wallet import Wallet

others_compass_api_worker = Worker(
    api_key=api_key,
    description=Others.worker_description,
    get_state_fn=get_state_fn,
    action_space=Others.action_space,
)
aave_compass_api_worker = Worker(
    api_key=api_key,
    description=AaveV3.worker_description,
    get_state_fn=get_state_fn,
    action_space=AaveV3.action_space,
)
aerodrome_compass_api_worker = Worker(
    api_key=api_key,
    description=Aerodrome.worker_description,
    get_state_fn=get_state_fn,
    action_space=Aerodrome.action_space,
)
uniswap_compass_api_worker = Worker(
    api_key=api_key,
    description=UniswapV3.worker_description,
    get_state_fn=get_state_fn,
    action_space=UniswapV3.action_space,
)
wallet_worker = Worker(
    api_key=api_key,
    description=Wallet.worker_description,
    get_state_fn=get_state_fn,
    action_space=Wallet.action_space,
)


# example usage:
# others_compass_api_worker.run("get the details of the ENS name vitalik.eth")
