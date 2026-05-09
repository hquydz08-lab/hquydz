import asyncio
import os
import random
import datetime
import glob
import json

from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError

# --- THÔNG SỐ CẤU HÌNH ---
API_ID = 34619338
API_HASH = '0f9eb480f7207cf57060f2f35c0ba137'
BOT_TOKEN = '8628695487:AAEV5oHUUMpGon6mFQnXIC7Z5zytnErMEvk'
ORIGINAL_ADMIN = 7153197678  # ID gốc của sếp (Bất tử)

# File lưu trữ dữ liệu
KEY_DB = "keys_config.json"
USER_DB = "user_expiry.json"
ADMIN_DB = "admins_list.json"

def load_data(file, default):
    try:
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                return json.loads(content) if content else default
    except Exception as e:
        print(f"Lỗi đọc file {file}: {e}")
    return default

def save_data(file, data):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Lỗi ghi file {file}: {e}")

# Khởi tạo dữ liệu ban đầu
keys_config = load_data(KEY_DB, {})
user_expiry = load_data(USER_DB, {})
admins = load_data(ADMIN_DB, [ORIGINAL_ADMIN])
if ORIGINAL_ADMIN not in admins:
    admins.append(ORIGINAL_ADMIN)
    save_data(ADMIN_DB, admins)

u_clients = {}
stop_tasks = {}
user_delays = {} 

# --- GIAO DIỆN ---
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
"""

AD_TEXT = """
👑 **𝑴𝑬𝑵𝑼 𝑸𝑼𝑨‌𝑵 𝑻𝑹𝑰 𝑨𝑫𝑴𝑰𝑵**
━━━━━━━━━━━━━━━
🔑 **𝑸𝑼𝑨‌𝑵 𝑳𝒀 𝑲𝑬𝒀**
┣ `/addkey <tên> <day/week/month/forever>`
┣ `/xoakey <tên>`
┗ `/listkey` - 𝑫𝒂𝒏𝒉 𝒔𝒂‌𝒄𝒉 𝒌𝒆𝒚 𝒄𝒉𝒖‌𝒂 𝒅𝒖‌𝒏𝒈

👥 **𝑸𝑼𝑨‌𝑵 𝑳𝒀 𝑵𝑯𝑨‌𝑵 𝑺𝑼‌**
┣ `/addadm <id>` - 𝑻𝒉𝒆‌𝒎 𝑨𝒅𝒎𝒊𝒏 𝒎𝒐‌𝒊
┗ `/xoaadm <id>` - 𝑿𝒐‌𝒂 𝑨𝒅𝒎𝒊𝒏

