import argparse
from typing import (
    Callable,
    NamedTuple,
    Type,
    TypeVar,
)

BaseArgs = NamedTuple


T = TypeVar("T", bound=BaseArgs)


def make_cli_arg_parser(
    *,
    name: str,
    desc: str,
    args_shape: Type[T],
) -> Callable[[], T]:
    type_map = args_shape.__annotations__
    defaults = args_shape._field_defaults

    parser = argparse.ArgumentParser(
        prog=name,
        description=desc,
    )
    for name, dtype in type_map.items():
        cli_argname = name.replace("_", "-")
        kwargs = {
            "dest": name,
            "required": name not in defaults,
            "type": dtype,
        }
        if name in defaults:
            kwargs["default"] = defaults[name]
        parser.add_argument(f"--{cli_argname}", **kwargs)

    def parse_args() -> T:
        args = parser.parse_args()
        return args_shape(**{k: v for k, v in vars(args).items() if v})  # type: ignore

    return parse_args
