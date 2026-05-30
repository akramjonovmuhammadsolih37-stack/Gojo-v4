#!/usr/bin/env python3
"""
GOJO-USERBOT — Asosiy fayl
"""
import sys, os, importlib, glob, asyncio, inspect

class PanelLogger:
    def __init__(self, stream):
        self.stream = stream
    def write(self, msg):
        if msg.strip():
            self.stream.write(msg)
            self.stream.flush()
    def flush(self):
        self.stream.flush()

sys.stdout = PanelLogger(sys.__stdout__)
sys.stderr = PanelLogger(sys.__stderr__)

try:
    from keep_alive import keep_alive
    keep_alive()
    print("[OK] Keep-alive ishga tushdi!")
except Exception as e:
    print(f"[INFO] Keep-alive yo'q: {e}")

import zeus.client
client = zeus.client.client

# ─────────────────────────────────────────
# PLUGIN LOADER
# ─────────────────────────────────────────

SKIP_FILES = {"client.py", "__init__.py", "magic.py", "emojify.py"}

base_dir = os.path.dirname(os.path.abspath(__file__))
plugin_files = sorted(glob.glob(os.path.join(base_dir, "zeus", "*.py")))

loaded = []
failed = []

for filepath in plugin_files:
    filename = os.path.basename(filepath)
    if filename in SKIP_FILES:
        continue

    module_name = f"zeus.{filename[:-3]}"
    try:
        module = importlib.import_module(module_name)

        count = 0

        # METHOD 1: HANDLERS ro'yxati
        if hasattr(module, "HANDLERS"):
            for handler, event in module.HANDLERS:
                client.add_event_handler(handler, event)
                count += 1

        # METHOD 2: vars() orqali barcha ob'ektlarni tekshir
        for attr_name in vars(module):
            obj = getattr(module, attr_name)
            # async funksiya va _events atributi bor
            if callable(obj) and hasattr(obj, "_events"):
                for ev in obj._events:
                    client.add_event_handler(obj, ev)
                    count += 1

        loaded.append(filename)
        print(f"[OK] {filename} ({count} handler)")

    except Exception as e:
        import traceback
        failed.append(filename)
        print(f"[XATO] {filename}: {e}")
        traceback.print_exc()

print(f"\n[INFO] {len(loaded)} plugin yuklandi, {len(failed)} xato")
if failed:
    print(f"[XATO] {', '.join(failed)}")
print("[OK] GOJO-USERBOT tayyor!\n")


async def startup_animation(cl):
    me = await cl.get_me()
    username = f"@{me.username}" if me.username else str(me.id)
    bot_name = os.environ.get("BOT_NAME", "GOJO Userbot")

    frames = [
        "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛",
        "🟦⬛⬛⬛⬛⬛⬛⬛⬛⬛",
        "🟦🟦⬛⬛⬛⬛⬛⬛⬛⬛",
        "🟦🟦🟦⬛⬛⬛⬛⬛⬛⬛",
        "🟦🟦🟦🟦⬛⬛⬛⬛⬛⬛",
        "🟦🟦🟦🟦🟦⬛⬛⬛⬛⬛",
        "🟦🟦🟦🟦🟦🟦⬛⬛⬛⬛",
        "🟦🟦🟦🟦🟦🟦🟦⬛⬛⬛",
        "🟦🟦🟦🟦🟦🟦🟦🟦⬛⬛",
        "🟦🟦🟦🟦🟦🟦🟦🟦🟦⬛",
        "🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦",
    ]

    msg = await cl.send_message("me", "⬛⬛⬛⬛⬛⬛⬛⬛⬛⬛\n`Yuklanmoqda...`")
    for frame in frames:
        await asyncio.sleep(0.35)
        await msg.edit(f"{frame}\n`Yuklanmoqda...`")

    for neon in ["⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️", "✨🌟✨🌟✨🌟✨🌟✨🌟", "💎💠💎💠💎💠💎💠💎💠"]:
        await msg.edit(neon)
        await asyncio.sleep(0.3)

    await msg.edit(
        f"✅ **{bot_name}** muvaffaqiyatli ishga tushirildi!\n\n"
        f"👤 **Foydalanuvchi:** {username}\n"
        f"🔌 **Yuklangan pluginlar:** {len(loaded)}\n"
        f"❌ **Xato pluginlar:** {len(failed)}\n\n"
        f"⚡️ Barcha buyruqlar tayyor!\n"
        f"📖 `.help` — buyruqlar ro'yxati"
    )


async def main():
    await client.start()
    print("[OK] Telegram ga ulandi!")
    try:
        await startup_animation(client)
    except Exception as e:
        print(f"[INFO] Animatsiya xatosi: {e}")
    await client.run_until_disconnected()


asyncio.run(main())
