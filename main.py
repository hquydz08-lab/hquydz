import asyncio
import os
import datetime
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
URL_SPAM2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# --- RENDER PORT FIX ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ALIVE")
    def log_message(self, format, *args): return

def run_server():
    try:
        port = int(os.environ.get("PORT", 10000))
        server = HTTPServer(('0.0.0.0', port), HealthCheck)
        server.serve_forever()
    except: pass

# --- DATABASE ---
def _load(f):
    if not os.path.exists(f): return []
    try:
        with open(f, "r", encoding="utf-8") as file: return file.read().splitlines()
    except: return []

def _save(f, d):
    try:
        with open(f, "w", encoding="utf-8") as file: file.write("\n".join(map(str, d)))
    except: pass

# --- KHỞI TẠO BIẾN ---
ADMINS = set([OWNER_ID])
for a in _load("admins.txt"): 
    if a.strip(): ADMINS.add(int(a))

user_clients = {}
spam_tasks = {}
user_delays = {}

MENU = """𖣘 Hai Quy.   2026 𖣘
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

👤 **ADMIN: Hquy** (Gõ /ad để quản lý)"""

# --- LOGIC BOT ---
async def start_everything():
    # Khởi tạo client bot chính
    bot = TelegramClient('bot_manage_session', API_ID, API_HASH)

    @bot.on(events.NewMessage(pattern='/start'))
    async def _st(e):
        u = set(_load("users.txt")); u.add(str(e.sender_id)); _save("users.txt", list(u))
        await e.respond(MENU)

    @bot.on(events.NewMessage(pattern='/ad'))
    async def _ad(e):
        if e.sender_id in ADMINS:
            await e.respond("🛠 **ADMIN PANEL**\n/addadmin <id>\n/tb <nội dung>")

    @bot.on(events.NewMessage(pattern='/login'))
    async def _lg(e):
        async with bot.conversation(e.sender_id) as cv:
            try:
                await cv.send_message("📱 **SĐT (+84...):**")
                p = (await cv.get_response()).text.strip()
                c = TelegramClient(StringSession(), API_ID, API_HASH); await c.connect()
                r = await c.send_code_request(p)
                await cv.send_message("📩 **OTP:**")
                o = (await cv.get_response()).text.strip().replace(".", "")
                await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
                user_clients[e.sender_id] = c
                _handle_logic(c, e.sender_id)
                await cv.send_message("✅ LOGIN THÀNH CÔNG!")
            except Exception as ex: await cv.send_message(f"❌ Lỗi: {str(ex)}")

    def _handle_logic(c, ui):
        @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
        async def _sp(e):
            t = int(e.pattern_match.group(1)); spam_tasks[ui] = True; await e.delete()
            d = user_delays.get(ui, 0.3)
            while spam_tasks.get(ui):
                try:
                    res = requests.get(URL_CHUI, timeout=5)
                    for line in res.text.splitlines():
                        if not spam_tasks.get(ui): break
                        await c.send_message(e.chat_id, f"{line.strip()} [\u200b](tg://user?id={t})")
                        await asyncio.sleep(d)
                except: break

        @c.on(events.NewMessage(outgoing=True, pattern='/stop'))
        async def _st(e): 
            spam_tasks[ui] = False; await e.edit("🛑 ĐÃ DỪNG.")

    # Khởi động Web Server (giữ port Render)
    threading.Thread(target=run_server, daemon=True).start()

    # Chạy bot
    await bot.start(bot_token=BOT_TOKEN)
    print("Bot is Online and Ready!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    # Đây là "thuốc đặc trị" cho lỗi No Event Loop trên Python đời cao
    try:
        asyncio.run(start_everything())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        print(f"Lỗi khởi động: {e}")


