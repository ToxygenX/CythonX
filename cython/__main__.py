import asyncio
import glob
import logging
import os
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon import __version__ as vers
from telethon.errors.rpcerrorlist import AuthKeyDuplicatedError
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import InputMessagesFilterDocument

from . import *
from .utils import *
from .version import __version__ as ver

# logging.basicConfig(filename="cipherx.log", filemode="w",
#    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
# )

# remove the old logs file.
if os.path.exists("cipherx.log"):
    os.remove("cipherx.log")

# start logging into a new file.
logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("cipherx.log"), logging.StreamHandler()],
)

if not os.path.isdir("resources/auths"):
    os.mkdir("resources/auths")

if not os.path.isdir("resources/downloads"):
    os.mkdir("resources/downloads")

if not os.path.isdir("addons"):
    os.mkdir("addons")

token = udB.get("GDRIVE_TOKEN")
if token:
    with open("resources/auths/auth_token.txt", "w") as t_file:
        t_file.write(token)

websocket = udB.get("WEBSOCKET_URL")
if websocket:
    ulr = f"WEBSOCKET_URL={websocket}"
    with open(".env", "w") as t:
        t.write(ulr)


async def istart(ult):
    await ultroid_bot.start(ult)
    ultroid_bot.me = await ultroid_bot.get_me()
    ultroid_bot.uid = telethon.utils.get_peer_id(ultroid_bot.me)
    ultroid_bot.first_name = ultroid_bot.me.first_name


async def bot_info(BOT_TOKEN):
    asstinfo = await asst.get_me()
    asstinfo.username


LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)

ultroid_bot.asst = None
LOGS.info("Initialising...")
LOGS.info(f"CythonX Version - {ver}")
LOGS.info(f"Telethon Version - {vers}")
LOGS.info("CɪᴘʜᴇʀX Bot Version - 0.0.5")

if Var.BOT_TOKEN:
    LOGS.info("Starting CɪᴘʜᴇʀX Bot...")
    try:
        ultroid_bot.asst = TelegramClient(
            None, api_id=Var.API_ID, api_hash=Var.API_HASH
        ).start(bot_token=Var.BOT_TOKEN)
        ultroid_bot.loop.run_until_complete(istart(Var.BOT_USERNAME))
        LOGS.info("User Mode - Done")
        LOGS.info("Done, startup completed")
    except AuthKeyDuplicatedError:
        LOGS.info(
            "Session String expired. Please create a new one! CɪᴘʜᴇʀX Bot is stopping..."
        )
        exit(1)
    except BaseException as e:
        LOGS.info("Error: " + str(e))
        exit(1)
else:
    LOGS.info("Starting User Mode...")
    ultroid_bot.start()

udB.set("OWNER_ID", ultroid_bot.uid)

# for userbot
path = "plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_plugins(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"CɪᴘʜᴇʀX Bot - Official -  Installed - {plugin_name}")
        except Exception as e:
            LOGS.info(f"CɪᴘʜᴇʀX Bot - Official - ERROR - {plugin_name}")
            LOGS.info(str(e))


# for addons
addons = udB.get("ADDONS")
if addons == "True" or addons is None:
    os.system("git clone https://github.com/CipherX1-ops/Megatron-addons.git ./addons/")
    LOGS.info("Installing packages for addons")
    os.system("pip install -r ./addons/addons.txt")
    path = "addons/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            try:
                load_addons(plugin_name.replace(".py", ""))
                if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                    LOGS.info(f"CɪᴘʜᴇʀX Bot - Addons - Installed - {plugin_name}")
            except Exception as e:
                LOGS.warning(f"CɪᴘʜᴇʀX Bot - Addons - ERROR - {plugin_name}")
                LOGS.warning(str(e))
else:
    os.system("cp plugins/__init__.py addons/")


# for assistant
path = "assistant/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        try:
            load_assistant(plugin_name.replace(".py", ""))
            if not plugin_name.startswith("__") or plugin_name.startswith("_"):
                LOGS.info(f"CɪᴘʜᴇʀX Bot - Assistant - Installed - {plugin_name}")
        except Exception as e:
            LOGS.warning(f"CɪᴘʜᴇʀX Bot - Assistant - ERROR - {plugin_name}")
            LOGS.warning(str(e))

