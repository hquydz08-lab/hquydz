import asyncio
import os
import datetime
import glob
import json
import requests

from telethon import TelegramClient, events, Button
from telethon.errors import FloodWaitError, SessionPasswordNeededError

# ================== CONFIG ==================
API_ID = 34619338
API_HASH = '0f9eb480f7207cf57060f2f35c0ba137'
BOT_TOKEN = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
ORIGINAL_ADMIN = 7153197678

KEY_DB = "keys_config.json"
USER_DB = "user_expiry.json"
ADMIN_DB = "admins_list.json"

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except: 
            return default
    return default

def save_data(file, data):
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except: pass

keys_config = load_data(KEY_DB, {})
user_expiry = load_data(USER_DB, {})
admins = load_data(ADMIN_DB, [ORIGINAL_ADMIN])

u_clients = {}
stop_tasks = {}
user_delays = {}

# ================== MENU ADMIN (CHUẨN ẢNH) ==================
AD_MENU = """
👑 **ADMIN MASTER PANEL**
━━━━━━━━━━━━━━━━━━

🔑 **QUAN LÝ KEY**
┣ `/addkey <tên> <day/week/month/forever>`
┣ `/xoakey <tên>`
┗ `/listkey` - Danh sách key chưa dùng

👥 **QUAN LÝ ADMIN**
┣ `/addadm <id>` - Thêm Admin mới
┗ `/xoaadm <id>` - Xóa Admin

📊 **HỆ THỐNG**
┣ `/stats` - Thống kê người dùng
┗ `/broadcast <nội dung>` - Thông báo

ℹ️ **THÔNG TIN**
┣ **Admin gốc:** `7153197678`
┗ **Phiên bản:** `Master Key 2026`
━━━━━━━━━━━━━━━━━━
"""

# ================== MENU WAR (HÀNG DỌC) ==================
M_TEXT = """
⚠️ **WARNING: BẠN QUYỀN THUỘC VỀ HQY**

. 　˚　. . ✦˚ .     　　˚　　　　✦　.
𖣘 𝑯𝒂𝒊 𝑸𝒖𝒚.   𝟐𝟎𝟐𝟔 𖣘
.  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.

🔥 **USERBOT (SPAM & TAG)**
┣ ⚡️ `/sp <id>` - Spam chửi
┣ 📝 `/sp2 <id>` - Spam nội dung
┣ 🤡 `/spicon <số>` - Spam icon
┣ 📌 `/spnd <nd>` - Spam treo
┣ 🎭 `/spstick <số>` - Spam sticker
┣ 📞 `/spcall <id>` - Spam call
┣ 🐌 `/spslow <on/off>` - Chế độ slow
┣ 🎤 `/voice <nd>` - Voice AI
┣ 💖 `/autore <on/off>` - Tự động tha tim
┗ 🛑 `/stop` - Dừng tất cả

☠ **HỆ THỐNG ĐEO RO**
┣ 🔇 `/cam <id> <box>` - Cam box
┣ 🔊 `/sua <id> <box>` - Gỡ cam
┣ 😶 `/camib <id>` - Cam ib
┣ 🗣 `/suaib <id>` - Gỡ cam ib
┣ 🔍 `/info` - Soi info
┣ 🎭 `/fake <id>` - Fake người
┣ 🔙 `/diefake` - Về gốc
┣ 💤 `/off <on/off>` - Ban off
┣ 📝 `/setoff <nd>` - Đặt tin nhắn off
┗ ❌ `/deloff` - Xóa tin nhắn off

⚙️ **BOT MANAGER**
┣ 📱 `/login` - Đăng nhập
┣ 🚪 `/logout` - Đăng xuất
┣ 🧹 `/clear` - Xóa tin nhắn
┣ 🧹 `/clear2` - Xóa tin bot
┣ 📊 `/checkmode` - Kiểm tra mode
┣ 🔑 `/checkkey` - Kiểm tra key
┗ ⏳ `/setdelay <giây>` - Chỉnh tốc độ
"""

X_TEXT = """📣 **XÁC THỰC NGƯỜI DÙNG** ..."""  # mày tự điền đầy đủ nếu cần

bot = TelegramClient('bot_manage', API_ID, API_HASH)

def is_active(user_id):
    expiry_str = user_expiry.get(str(user_id))
    if not expiry_str: return False
    try:
        return datetime.datetime.now() < datetime.datetime.fromisoformat(expiry_str)
    except: return False

# ====================== ADMIN COMMANDS ======================
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

