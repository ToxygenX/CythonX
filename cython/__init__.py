from .connections import *

LOGS = LOGS

udB = redis_connection()

ultroid_bot, asst = client_connection()

vcasst, vcClient, CallsClient = vc_connection(udB)

if not udB.get("HNDLR"):
    udB.set("HNDLR", ".")

if not udB.get("SUDO"):
    udB.set("SUDO", "False")

if not udB.get("SUDOS"):
    udB.set("SUDOS", "777000")

if not udB.get("BLACKLIST_CHATS"):
    udB.set("BLACKLIST_CHATS", "[]")

if not udB.get("DUAL_HNDLR"):
    udB.set("DUAL_HNDLR", "/")

HNDLR = udB.get("HNDLR")

Evar = udB.get("SUDO_HNDLR")
SUDOHNDLR = Evar if Evar else HNDLR
