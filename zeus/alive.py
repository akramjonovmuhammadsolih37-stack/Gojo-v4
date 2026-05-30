from telethon import TelegramClient, events
import zeus.client
import asyncio
import os

client = zeus.client.client
BOT_NAME = zeus.client.BOT_NAME


PLUGIN_NAME = "alive"
PLUGIN_DESC = "Botning ishlash holatini ko'rsatadi"
COMMANDS = {'.alive': "Bot haqida ma'lumot"}

@events.register(events.NewMessage(outgoing=True, pattern=r'\.alive'))
async def alive(noob_py):
    client = noob_py.client
    me = await client.get_me()
    username = me.username or str(me.id)
    photo = await client.download_profile_photo(me.id)
    await noob_py.message.edit("Hayrli kun...")
    await asyncio.sleep(0.5)
    await noob_py.respond(
        f"🥷 **Foydalanuvchi**: @{username}\n\n"
        f"🥷 **Versia**: 1.0.1.3\n"
        f"├╴╴╴╴╴╴╴╴╴╴\n"
        f"└ 🧟‍♀️ **{BOT_NAME}** ishlayapti!",
        file=photo if photo else None
    )
    await noob_py.message.delete()
    if photo and os.path.exists(photo):
        os.remove(photo)
