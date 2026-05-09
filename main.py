
import asyncio, os, random, datetime, re, glob, requests, subprocess, sys, string

# --- TỰ ĐỘNG CÀI THƯ VIỆN (CHỐNG ĐỎ RENDER) ---
def install_requirements():
    try:
        import telethon
        import edge_tts
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "telethon", "edge-tts", "requests"])

install_requirements()

from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError
from telethon.sessions import StringSession
import edge_tts

# --- CẤU HÌNH HỆ THỐNG ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 # ID Của Sếp (Owner)

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

# File dữ liệu
F_USERS = "bot_users.txt"
F_KEYS = "keys.txt"
F_ADMINS = "admins.txt"
F_AUTH = "authorized_users.txt"

def _load_list(f):
    if not os.path.exists(f): return []
    with open(f, "r") as file: return file.read().splitlines()

def _save_list(f, data):
    with open(f, "w") as file: file.write("\n".join(map(str, data)))

# Nạp Admin
ADMINS = set([O_ID])
for a in _load_list(F_ADMINS): 
    if a.strip(): ADMINS.add(int(a))

def _load_keys():
    if not os.path.exists(F_KEYS): return {}
    keys = {}
    with open(F_KEYS, "r") as f:
        for line in f:
            if "|" in line:
                k, exp = line.strip().split("|")
                keys[k] = exp if exp == "forever" else datetime.datetime.fromisoformat(exp)
    return keys

def _save_keys(keys):
    with open(F_KEYS, "w") as f:
        for k, exp in keys.items():
            val = exp if exp == "forever" else exp.isoformat()
            f.write(f"{k}|{val}\n")

bot = TelegramClient('bot_manage_session', A_ID, A_HS).start(bot_token=B_TK)
u_c, s_t, d_l, s_l = {}, {}, {}, {}

# --- GIAO DIỆN MENU NGƯỜI DÙNG ---
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

# --- MENU ADMIN (LỆNH /ad) ---
M_AD = """🛠 **MENU QUẢN TRỊ (ADMIN ONLY)**
┣ /taokey <tên> <thời gian>
┣ /xoakey <tên>
┣ /addadmin <id>
┣ /deladmin <id>
┣ /tb <nội dung>
┗ /checkadmin - Xem danh sách admin

*Thời gian: day, week, month, forever*"""

# --- LOGIC QUẢN TRỊ ---

@bot.on(events.NewMessage(pattern='/ad'))
async def _admin_menu(e):
    if e.sender_id in ADMINS:
        await e.respond(M_AD)

@bot.on(events.NewMessage(pattern=r'/addadmin (\d+)'))
async def _aa(e):
    if e.sender_id != O_ID: return
    new_ad = int(e.pattern_match.group(1))
    ADMINS.add(new_ad); _save_list(F_ADMINS, list(ADMINS))
    await e.respond(f"✅ Đã thêm Admin: `{new_ad}`")

@bot.on(events.NewMessage(pattern=r'/taokey (.+) (day|week|month|forever)'))
async def _tk(e):
    if e.sender_id not in ADMINS: return
    name, time = e.pattern_match.group(1).strip(), e.pattern_match.group(2)
    now = datetime.datetime.now()
    if time == 'day': exp = now + datetime.timedelta(days=1)
    elif time == 'week': exp = now + datetime.timedelta(weeks=1)
    elif time == 'month': exp = now + datetime.timedelta(days=30)
    else: exp = "forever"
    ks = _load_keys(); ks[name] = exp; _save_keys(ks)
    await e.respond(f"🔑 Key `{name}` ({time}) đã sẵn sàng!")

@bot.on(events.NewMessage(pattern=r'/xoakey (.+)'))
async def _xk(e):
    if e.sender_id not in ADMINS: return
    name = e.pattern_match.group(1).strip()
    ks = _load_keys()
    if name in ks:
        del ks[name]; _save_keys(ks)
        await e.respond(f"✅ Đã xóa key: `{name}`")

@bot.on(events.NewMessage(pattern=r'/tb (.+)'))
async def _broadcast(e):
    if e.sender_id not in ADMINS: return
    msg = e.pattern_match.group(1)
    us = _load_list(F_USERS)
    await e.respond(f"📣 Đang gửi thông báo đến {len(us)} người...")
    for u in us:
        try: await bot.send_message(int(u), f"📢 **THÔNG BÁO:**\n\n{msg}"); await asyncio.sleep(0.3)
        except: pass

# --- LOGIC NGƯỜI DÙNG ---

@bot.on(events.NewMessage(pattern=r'/nhapkey (.+)'))
async def _nk(e):
    k_in = e.pattern_match.group(1).strip()
    ks = _load_keys()
    if k_in in ks:
        exp = ks[k_in]
        if exp != "forever" and datetime.datetime.now() > exp:
            await e.respond("❌ Key hết hạn!"); return
        auths = set(_load_list(F_AUTH)); auths.add(str(e.sender_id)); _save_list(F_AUTH, list(auths))
        await e.respond("✅ Kích hoạt thành công! Gõ `/login` để bắt đầu.")
    else: await e.respond("❌ Key sai!")

@bot.on(events.NewMessage(pattern='/login'))
async def _login(ev):
    u = ev.sender_id
    if str(u) not in _load_list(F_AUTH):
        await ev.respond("❌ Sếp cần nhập key trước!"); return
    async with bot.conversation(u) as cv:
        try:
            await cv.send_message("📱 **SĐT (+84...):**")
            p = (await cv.get_response()).text.strip().replace(" ", "")
            c = TelegramClient(StringSession(), A_ID, A_HS); await c.connect()
            r = await c.send_code_request(p)
            await cv.send_message("📩 **OTP:**")
            o = (await cv.get_response()).text.strip().replace(".", "")
            await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[u] = c; _logic(c, u); await cv.send_message("✅ ĐÃ LOG ACC!")
        except Exception as e: await cv.send_message(f"❌ {str(e)}")

def _logic(c, u_i):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/setdelay ([\d.]+)'))
    async def _sd(e):
        d_l[u_i] = float(e.pattern_match.group(1))
        await e.edit(f"✅ Tốc độ spam: {d_l[u_i]}s")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp(e):
        t = int(e.pattern_match.group(1)); s_t[u_i] = True; await e.delete()
        delay = d_l.get(u_i, 0.3)
        while s_t.get(u_i):
            try:
                with open('chui.txt', 'r', encoding='utf-8') as f:
                    for m in f:
                        if not s_t.get(u_i): break
                        await c.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={t})", parse_mode='markdown')
                        await asyncio.sleep(delay)
            except: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e): s_t[u_i] = False; await e.edit("🛑 **DỪNG**")

@bot.on(events.NewMessage(pattern='/start'))
async def _start(ev):
    us = set(_load_list(F_USERS)); us.add(str(ev.sender_id)); _save_list(F_USERS, list(us))
    await ev.respond(M_T)

if __name__ == '__main__':
    bot.run_until_disconnected()


