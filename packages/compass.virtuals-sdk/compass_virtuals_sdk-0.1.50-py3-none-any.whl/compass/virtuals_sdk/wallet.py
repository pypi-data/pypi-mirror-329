"""The [Wallet] class contains a suggested WorkerConfig for a worker that can know its
own public address, and send signed transactions.

This is a minimal implementation needed to use the CompassLabs API. The API should
handle the work of assembling complex transations, fetching complicated data, et cetera.
"""

from ast import literal_eval

import dotenv
import web3
from typing import Callable, TypedDict
from eth_account import Account
from eth_account.signers.local import LocalAccount
from game_sdk.game.custom_types import (
    Argument,
    Function,
    FunctionResultStatus,
)
from web3.middleware import SignAndSendRawMiddlewareBuilder

from compass.virtuals_sdk.config import ethereum_private_key, ethereum_rpc_url
from compass.virtuals_sdk.shared_defaults import get_state_fn

dotenv.load_dotenv()


class FunctionResult[T](TypedDict):
    fn_name: str
    result: T


class Wallet:
    worker_description = "wallet manager and unsigned transaction sender"
    id = worker_description
    get_state_fn = get_state_fn

    w3 = web3.Web3(web3.Web3.HTTPProvider(ethereum_rpc_url))
    account: LocalAccount = Account.from_key(private_key=ethereum_private_key)
    w3.middleware_onion.inject(SignAndSendRawMiddlewareBuilder.build(account), layer=0)

    @staticmethod
    def wrap_result[
        P, R
    ](fn_name: str, f: Callable[P, R]) -> Callable[
        P, tuple[FunctionResultStatus, str, FunctionResult[R]]
    ]:
        def aux(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                result = {"fn_name": fn_name, "result": result}
                return FunctionResultStatus.DONE, str(result), result
            except Exception as e:
                import traceback

                print(traceback.format_exc())
                return FunctionResultStatus.FAILED, str(e), {}

        return aux

    @staticmethod
    def _send_transaction(unsigned_transaction: str) -> None:
        try:
            unsigned_transaction = literal_eval(unsigned_transaction)
        except Exception as _:  # noqa F841
            pass
        return Wallet.w3.eth.send_transaction(unsigned_transaction)

    send_transaction = Function(
        fn_name="send_transaction",
        fn_description="send transaction",
        args=[
            Argument(
                name="unsigned_transaction",
                description="a transaction",
                type="transaction dictionary",
            )
        ],
        executable=wrap_result("send_transaction", _send_transaction),
    )

    get_address = Function(
        fn_name="get address",
        fn_description="get wallet address",
        args=[],
        executable=wrap_result("get_address", lambda: Wallet.account.address),
    )

    action_space = [send_transaction, get_address]
