"""A simple agent using our suggested 'WorkerConfig's.

This agent can perform some interesting actions if you fund its account. The more
plugins you integrate the more interesting the actions of an agent built on CompassLabs'
API could be.
"""

from game_sdk.game.agent import Agent, WorkerConfig

from compass.api_client import Chain
from compass.virtuals_sdk.api_wrapper import (
    AaveV3,
    Aerodrome,
    Others,
    UniswapV3,
)
from compass.virtuals_sdk.config import api_key
from compass.virtuals_sdk.shared_defaults import get_state_fn
from compass.virtuals_sdk.wallet import Wallet

available_chains = [i.value for i in Chain]
worker_instruction = "Interact with your assigned defi protocol."

compass_agent = Agent(
    api_key=api_key,
    name="A defi agent that can operate on multiple defi exchanges",
    agent_goal=f"Make some money. Your ethereum wallet address is can be obtained via the wallet worker.When you need to set the sender or user of a transaction request, set if to to your wallet address. When you must choose between chains, choose one of {available_chains}",
    agent_description="defi agent",
    get_agent_state_fn=get_state_fn,
    workers=[
        WorkerConfig(cls.id, cls.worker_description, cls.get_state_fn, cls.action_space)
        for cls in [Wallet, Aerodrome, AaveV3, Others, UniswapV3]
    ],
)

if __name__ == "__main__":
    compass_agent.compile()
    compass_agent.run()
