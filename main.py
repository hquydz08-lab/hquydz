import asyncio
import os
import random
import datetime
import glob
import json
import requests

from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError

# --- THÔNG SỐ CẤU HÌNH ---
API_ID = 34619338
API_HASH = '0f9eb480f7207cf57060f2f35c0ba137'
BOT_TOKEN = '8628695487:AAEV5oHUUMpGon6mFQnXIC7Z5zytnErMEvk
ORIGINAL_ADMIN = 7153197678  # ID của sếp

# File lưu trữ dữ liệu
KEY_DB = "keys_config.json"
USER_DB = "user_expiry.json"
ADMIN_DB = "admins_list.json"

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: return default
    return default

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Khởi tạo dữ liệu
keys_config = load_data(KEY_DB, {})
user_expiry = load_data(USER_DB, {})
admins = load_data(ADMIN_DB, [ORIGINAL_ADMIN])

u_clients = {}
stop_tasks = {}
user_delays = {} 

# --- GIAO DIỆN START (CHO KHÁCH CHƯA NẠP) ---
X_TEXT = """
📣 **𝑿𝑨‌𝑪 𝑻𝑯𝑼‌𝑪 𝑵𝑮𝑼‌𝑶‌𝑰 𝑫𝑼‌𝑵𝑮**
━━━━━━━━━━━━━━━
💰 **𝑩𝑨‌𝑵𝑮 𝑮𝑰𝑨‌**
━━━━━━━━━━━━━━━
🎫 2K/DAY
🎫 10K/WEEK
🎫 20K/MONTH
🎫 70K/VV
━━━━━━━━━━━━━━━
🔑 **𝑽𝒖𝒊 𝒍𝒐‌𝒏𝒈 𝒏𝒉𝒂‌𝒑 𝒌𝒆𝒚 đ𝒆‌ 𝒔𝒖‌ 𝒅𝒖‌𝒏𝒈 𝒃𝒐𝒕**
📝 `/nhapkey <key>`
━━━━━━━━━━━━━━━
👑 **𝑨𝑫𝑴𝑰𝑵:** @hquycute
"""

# --- MENU ADMIN 4 ĐOẠN CHUẨN (THEO HÌNH) ---
AD_MENU = """
👑 **𝑨𝑫𝑴𝑰𝑵 𝑴𝑨𝑺𝑻𝑬𝑹 𝑷𝑨𝑵𝑬𝑳**
━━━━━━━━━━━━━━━
🔑 **𝑸𝑼𝑨‌𝑵 𝑳𝒀 𝑲𝑬𝒀**
┣ `/addkey <tên> <day/week/month/forever>`
┣ `/xoakey <tên>`
┗ `/listkey` - 𝑫𝒂𝒏𝒉 𝒔𝒂‌𝒄𝒉 𝒌𝒆𝒚 𝒄𝒉𝒖‌𝒂 𝒅𝒖‌𝒏𝒈

👥 **𝑸𝑼𝑨‌𝑵 𝑳𝒀 𝑨𝑫𝑴𝑰𝑵**
┣ `/addadm <id>` - 𝑻𝒉𝒆‌𝒎 𝑨𝒅𝒎𝒊𝒏 𝒎𝒐‌𝒊
┗ `/xoaadm <id>` - 𝑿𝒐‌𝒂 𝑨𝒅𝒎𝒊𝒏

📊 **𝑯𝑬‌ 𝑻𝑯𝑶‌𝑵𝑮**
┣ `/stats` - 𝑻𝒉𝒐‌𝒏𝒈 𝒌𝒆‌ 𝒏𝒈𝒖‌𝒐‌𝒊 𝒅𝒖‌𝒏𝒈
┗ `/broadcast <nội dung>` - 𝑻𝒉𝒐‌𝒏𝒈 𝒃𝒂‌𝒐

ℹ️ **𝑻𝑯𝑶‌𝑵𝑮 𝑻𝑰𝑵**
┣ **Admin gốc:** `7153197678`
┗ **Phiên bản:** `Master Key 2026`
━━━━━━━━━━━━━━━
"""

