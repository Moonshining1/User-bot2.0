# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import re

from . import *

STRINGS = {
    1: """🎇 **Thanks for Deploying Kitty Userbot!**

• Here, are the Some Basic stuff from, where you can Know, about its Usage.""",
    2: """🎉** About Kitty**

🧿 Kitty is Pluggable and powerful Telethon Userbot, made in Python from Scratch. It is Aimed to Increase Security along with Addition of Other Useful Features.

❣ Made by **@Kittyxupdates**""",
    3: """**💡• FAQs •**

-> [Username Tracker](https://t.me/Kittyxupdates/31)
-> [Keeping Custom Addons Repo](https://t.me/Kittyxupdates/32)
-> [Disabling Deploy message](https://t.me/Kittyxupdates/33)
-> [Setting up TimeZone](https://t.me/Kittyxupdates/34)
-> [About Inline PmPermit](https://t.me/Kittyxupdates/35)
-> [About Dual Mode](https://t.me/Kittyxupdates/36)
-> [Custom Thumbnail](https://t.me/Kittyxupdates/37)
-> [About FullSudo](https://t.me/Kittyxupdates/38)
-> [Setting Up PmBot](https://t.me/Kittyxupdates/27)
-> [Also Check](https://t.me/Kittyxupdates/39)

**• To Know About Updates**
  - Join @kittyxupdates.""",
    4: f"""• `To Know All Available Commands`

  - `{HNDLR}help`
  - `{HNDLR}cmds`""",
    5: """• **For Any Other Query or Suggestion**
  - Move to **@grandxmasti**.

• Thanks for Reaching till END.""",
}


@callback(re.compile("initft_(\\d+)"))
async def init_depl(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 5:
        return await e.edit(
            STRINGS[5],
            buttons=Button.inline("<< Back", "initbk_4"),
            link_preview=False,
        )

    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )


@callback(re.compile("initbk_(\\d+)"))
async def ineiq(e):
    CURRENT = int(e.data_match.group(1))
    if CURRENT == 1:
        return await e.edit(
            STRINGS[1],
            buttons=Button.inline("Start Back >>", "initft_2"),
            link_preview=False,
        )

    await e.edit(
        STRINGS[CURRENT],
        buttons=[
            Button.inline("<<", f"initbk_{str(CURRENT - 1)}"),
            Button.inline(">>", f"initft_{str(CURRENT + 1)}"),
        ],
        link_preview=False,
    )
