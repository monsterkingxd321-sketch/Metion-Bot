import os
import logging
import asyncio
import time
import random
from telethon import Button, TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors import FloodWaitError

# ---------- HARDCODED CREDENTIALS (do not share this file) ----------
API_ID = 22091901
API_HASH = "54b0cd5fb47a40265b197f1a110b20b8"
BOT_TOKEN = "8714923646:AAEiU-2vTvtYkzXdoLUlV6ceQqyzfjrjhY8"

# ---------- SETUP ----------
logging.basicConfig(level=logging.INFO, format='%(name)s - [%(levelname)s] - %(message)s')
client = TelegramClient('client', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

moment_worker = []

# ---------- STYLES FOR /call ----------
STYLES = [
    "🔥 𝗔𝗝𝗝 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗝𝗢 𝗖𝗛𝗨𝗣 𝗕𝗔𝗜𝗧𝗛𝗔 𝗛𝗔𝗜 𝗨𝗦𝗘 𝗔𝗝𝗝 𝗦𝗔𝗕𝗞𝗘 𝗦𝗔𝗠𝗡𝗘 𝗟𝗔𝗬𝗔 𝗝𝗔𝗬𝗘𝗚𝗔 🔥",
    "⚡ 𝗞𝗢𝗜 𝗧𝗢 𝗕𝗢𝗟𝗢 𝗬𝗔𝗥 𝗔𝗜𝗦𝗔 𝗟𝗔𝗚 𝗥𝗛𝗔 𝗛𝗔𝗜 𝗝𝗔𝗜𝗦𝗘 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗦𝗔𝗕 𝗠𝗨𝗧𝗘 𝗠𝗢𝗗𝗘 𝗠𝗘 𝗛𝗔𝗜 ⚡",
    "🚨 𝗝𝗢 𝗔𝗝𝗝 𝗥𝗘𝗣𝗟𝗬 𝗡𝗔𝗛𝗜 𝗗𝗘𝗚𝗔 𝗨𝗦𝗞𝗔 𝗡𝗔𝗠 𝗟𝗘 𝗟𝗘 𝗞𝗘 𝗦𝗣𝗔𝗠 𝗛𝗢𝗚𝗔 🚨",
    "💥 𝗔𝗝𝗝 𝗠𝗘𝗜𝗡 𝗔𝗬𝗔 𝗛𝗨 𝗚𝗥𝗢𝗨𝗣 𝗞𝗢 𝗙𝗨𝗟𝗟 𝗔𝗖𝗧𝗜𝗩𝗘 𝗕𝗔𝗡𝗔𝗡𝗘 💥",
    "🎯 𝗦𝗔𝗕 𝗟𝗢𝗚 𝗘𝗞 𝗘𝗞 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗗𝗔𝗟𝗢 𝗔𝗝𝗝 𝗦𝗜𝗟𝗘𝗡𝗧 𝗡𝗔𝗛𝗜 𝗥𝗛𝗘𝗡𝗔 🎯",
    "🔥 𝗢𝗬𝗘 𝗞𝗨𝗠𝗔𝗥𝗔𝗡 𝗞𝗜𝗧𝗡𝗔 𝗦𝗢𝗘𝗚𝗔 𝗔𝗕 𝗧𝗢 𝗨𝗧𝗛 𝗝𝗔 🔥",
    "⚡ 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗔𝗢 𝗦𝗔𝗕 𝗟𝗢𝗚 𝗔𝗝𝗝 𝗕𝗢𝗥𝗜𝗡𝗚 𝗡𝗔𝗛𝗜 𝗛𝗢𝗡𝗔 ⚡",
    "🚨 𝗞𝗢𝗜 𝗠𝗘𝗠𝗘 𝗕𝗛𝗘𝗝𝗢 𝗬𝗔𝗥 𝗛𝗔𝗦𝗜 𝗡𝗜𝗞𝗟𝗪𝗔𝗢 🚨",
    "💥 𝗝𝗢 𝗢𝗡𝗟𝗜𝗡𝗘 𝗛𝗔𝗜 𝗪𝗢 𝗥𝗘𝗣𝗟𝗬 𝗞𝗔𝗥𝗘 𝗩𝗔𝗥𝗡𝗔 𝗧𝗔𝗚 𝗠𝗜𝗟𝗘𝗚𝗔 💥",
    "🎯 𝗔𝗝𝗝 𝗦𝗔𝗕𝗞𝗢 𝗔𝗖𝗧𝗜𝗩𝗘 𝗞𝗔𝗥𝗡𝗔 𝗠𝗬 𝗠𝗜𝗦𝗦𝗜𝗢𝗡 🎯",
    "🔥 𝗚𝗥𝗢𝗨𝗣 𝗞𝗢 𝗗𝗘𝗔𝗗 𝗠𝗢𝗗𝗘 𝗦𝗘 𝗭𝗜𝗡𝗗𝗔 𝗠𝗢𝗗𝗘 𝗠𝗘 𝗟𝗔𝗡𝗔 𝗛𝗔𝗜 🔥",
    "⚡ 𝗔𝗝𝗝 𝗝𝗢 𝗖𝗛𝗨𝗣 𝗥𝗛𝗘𝗚𝗔 𝗨𝗦𝗘 𝗗𝗢𝗨𝗕𝗟𝗘 𝗦𝗣𝗔𝗠 ⚡",
    "🚨 𝗔𝗧𝗧𝗘𝗡𝗗𝗔𝗡𝗖𝗘 𝗟𝗔𝗚𝗔𝗢 𝗡𝗔𝗛𝗜 𝗧𝗢 𝗙𝗜𝗡𝗘 🚨",
    "💥 𝗦𝗔𝗕 𝗔𝗣𝗡𝗔 𝗦𝗧𝗔𝗧𝗨𝗦 𝗕𝗔𝗧𝗔𝗢 💥",
    "🎯 𝗔𝗝𝗝 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗙𝗨𝗟𝗟 𝗠𝗔𝗦𝗧𝗜 🎯",
    "🔥 𝗝𝗢 𝗥𝗘𝗣𝗟𝗬 𝗡𝗔𝗛𝗜 𝗗𝗘𝗚𝗔 𝗨𝗦𝗘 𝗧𝗔𝗚 𝗦𝗧𝗢𝗥𝗠 🔥",
    "⚡ 𝗢𝗬𝗘 𝗟𝗔𝗭𝗬 𝗟𝗢𝗚 𝗝𝗔𝗚 𝗝𝗔𝗢 ⚡",
    "🚨 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗖𝗛𝗨𝗣 𝗥𝗘𝗛𝗡𝗔 𝗠𝗔𝗡𝗔 🚨",
    "💥 𝗦𝗔𝗕 𝗟𝗢𝗚 𝗕𝗢𝗟𝗢 𝗬𝗔𝗥 💥",
    "🎯 𝗔𝗝𝗝 𝗡𝗢 𝗘𝗦𝗖𝗔𝗣𝗘 🎯",
    "🔥 𝗔𝗝𝗝 𝗞𝗔 𝗚𝗢𝗔𝗟 𝗚𝗥𝗢𝗨𝗣 𝗞𝗢 𝗧𝗢𝗣 𝗣𝗘 𝗟𝗘 𝗝𝗔𝗡𝗔 🔥",
    "⚡ 𝗦𝗔𝗕 𝗟𝗢𝗚 𝗘𝗡𝗚𝗔𝗚𝗘 𝗛𝗢 ⚡",
    "🚨 𝗞𝗢𝗜 𝗦𝗧𝗢𝗥𝗬 𝗦𝗨𝗡𝗔𝗢 🚨",
    "💥 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗔𝗔𝗚 𝗟𝗔𝗚𝗔𝗢 💥",
    "🎯 𝗙𝗨𝗟𝗟 𝗥𝗔𝗜𝗗 𝗠𝗢𝗗𝗘 🎯",
    "🔥 𝗠𝗔𝗜𝗡 𝗥𝗨𝗞𝗡𝗘 𝗪𝗔𝗟𝗔 𝗡𝗔𝗛𝗜 🔥",
    "⚡ 𝗦𝗣𝗔𝗠 𝗖𝗢𝗡𝗧𝗜𝗡𝗨𝗘 ⚡",
    "🚨 𝗡𝗢 𝗦𝗜𝗟𝗘𝗡𝗖𝗘 🚨",
    "💥 𝗦𝗔𝗕 𝗔𝗢 💥",
    "🎯 𝗡𝗢𝗪 𝗥𝗘𝗣𝗟𝗬 🎯",
  "🔥 𝗚𝗥𝗢𝗨𝗣 𝗞𝗘 𝗦𝗔𝗕 𝗟𝗨𝗥𝗞𝗘𝗥𝗦 𝗔𝗕 𝗕𝗔𝗛𝗔𝗥 𝗔𝗢 🔥",
"⚡ 𝗔𝗝𝗝 𝗦𝗜𝗟𝗘𝗡𝗧 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗞𝗜 𝗧𝗘𝗦𝗧𝗜𝗡𝗚 ⚡",
"🚨 𝗝𝗢 𝗔𝗕𝗛𝗜 𝗢𝗡𝗟𝗜𝗡𝗘 𝗛𝗔𝗜 𝗪𝗢 𝗥𝗘𝗣𝗟𝗬 𝗗𝗘 🚨",
"💥 𝗚𝗥𝗢𝗨𝗣 𝗞𝗢 𝗔𝗖𝗧𝗜𝗩𝗘 𝗠𝗢𝗗𝗘 𝗠𝗘 𝗟𝗔𝗡𝗔 𝗛𝗔𝗜 💥",
"🎯 𝗘𝗞 𝗘𝗞 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗦𝗔𝗕 𝗕𝗛𝗘𝗝𝗢 🎯",
"🔥 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗠𝗘𝗠𝗘 𝗗𝗥𝗢𝗣 𝗞𝗔𝗥𝗢 🔥",
"⚡ 𝗔𝗕 𝗡𝗜𝗞𝗟𝗢 𝗦𝗜𝗟𝗘𝗡𝗧 𝗠𝗢𝗗𝗘 𝗦𝗘 ⚡",
"🚨 𝗝𝗢 𝗖𝗛𝗨𝗣 𝗕𝗔𝗜𝗧𝗛𝗔 𝗛𝗔𝗜 𝗪𝗢 𝗔𝗕 𝗕𝗢𝗟𝗘 🚨",
"💥 𝗚𝗥𝗢𝗨𝗣 𝗞𝗔 𝗧𝗘𝗠𝗣𝗘𝗥𝗔𝗧𝗨𝗥𝗘 𝗕𝗔𝗗𝗛𝗔𝗢 💥",
"🎯 𝗔𝗝𝗝 𝗡𝗢 𝗚𝗛𝗢𝗦𝗧 𝗠𝗢𝗗𝗘 🎯",
"🔥 𝗦𝗔𝗕 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗥𝗘𝗣𝗢𝗥𝗧 𝗛𝗘𝗥𝗘 🔥",
"⚡ 𝗞𝗢𝗡 𝗞𝗢𝗡 𝗔𝗖𝗧𝗜𝗩𝗘 𝗛𝗔𝗜 ⚡",
"🚨 𝗔𝗝𝗝 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗡𝗢 𝗟𝗨𝗥𝗞𝗜𝗡𝗚 🚨",
"💥 𝗦𝗜𝗟𝗘𝗡𝗧 𝗚𝗔𝗡𝗚 𝗞𝗢 𝗝𝗔𝗚𝗔𝗢 💥",
"🎯 𝗘𝗩𝗘𝗥𝗬𝗢𝗡𝗘 𝗧𝗬𝗣𝗘 𝗦𝗢𝗠𝗘𝗧𝗛𝗜𝗡𝗚 🎯",
"🔥 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬 𝗖𝗛𝗔𝗜𝗬𝗘 🔥",
"⚡ 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗖𝗢𝗨𝗡𝗧 𝗕𝗔𝗗𝗛𝗔𝗢 ⚡",
"🚨 𝗡𝗢 𝗠𝗢𝗥𝗘 𝗦𝗜𝗟𝗘𝗡𝗖𝗘 🚨",
"💥 𝗔𝗝𝗝 𝗙𝗨𝗟𝗟 𝗖𝗛𝗔𝗧 💥",
"🎯 𝗚𝗥𝗢𝗨𝗣 𝗖𝗛𝗔𝗧 𝗦𝗧𝗔𝗥𝗧 🎯",
"🔥 𝗔𝗝𝗝 𝗚𝗥𝗢𝗨𝗣 𝗕𝗢𝗥𝗜𝗡𝗚 𝗡𝗔𝗛𝗜 🔥",
"⚡ 𝗠𝗘𝗠𝗘 𝗕𝗢𝗠𝗕𝗜𝗡𝗚 ⚡",
"🚨 𝗝𝗢 𝗖𝗛𝗨𝗣 𝗥𝗛𝗘𝗚𝗔 𝗨𝗦𝗘 𝗧𝗔𝗚 🚨",
"💥 𝗔𝗖𝗧𝗜𝗩𝗘 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗥𝗘𝗦𝗣𝗘𝗖𝗧 💥",
"🎯 𝗡𝗢 𝗟𝗔𝗭𝗬 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 🎯",
"🔥 𝗦𝗔𝗕 𝗚𝗥𝗢𝗨𝗣 𝗠𝗘 𝗛𝗔𝗜 𝗬𝗔 𝗡𝗔𝗛𝗜 🔥",
"⚡ 𝗢𝗬𝗘 𝗥𝗘𝗣𝗟𝗬 𝗗𝗘 ⚡",
"🚨 𝗠𝗘𝗠𝗕𝗘𝗥 𝗖𝗛𝗘𝗖𝗞 🚨",
"💥 𝗔𝗧𝗧𝗘𝗡𝗗𝗔𝗡𝗖𝗘 𝗧𝗜𝗠𝗘 💥",
"🎯 𝗥𝗘𝗣𝗟𝗬 𝗡𝗢𝗪 🎯",
"🔥 𝗚𝗥𝗢𝗨𝗣 𝗔𝗖𝗧𝗜𝗩𝗘 𝗠𝗢𝗗𝗘 🔥",
"⚡ 𝗖𝗛𝗔𝗧 𝗦𝗧𝗔𝗥𝗧 ⚡",
"🚨 𝗝𝗢 𝗔𝗕𝗛𝗜 𝗢𝗡𝗟𝗜𝗡𝗘 𝗛𝗔𝗜 𝗦𝗣𝗘𝗔𝗞 🚨",
"💥 𝗦𝗔𝗕 𝗕𝗢𝗟𝗢 💥",
"🎯 𝗚𝗥𝗢𝗨𝗣 𝗥𝗘𝗩𝗜𝗩𝗘 🎯",
"🔥 𝗡𝗢 𝗗𝗘𝗔𝗗 𝗚𝗥𝗢𝗨𝗣 🔥",
"⚡ 𝗖𝗛𝗔𝗧 𝗘𝗡𝗚𝗔𝗚𝗘 ⚡",
"🚨 𝗦𝗜𝗟𝗘𝗡𝗧 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗢𝗨𝗧 🚨",
"💥 𝗦𝗔𝗕 𝗟𝗢𝗚 𝗔𝗢 💥",
"🎯 𝗥𝗘𝗦𝗣𝗢𝗡𝗦𝗘 𝗧𝗜𝗠𝗘 🎯",
"🔥 𝗔𝗝𝗝 𝗙𝗨𝗟𝗟 𝗖𝗛𝗔𝗧 🔥",
"⚡ 𝗚𝗥𝗢𝗨𝗣 𝗥𝗔𝗜𝗗 ⚡",
"🚨 𝗘𝗩𝗘𝗥𝗬𝗢𝗡𝗘 𝗦𝗣𝗘𝗔𝗞 🚨",
"💥 𝗔𝗖𝗧𝗜𝗩𝗘 𝗚𝗔𝗡𝗚 💥",
"🎯 𝗖𝗛𝗔𝗧 𝗠𝗢𝗗𝗘 🎯",
"🔥 𝗡𝗢 𝗠𝗢𝗥𝗘 𝗚𝗛𝗢𝗦𝗧 🔥",
"⚡ 𝗥𝗘𝗣𝗟𝗬 𝗤𝗨𝗜𝗖𝗞 ⚡",
"🚨 𝗚𝗥𝗢𝗨𝗣 𝗪𝗔𝗞𝗘 𝗨𝗣 🚨",
"💥 𝗖𝗛𝗔𝗧 𝗧𝗜𝗠𝗘 💥",
"🎯 𝗠𝗘𝗦𝗦𝗔𝗚𝗘 𝗡𝗢𝗪 🎯",
"🔥 𝗖𝗛𝗔𝗧 𝗕𝗢𝗢𝗦𝗧 🔥",
"⚡ 𝗚𝗥𝗢𝗨𝗣 𝗛𝗬𝗣𝗘 ⚡",
"🚨 𝗚𝗥𝗢𝗨𝗣 𝗥𝗘𝗩𝗜𝗩𝗔𝗟 🚨",
"💥 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗦𝗣𝗘𝗔𝗞 💥",
"🎯 𝗖𝗛𝗔𝗧 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬 🎯",
"🔥 𝗡𝗢 𝗚𝗛𝗢𝗦𝗧𝗦 🔥",
"⚡ 𝗦𝗣𝗘𝗔𝗞 𝗨𝗣 ⚡",
"🚨 𝗠𝗘𝗠𝗕𝗘𝗥 𝗥𝗢𝗟𝗟 𝗖𝗔𝗟𝗟 🚨",
"💥 𝗖𝗛𝗔𝗧 𝗠𝗢𝗠𝗘𝗡𝗧 💥",
"🎯 𝗥𝗘𝗦𝗣𝗢𝗡𝗗 🎯",
"🔥 𝗙𝗨𝗟𝗟 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬 🔥",
"⚡ 𝗖𝗛𝗔𝗧 𝗕𝗢𝗢𝗠 ⚡",
"🚨 𝗡𝗢 𝗦𝗜𝗟𝗘𝗡𝗖𝗘 𝗧𝗢𝗗𝗔𝗬 🚨",
"💥 𝗠𝗘𝗠𝗕𝗘𝗥𝗦 𝗥𝗘𝗦𝗣𝗢𝗡𝗗 💥",
"🎯 𝗚𝗥𝗢𝗨𝗣 𝗖𝗛𝗔𝗧 𝗡𝗢𝗪 🎯",
"🔥 𝗖𝗛𝗔𝗧 𝗦𝗣𝗔𝗥𝗞 🔥",
"⚡ 𝗠𝗘𝗠𝗕𝗘𝗥 𝗖𝗔𝗟𝗟 ⚡",
"🚨 𝗘𝗩𝗘𝗥𝗬𝗢𝗡𝗘 𝗢𝗨𝗧 🚨",
"💥 𝗔𝗖𝗧𝗜𝗩𝗘 𝗠𝗢𝗗𝗘 💥",
"🎯 𝗦𝗣𝗘𝗔𝗞 𝗡𝗢𝗪 🎯"
]

# ---------- HELPER FUNCTIONS ----------
def format_users_batch(users, start_idx):
    """Return a stylish string of users with fancy bullets (5 per batch)."""
    bullets = ["◎", "✦", "✧", "♡", "❥"]
    lines = []
    for i, (user_id, name) in enumerate(users):
        bullet = bullets[i % len(bullets)]
        lines.append(f"{bullet} [{name}](tg://user?id={user_id})")
    return "\n".join(lines)

# ---------- /cancel ----------
@client.on(events.NewMessage(pattern='(?i)^/cancel$'))
async def cancel(event):
    if event.chat_id in moment_worker:
        moment_worker.remove(event.chat_id)
        await event.reply("✅ **Process stopped.**")
    else:
        await event.reply("ℹ️ No active process to cancel.")

# ---------- /utag – tag all users (skip bots and deleted) ----------
@client.on(events.NewMessage(pattern='(?i)^/utag ?(.*)'))
async def utag(event):
    global moment_worker
    if event.is_private:
        return await event.reply("❌ This command works only in groups.")

    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.reply("❌ You need to be an admin to use this command.")

    text = event.pattern_match.group(1)
    if not text:
        return await event.reply("⚠️ Please provide text to accompany the tag.\nExample: `/utag Hello everyone!`")

    moment_worker.append(event.chat_id)

    bot_id = (await client.get_me()).id
    users = []
    async for user in client.iter_participants(event.chat_id):
        if user.id == bot_id:
            continue
        if getattr(user, 'bot', False):
            continue
        if getattr(user, 'deleted', False):
            continue
        name = user.first_name or "User"
        users.append((user.id, name))

    total = len(users)
    if total == 0:
        moment_worker.remove(event.chat_id)
        return await event.reply("❌ No valid members found (bots and deleted accounts were skipped).")

    start_msg = await event.reply(f"⏳ **Tagging {total} users...**")

    batch_size = 5
    start_time = time.time()

    for i in range(0, total, batch_size):
        if event.chat_id not in moment_worker:
            await start_msg.edit("⛔ **Tagging cancelled.**")
            return

        batch = users[i:i+batch_size]
        formatted = format_users_batch(batch, i)

        header = f"{text}\n\n"
        footer = f"\n\n🏆 **TAGGED {len(batch)} USERS**\n⏱️ Batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}"
        message = header + formatted + footer

        try:
            await client.send_message(event.chat_id, message)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await client.send_message(event.chat_id, message)

        await asyncio.sleep(random.uniform(1.8, 2.5))

    elapsed = time.time() - start_time
    final = f"✅ **Tagging complete!**\n👥 **{total}** users tagged.\n⏱️ Time: {elapsed:.1f} seconds."
    await start_msg.edit(final)

    if event.chat_id in moment_worker:
        moment_worker.remove(event.chat_id)

# ---------- /atag – tag only admins ----------
@client.on(events.NewMessage(pattern='(?i)^/atag ?(.*)'))
async def atag(event):
    global moment_worker
    if event.is_private:
        return await event.reply("❌ This command works only in groups.")

    admins_list = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins_list:
        return await event.reply("❌ You need to be an admin to use this command.")

    text = event.pattern_match.group(1)
    if not text:
        return await event.reply("⚠️ Please provide text to accompany the admin tag.\nExample: `/atag Hello admins!`")

    moment_worker.append(event.chat_id)

    bot_id = (await client.get_me()).id
    admins = []
    async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        if admin.id == bot_id:
            continue
        if getattr(admin, 'bot', False):
            continue
        if getattr(admin, 'deleted', False):
            continue
        name = admin.first_name or "Admin"
        admins.append((admin.id, name))

    total = len(admins)
    if total == 0:
        moment_worker.remove(event.chat_id)
        return await event.reply("❌ No valid admins found (excluding bot and deleted).")

    start_msg = await event.reply(f"⏳ **Tagging {total} admins...**")

    batch_size = 5
    start_time = time.time()

    for i in range(0, total, batch_size):
        if event.chat_id not in moment_worker:
            await start_msg.edit("⛔ **Tagging cancelled.**")
            return

        batch = admins[i:i+batch_size]
        formatted = format_users_batch(batch, i)

        header = f"{text}\n\n"
        footer = f"\n\n🏆 **TAGGED {len(batch)} ADMINS**\n⏱️ Batch {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}"
        message = header + formatted + footer

        try:
            await client.send_message(event.chat_id, message)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await client.send_message(event.chat_id, message)

        await asyncio.sleep(random.uniform(1.8, 2.5))

    elapsed = time.time() - start_time
    final = f"✅ **Admin tagging complete!**\n👥 **{total}** admins tagged.\n⏱️ Time: {elapsed:.1f} seconds."
    await start_msg.edit(final)

    if event.chat_id in moment_worker:
        moment_worker.remove(event.chat_id)

# ---------- /call – one message per user, cycling through styles ----------
@client.on(events.NewMessage(pattern='(?i)^/call ?(.*)'))
async def call(event):
    global moment_worker
    if event.is_private:
        return await event.reply("❌ Group only.")

    admins = [admin.id async for admin in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins)]
    if event.sender_id not in admins:
        return await event.reply("❌ Admin only.")

    custom_text = event.pattern_match.group(1)
    moment_worker.append(event.chat_id)

    users = []
    bot_id = (await client.get_me()).id
    async for user in client.iter_participants(event.chat_id):
        if user.id == bot_id:
            continue
        if getattr(user, 'bot', False):
            continue
        if getattr(user, 'deleted', False):
            continue
        name = user.first_name or "User"
        users.append((user.id, name))

    if not users:
        moment_worker.remove(event.chat_id)
        return await event.reply("❌ No valid members found (bots and deleted accounts were skipped).")

    await event.reply(f"🚀 **Starting call loop for {len(users)} users.**\nUse `/cancel` to stop.")

    total_styles = len(STYLES)
    user_idx = 0

    while event.chat_id in moment_worker:
        user_id, user_name = users[user_idx % len(users)]
        style = STYLES[user_idx % total_styles]

        msg = f"[{user_name}](tg://user?id={user_id})\n\n{style}"
        if custom_text:
            msg += f"\n\n💬 {custom_text}"

        try:
            await client.send_message(event.chat_id, msg)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)
            await client.send_message(event.chat_id, msg)

        user_idx += 1
        await asyncio.sleep(random.uniform(1.8, 2.5))

    if event.chat_id not in moment_worker:
        await event.reply("⛔ **Call stopped.**")

