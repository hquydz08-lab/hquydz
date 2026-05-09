import asyncio, os, random, datetime, edge_tts, re, glob, requests, json, threading
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError, PremiumAccountRequiredError
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CẤU HÌNH ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678  # ID của sếp Hữu Tiến

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

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

# --- WEB SERVER CHỐNG FAILED RENDER ---
class HealthCheck(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"SERVER_ALIVE")
    def log_message(self, format, *args): return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    try:
        server = HTTPServer(('0.0.0.0', port), HealthCheck)
        server.serve_forever()
    except: pass

def _sync():
    for n, u in {"chui.txt": U1, "spam2.txt": U2}.items():
        try:
            r = requests.get(u, timeout=10)
            if r.status_code == 200:
                with open(n, "w", encoding="utf-8") as f: f.write(r.text)
        except: pass
_sync()

# --- KHỞI TẠO ---
bot = TelegramClient('bot_manage', A_ID, A_HS).start(bot_token=B_TK)
o_p, u_c, c_b, c_i, s_t, cl_t, a_r, o_f, w_m = {}, {}, {}, {}, {}, {}, {}, {}, {}
u_delays = {} 

F_AUTH, F_KEYS = "auth_db.json", "keys_db.json"
F_USERS = "users_list.txt" # Lưu danh sách người dùng để gửi thông báo

def _load_j(f):
    if not os.path.exists(f): return {}
    try:
        with open(f, "r") as file: return json.load(file)
    except: return {}
def _save_j(f, d):
    try:
        with open(f, "w") as file: json.dump(d, file)
    except: pass

def _log_user(uid):
    u = set()
    if os.path.exists(F_USERS):
        with open(F_USERS, "r") as f: u = set(f.read().splitlines())
    if str(uid) not in u:
        with open(F_USERS, "a") as f: f.write(f"{uid}\n")

# --- MENU CHÍNH ---
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
┣ /setdelay <giây> - Tốc độ (0.001-5.0)
┣ /checkkey - Kiểm tra hạn dùng
┗ /logout - Thoát acc