# --- MENU WAR 3 ĐOẠN CHUẨN ---
M_TEXT = """
⚠️ **𝑾𝑨𝑹𝑵𝑰𝑵𝑮: 𝑩𝑨‌𝑵 𝑸𝑼𝒀𝑬‌𝑵 𝑻𝑯𝑼𝑶‌𝑪 𝑽𝑬‌ 𝑯𝑸𝒀**

. 　˚　. . ✦˚ .     　　˚　　　　✦　.
𖣘 𝑯𝒂𝒊 𝑸𝒖𝒚.   𝟐𝟎𝟐𝟔 𖣘
.  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.

🔥 **𝑼𝑺𝑬𝑹𝑩𝑶𝑻 (𝑺𝑷𝑨𝑴 & 𝑻𝑨𝑮)**
┣ ⚡️ `/sp <id>` - 𝑺𝒑𝒂𝒎 𝒄𝒉𝒖‌𝒊
┣ 📝 `/sp2 <id>` - 𝑺𝒑𝒂𝒎 𝒏𝒐‌𝒊 𝒅𝒖𝒏𝒈
┣ 🤡 `/spicon <số>` - 𝑺𝒑𝒂𝒎 𝒊𝒄𝒐𝒏
┣ 📌 `/spnd <nd>` - 𝑺𝒑𝒂𝒎 𝒕𝒓𝒆𝒐
┣ 🎭 `/spstick <số>` - 𝑺𝒑𝒂𝒎 𝒔𝒕𝒊𝒄𝒌𝒆𝒓
┣ 📞 `/spcall <id>` - 𝑺𝒑𝒂𝒎 𝒄𝒂𝒍𝒍
┣ 🐌 `/spslow <on/off>` - 𝑪𝒉𝒆‌ đ𝒐‌ 𝒔𝒍𝒐𝒘
┣ 🎤 `/voice <nd>` - 𝑽𝒐𝒊𝒄𝒆 𝑨𝑰
┣ 💖 `/autore <on/off>` - 𝑻𝒖‌ đ𝒐‌𝒏𝒈 𝒕𝒉𝒂‌ 𝒕𝒊𝒎
┗ 🛑 `/stop` - 𝑫𝒖‌𝒏𝒈 𝒕𝒂‌𝒕 𝒄𝒂‌

☠ **𝑯𝑬‌ 𝑻𝑯𝑶‌𝑵𝑮 Đ𝑬𝑶 𝑹𝑶‌**
┣ 🔇 `/cam <id> <box>` - 𝑪𝒂‌𝒎 𝒃𝒐𝒙
┣ 🔊 `/sua <id> <box>` - 𝑮𝒐‌ 𝒄𝒂‌𝒎
┣ 😶 `/camib <id>` - 𝑪𝒂‌𝒎 𝒊𝒃
┣ 🗣 `/suaib <id>` - 𝑮𝒐‌ 𝒄𝒂‌𝒎 𝒊𝒃
┣ 🔍 `/info` - 𝑺𝒐𝒊 𝒊𝒏𝒇𝒐
┣ 🎭 `/fake <id>` - 𝑭𝒂𝒌𝒆 𝒏𝒈𝒖‌𝒐‌𝒊
┣ 🔙 `/diefake` - 𝑽𝒆‌ 𝒈𝒐‌𝒄
┣ 💤 `/off <on/off>` - 𝑩𝒂‌𝒏 𝒐𝒇𝒇
┣ 📝 `/setoff <nd>` - Đ𝒂‌𝒕 𝒕𝒊𝒏 𝒏𝒉𝒂‌𝒏 𝒐𝒇𝒇
┗ ❌ `/deloff` - 𝑿𝒐‌𝒂 𝒕𝒊𝒏 𝒏𝒉𝒂‌𝒏 𝒐𝒇𝒇

⚙️ **𝑩𝑶𝑻 𝑴𝑨𝑵𝑨𝑮𝑬𝑹**
┣ 📱 `/login` - Đ𝒂‌𝒏𝒈 𝒏𝒉𝒂‌𝒑
┣ 🚪 `/logout` - Đ𝒂‌𝒏𝒈 𝒙𝒖𝒂‌𝒕
┣ 🧹 `/clear` - 𝑿𝒐‌𝒂 𝒕𝒊𝒏 𝒏𝒉𝒂‌𝒏
┣ 🧹 `/clear2` - 𝑿𝒐‌𝒂 𝒕𝒊𝒏 𝒃𝒐𝒕
┣ 📊 `/checkmode` - 𝑲𝒊𝒆‌𝒎 𝒕𝒓𝒂 𝒎𝒐𝒅𝒆
┣ 🔑 `/checkkey` - 𝑲𝒊𝒆‌𝒎 𝒕𝒓𝒂 𝒌𝒆𝒚
┗ ⏳ `/setdelay <giây>` - 𝑪𝒉𝒊‌𝒏𝒉 𝒕𝒐‌𝒄 đ𝒐‌

👤 **𝑨𝑫𝑴𝑰𝑵:** [𝙃𝑸𝑼𝒀](tg://user?id=7153197678)
"""

