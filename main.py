import asyncio
import os
import datetime
import re
import requests
import threading
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession

# --- CẤU HÌNH HỆ THỐNG ---
API_ID = 34619338
API_HASH = '0f9eb480f7207cf57060f2f35c0ba137'
BOT_TOKEN = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
OWNER_ID = 7153197678 

URL_CHUI = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"

# --- RENDER HEALTH CHECK ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ONLINE")
    def log_message(self, format, *args): return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# --- QUẢN LÝ FILE ---
def _load(f):
    if not os.path.exists(f): return []
    try:
        with open(f, "r", encoding="utf-8") as file: return file.read().splitlines()
    except: return []

def _save(f, d):
    try:
        with open(f, "w", encoding="utf-8") as file: file.write("\n".join(map(str, d)))
    except: pass

# --- KHỞI TẠO ---
ADMINS = set([OWNER_ID])
for a in _load("admins.txt"): 
    if a.strip(): ADMINS.add(int(a))

bot = TelegramClient('bot_manage_session', API_ID, API_HASH)
user_clients = {}
spam_active = {}
user_delays = {}

MENU_TEXT = """𖣘 Hai Quy.   2026 𖣘
🔥 **𝑺𝒑𝒂𝒎 & 𝑻𝒂𝒈**
┣ /sp <id> - Spam chửi
┣ /sp2 <id> - Spam nội dung
┣ /spicon <số> - Spam icon
┣ /spnd <nd> - Spam treo
┣ /spstick <số> - Spam sticker
┣ /spcall <id> - Spam call
┗ /spslow <on/off> - Chế độ spam chậm

☠ **𝑯𝒆‌‌ 𝑻𝒉𝒐‌‌𝒏𝒈 Đ𝒆𝒐 𝑹𝒐‌**
┣ /cam <id> <box> - Câm box
┣ /sua <id> <box> - Gỡ câm
┣ /camib <id> - Câm ib
┗ /suaib <id> - Gỡ câm ib

📦 **𝑳𝒂‌𝒕 𝑽𝒂‌𝒕**
┣ /info <@/id/rep> - Soi trang
┣ /fake <@/id/rep> - Fake người khác
┣ /diefake - Về lại acc gốc
┣ /voice <text> - Voice
┣ /autore <on/off> - Tự thả tim
┣ /off <on/off> - Chế độ bận
┣ /stop - Dừng tất cả
┣ /clear - Xóa 100 tin
┣ /checkkey - Kiểm tra key
┣ /logout - Thoát acc
┗ /setdelay - Chỉnh tốc độ

👤 **ADMIN: Hquy**"""

# --- LỆNH ADMIN ---
@bot.on(events.NewMessage(pattern='/ad'))
async def admin_panel(e):
    if e.sender_id in ADMINS:
        await e.respond("🛠 **ADMIN CONTROL**\n/addadmin <id>\n/taokey <tên> <hạn>\n/tb <nội dung>")

@bot.on(events.NewMessage(pattern=r'/addadmin (\d+)'))
async def add_ad(e):
    if e.sender_id != OWNER_ID: return
    nid = int(e.pattern_match.group(1))
    ADMINS.add(nid); _save("admins.txt", list(ADMINS))
    await e.respond(f"✅ Thêm Admin: `{nid}`")

# --- LỆNH USER ---
@bot.on(events.NewMessage(pattern='/start'))
async def start_cmd(e):
    u = set(_load("users.txt")); u.add(str(e.sender_id)); _save("users.txt", list(u))
    await e.respond(MENU_TEXT)

@bot.on(events.NewMessage(pattern='/login'))
async def login_cmd(e):
    async with bot.conversation(e.sender_id) as conv:
        try:
            await conv.send_message("📱 **SĐT (+84...):**")
            phone = (await conv.get_response()).text.strip()
            client = TelegramClient(StringSession(), API_ID, API_HASH); await client.connect()
            code_req = await client.send_code_request(phone)
            await conv.send_message("📩 **Mã OTP:**")
            otp = (await conv.get_response()).text.strip().replace(".", "")
            await client.sign_in(phone, otp, phone_code_hash=code_req.phone_code_hash)
            user_clients[e.sender_id] = client
            _handle_user_logic(client, e.sender_id)
            await conv.send_message("✅ Đăng nhập hoàn tất!")
        except Exception as ex:
            await conv.send_message(f"❌ Lỗi: {str(ex)}")

def _handle_user_logic(c, uid):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def sp_chui(e):
        target = int(e.pattern_match.group(1))
        spam_active[uid] = True; await e.delete()
        delay = user_delays.get(uid, 0.3)
        while spam_active.get(uid):
            try:
                lines = requests.get(URL_CHUI).text.splitlines()
                for l in lines:
                    if not spam_active.get(uid): break
                    await c.send_message(e.chat_id, f"{l.strip()} [\u200b](tg://user?id={target})")
                    await asyncio.sleep(delay)
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern='/stop'))
    async def stop_all(e):
        spam_active[uid] = False; await e.edit("🛑 Đã dừng toàn bộ spam.")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def set_dl(e):
        user_delays[uid] = float(e.pattern_match.group(1))
        await e.edit(f"✅ Đã chỉnh delay: {user_delays[uid]}s")

# --- KHỞI CHẠY (FIX TRIỆT ĐỂ LỖI LOOP) ---
async def start_system():
    # Chạy Server Health Check
    threading.Thread(target=run_server, daemon=True).start()
    
    # Khởi động Bot Management
    await bot.start(bot_token=BOT_TOKEN)
    print("Hệ thống đã sẵn sàng!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    # Ép buộc tạo loop mới để tương thích với mọi môi trường Python trên Render
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_system())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as err:
        print(f"Lỗi khởi động: {err}")


