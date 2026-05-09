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
import edge_tts

# --- CẤU HÌNH HỆ THỐNG ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# --- SERVER HEALTH CHECK (NGĂN RENDER STATUS 1) ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"BOT STATUS: ACTIVE & GREEN")
    def log_message(self, format, *args): return

def run_port_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    print(f"Health server started on port {port}")
    server.serve_forever()

# --- QUẢN LÝ DỮ LIỆU ---
def _load_list(f):
    if not os.path.exists(f): return []
    try:
        with open(f, "r", encoding="utf-8") as file: return file.read().splitlines()
    except: return []

def _save_list(f, data):
    try:
        with open(f, "w", encoding="utf-8") as file: file.write("\n".join(map(str, data)))
    except: pass

def _load_keys():
    if not os.path.exists("keys.txt"): return {}
    keys = {}
    try:
        with open("keys.txt", "r", encoding="utf-8") as f:
            for line in f:
                if "|" in line:
                    k, exp = line.strip().split("|")
                    keys[k] = exp if exp == "forever" else datetime.datetime.fromisoformat(exp)
    except: pass
    return keys

def _save_keys(keys):
    try:
        with open("keys.txt", "w", encoding="utf-8") as f:
            for k, exp in keys.items():
                val = exp if exp == "forever" else exp.isoformat()
                f.write(f"{k}|{val}\n")
    except: pass

# --- KHỞI TẠO ---
ADMINS = set([O_ID])
for a in _load_list("admins.txt"): 
    if a.strip(): ADMINS.add(int(a))

bot = TelegramClient('bot_manage_session', A_ID, A_HS)
u_c, s_t, d_l, s_l = {}, {}, {}, {}

M_T = """. 　˚　. . ✦˚ .     　　˚　　　　✦　.
𖣘 Hai Quy.   2026 𖣘
.  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.

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
┣ /diefake - về lại acc gốc
┣ /voice <text> - Voice
┣ /autore <on/off> - Tự động thả tim
┣ /off <on/off> - Chế độ bận
┣ /stop - Dừng tất cả
┣ /clear - Xóa 100 tin nhắn
┣ /checkkey - Kiểm tra key
┣ /logout - Thoát acc
┗ /setdelay - Chỉnh tốc độ

👤 **ADMIN: Hquy**"""

# --- LOGIC ADMIN ---
@bot.on(events.NewMessage(pattern='/ad'))
async def _ad(e):
    if e.sender_id in ADMINS:
        msg = "🛠 **ADMIN PANEL**\n/taokey <tên> <day/week/month/forever>\n/xoakey <tên>\n/addadmin <id>\n/deladmin <id>\n/tb <nội dung>"
        await e.respond(msg)

@bot.on(events.NewMessage(pattern=r'/addadmin (\d+)'))
async def _aa(e):
    if e.sender_id != O_ID: return
    nid = int(e.pattern_match.group(1))
    ADMINS.add(nid); _save_list("admins.txt", list(ADMINS))
    await e.respond(f"✅ Đã thêm Admin: `{nid}`")

@bot.on(events.NewMessage(pattern=r'/taokey (.+) (day|week|month|forever)'))
async def _tk(e):
    if e.sender_id not in ADMINS: return
    k, t = e.pattern_match.group(1).strip(), e.pattern_match.group(2)
    now = datetime.datetime.now()
    exp = (now + datetime.timedelta(days=1) if t=='day' else 
           now + datetime.timedelta(weeks=1) if t=='week' else 
           now + datetime.timedelta(days=30) if t=='month' else "forever")
    ks = _load_keys(); ks[k] = exp; _save_keys(ks)
    await e.respond(f"🔑 Tạo Key `{k}` ({t}) thành công!")

@bot.on(events.NewMessage(pattern=r'/tb (.+)'))
async def _tb(e):
    if e.sender_id not in ADMINS: return
    msg = e.pattern_match.group(1)
    for uid in _load_list("users.txt"):
        try: await bot.send_message(int(uid), f"📢 **TB Admin:** {msg}")
        except: pass
    await e.respond("✅ Đã gửi thông báo!")

# --- LOGIC NGƯỜI DÙNG ---
@bot.on(events.NewMessage(pattern='/start'))
async def _start(ev):
    us = set(_load_list("users.txt")); us.add(str(ev.sender_id)); _save_list("users.txt", list(us))
    await ev.respond(M_T)

@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nk(e):
    kin = e.pattern_match.group(1).strip()
    ks = _load_keys()
    if kin in ks or kin == "masterkey":
        auths = set(_load_list("auth.txt")); auths.add(str(e.sender_id)); _save_list("auth.txt", list(auths))
        await e.respond("✅ Kích hoạt thành công! Dùng `/login`.")
    else: await e.respond("❌ Key sai!")

@bot.on(events.NewMessage(pattern='/login'))
async def _lg(ev):
    if str(ev.sender_id) not in _load_list("auth.txt"):
        await ev.respond("❌ Nhập key trước sếp!"); return
    async with bot.conversation(ev.sender_id) as cv:
        try:
            await cv.send_message("📱 **SĐT (+84...):**")
            p = (await cv.get_response()).text.strip().replace(" ", "")
            c = TelegramClient(StringSession(), A_ID, A_HS); await c.connect()
            r = await c.send_code_request(p)
            await cv.send_message("📩 **OTP:**")
            o = (await cv.get_response()).text.strip().replace(".", "")
            await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[ev.sender_id] = c; _logic(c, ev.sender_id); await cv.send_message("✅ LOGIN THÀNH CÔNG!")
        except Exception as e: await cv.send_message(f"❌ Lỗi: {str(e)}")

def _logic(c, ui):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp(e):
        t = int(e.pattern_match.group(1)); s_t[ui] = True; await e.delete()
        delay = d_l.get(ui, 0.3)
        while s_t.get(ui):
            try:
                r = requests.get(U1, timeout=5)
                for m in r.text.splitlines():
                    if not s_t.get(ui): break
                    await c.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={t})")
                    await asyncio.sleep(delay)
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern='/stop'))
    async def _stp(e): s_t[ui] = False; await e.edit("🛑 Đã dừng.")

# --- KHỞI CHẠY ---
async def start_bot():
    await bot.start(bot_token=B_TK)
    print("Bot đang trực tuyến!")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    # Chạy server Port 10000 ở luồng riêng
    threading.Thread(target=run_port_server, daemon=True).start()
    
    # Ép buộc tạo vòng lặp mới chống treo Render
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_bot())
    except Exception as e:
        print(f"Lỗi: {e}")
        sys.exit(0) # Thoát sạch sẽ nếu có lỗi để Render restart lại
