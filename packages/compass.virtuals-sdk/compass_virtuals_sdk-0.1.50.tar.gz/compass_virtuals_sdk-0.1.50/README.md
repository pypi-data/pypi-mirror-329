Wrappers around [CompassLabs](https://compasslabs.ai)' [API](https://api.compasslabs.ai) to provide support for the GAME SDK.

# Description

Compass Labs runs an API that allows users to interact and transact on DeFi with ease.

This API allows users to intuitively and transparently read information from decentralised exchanges. Users can then use the API to build a transaction, which can be safely and securely signed and submitted by the user once the transaction is fully built by the API. 

This allows users to retain full custody of their funds, and full visibility of where their funds are moved.

## Virtuals GAME SDK

The [GAME Framework](https://whitepaper.virtuals.io/developer-documents/game-framework) is a modular agentic framework that enables an agent to plan actions and make decisions autonomously based on the information provided to it. 

Compass Labs publishes a library containing Python functions which allow clients to easily interact with their API (compass.api_client). This package is a wrapper around that package, presenting the API endpoints as tools for the GAME agents to utilise. This means that any agent can be given the power to transact on-chain - without any difficult prompt engineering or further tools that requires the agent to decipher Solidity, or the mixed technical and financial documentation of decentralised platforms!

# Examples

## Setup

Install this package using your favourite package manager, e.g.
```bash
pip install compass.virtuals_sdk
```

Then create a .env file at the root of whatever project directory you want to use for you virtuals code.

Include the following variables:
```
ETHEREUM_RPC_URL=<JSON RPC NODE URL>
ETHEREUM_PRIVATE_KEY=<PRIVATE KEY>
GAME_API_KEY=<api key>
```

You can get an rpc url from a provider like Anker, or check your Metamask settings to see which node it talks to.

Your private key can be obtained from whatever wallet you use. We encourage you to read the code of this package to see how the private key is handled; it is never sent on the network, and is entirely used locally to sign transactions for the agent. The Game framework never sees the private key, only knows that it can request for a transaction to be signed and sent. Similarly, Compass Labs will never see your private key.

However: by giving the agent the ability to send transactions on your wallet, all your funds in the associated wallet are liable to be lost! The agents you build will have full power to submit any transaction on behalf of that wallet. A well-tuned agent can make money; but a recklessly prompted one (e.g. "send all my tokens to Vitalik"!) would be capable of transferring funds recklessly. Compass Labs accepts no liability for the funds associated with any wallet that an agent is given the key to.

The Game SDK API can be obtained from the [Virtuals Game Console](https://console.game.virtuals.io/projects).

## The Sample Agent

If you want to immediately try out the capabilities offered by this SDK then you can run our simple agent provided in our package.

```bash
python -c 'import compass.virtuals_sdk.simple_agent as s; s.compass_agent.compile(); s.compass_agent.run()'
```

You should see that the agent first figures out its address, then checks all of its capabilities. It will proceed to check some prices, and finally send some transactions! (Tip: You can easily prevent the agent from having access to funds by providing an invalid PRIVATE_KEY in the .env file.)

## Using the API in your own agents

We suggest creating one worker per protocol that our API supports, and then one worker for interacting with your wallet. 

You can do this by importing our classes from `compass.virtuals_sdk.api_wrapper` and `compass.virtuals_sdk.wallet`.

For example, the simple agent code looks like this:
```python
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
```

Note that each of the classes that we provide for suggested WorkerConfig's contains an `id`, `worker_description`, `get_state_fn`, and `action_space`. You can change any of these as you like. The `action_space` is the only really crucial part.

If you would like to pick and choose which tools you use with which agents, then as well as all tools being listed in the respective `action_space`, each tool is set as a method on the helper classes. For example, you can get the game_sdk `Function` instance for checking on-chain balances from `compass.virtuals_sdk.api_wrapper.Others.generic_balance_get`. 

Have fun building with Compass Labs' DeFi API!