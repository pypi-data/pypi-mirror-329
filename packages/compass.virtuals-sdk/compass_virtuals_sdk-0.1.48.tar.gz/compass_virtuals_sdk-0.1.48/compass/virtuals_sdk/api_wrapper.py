"""This module dynamically loads the CompassLabs API client and sets up classes to
export.

These classes contain static values that can be used for constructing 'Worker's/'WorkerConfig's:
- worker_description
- id
- action_space
- get_state_fn
"""

import inspect
import os
from ast import literal_eval
from typing import Any, Callable

import dotenv
from game_sdk.game.custom_types import (
    Argument,
    Function,
    FunctionResultStatus,
)
from pydantic import BaseModel

from compass.api_client import *
from compass.virtuals_sdk.shared_defaults import get_state_fn

dotenv.load_dotenv()
api_key = os.getenv("GAME_API_KEY", "")

aave_api = AaveV3Api()
aerodrome_api = AerodromeApi()
others_api = OthersApi()
uniswap_api = UniswapV3Api()


def wrap_api_function(api: Any, f: Callable) -> Function:
    s = inspect.signature(f)
    p = s.parameters
    excluded_args = [
        "self",
        "_request_timeout",
        "_request_auth",
        "_content_type",
        "_headers",
        "_host_index",
    ]

    def make_arg(name: str, type_: type) -> Argument:
        if issubclass(type_.annotation, BaseModel):
            arg = Argument(
                name=name,
                description=f"A pydantic model (can also be passed as a dictionary) which has the schema {type_._annotation.model_json_schema()}",
                type=str(type_.annotation),
            )
        else:
            arg = Argument(
                name=name, description=str(type_), type=str(type_.annotation)
            )
        return arg

    args_ = [
        make_arg(name, type_)
        for (name, type_) in p.items()
        if not (name in excluded_args)
    ]
    fn_name = f.__name__.removeprefix("process_request_v0_").removesuffix("_post")

    def f_wrapper(*args, **kwargs):

        def try_eval(v):
            try:
                return literal_eval(v)
            except Exception as _:  # noqa F841
                return v

        kwargs = {name: try_eval(v) for name, v in kwargs.items()}
        try:
            result = f(*args, **kwargs)
            result = result.model_dump()
            result.update({"fn_name": fn_name})
            return FunctionResultStatus.DONE, str(result), result
        except Exception as e:
            print(f"Failure calling function; {f.__name__} {args=} {kwargs=} {e=}")
            return FunctionResultStatus.FAILED, str(e), {}

    fn = Function(
        fn_name=fn_name, fn_description=f.__doc__, args=args_, executable=f_wrapper
    )
    return fn


def get_endpoint_functions_for_api(api: Any) -> list[Callable]:
    """Inspect [api] to get all the endpoint functions in it, returned as a list."""
    ret = []
    # all our endpoint functions start with "process_request"
    fs = [f for f in dir(api) if f.startswith("process_request_")]
    # all endpoint functions are duplicated twice; let's remove those versions
    fs = [
        f
        for f in fs
        if not f.endswith("with_http_info")
        and not f.endswith("without_preload_content")
    ]
    for f in fs:
        ret.append(getattr(api, f))
    return ret


def get_game_functions_for_api(api: Any) -> list[Function]:
    return [wrap_api_function(api, f) for f in get_endpoint_functions_for_api(api)]


def attach_fs(cls: Any, api: Any) -> None:
    functions = get_game_functions_for_api(api)
    cls.action_space = functions
    for f in functions:
        setattr(cls, f.fn_name, f)


class Aerodrome:
    worker_description = "aerodrome worker"
    id = worker_description
    get_state_fn = get_state_fn


attach_fs(Aerodrome, aerodrome_api)


class AaveV3:
    worker_description = "aave v3 worker"
    id = worker_description
    get_state_fn = get_state_fn


attach_fs(AaveV3, aave_api)


class Others:
    worker_description = "generic web3 worker"
    id = worker_description
    get_state_fn = get_state_fn


attach_fs(Others, others_api)


class UniswapV3:
    worker_description = "uniswap v3 worker"
    id = worker_description
    get_state_fn = get_state_fn


attach_fs(UniswapV3, uniswap_api)

# example usage:
# Others.generic_ens_get.executable(Chain.ETHEREUM_COLON_MAINNET, RequestEnsDetails(ens_name="vitalik.eth"))
