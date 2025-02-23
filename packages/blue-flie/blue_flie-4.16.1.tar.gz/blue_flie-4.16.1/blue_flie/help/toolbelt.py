from typing import List

from blue_options.terminal import show_usage, xtra


def help_install(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("dryrun", mono=mono)

    return show_usage(
        [
            "toolbelt",
            "install",
            f"[{options}]",
        ],
        "install toolbelt.",
        mono=mono,
    )


help_functions = {
    "install": help_install,
}