📊 **𝑯𝑬‌ 𝑻𝑯𝑶‌𝑵𝑮**
┣ `/stats` - 𝑻𝒉𝒐‌𝒏𝒈 𝒌𝒆‌ 𝒏𝒈𝒖‌𝒐‌𝒊 𝒅𝒖‌𝒏𝒈
┗ `/broadcast <nội dung>` - 𝑻𝒉𝒐‌𝒏𝒈 𝒃𝒂‌𝒐
━━━━━━━━━━━━━━━
"""

bot = TelegramClient('bot_manage', API_ID, API_HASH)

def is_active(user_id):
    expiry_str = user_expiry.get(str(user_id))
    if not expiry_str: return False
    expiry = datetime.datetime.fromisoformat(expiry_str)
    return datetime.datetime.now() < expiry

# --- LỆNH ADMIN MASTER ---
@bot.on(events.NewMessage(pattern='/ad'))
async def admin_menu(e):
    if e.sender_id not in admins: return
    await e.respond(AD_TEXT)

@bot.on(events.NewMessage(pattern=r'/addadm (\d+)'))
async def add_admin(e):
    if e.sender_id not in admins: return
    new_id = int(e.pattern_match.group(1))
    if new_id not in admins:
        admins.append(new_id)
        save_data(ADMIN_DB, admins)
        await e.respond(f"✅ Đã thêm Admin: `{new_id}`")
    else:
        await e.respond("❌ ID này đã là Admin.")

@bot.on(events.NewMessage(pattern=r'/xoaadm (\d+)'))
async def xoa_admin(e):
    if e.sender_id not in admins: return
    del_id = int(e.pattern_match.group(1))
    if del_id == ORIGINAL_ADMIN:
        return await e.respond("⚠️ Không thể xóa Admin gốc!")
    if del_id in admins:
        admins.remove(del_id)
        save_data(ADMIN_DB, admins)
        await e.respond(f"🗑 Đã xóa Admin: `{del_id}`")
    else:
        await e.respond("❌ Không tìm thấy Admin này.")

@bot.on(events.NewMessage(pattern=r'/addkey (\w+) (day|week|month|forever)'))
async def add_key(e):
    if e.sender_id not in admins: return
    k_name, k_type = e.pattern_match.group(1), e.pattern_match.group(2)
    keys_config[k_name] = k_type
    save_data(KEY_DB, keys_config)
    await e.respond(f"✅ Đã tạo key: `{k_name}` ({k_type.upper()})")

@bot.on(events.NewMessage(pattern=r'/xoakey (\w+)'))
async def xoa_key(e):
    if e.sender_id not in admins: return
    k_name = e.pattern_match.group(1)
    if k_name in keys_config:
        del keys_config[k_name]
        save_data(KEY_DB, keys_config)
        await e.respond(f"🗑 Đã xóa key: `{k_name}`")
    else:
        await e.respond("❌ Không tìm thấy key.")

@bot.on(events.NewMessage(pattern='/listkey'))
async def list_key(e):
    if e.sender_id not in admins: return
    if not keys_config: return await e.respond("Hệ thống chưa có key.")
    msg = "🔑 **KEY CHƯA DÙNG:**\n" + "\n".join([f"┣ `{k}`: {v.upper()}" for k, v in keys_config.items()])
    await e.respond(msg)

# --- LOGIC NGƯỜI DÙNG & WAR ---
def setup_user_logic(client, user_id):
    @client.on(events.NewMessage(outgoing=True))
    async def guard(e):
        if not is_active(user_id):
            await e.edit("⚠️ **𝑯𝑬‌𝑻 𝑯𝑨‌𝑵!** Liên hệ @hquycute.")
            await client.log_out()

    @client.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def sd(e):
        user_delays[user_id] = float(e.pattern_match.group(1))
        await e.edit(f"⏳ **𝑫𝒆𝒍𝒂𝒚:** `{user_delays[user_id]}s`")

    @client.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def sp(e):
        target = int(e.pattern_match.group(1)); await e.delete()
        stop_tasks[user_id] = False
        lines = open('chui.txt','r',encoding='utf-8').readlines() if os.path.exists('chui.txt') else ["Hết chửi rồi sếp ơi!"]
        while not stop_tasks.get(user_id):
            d = user_delays.get(user_id, 0.05)
            for m in lines:
                if stop_tasks.get(user_id): break
                try:
                    await client.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={target})")
                    await asyncio.sleep(d)
                except: break

    @client.on(events.NewMessage(outgoing=True, pattern='/stop'))
    async def st(e):
        stop_tasks[user_id] = True
        await e.edit("🛑 **𝑫𝑼‌𝑵𝑮 𝑻𝑨‌𝑻 𝑪𝑨‌!**")

# --- LOGIN & NHẬP KEY ---
@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def nhapkey(e):
    k = e.pattern_match.group(1).strip()
    if k in keys_config:
        k_type = keys_config[k]
        now = datetime.datetime.now()
        days = {"day":1, "week":7, "month":30, "forever":36500}[k_type]
        expiry = now + datetime.timedelta(days=days)
        user_expiry[str(e.sender_id)] = expiry.isoformat()
        del keys_config[k]
        save_data(KEY_DB, keys_config); save_data(USER_DB, user_expiry)
        await e.respond(f"✅ **𝑲𝑰𝑪𝑯 𝑯𝑶𝑨‌𝑻:** `{k_type.upper()}`\n📅 Hạn: `{expiry.strftime('%d/%m/%Y') if days < 30000 else 'VĨNH VIỄN'}`",
                        buttons=[[Button.inline("📱 LOGIN ACC WAR", data="login")]])
    else:
        await e.respond("❌ Key sai hoặc đã dùng.")

@bot.on(events.CallbackQuery(data="login"))
async def login_cb(e):
    if not is_active(e.sender_id): return await e.answer("Hết hạn!", alert=True)
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
async def start(e):
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
