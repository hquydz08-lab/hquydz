
import asyncio, os, random, datetime, re, glob, requests, string
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError
from telethon.sessions import StringSession
import edge_tts

# --- CẤU HÌNH HỆ THỐNG ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 # ID Owner

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# Quản lý file dữ liệu an toàn
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

# Khởi tạo Admin
ADMINS = set([O_ID])
for a in _load_list("admins.txt"): 
    if a.strip(): ADMINS.add(int(a))

bot = TelegramClient('bot_manage_session', A_ID, A_HS).start(bot_token=B_TK)
u_c, s_t, d_l, s_l = {}, {}, {}, {}

# --- GIAO DIỆN MENU ---
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
┣ /setoff <nội dung> - Đặt tin nhắn khi bận
┣ /deloff - Xóa tin nhắn đã đặt
┣ /stop - Dừng tất cả
┣ /clear - Xóa 100 tin nhắn
┣ /clear2 - Xoá tin nhắn bot
┣ /checkmode - Kiểm tra chế độ spam
┣ /checkkey - Kiểm tra thông tin key
┣ /logoutkey - Thoát key
┣ /logout - Thoát acc
┗ /setdelay - chỉnh thời gian spam

👤 **ADMIN: Hquy**"""

M_AD = """🛠 **ADMIN MENU**
┣ /taokey <tên> <day/week/month/forever>
┣ /xoakey <tên>
┣ /addadmin <id>
┣ /deladmin <id>
┣ /tb <nội dung>
┗ /checkadmin"""

# --- LOGIC QUẢN TRỊ ---
@bot.on(events.NewMessage(pattern='/ad'))
async def _ad(e):
    if e.sender_id in ADMINS: await e.respond(M_AD)

@bot.on(events.NewMessage(pattern=r'/addadmin (\d+)'))
async def _aa(e):
    if e.sender_id != O_ID: return
    nid = int(e.pattern_match.group(1))
    ADMINS.add(nid); _save_list("admins.txt", list(ADMINS))
    await e.respond(f"✅ Admin `{nid}` đã được thêm!")

@bot.on(events.NewMessage(pattern=r'/taokey (.+) (day|week|month|forever)'))
async def _tk(e):
    if e.sender_id not in ADMINS: return
    k, t = e.pattern_match.group(1).strip(), e.pattern_match.group(2)
    now = datetime.datetime.now()
    exp = (now + datetime.timedelta(days=1) if t=='day' else 
           now + datetime.timedelta(weeks=1) if t=='week' else 
           now + datetime.timedelta(days=30) if t=='month' else "forever")
    ks = _load_keys(); ks[k] = exp; _save_keys(ks)
    await e.respond(f"🔑 Key `{k}` ({t}) đã tạo!")

@bot.on(events.NewMessage(pattern=r'/xoakey (.+)'))
async def _xk(e):
    if e.sender_id not in ADMINS: return
    k = e.pattern_match.group(1).strip()
    ks = _load_keys()
    if k in ks:
        del ks[k]; _save_keys(ks); await e.respond(f"✅ Xóa key `{k}`")

# --- LOGIC NGƯỜI DÙNG ---
@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nk(e):
    kin = e.pattern_match.group(1).strip()
    ks = _load_keys()
    if kin in ks:
        exp = ks[kin]
        if exp != "forever" and datetime.datetime.now() > exp:
            await e.respond("❌ Key hết hạn!"); return
        auths = set(_load_list("auth.txt")); auths.add(str(e.sender_id)); _save_list("auth.txt", list(auths))
        await e.respond("✅ Kích hoạt thành công! Gõ `/login` để log acc.")
    else: await e.respond("❌ Key sai!")

@bot.on(events.NewMessage(pattern='/login'))
async def _lg(ev):
    if str(ev.sender_id) not in _load_list("auth.txt"):
        await ev.respond("❌ Chưa nhập key!"); return
    async with bot.conversation(ev.sender_id) as cv:
        try:
            await cv.send_message("📱 **SĐT (+84...):**")
            p = (await cv.get_response()).text.strip().replace(" ", "")
            c = TelegramClient(StringSession(), A_ID, A_HS); await c.connect()
            r = await c.send_code_request(p)
            await cv.send_message("📩 **OTP:**")
            o = (await cv.get_response()).text.strip().replace(".", "")
            await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[ev.sender_id] = c; _logic(c, ev.sender_id); await cv.send_message("✅ LOG ACC THÀNH CÔNG!")
        except Exception as e: await cv.send_message(f"❌ Lỗi: {str(e)}")

def _logic(c, ui):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def _sd(e):
        d_l[ui] = float(e.pattern_match.group(1))
        await e.edit(f"✅ Delay: {d_l[ui]}s")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp(e):
        t = int(e.pattern_match.group(1)); s_t[ui] = True; await e.delete()
        delay = d_l.get(ui, 0.3)
        while s_t.get(ui):
            try:
                r = requests.get(U1, timeout=5)
                for m in r.text.splitlines():
                    if not s_t.get(ui): break
                    await c.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={t})", parse_mode='markdown')
                    await asyncio.sleep(delay)
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e): s_t[ui] = False; await e.edit("🛑 **DỪNG**")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/voice (.+)'))
    async def _v(e):
        txt = e.pattern_match.group(1); await e.delete(); p = f"v_{ui}.mp3"
        try:
            comm = edge_tts.Communicate(txt, "vi-VN-NamMinhNeural")
            await comm.save(p); await c.send_file(e.chat_id, p, voice_note=True)
        except: pass
        if os.path.exists(p): os.remove(p)

@bot.on(events.NewMessage(pattern='/start'))
async def _start(ev):
    us = set(_load_list("users.txt")); us.add(str(ev.sender_id)); _save_list("users.txt", list(us))
    await ev.respond(M_T)

if __name__ == '__main__':
    bot.run_until_disconnected()


