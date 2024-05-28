# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

import ast
import asyncio
import re
import sys
import time
from asyncio.exceptions import TimeoutError as AsyncTimeOut
from os import execl, remove
from random import choice

from bs4 import BeautifulSoup as bs

try:
    from pyUltroid.fns.gDrive import GDriveManager
except ImportError:
    GDriveManager = None
from telegraph import upload_file as upl
from telethon import Button, events
from telethon.tl.types import MessageMediaWebPage
from telethon.utils import get_peer_id

from pyUltroid.fns.helper import fast_download, progress
from pyUltroid.fns.tools import Carbon, async_searcher, get_paste, telegraph_client
from pyUltroid.startup.loader import Loader

from . import *

# --------------------------------------------------------------------#
telegraph = telegraph_client()
GDrive = GDriveManager() if GDriveManager else None
# --------------------------------------------------------------------#


def text_to_url(event):
    """function to get media url (with|without) Webpage"""
    if isinstance(event.media, MessageMediaWebPage):
        webpage = event.media.webpage
        if not isinstance(webpage, types.WebPageEmpty) and webpage.type in ["photo"]:
            return webpage.display_url
    return event.text


# --------------------------------------------------------------------#

_buttons = {
    "otvars": {
        "text": "Other Variables to set for @Kittyxupdates:",
        "buttons": [
            [
                Button.inline("Tᴀɢ Lᴏɢɢᴇʀ", data="taglog"),
                Button.inline("SᴜᴘᴇʀFʙᴀɴ", data="cbs_sfban"),
            ],
            [
                Button.inline("Sᴜᴅᴏ Mᴏᴅᴇ", data="sudo"),
                Button.inline("Hᴀɴᴅʟᴇʀ", data="hhndlr"),
            ],
            [
                Button.inline("Exᴛʀᴀ Pʟᴜɢɪɴs", data="plg"),
                Button.inline("Aᴅᴅᴏɴs", data="eaddon"),
            ],
            [
                Button.inline("Eᴍᴏᴊɪ ɪɴ Hᴇʟᴘ", data="emoj"),
                Button.inline("Sᴇᴛ ɢDʀɪᴠᴇ", data="gdrive"),
            ],
            [
                Button.inline("Iɴʟɪɴᴇ Pɪᴄ", data="inli_pic"),
                Button.inline("Sᴜᴅᴏ HNDLR", data="shndlr"),
            ],
            [Button.inline("Dᴜᴀʟ Mᴏᴅᴇ", "cbs_oofdm")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    },
    "sfban": {
        "text": "SuperFban Settings:",
        "buttons": [
            [Button.inline("FBᴀɴ Gʀᴏᴜᴘ", data="sfgrp")],
            [Button.inline("Exᴄʟᴜᴅᴇ Fᴇᴅs", data="abs_sfexf")],
            [Button.inline("« Bᴀᴄᴋ", data="cbs_otvars")],
        ],
    },
    "apauto": {
        "text": "This'll auto approve on outgoing messages",
        "buttons": [
            [Button.inline("Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ ON", data="apon")],
            [Button.inline("Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ OFF", data="apof")],
            [Button.inline("« Bᴀᴄᴋ", data="cbs_pmcstm")],
        ],
    },
    "alvcstm": {
        "text": f"Customise your {HNDLR}alive. Choose from the below options -",
        "buttons": [
            [Button.inline("Aʟɪᴠᴇ Tᴇxᴛ", data="abs_alvtx")],
            [Button.inline("Aʟɪᴠᴇ ᴍᴇᴅɪᴀ", data="alvmed")],
            [Button.inline("Dᴇʟᴇᴛᴇ Aʟɪᴠᴇ Mᴇᴅɪᴀ", data="delmed")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    },
    "pmcstm": {
        "text": "Customise your PMPERMIT Settings -",
        "buttons": [
            [
                Button.inline("Pᴍ Tᴇxᴛ", data="pmtxt"),
                Button.inline("Pᴍ Mᴇᴅɪᴀ", data="pmmed"),
            ],
            [
                Button.inline("Aᴜᴛᴏ Aᴘᴘʀᴏᴠᴇ", data="cbs_apauto"),
                Button.inline("PMLOGGER", data="pml"),
            ],
            [
                Button.inline("Sᴇᴛ Wᴀʀɴs", data="swarn"),
                Button.inline("Dᴇʟᴇᴛᴇ Pᴍ Mᴇᴅɪᴀ", data="delpmmed"),
            ],
            [Button.inline("PMPermit Type", data="cbs_pmtype")],
            [Button.inline("« Bᴀᴄᴋ", data="cbs_ppmset")],
        ],
    },
    "pmtype": {
        "text": "Select the type of PMPermit needed.",
        "buttons": [
            [Button.inline("Inline", data="inpm_in")],
            [Button.inline("Normal", data="inpm_no")],
            [Button.inline("« Bᴀᴄᴋ", data="cbs_pmcstm")],
        ],
    },
    "ppmset": {
        "text": "PMPermit Settings:",
        "buttons": [
            [Button.inline("Tᴜʀɴ PMPᴇʀᴍɪᴛ Oɴ", data="pmon")],
            [Button.inline("Tᴜʀɴ PMPᴇʀᴍɪᴛ Oғғ", data="pmoff")],
            [Button.inline("Cᴜsᴛᴏᴍɪᴢᴇ PMPᴇʀᴍɪᴛ", data="cbs_pmcstm")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    },
    "chatbot": {
        "text": "From This Feature U can chat with ppls Via ur Assistant Bot.\n[More info](https://t.me/Kittyxupdates/27)",
        "buttons": [
            [
                Button.inline("Cʜᴀᴛ Bᴏᴛ  Oɴ", data="onchbot"),
                Button.inline("Cʜᴀᴛ Bᴏᴛ  Oғғ", data="ofchbot"),
            ],
            [
                Button.inline("Bᴏᴛ Wᴇʟᴄᴏᴍᴇ", data="bwel"),
                Button.inline("Bᴏᴛ Wᴇʟᴄᴏᴍᴇ Mᴇᴅɪᴀ", data="botmew"),
            ],
            [Button.inline("Bᴏᴛ Iɴғᴏ Tᴇxᴛ", data="botinfe")],
            [Button.inline("Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇ", data="pmfs")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    },
    "vcb": {
        "text": "From This Feature U can play songs in group voice chat\n\n[moreinfo](https://t.me/Kittyxupdates/27)",
        "buttons": [
            [Button.inline("VC Sᴇssɪᴏɴ", data="abs_vcs")],
            [Button.inline("« Bᴀᴄᴋ", data="setter")],
        ],
    },
    "oofdm": {
        "text": "About [Dual Mode](https://t.me/Kittyxupdates/28)",
        "buttons": [
            [
                Button.inline("Dᴜᴀʟ Mᴏᴅᴇ Oɴ", "dmof"),
                Button.inline("Dᴜᴀʟ Mᴏᴅᴇ Oғғ", "dmof"),
            ],
            [Button.inline("Dᴜᴀʟ Mᴏᴅᴇ Hɴᴅʟʀ", "dmhn")],
            [Button.inline("« Back", data="cbs_otvars")],
        ],
    },
    "apiset": {
        "text": get_string("ast_1"),
        "buttons": [
            [Button.inline("Remove.bg API", data="abs_rmbg")],
            [Button.inline("DEEP API", data="abs_dapi")],
            [Button.inline("OCR API", data="abs_oapi")],
            [Button.inline("« Back", data="setter")],
        ],
    },
}

_convo = {
    "rmbg": {
        "var": "RMBG_API",
        "name": "Remove.bg API Key",
        "text": get_string("ast_2"),
        "back": "cbs_apiset",
    },
    "dapi": {
        "var": "DEEP_AI",
        "name": "Deep AI Api Key",
        "text": "Get Your Deep Api from deepai.org and send here.",
        "back": "cbs_apiset",
    },
    "oapi": {
        "var": "OCR_API",
        "name": "Ocr Api Key",
        "text": "Get Your OCR api from ocr.space and send that Here.",
        "back": "cbs_apiset",
    },
    "pmlgg": {
        "var": "PMLOGGROUP",
        "name": "Pm Log Group",
        "text": "Send chat id of chat which you want to save as Pm log Group.",
        "back": "pml",
    },
    "vcs": {
        "var": "VC_SESSION",
        "name": "Vc Session",
        "text": "**Vc session**\nEnter the New session u generated for vc bot.\n\nUse /cancel to terminate the operation.",
        "back": "cbs_vcb",
    },
    "settag": {
        "var": "TAG_LOG",
        "name": "Tag Log Group",
        "text": f"Make a group, add your assistant and make it admin.\nGet the `{HNDLR}id` of that group and send it here for tag logs.\n\nUse /cancel to cancel.",
        "back": "taglog",
    },
    "alvtx": {
        "var": "ALIVE_TEXT",
        "name": "Alive Text",
        "text": "**Alive Text**\nEnter the new alive text.\n\nUse /cancel to terminate the operation.",
        "back": "cbs_alvcstm",
    },
    "sfexf": {
        "var": "EXCLUDE_FED",
        "name": "Excluded Fed",
        "text": "Send the Fed IDs you want to exclude in the ban. Split by a space.\neg`id1 id2 id3`\nSet is as `None` if you dont want any.\nUse /cancel to go back.",
        "back": "cbs_sfban",
    },
}


TOKEN_FILE = "resources/auths/auth_token.txt"


@callback(
    re.compile(
        "sndplug_(.*)",
    ),
    owner=True,
)
async def send(eve):
    key, name = (eve.data_match.group(1)).decode("UTF-8").split("_")
    thumb = "resources/extras/inline.jpg"
    await eve.answer("■ Sending ■")
    data = f"uh_{key}_"
    index = None
    if "|" in name:
        name, index = name.split("|")
    key = "plugins" if key == "Official" else key.lower()
    plugin = f"{key}/{name}.py"
    _ = f"pasta-{plugin}"
    if index is not None:
        data += f"|{index}"
        _ += f"|{index}"
    buttons = [
        [
            Button.inline(
                "« Pᴀsᴛᴇ »",
                data=_,
            )
        ],
        [
            Button.inline("« Bᴀᴄᴋ", data=data),
        ],
    ]
    try:
        await eve.edit(file=plugin, thumb=thumb, buttons=buttons)
    except Exception as er:
        await eve.answer(str(er), alert=True)


heroku_api, app_name = Var.HEROKU_API, Var.HEROKU_APP_NAME


@callback("updatenow", owner=True)
async def update(eve):
    repo = Repo()
    ac_br = repo.active_branch
    ups_rem = repo.remote("upstream")
    if heroku_api:
        import heroku3

        try:
            heroku = heroku3.from_key(heroku_api)
            heroku_app = None
            heroku_applications = heroku.apps()
        except BaseException as er:
            LOGS.exception(er)
            return await eve.edit("`Wrong HEROKU_API.`")
        for app in heroku_applications:
            if app.name == app_name:
                heroku_app = app
        if not heroku_app:
            await eve.edit("`Wrong HEROKU_APP_NAME.`")
            repo.__del__()
            return
        await eve.edit(get_string("clst_1"))
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", f"https://api:{heroku_api}@"
        )

        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            await eve.edit(f"`Here is the error log:\n{error}`")
            repo.__del__()
            return
        await eve.edit("`Successfully Updated!\nRestarting, please wait...`")
    else:
        await eve.edit(get_string("clst_1"))
        call_back()
        await bash("git pull && pip3 install -r requirements.txt")
        execl(sys.executable, sys.executable, "-m", "pyUltroid")


@callback(re.compile("changes(.*)"), owner=True)
async def changes(okk):
    match = okk.data_match.group(1).decode("utf-8")
    await okk.answer(get_string("clst_3"))
    repo = Repo.init()
    button = [[Button.inline("Update Now", data="updatenow")]]
    changelog, tl_chnglog = await gen_chlog(
        repo, f"HEAD..upstream/{repo.active_branch}"
    )
    cli = "\n\nClick the below button to update!"
    if not match:
        try:
            if len(tl_chnglog) > 700:
                tl_chnglog = f"{tl_chnglog[:700]}..."
                button.append([Button.inline("View Complete", "changesall")])
            await okk.edit("• Writing Changelogs 📝 •")
            img = await Carbon(
                file_name="changelog",
                code=tl_chnglog,
                backgroundColor=choice(ATRA_COL),
                language="md",
            )
            return await okk.edit(
                f"**• Ultroid Userbot •**{cli}", file=img, buttons=button
            )
        except Exception as er:
            LOGS.exception(er)
    changelog_str = changelog + cli
    if len(changelog_str) > 1024:
        await okk.edit(get_string("upd_4"))
        await asyncio.sleep(2)
        with open("ultroid_updates.txt", "w+") as file:
            file.write(tl_chnglog)
        await okk.edit(
            get_string("upd_5"),
            file="ultroid_updates.txt",
            buttons=button,
        )
        remove("ultroid_updates.txt")
        return
    await okk.edit(
        changelog_str,
        buttons=button,
        parse_mode="html",
    )


@callback(
    re.compile(
        "pasta-(.*)",
    ),
    owner=True,
)
async def _(e):
    ok = (e.data_match.group(1)).decode("UTF-8")
    index = None
    if "|" in ok:
        ok, index = ok.split("|")
    with open(ok, "r") as hmm:
        _, key = await get_paste(hmm.read())
    link = f"https://spaceb.in/{key}"
    raw = f"https://spaceb.in/api/v1/documents/{key}/raw"
    if not _:
        return await e.answer(key[:30], alert=True)
    if ok.startswith("addons"):
        key = "Addons"
    elif ok.startswith("vcbot"):
        key = "VCBot"
    else:
        key = "Official"
    data = f"uh_{key}_"
    if index is not None:
        data += f"|{index}"
    await e.edit(
        "",
        buttons=[
            [Button.url("Lɪɴᴋ", link), Button.url("Rᴀᴡ", raw)],
            [Button.inline("« Bᴀᴄᴋ", data=data)],
        ],
    )


@callback(re.compile("cbs_(.*)"), owner=True)
async def _edit_to(event):
    match = event.data_match.group(1).decode("utf-8")
    data = _buttons.get(match)
    if not data:
        return
    await event.edit(data["text"], buttons=data["buttons"], link_preview=False)


@callback(re.compile("abs_(.*)"), owner=True)
async def convo_handler(event: events.CallbackQuery):
    match = event.data_match.group(1).decode("utf-8")
    if not _convo.get(match):
        return
    await event.delete()
    get_ = _convo[match]
    back = get_["back"]
    async with event.client.conversation(event.sender_id) as conv:
        await conv.send_message(get_["text"])
        response = await conv.get_response()
        themssg = response.message
        try:
            themssg = ast.literal_eval(themssg)
        except Exception:
            pass
        if themssg == "/cancel":
            return await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button(back),
            )
        await setit(event, get_["var"], themssg)
        await conv.send_message(
            f"{get_['name']} changed to `{themssg}`",
            buttons=get_back_button(back),
        )


@callback("authorise", owner=True)
async def _(e):
    if not e.is_private:
        return
    url = GDrive._create_token_file()
    await e.edit("Go to the below link and send the code!")
    async with asst.conversation(e.sender_id) as conv:
        await conv.send_message(url)
        code = await conv.get_response()
        if GDrive._create_token_file(code=code.text):
            await conv.send_message(
                "`Success!\nYou are all set to use Google Drive with Ultroid Userbot.`",
                buttons=Button.inline("Main Menu", data="setter"),
            )
        else:
            await conv.send_message("Wrong code! Click authorise again.")


@callback("folderid", owner=True, func=lambda x: x.is_private)
async def _(e):
    if not e.is_private:
        return
    msg = (
        "Send your FOLDER ID\n\n"
        + "For FOLDER ID:\n"
        + "1. Open Google Drive App.\n"
        + "2. Create Folder.\n"
        + "3. Make that folder public.\n"
        + "4. Send link of that folder."
    )
    await e.delete()
    async with asst.conversation(e.sender_id, timeout=150) as conv:
        await conv.send_message(msg)
        repl = await conv.get_response()
        id = repl.text
        if id.startswith("https"):
            id = id.split("?id=")[-1]
        udB.set_key("GDRIVE_FOLDER_ID", id)
        await repl.reply(
            "`Success.`",
            buttons=get_back_button("gdrive"),
        )


@callback("gdrive", owner=True)
async def _(e):
    if not e.is_private:
        return
    await e.edit(
        "Click Authorise and send the code.\n\nYou can use your own CLIENT ID and SECRET by [this](https://t.me/Kittyxupdates/30)",
        buttons=[
            [
                Button.inline("Folder ID", data="folderid"),
                Button.inline("Authorise", data="authorise"),
            ],
            [Button.inline("« Back", data="cbs_otvars")],
        ],
        link_preview=False,
    )


@callback("dmof", owner=True)
async def rhwhe(e):
    if udB.get_key("DUAL_MODE"):
        udB.del_key("DUAL_MODE")
        key = "Off"
    else:
        udB.set_key("DUAL_MODE", "True")
        key = "On"
    Msg = f"Dual Mode : {key}"
    await e.edit(Msg, buttons=get_back_button("cbs_otvars"))


@callback("dmhn", owner=True)
async def hndlrr(event):
    await event.delete()
    pru = event.sender_id
    var = "DUAL_HNDLR"
    name = "Dual Handler"
    CH = udB.get_key(var) or "/"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            f"Send The Symbol Which u want as Handler/Trigger to use your Assistant bot\nUr Current Handler is [ `{CH}` ]\n\n use /cancel to cancel.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button("cbs_otvars"),
            )
        elif len(themssg) > 1:
            await conv.send_message(
                "Incorrect Handler",
                buttons=get_back_button("cbs_otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}",
                buttons=get_back_button("cbs_otvars"),
            )


@callback("emoj", owner=True)
async def emoji(event):
    await event.delete()
    pru = event.sender_id
    var = "EMOJI_IN_HELP"
    name = f"Emoji in `{HNDLR}help` menu"
    async with event.client.conversation(pru) as conv:
        await conv.send_message("Send emoji u want to set 🙃.\n\nUse /cancel to cancel.")
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button("cbs_otvars"),
            )
        elif themssg.startswith(("/", HNDLR)):
            await conv.send_message(
                "Incorrect Emoji",
                buttons=get_back_button("cbs_otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}\n",
                buttons=get_back_button("cbs_otvars"),
            )


@callback("plg", owner=True)
async def pluginch(event):
    await event.delete()
    pru = event.sender_id
    var = "PLUGIN_CHANNEL"
    name = "Plugin Channel"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "Send id or username of a channel from where u want to install all plugins\n\nOur Channel~ @Herokue_cc\n\nUse /cancel to cancel.",
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            await conv.send_message(
                "Cancelled!!",
                buttons=get_back_button("cbs_otvars"),
            )
        elif themssg.startswith(("/", HNDLR)):
            await conv.send_message(
                "Incorrect channel",
                buttons=get_back_button("cbs_otvars"),
            )
        else:
            await setit(event, var, themssg)
            await conv.send_message(
                f"{name} changed to {themssg}\n After Setting All Things Do Restart",
                buttons=get_back_button("cbs
