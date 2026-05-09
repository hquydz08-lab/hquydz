import asyncio, os, random, datetime, edge_tts, re, glob, requests, json, threading
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError, PremiumAccountRequiredError
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CẤU HÌNH CỦA SẾP (GIỮ NGUYÊN) ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# --- BẢNG GIÁ XÁC THỰC ---
XAC_THUC_TEXT = """📣 XÁC THỰC NGƯỜI DÙNG
━━━━━━━━━━━━━━━
💰 BẢNG GIÁ
━━━━━━━━━━━━━━━
🎫 2K/DAY
🎫 10K/WEEK
🎫 20K/MONTH
🎫 70K/VV
━━━━━━━━━━━━━━━
🔑 Vui lòng nhập key để sử dụng bot
📝 /nhapkey <key>
━━━━━━━━━━━━━━━
👑 ADMIN: @hquycute"""

# --- SERVER ĐỂ FIX LỖI STATUS 1 TRÊN RENDER ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ONLINE")
    def log_message(self, format, *args): return

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheck)
    server.serve_forever()

# --- ĐỒNG BỘ FILE ---
def _sync():
    for n, u in {"chui.txt": U1, "spam2.txt": U2}.items():
        try:
            r = requests.get(u, timeout=10)
            if r.status_code == 200:
                with open(n, "w", encoding="utf-8") as f: f.write(r.text)
        except: pass
_sync()

# --- KHỞI TẠO BIẾN ---
bot = TelegramClient('bot_manage', A_ID, A_HS).start(bot_token=B_TK)
o_p, u_c, c_b, c_i, s_t, cl_t, a_r, o_f, w_m = {}, {}, {}, {}, {}, {}, {}, {}, {}
u_delays = {} # Lưu delay

F_AUTH, F_KEYS = "auth_users.json", "keys_pool.json"
F1, F2 = "bot_users.txt", "banned_users.txt"

def _load_j(f):
    if not os.path.exists(f): return {}
    with open(f, "r") as file: return json.load(file)
def _save_j(f, d):
    with open(f, "w") as file: json.dump(d, file)

b_u = set()
if os.path.exists(F2):
    with open(F2, "r") as f: b_u = set(int(l.strip()) for l in f if l.strip())

# Menu (Đã ẩn /ad)
M_T = """
. 　˚　. . ✦˚ .     　　˚　　　　✦　.
𖣘Hai Quy x Bot War .   2026 𖣘
.  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.

🔥 𝑺𝒑𝒂𝒎 & 𝑻𝒂𝒈
┣ /sp <id> - Spam chửi
┣ /sp2 <id> - Spam nội dung
┣ /spicon <số> - Spam icon
┣ /spnd <nd> - Spam treo
┣ /spstick <số> - Spam sticker
┗ /spcall <id> - Spam call

☠ 𝑯𝒆‌‌ 𝑻𝒉𝒐‌‌𝒏𝒈 Đ𝒆𝒐 𝑹𝒐‌
┣ /cam <id> <box> - Câm box
┣ /sua <id> <box> - Gỡ câm
┣ /camib <id> - Câm ib
┗ /suaib <id> - Gỡ câm ib

📦 𝑳𝒂‌𝒕 𝑽𝒂‌𝒕
┣ /info <@/id/rep> - Soi trang
┣ /fake <@/id/rep> - Fake người khác
┣ /diefake - về lại acc gốc
┣ /voice <text> - Voice 
┣ /autore <on/off> - Tự động thả tim
┣ /off <on/off> - Chế độ bận
┣ /stop - Dừng tất cả
┣ /clear - Xóa 100 tin nhắn
┣ /setdelay <giây> - Chỉnh tốc độ (0.001-5.0)
┣ /checkkey - Kiểm tra hạn dùng
┗ /logout - Thoát acc

👤 **Tài khoản:** [𝙃QUY CUTI](tg://user?id=7153197678)
"""

