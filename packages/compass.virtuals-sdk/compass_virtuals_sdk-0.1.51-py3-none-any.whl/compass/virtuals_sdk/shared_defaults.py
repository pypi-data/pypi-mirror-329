"""Shared default functions for the plugin."""

from game_sdk.game.custom_types import FunctionResult


def get_state_fn(function_result: FunctionResult, current_state: dict) -> dict:
    if not current_state:
        return {}

    match function_result:
        case FunctionResult(info={"fn_name": fn_name, **kwargs}):
            current_state.update({fn_name: kwargs})

    return current_state