bot = TelegramClient('bot_manage', API_ID, API_HASH)

def is_active(user_id):
    expiry_str = user_expiry.get(str(user_id))
    if not expiry_str: return False
    return datetime.datetime.now() < datetime.datetime.fromisoformat(expiry_str)

# --- XỬ LÝ LỆNH ADMIN ---
@bot.on(events.NewMessage(pattern='/ad'))
async def admin_menu_handler(e):
    if e.sender_id in admins:
        await e.respond(AD_MENU)

@bot.on(events.NewMessage(pattern=r'/addadm (\d+)'))
async def add_admin_handler(e):
    if e.sender_id not in admins: return
    new_id = int(e.pattern_match.group(1))
    if new_id not in admins:
        admins.append(new_id)
        save_data(ADMIN_DB, admins)
        await e.respond(f"✅ Đã thêm Admin: `{new_id}`")
    else:
        await e.respond("❌ ID này đã là Admin rồi.")

@bot.on(events.NewMessage(pattern=r'/xoaadm (\d+)'))
async def xoa_admin_handler(e):
    if e.sender_id not in admins: return
    del_id = int(e.pattern_match.group(1))
    if del_id == ORIGINAL_ADMIN:
        return await e.respond("⚠️ Không thể xóa Admin gốc!")
    if del_id in admins:
        admins.remove(del_id)
        save_data(ADMIN_DB, admins)
        await e.respond(f"🗑 Đã xóa Admin: `{del_id}`")

@bot.on(events.NewMessage(pattern=r'/addkey (\w+) (day|week|month|forever)'))
async def add_key_handler(e):
    if e.sender_id not in admins: return
    k, t = e.pattern_match.group(1), e.pattern_match.group(2)
    keys_config[k] = t
    save_data(KEY_DB, keys_config)
    await e.respond(f"✅ Đã tạo key: `{k}` loại `{t.upper()}`")

@bot.on(events.NewMessage(pattern=r'/xoakey (\w+)'))
async def xoa_key_handler(e):
    if e.sender_id not in admins: return
    k = e.pattern_match.group(1)
    if k in keys_config:
        del keys_config[k]
        save_data(KEY_DB, keys_config)
        await e.respond(f"🗑 Đã xóa key: `{k}`")