# ---------- /start ----------
@client.on(events.NewMessage(pattern='(?i)^/start$'))
async def start(event):
    await event.reply(
        "✨ **Hello! I'm User Tagger Bot** ✨\n\n"
        "I can help you tag all members in a group with style.\n\n"
        "🔹 `/utag` – tag all users (5 per message)\n"
        "🔹 `/atag` – tag only admins (5 per message)\n"
        "🔹 `/call` – individual messages with rotating quotes\n"
        "🔹 `/cancel` – stop any running process\n\n"
        "➡️ **Add me to your group and make me admin to start tagging!**",
        buttons=[
            [Button.url("➕ Add to Group", "https://t.me/iammention_bot?startgroup=true")],
            [Button.url("💬 Support", "https://t.me/+jg6CtmDzz3E3ZWNl")],
            [Button.url("📢 Channel", "https://t.me/+Qzy2vnoy3g00OTE1")],
            [Button.url("👑 Owner", "https://t.me/mvtyy")]
        ]
    )

# ---------- /help ----------
@client.on(events.NewMessage(pattern='(?i)^/help$'))
async def help(event):
    await event.reply(
        "📖 **Commands**\n\n"
        "• `/utag <text>` – Tags all group members (skips bots and deleted accounts).\n"
        "• `/atag <text>` – Tags only admins (skips bots and deleted).\n"
        "• `/call <text>` – Sends each member a separate message with a rotating style.\n"
        "• `/cancel` – Stops any ongoing tagging or calling session.\n\n"
        "🔰 **Requirements**\n"
        "• Bot must be admin in the group.\n"
        "• Only admins can use these commands.\n\n"
        "👨‍💻 **Support** – Click the buttons below.",
        buttons=[
            [Button.url("➕ Add to Group", "https://t.me/iammention_bot?startgroup=true")],
            [Button.url("💬 Support", "https://t.me/+jg6CtmDzz3E3ZWNl")],
            [Button.url("📢 Channel", "https://t.me/+Qzy2vnoy3g00OTE1")],
            [Button.url("👑 Owner", "https://t.me/mvtyy")]
        ]
    )

# ---------- /repository ----------
@client.on(events.NewMessage(pattern='(?i)^/repository$'))
async def repo(event):
    await event.reply(
        "🚀 **Deploy your own bot**\n\n"
        "Get the source code and host it yourself!\n"
        "Join our channel for updates.",
        buttons=[
            [Button.url("📢 Channel", "https://t.me/+Qzy2vnoy3g00OTE1")],
            [Button.url("💬 Group", "https://t.me/+jg6CtmDzz3E3ZWNl")],
            [Button.url("👑 Owner", "https://t.me/mvtyy")]
        ]
    )

# ---------- START BOT ----------
print("✅ BOT STARTED")
client.run_until_disconnected()
