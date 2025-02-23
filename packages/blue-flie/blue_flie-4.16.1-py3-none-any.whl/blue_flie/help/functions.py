from typing import List

from blue_options.terminal import show_usage, xtra
from abcli.help.generic import help_functions as generic_help_functions

from blue_flie import ALIAS
from blue_flie.help.toolbelt import help_functions as help_toolbelt


def help_browse(
    tokens: List[str],
    mono: bool,
) -> str:
    options = "actions|repo"

    return show_usage(
        [
            "@flie",
            "browse",
            f"[{options}]",
        ],
        "browse blue_flie.",
        mono=mono,
    )


help_functions = generic_help_functions(plugin_name=ALIAS)

help_functions.update(
    {
        "browse": help_browse,
        "toolbelt": help_toolbelt,
    }
)