👤 **Tài khoản:** [𝙃QUY CUTI](tg://user?id=7153197678)
"""

# --- LOGIC NGƯỜI DÙNG (USER) ---
def _logic(c, u_i):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay (\d+\.?\d*)'))
    async def _sd_set(e):
        try:
            val = float(e.pattern_match.group(1))
            if 0.001 <= val <= 5.0:
                u_delays[u_i] = val
                await e.edit(f"✅ Tốc độ hiện tại: `{val}`s")
            else: await e.edit("❌ 0.001 - 5.0")
        except: await e.edit("❌ Lỗi định dạng")
        await asyncio.sleep(1.5); await e.delete()

    async def _sd(cid, ct, tid=None):
        s_t[u_i] = True
        ls = ct if not isinstance(ct, str) else [ct]
        while s_t.get(u_i):
            dv = u_delays.get(u_i, 0.8)
            for m in ls:
                if not s_t.get(u_i): break
                try:
                    fm = f"{m.strip()} [\u200b](tg://user?id={tid})" if tid else m.strip()
                    await c.send_message(cid, fm, parse_mode='markdown')
                    await asyncio.sleep(dv)
                except FloodWaitError as err: await asyncio.sleep(err.seconds + 1)
                except: break
            if isinstance(ct, str): break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp1(e):
        t = int(e.pattern_match.group(1)); await e.delete()
        if os.path.exists('chui.txt'): await _sd(e.chat_id, open('chui.txt', 'r', encoding='utf-8').readlines(), t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp2 (\d+)'))
    async def _sp2(e):
        t = int(e.pattern_match.group(1)); await e.delete()
        if os.path.exists('spam2.txt'): await _sd(e.chat_id, open('spam2.txt', 'r', encoding='utf-8').read().strip(), t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/spnd\s+([\s\S]+)'))
    async def _spn(e):
        v = e.pattern_match.group(1).strip(); await e.delete(); s_t[u_i] = True
        while s_t.get(u_i):
            try: await c.send_message(e.chat_id, v); await asyncio.sleep(u_delays.get(u_i, 0.8))
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/fake(?:\s+(.+))?'))
    async def _fake(e):
        t = e.pattern_match.group(1)
        try:
            target = await c.get_entity(int(t) if t and t.isdigit() else (t or (await e.get_reply_message()).sender_id))
            await e.edit("🔄 Fake..."); me = await c.get_me()
            me_f = await c(functions.users.GetFullUserRequest(id=me.id))
            o_p[u_i] = {'f': me.first_name, 'l': me.last_name, 'a': me_f.full_user.about or "", 'p': await c.download_profile_photo('me')}
            tf = await c(functions.users.GetFullUserRequest(id=target.id))
            await c(functions.account.UpdateProfileRequest(first_name=tf.users[0].first_name or "", last_name=tf.users[0].last_name or "", about=tf.full_user.about or ""))
            p = await c.get_profile_photos(target.id, limit=1)
            if p: await c(functions.photos.UploadProfilePhotoRequest(file=await c.upload_file(await c.download_media(p[0]))))
            await e.edit("✅ Xong"); await asyncio.sleep(1); await e.delete()
        except: await e.edit("❌ Lỗi")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e):
        s_t[u_i] = False; await e.edit("🛑 ĐÃ DỪNG"); await asyncio.sleep(1); await e.delete()

# --- KHU VỰC QUẢN TRỊ (ADMIN) ---
@bot.on(events.NewMessage(pattern='/ad'))
async def _admin_panel(e):
    if e.sender_id != O_ID: return
    t = """🛠 **ADMIN CONTROL PANEL**
━━━━━━━━━━━━━━━
🔑 **Lệnh Key:**
┣ `/taokey <key> <ngày>`
┣ `/xoakey <key>`

📢 **Lệnh Thông Báo:**
┣ `/tb <nội dung>` (Gửi cho tất cả user)

🚫 **Lệnh Hệ Thống:**
┣ `/unban <id>`
┣ `/listuser` (Xem sl user)
━━━━━━━━━━━━━━━"""
    await e.respond(t)

@bot.on(events.NewMessage(pattern=r'/taokey (\S+) (\d+)'))
async def _tk(e):
    if e.sender_id != O_ID: return
    k, d = e.pattern_match.group(1), e.pattern_match.group(2)
    p = _load_j(F_KEYS); p[k] = d; _save_j(F_KEYS, p)
    await e.respond(f"✅ Đã tạo key: `{k}` có hạn `{d}` ngày.")

@bot.on(events.NewMessage(pattern=r'/tb\s+([\s\S]+)'))
async def _tb_cmd(e):
    if e.sender_id != O_ID: return
    msg = e.pattern_match.group(1)
    if not os.path.exists(F_USERS): return await e.respond("⚠️ Chưa có user nào!")
    await e.respond("🚀 Đang gửi thông báo...")
    with open(F_USERS, "r") as f: ids = f.read().splitlines()
    count = 0
    for uid in ids:
        try:
            await bot.send_message(int(uid), f"📢 **THÔNG BÁO ADMIN**\n\n{msg}")
            count += 1
            await asyncio.sleep(0.3)
        except: continue
    await e.respond(f"✅ Đã gửi cho {count} người dùng.")

# --- XỬ LÝ START & KEY ---
@bot.on(events.NewMessage(pattern='/start'))
async def _start_h(ev):
    _log_user(ev.sender_id)
    uid = str(ev.sender_id); db = _load_j(F_AUTH)
    is_ok = (uid in db and (db[uid] == "forever" or datetime.datetime.now().timestamp() < db[uid]))
    if not is_ok and ev.sender_id != O_ID: return await ev.respond(XAC_THUC_TEXT)
    await ev.respond(M_T, buttons=[[Button.inline("📱 LOGIN ACCOUNT", data="login")]])

@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nhap_k(e):
    k_in = e.pattern_match.group(1).strip(); pool = _load_j(F_KEYS)
    if k_in in pool:
        d = int(pool[k_in]); db = _load_j(F_AUTH)
        db[str(e.sender_id)] = datetime.datetime.now().timestamp() + (d * 86400)
        del pool[k_in]; _save_j(F_KEYS, pool); _save_j(F_AUTH, db)
        await e.respond("✅ Kích hoạt thành công! Gõ /start để bắt đầu.")
    else: await e.respond("❌ Key sai hoặc đã hết hạn!")

@bot.on(events.CallbackQuery(data="login"))
async def _login_cb(ev):
    async with bot.conversation(ev.sender_id) as cv:
        try:
            await cv.send_message("📱 Nhập SĐT (+84...):")
            p = (await cv.get_response()).text.strip()
            c = TelegramClient(f"u_{ev.sender_id}", A_ID, A_HS); await c.connect()
            if not await c.is_user_authorized():
                r = await c.send_code_request(p)
                await cv.send_message("📩 Nhập OTP:")
                o = (await cv.get_response()).text.strip()
                await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[ev.sender_id] = c; _logic(c, ev.sender_id)
            await cv.send_message("✅ Đăng nhập thành công!")
        except Exception as ex: await cv.send_message(f"❌ Lỗi: {ex}")

async def main_run():
    threading.Thread(target=run_server, daemon=True).start()
    for f in glob.glob("u_*.session"):
        try:
            u_id = int(f.split('_')[1].split('.')[0])
            c = TelegramClient(f, A_ID, A_HS); await c.connect()
            if await c.is_user_authorized(): u_c[u_id] = c; _logic(c, u_id)
        except: pass
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main_run())