# --- LOGIC USERBOT ---
def setup_user_logic(client, user_id):
    @client.on(events.NewMessage(outgoing=True))
    async def global_check(e):
        if not is_active(user_id):
            await e.edit("⚠️ **𝑯𝑬‌𝑻 𝑯𝑨‌𝑵!** Liên hệ Admin để gia hạn.")
            await client.log_out()

    @client.on(events.NewMessage(outgoing=True, pattern='/checkkey'))
    async def check_key_user(e):
        exp = datetime.datetime.fromisoformat(user_expiry[str(user_id)])
        t = "𝑽𝑰𝑵𝑯 𝑽𝑰𝑬‌𝑵" if exp.year > 9000 else exp.strftime('%d/%m/%Y %H:%M')
        await e.edit(f"🔑 **𝑻𝒉𝒐‌𝒊 𝒉𝒂‌𝒏:** `{t}`")

    @client.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def set_delay_user(e):
        user_delays[user_id] = float(e.pattern_match.group(1))
        await e.edit(f"⏳ **𝑻𝒐‌𝒄 đ𝒐‌:** `{user_delays[user_id]}s`")

    @client.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def sp_war(e):
        target = int(e.pattern_match.group(1)); await e.delete()
        stop_tasks[user_id] = False
        try:
            lines = requests.get("https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt").text.splitlines()
        except: lines = ["War mạnh lên sếp!"]
        while not stop_tasks.get(user_id):
            d = user_delays.get(user_id, 0.05)
            for m in lines:
                if stop_tasks.get(user_id): break
                try:
                    await client.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={target})")
                    await asyncio.sleep(d)
                except: break

    @client.on(events.NewMessage(outgoing=True, pattern='/stop'))
    async def stop_war(e):
        stop_tasks[user_id] = True; await e.edit("🛑 **𝑫𝑼‌𝑵𝑮!**")

# --- XỬ LÝ NHẬP KEY & LOGIN ---
@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def nhap_key_logic(e):
    k = e.pattern_match.group(1).strip()
    if k in keys_config:
        k_type = keys_config[k]
        now = datetime.datetime.now()
        days = {"day":1, "week":7, "month":30, "forever":36500}[k_type]
        expiry = now + datetime.timedelta(days=days)
        user_expiry[str(e.sender_id)] = expiry.isoformat()
        del keys_config[k]; save_data(KEY_DB, keys_config); save_data(USER_DB, user_expiry)
        await e.respond(f"✅ **𝑵𝒂𝒑 𝒕𝒉𝒂‌𝒏𝒉 𝒄𝒐‌𝒏𝒈:** `{k_type.upper()}`", buttons=[[Button.inline("📱 LOGIN ACC WAR", data="login")]])
    else:
        await e.respond("❌ Key sai hoặc đã được sử dụng.")

@bot.on(events.CallbackQuery(data="login"))
async def login_callback_handler(e):
    if not is_active(e.sender_id): return
    async with bot.conversation(e.sender_id) as cv:
        await cv.send_message("📞 Nhập SĐT (+84...):")
        phone = (await cv.get_response()).text.strip()
        c = TelegramClient(f"u_{e.sender_id}", API_ID, API_HASH)
        await c.connect()
        if not await c.is_user_authorized():
            res = await c.send_code_request(phone)
            await cv.send_message("🔐 Nhập OTP:")
            otp = (await cv.get_response()).text.strip()
            try: await c.sign_in(phone, otp, phone_code_hash=res.phone_code_hash)
            except:
                await cv.send_message("🔑 Nhập 2FA:")
                await c.sign_in(password=(await cv.get_response()).text.strip())
        me = await c.get_me()
        u_clients[me.id] = c; setup_user_logic(c, me.id)
        await cv.send_message(f"✅ Đã login: {me.first_name}")

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler_bot(e):
    if not e.out: await e.respond(X_TEXT)
    else: await e.edit(M_TEXT)

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    for f in glob.glob("u_*.session"):
        try:
            uid = int(f.split('_')[1].split('.')[0])
            if is_active(uid):
                c = TelegramClient(f.replace(".session",""), API_ID, API_HASH)
                await c.connect()
                if await c.is_user_authorized():
                    me = await c.get_me()
                    u_clients[me.id] = c; setup_user_logic(c, me.id)
        except: pass
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