# ====================== USERBOT ======================
def setup_user_logic(client, user_id):
    @client.on(events.NewMessage(outgoing=True))
    async def global_check(e):
        if not is_active(user_id):
            try:
                await e.edit("⚠️ **HẾT HẠN!** Liên hệ @hquycute")
                await client.log_out()
            except: pass

    @client.on(events.NewMessage(outgoing=True, pattern='/checkkey'))
    async def check_key(e):
        try:
            exp = datetime.datetime.fromisoformat(user_expiry[str(user_id)])
            t = "VĨNH VIỄN" if exp.year > 9000 else exp.strftime('%d/%m/%Y %H:%M')
            await e.edit(f"🔑 **Thời hạn:** `{t}`")
        except:
            await e.edit("❌ Chưa có key.")

    @client.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def set_delay(e):
        user_delays[user_id] = float(e.pattern_match.group(1))
        await e.edit(f"⏳ **Delay:** `{user_delays[user_id]}s`")

    @client.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def sp_war(e):
        target = int(e.pattern_match.group(1))
        await e.delete()
        stop_tasks[user_id] = False
        try:
            r = requests.get("https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt", timeout=10)
            lines = r.text.splitlines() if r.status_code == 200 else ["War..."]
        except:
            lines = ["War..."]
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
        stop_tasks[user_id] = True
        await e.edit("🛑 **𝑫𝑼‌𝑵𝑮!**")

    # ================== LỆNH VOICE AI ==================
    @client.on(events.NewMessage(outgoing=True, pattern=r'/voice (.+)'))
    async def voice_cmd(e):
        text = e.pattern_match.group(1).strip()
        if not text:
            return await e.edit("❌ Vui lòng nhập nội dung cần đọc.")
        if len(text) > 500:
            return await e.edit("❌ Nội dung quá dài (tối đa 500 ký tự).")

        await e.edit("🔄 Đang tạo giọng nói AI...")

        try:
            from gtts import gTTS
            import io

            tts = gTTS(text=text, lang='vi', slow=False)
            voice_bytes = io.BytesIO()
            tts.write_to_fp(voice_bytes)
            voice_bytes.seek(0)

            await client.send_file(
                e.chat_id,
                voice_bytes,
                voice_note=True,
                caption=f"🔊 Voice AI\n\n{text[:100]}{'...' if len(text) > 100 else ''}"
            )
            await e.delete()
        except Exception as err:
            await e.edit(f"❌ Lỗi tạo voice: {err}")

    print(f"✅ Userbot {user_id} loaded!")
# ====================== KEY + LOGIN ======================
@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def nhap_key_logic(e):
    k = e.pattern_match.group(1).strip()
    if k in keys_config:
        k_type = keys_config[k]
        days = {"day":1, "week":7, "month":30, "forever":36500}[k_type]
        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        user_expiry[str(e.sender_id)] = expiry.isoformat()
        del keys_config[k]
        save_data(KEY_DB, keys_config)
        save_data(USER_DB, user_expiry)
        await e.respond(f"✅ **NẠP THÀNH CÔNG:** `{k_type.upper()}`", 
                        buttons=[[Button.inline("📱 LOGIN ACC WAR", data="login")]])
    else:
        await e.respond("❌ Key sai hoặc đã được sử dụng.")

@bot.on(events.CallbackQuery(data="login"))
async def login_callback_handler(e):
    if not is_active(e.sender_id):
        return await e.answer("Key đã hết hạn!", alert=True)
    
    async with bot.conversation(e.sender_id) as cv:
        await cv.send_message("📞 Nhập SĐT (+84...):")
        phone = (await cv.get_response()).text.strip()
        c = TelegramClient(f"u_{e.sender_id}", API_ID, API_HASH)
        await c.connect()
        if not await c.is_user_authorized():
            res = await c.send_code_request(phone)
            await cv.send_message("🔐 Nhập OTP:")
            otp = (await cv.get_response()).text.strip()
            try:
                await c.sign_in(phone, otp, phone_code_hash=res.phone_code_hash)
            except SessionPasswordNeededError:
                await cv.send_message("🔑 Nhập 2FA:")
                await c.sign_in(password=(await cv.get_response()).text.strip())
            except Exception as err:
                await cv.send_message(f"❌ Lỗi: {err}")
                return
        me = await c.get_me()
        u_clients[me.id] = c
        setup_user_logic(c, me.id)
        await cv.send_message(f"✅ Đã login: {me.first_name}")

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler_bot(e):
    if not e.out: 
        await e.respond(X_TEXT)
    else: 
        await e.edit(M_TEXT)

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("✅ Bot War Master 2026 Started!")

    for f in glob.glob("u_*.session"):
        try:
            uid = int(f.split('_')[1].split('.')[0])
            if is_active(uid):
                c = TelegramClient(f.replace(".session",""), API_ID, API_HASH)
                await c.connect()
                if await c.is_user_authorized():
                    me = await c.get_me()
                    u_clients[me.id] = c
                    setup_user_logic(c, me.id)
        except: pass
            
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