# for channel plugin
Plug_channel = udB.get("PLUGIN_CHANNEL")
if Plug_channel:

    async def plug():
        try:
            try:
                if not Plug_channel.startswith("/"):
                    chat = int(Plug_channel)
                else:
                    return
            except BaseException:
                if Plug_channel.startswith("@"):
                    chat = Plug_channel
                else:
                    return
            plugins = await ultroid_bot.get_messages(
                chat,
                None,
                search=".py",
                filter=InputMessagesFilterDocument,
            )
            total = int(plugins.total)
            totals = range(0, total)
            for ult in totals:
                uid = plugins[ult].id
                file = await ultroid_bot.download_media(
                    await ultroid_bot.get_messages(chat, ids=uid), "./addons/"
                )
                if "(" not in file:
                    upath = Path(file)
                    name = upath.stem
                    try:
                        load_addons(name.replace(".py", ""))
                        LOGS.info(
                            f"CɪᴘʜᴇʀX Bot - PLUGIN_CHANNEL - Installed - {(os.path.basename(file))}"
                        )
                    except Exception as e:
                        LOGS.warning(
                            f"CɪᴘʜᴇʀX Bot - PLUGIN_CHANNEL - ERROR - {(os.path.basename(file))}"
                        )
                        LOGS.warning(str(e))
                else:
                    LOGS.info(f"Plugin {(os.path.basename(file))} is Pre Installed")
                    os.remove(file)
        except Exception as e:
            LOGS.warning(str(e))


# chat via assistant
pmbot = udB.get("PMBOT")
if pmbot == "True":
    path = "assistant/pmbot/*.py"
    files = glob.glob(path)
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem
            load_pmbot(plugin_name.replace(".py", ""))
    LOGS.info(f"CɪᴘʜᴇʀX Bot - PM Bot Message Forwards - Enabled.")


async def semxy():
    try:
        xx = await ultroid_bot.get_entity(Var.BOT_USERNAME)
        if xx.photo is None:
            LOGS.info("Customizing your Assistant Bot in @BOTFATHER")
            RD = Var.BOT_USERNAME
            if RD.startswith("@"):
                UL = RD
            else:
                UL = f"@{RD}"
            if (ultroid_bot.me.username) is None:
                sir = ultroid_bot.me.first_name
            else:
                sir = f"@{ultroid_bot.me.username}"
            await ultroid_bot.send_message(
                Var.LOG_CHANNEL, "Auto Customisation Started on @botfather"
            )
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/cancel")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", "/setuserpic")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_file(
                "botfather", "resources/extras/ultroid_assistant.jpg"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setabouttext")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather", f"✨Hello✨!! I'm Assistant Bot of {sir}"
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/setdescription")
            await asyncio.sleep(1)
            await ultroid_bot.send_message("botfather", UL)
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                "botfather",
                f"✨PowerFull CɪᴘʜᴇʀX Bot Assistant Bot✨\n✨Master ~ {sir} ✨\n\n✨Powered By ~ CɪᴘʜᴇʀX ✨",
            )
            await asyncio.sleep(2)
            await ultroid_bot.send_message("botfather", "/start")
            await asyncio.sleep(1)
            await ultroid_bot.send_message(
                Var.LOG_CHANNEL, "**Auto Customisation** Done at @BotFather"
            )
            LOGS.info("Customisation Done")
    except Exception as e:
        LOGS.warning(str(e))


async def hehe():
    if Var.LOG_CHANNEL:
        try:
            RD = Var.BOT_USERNAME
            if RD.startswith("@"):
                UL = RD
            else:
                UL = f"@{RD}"
            await ultroid_bot.asst.send_message(
                Var.LOG_CHANNEL,
                f"**CɪᴘʜᴇʀX Bot has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: {UL}\n➖➖➖➖➖➖➖➖➖\n**Support**: CɪᴘʜᴇʀX Bot\n➖➖➖➖➖➖➖➖➖",
            )
        except BaseException:
            try:
                await ultroid_bot.send_message(
                    Var.LOG_CHANNEL,
                    f"**CɪᴘʜᴇʀX Bot has been deployed!**\n➖➖➖➖➖➖➖➖➖\n**UserMode**: [{ultroid_bot.me.first_name}](tg://user?id={ultroid_bot.me.id})\n**Assistant**: {UL}\n➖➖➖➖➖➖➖➖➖\n***Support**: CɪᴘʜᴇʀX Bot\n➖➖➖➖➖➖➖➖➖",
                )
            except BaseException:
                pass
    try:
        await ultroid_bot(JoinChannelRequest("@FutureTechnologyGuardX"))
    except BaseException:
        pass


ultroid_bot.loop.run_until_complete(semxy())
if Plug_channel:
    ultroid_bot.loop.run_until_complete(plug())

ultroid_bot.loop.run_until_complete(hehe())

LOGS.info(
    """
                ----------------------------------------------------------------------
                    CɪᴘʜᴇʀX Bot has been deployed! Visit @CipherXBot for updates!!
                ----------------------------------------------------------------------
"""
)

if __name__ == "__main__":
    ultroid_bot.run_until_disconnected()
