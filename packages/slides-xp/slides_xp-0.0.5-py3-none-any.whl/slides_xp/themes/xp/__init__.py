"""
slides_xp / Windows XP theme.
"""

import random
import pyhtml as p


def make_intro_slide(
    author: str,
    title: str,
    copyright: str,
) -> p.div:
    return p.div(class_="bootloader")(
        p.span(class_="bootloader-title")(
            p.h2(author),
            p.sup("®"),
            p.img(class_="windows-logo")(
                alt="Windows XP logo", src="/theme/xp.png"
            ),
            p.sub("TM"),
        ),
        p.span(class_="bootloader-subtitle")(
            p.h1(f"{title}", p.sup(p.small("®"))),
            p.h1(class_="xp")("xp"),
        ),
        p.div(class_="boot-animation")(
            [p.div()] * 3,
        ),
        p.div(class_="gap"),
        p.div(class_="copyright")(f"Copyright © {copyright}"),
    )


def make_bsod_slide(
    slide_type: str,
    instructions: str,
) -> p.div:
    exc_addr = f"{random.randint(0x0000_0000, 0xFFFF_FFFF):08X}"
    vxd_id = f"{random.randint(1, 0xFF):02X}"
    vxd_addr = f"{random.randint(0x1000, 0xFFFF):04X}"
    return p.div(class_="bsod")(
        p.div(class_="bsod-title")("SLIDES XP"),
        p.pre(
            f"A fatal exception has occurred at 00:{exc_addr} in VXD "
            f"sdxp9x({vxd_id}) + 0000{vxd_addr}, The {slide_type} will be "
            "terminated."
        ),
        p.pre(instructions),
        p.span(
            p.pre("Press any key to continue"),
            p.pre(class_="caret")("_"),
        ),
    )
