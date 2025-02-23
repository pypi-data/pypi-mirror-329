from typing import List

from abcli.host import signature as abcli_signature
from blue_sbc import fullname as blue_sbc_fullname

from blue_flie import fullname


def signature() -> List[str]:
    return [
        fullname(),
        blue_sbc_fullname(),
    ] + abcli_signature()
