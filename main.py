import asyncio, os, random, datetime, edge_tts, re, glob, requests, json, threading
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError, PremiumAccountRequiredError
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- CẤU HÌNH (GIỮ NGUYÊN TỪ FILE GỐC CỦA SẾP) ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# --- VĂN BẢN BẢNG GIÁ ---
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

# --- FIX LỖI RENDER ---
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

# --- ĐỒNG BỘ NỘI DUNG ---
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
u_delays = {} # Lưu delay từng user

F_AUTH, F_KEYS = "auth_db.json", "keys_db.json"
F1, F2 = "bot_users.txt", "banned_users.txt"

def _load_j(f):
    if not os.path.exists(f): return {}
    try:
        with open(f, "r") as file: return json.load(file)
    except: return {}
def _save_j(f, d):
    try:
        with open(f, "w") as file: json.dump(d, file)
    except: pass

if os.path.exists(F2):
    with open(F2, "r") as f: b_u = set(int(l.strip()) for l in f if l.strip())
else: b_u = set()

# MENU CHUẨN (ẨN /AD)
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

# --- LOGIC CỦA USER ---
def _logic(c, u_i):
    def _mk(cid): w_m[f"{u_i}_{cid}"] = datetime.datetime.now(datetime.timezone.utc)

    # Thêm lệnh /setdelay
    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay (\d+\.?\d*)'))
    async def _setdelay(e):
        try:
            val = float(e.pattern_match.group(1))
            if 0.001 <= val <= 5.0:
                u_delays[u_i] = val
                await e.edit(f"✅ Đã chỉnh delay về: `{val}`s")
            else: await e.edit("❌ Delay từ 0.001 đến 5.0")
        except: await e.edit("❌ Sai định dạng")
        await asyncio.sleep(1.5); await e.delete()

    async def _sd(cid, ct, tid=None):
        s_t[u_i] = True
        inf = isinstance(ct, str)
        ls = ct if not inf else [ct]
        while s_t.get(u_i):
            d_val = u_delays.get(u_i, 0.8) # Delay mặc định 0.8
            for m in ls:
                if not s_t.get(u_i): break
                try:
                    fm = f"{m.strip()} [\u200b](tg://user?id={tid})" if tid else m.strip()
                    await c.send_message(cid, fm, parse_mode='markdown')
                    await asyncio.sleep(d_val)
                except FloodWaitError as e: await asyncio.sleep(e.seconds + 1)
                except: break
            if inf: break

    # --- CÁC LỆNH CHIẾN ---
    @c.on(events.NewMessage(outgoing=True, pattern=r'/info(?:\s+(.+))?'))
    async def _inf(e):
        target = e.pattern_match.group(1)
        try:
            if target:
                if target.isdigit(): user = await c.get_entity(int(target))
                else: user = await c.get_entity(target)
            elif e.is_reply: user = await c.get_entity((await e.get_reply_message()).sender_id)
            else: user = await c.get_me()
            await e.edit(f"👤 **Name:** {user.first_name}\n🆔 **ID:** `{user.id}`\n🏷 **User:** @{user.username if user.username else 'N/A'}")
        except: await e.edit("❌ Không thấy!")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/fake(?:\s+(.+))?'))
    async def _fk(e):
        t = e.pattern_match.group(1)
        try:
            if t: target = await c.get_entity(int(t) if t.isdigit() else t)
            elif e.is_reply: target = await c.get_entity((await e.get_reply_message()).sender_id)
            else: return await e.edit("⚠️ Tag/ID/Reply!")
            await e.edit("🔄 Đang lột xác...")
            me = await c.get_me()
            me_f = await c(functions.users.GetFullUserRequest(id=me.id))
            o_p[u_i] = {'f': me.first_name, 'l': me.last_name, 'a': me_f.full_user.about or "", 'p': await c.download_profile_photo('me')}
            tf = await c(functions.users.GetFullUserRequest(id=target.id))
            await c(functions.account.UpdateProfileRequest(first_name=tf.users[0].first_name or "", last_name=tf.users[0].last_name or "", about=tf.full_user.about or ""))
            p = await c.get_profile_photos(target.id, limit=1)
            if p: await c(functions.photos.UploadProfilePhotoRequest(file=await c.upload_file(await c.download_media(p[0]))))
            await e.edit("✅ Xong"); await asyncio.sleep(1); await e.delete()
        except: await e.edit("❌ Lỗi fake")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/diefake'))
    async def _dfk(e):
        if u_i not in o_p: return await e.edit("⚠️ Chưa lưu gốc!")
        await e.edit("🔙 Hoàn hồn...")
        o = o_p[u_i]
        try:
            await c(functions.account.UpdateProfileRequest(first_name=o['f'], last_name=o['l'], about=o['a']))
            if o['p']: await c(functions.photos.UploadProfilePhotoRequest(file=await c.upload_file(o['p'])))
            o_p.pop(u_i); await e.edit("✅ Xong"); await asyncio.sleep(1); await e.delete()
        except: await e.edit("❌ Lỗi")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp1(e):
        t = int(e.pattern_match.group(1)); _mk(e.chat_id); await e.delete()
        if os.path.exists('chui.txt'): await _sd(e.chat_id, open('chui.txt', 'r', encoding='utf-8').readlines(), t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp2 (\d+)'))
    async def _sp2(e):
        t = int(e.pattern_match.group(1)); _mk(e.chat_id); await e.delete()
        if os.path.exists('spam2.txt'): await _sd(e.chat_id, open('spam2.txt', 'r', encoding='utf-8').read().strip(), t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/spnd\s+([\s\S]+)'))
    async def _spn(e):
        v = e.pattern_match.group(1).strip(); _mk(e.chat_id); await e.delete(); s_t[u_i] = True
        while s_t.get(u_i):
            try: await c.send_message(e.chat_id, v); await asyncio.sleep(u_delays.get(u_i, 0.8))
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e):
        s_t[u_i] = False; cl_t[u_i] = False; await e.edit("🛑 STOP"); await asyncio.sleep(1); await e.delete()

    @c.on(events.NewMessage(outgoing=True, pattern=r'/voice (.+)'))
    async def _v(e):
        t = e.pattern_match.group(1); await e.delete(); p = f"v_{u_i}.mp3"
        await edge_tts.Communicate(t, "vi-VN-NamMinhNeural", rate="-15%").save(p)
        await c.send_file(e.chat_id, p, voice_note=True)
        if os.path.exists(p): os.remove(p)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/(cam|sua)(?:\s+(\d+))?(?:\s+(-?\d+))?'))
    async def _cam(e):
        m, u, b = e.pattern_match.group(1), e.pattern_match.group(2), e.pattern_match.group(3)
        if not u and e.is_reply: u = str((await e.get_reply_message()).sender_id)
        if not b: b = str(e.chat_id)
        if u:
            k = f"{u_i}_{b}_{u}"
            if m == "cam": c_b[k] = True
            else: c_b.pop(k, None)
            await e.edit(f"✅ {m.upper()} {u}"); await asyncio.sleep(1); await e.delete()

    @c.on(events.NewMessage(outgoing=True, pattern=r'/(autore|off)\s+(on|off)'))
    async def _tg(e):
        x, y = e.pattern_match.group(1), e.pattern_match.group(2)
        if x == "autore": a_r[u_i] = (y == "on")
        else: o_f[u_i] = (y == "on")
        await e.edit(f"✅ {x.upper()} {y.upper()} "); await asyncio.sleep(1); await e.delete()

    # XỬ LÝ TIN NHẮN ĐẾN (CAM/OFF)
    @c.on(events.NewMessage(incoming=True))
    async def _in(ev):
        kb = f"{u_i}_{ev.chat_id}_{ev.sender_id}"
        if c_b.get(kb):
            try: await ev.delete()
            except: pass
        if a_r.get(u_i) and ev.sender_id != u_i:
            try: await c(functions.messages.SendReactionRequest(peer=ev.chat_id, msg_id=ev.id, reaction=[types.ReactionEmoji(emoticon='❤️')]))
            except: pass
        if o_f.get(u_i) and ev.is_private and ev.sender_id != u_i:
            try: await ev.reply("Tao đang bận nhắn cl")
            except: pass

# --- QUẢN LÝ ADMIN ---
@bot.on(events.NewMessage(pattern='/ad'))
async def _ad(e):
    if e.sender_id != O_ID: return
    await e.respond("🛠 **ADMIN PANEL**\n\n/taokey <key> <day>\n/tb <nội dung>")

@bot.on(events.NewMessage(pattern=r'/taokey (\S+) (\d+)'))
async def _taokey(e):
    if e.sender_id != O_ID: return
    k, d = e.pattern_match.group(1), e.pattern_match.group(2)
    p = _load_j(F_KEYS); p[k] = d; _save_j(F_KEYS, p)
    await e.respond(f"✅ Key: `{k}` ({d} ngày) OK")

@bot.on(events.NewMessage(pattern='/start'))
async def _st(ev):
    uid = str(ev.sender_id)
    db = _load_j(F_AUTH)
    is_ok = (uid in db and (db[uid] == "forever" or datetime.datetime.now().timestamp() < db[uid]))
    if not is_ok and ev.sender_id != O_ID: return await ev.respond(XAC_THUC_TEXT)
    await ev.respond(M_T, buttons=[[Button.inline("📱 LOGIN", data="login")]])

@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nhapkey(e):
    k_in = e.pattern_match.group(1).strip()
    pool = _load_j(F_KEYS)
    if k_in in pool:
        d = int(pool[k_in]); db = _load_j(F_AUTH)
        db[str(e.sender_id)] = datetime.datetime.now().timestamp() + (d * 86400)
        del pool[k_in]; _save_j(F_KEYS, pool); _save_j(F_AUTH, db)
        await e.respond("✅ OK! Gõ /start")
    else: await e.respond("❌ Key sai!")

@bot.on(events.CallbackQuery(data="login"))
async def _log_cb(ev):
    async with bot.conversation(ev.sender_id) as cv:
        try:
            await cv.send_message("📱 SĐT (+84...):")
            p = (await cv.get_response()).text.strip()
            c = TelegramClient(f"u_{ev.sender_id}", A_ID, A_HS); await c.connect()
            if not await c.is_user_authorized():
                r = await c.send_code_request(p)
                await cv.send_message("📩 OTP:")
                o = (await cv.get_response()).text.strip()
                await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[ev.sender_id] = c; _logic(c, ev.sender_id)
            await cv.send_message("✅ LOGIN OK!")
        except Exception as ex: await cv.send_message(f"❌ {ex}")

async def main():
    threading.Thread(target=run_server, daemon=True).start()
    for f in glob.glob("u_*.session"):
        try:
            u = int(f.split('_')[1].split('.')[0])
            c = TelegramClient(f, A_ID, A_HS); await c.connect()
            if await c.is_user_authorized(): u_c[u] = c; _logic(c, u)
        except: pass
    await bot.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())