# --- LOGIC CHIẾN (BÊ NGUYÊN TỪ FILE SẾP SANG) ---
def _logic(c, u_i):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay (\d+\.?\d*)'))
    async def _sd_val(e):
        try:
            v = float(e.pattern_match.group(1))
            if 0.001 <= v <= 5.0:
                u_delays[u_i] = v
                await e.edit(f"✅ Đã chỉnh delay: `{v}`s")
            else: await e.edit("❌ 0.001 -> 5.0 thôi sếp!")
        except: await e.edit("❌ Sai định dạng")
        await asyncio.sleep(1); await e.delete()

    async def _sd(cid, ct, tid=None):
        s_t[u_i] = True
        inf = isinstance(ct, str)
        ls = ct if not inf else [ct]
        while s_t.get(u_i):
            d_val = u_delays.get(u_i, 0.8) # Mặc định 0.8 nếu chưa set
            for m in ls:
                if not s_t.get(u_i): break
                try:
                    fm = f"{m.strip()} [\u200b](tg://user?id={tid})" if tid else m.strip()
                    await c.send_message(cid, fm, parse_mode='markdown')
                    await asyncio.sleep(d_val)
                except FloodWaitError as e: await asyncio.sleep(e.seconds + 1)
                except: break
            if not inf: break

    # Sếp dán tiếp toàn bộ lệnh /sp, /fake, /cam, /voice... của sếp vào đây
    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp1(e):
        t = int(e.pattern_match.group(1)); await e.delete()
        if os.path.exists('chui.txt'): await _sd(e.chat_id, open('chui.txt', 'r', encoding='utf-8').readlines(), t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e):
        s_t[u_i] = False; cl_t[u_i] = False; await e.edit("🛑 STOP"); await asyncio.sleep(1); await e.delete()

# --- ADMIN PANEL (ẨN) ---
@bot.on(events.NewMessage(pattern='/ad'))
async def _ad_hidden(e):
    if e.sender_id != O_ID: return
    await e.respond("🛠 **ADMIN**\n/taokey <key> <day>\n/xoakey <key>\n/tb <nội dung>")

@bot.on(events.NewMessage(pattern=r'/taokey (\S+) (\S+)'))
async def _tk(e):
    if e.sender_id != O_ID: return
    k, d = e.pattern_match.group(1), e.pattern_match.group(2)
    p = _load_j(F_KEYS); p[k] = d; _save_j(F_KEYS, p)
    await e.respond(f"✅ Key: `{k}` | Hạn: `{d}`")

# --- AUTH & LOGIN ---
@bot.on(events.NewMessage(pattern='/start'))
async def _start(ev):
    uid = str(ev.sender_id)
    db = _load_j(F_AUTH)
    is_ok = (uid in db and (db[uid] == "forever" or datetime.datetime.now().timestamp() < db[uid]))
    if not is_ok and ev.sender_id != O_ID: return await ev.respond(XAC_THUC_TEXT)
    await ev.respond(M_T, buttons=[[Button.inline("📱 LOGIN", data="login")]])

@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nhap(e):
    k = e.pattern_match.group(1).strip()
    pool = _load_j(F_KEYS)
    if k in pool:
        d = pool[k]; db = _load_j(F_AUTH)
        db[str(e.sender_id)] = "forever" if d == "forever" else (datetime.datetime.now().timestamp() + int(d)*86400)
        del pool[k]; _save_j(F_KEYS, pool); _save_j(F_AUTH, db)
        await e.respond("✅ Kích hoạt OK! Gõ /start")
    else: await e.respond("❌ Key sai!")

@bot.on(events.CallbackQuery(data="login"))
async def _log_cb(ev):
    async with bot.conversation(ev.sender_id) as cv:
        try:
            await cv.send_message("SĐT (+84...):")
            p = (await cv.get_response()).text.strip()
            c = TelegramClient(f"u_{ev.sender_id}", A_ID, A_HS); await c.connect()
            if not await c.is_user_authorized():
                r = await c.send_code_request(p)
                await cv.send_message("OTP:")
                o = (await cv.get_response()).text.strip()
                await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[ev.sender_id] = c; _logic(c, ev.sender_id)
            await cv.send_message("✅ OK")
        except Exception as ex: await cv.send_message(f"❌ {ex}")

async def run_bot():
    # Chạy server health check song song để tránh lỗi Render
    threading.Thread(target=run_health_server, daemon=True).start()
    
    # Auto-reconnect acc cũ
    for f in glob.glob("u_*.session"):
        try:
            u = int(f.split('_')[1].split('.')[0])
            c = TelegramClient(f, A_ID, A_HS); await c.connect()
            if await c.is_user_authorized(): u_c[u] = c; _logic(c, u)
        except: pass
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(run_bot())


