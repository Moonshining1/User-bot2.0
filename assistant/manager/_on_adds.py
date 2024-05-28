# Moonshining1 - UserBot
# Copyright (C) 2021-2023 User-bot2.0
#
# This file is a part of < https://github.com/Moonshining1/User-bot2.0/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/Moonshining1/User-bot2.0/blob/main/LICENSE/>.

from telethon import events

from . import *


@asst.on(events.ChatAction(func=lambda x: x.user_added))
async def dueha(e):
    user = await e.get_user()
    if not user.is_self:
        return
    sm = udB.get_key("ON_MNGR_ADD")
    if sm == "OFF":
        return
    if not sm:
        sm = "Thanks for Adding me :)"
    await e.reply(sm, link_preview=False)
