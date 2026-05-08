
import asyncio, os, random, datetime, edge_tts, re, glob, requests
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError, PremiumAccountRequiredError
from telethon.sessions import StringSession

# --- CẤU HÌNH HỆ THỐNG ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678  # ID CỦA HAI QUY

U1 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/chui.txt"
U2 = "https://raw.githubusercontent.com/ehvuebe-png/Cailontaone/main/spam2.txt"

def _sync():
    for n, u in {"chui.txt": U1, "spam2.txt": U2}.items():
        try:
            r = requests.get(u, timeout=10)
            if r.status_code == 200:
                with open(n, "w", encoding="utf-8") as f: f.write(r.text)
        except: pass
_sync()

bot = TelegramClient('bot_manage_session', A_ID, A_HS).start(bot_token=B_TK)
o_p, u_c, c_b, c_i, s_t, cl_t, a_r, o_f, w_m = {}, {}, {}, {}, {}, {}, {}, {}, {}

F1, F2 = "bot_users.txt", "banned_users.txt"
if os.path.exists(F2):
    with open(F2, "r") as f: b_u = set(int(l.strip()) for l in f if l.strip())
else: b_u = set()

def _sb():
    with open(F2, "w") as f:
        for u in b_u: f.write(f"{u}\n")

def _su(u):
    if not os.path.exists(F1): 
        with open(F1, "w") as f: pass
    with open(F1, "r") as f: us = f.read().splitlines()
    if str(u) not in us:
        with open(F1, "a") as f: f.write(f"{u}\n")

# --- GIAO DIỆN MENU HQUY ---
M_T = """📣 **XÁC THỰC NGƯỜI DÙNG**
━━━━━━━━━━━━━━━
💰 **BẢNG GIÁ KEY**
🎫 2K/DAY | 10K/WEEK
🎫 20K/MONTH | 70K/VV
━━━━━━━━━━━━━━━
. 　˚　. . ✦˚ .   ADMIN:@hquycute ˚　　　　✦　.
𖣘 **HQUY CUTI** .   2026 𖣘
.  ˚　.　 . ✦　˚　 .   .　.  　˚　  　.

🔥 **𝑺𝒑𝒂𝒎 & 𝑻𝒂𝒈**
┣ /sp <id> - Spam chửi
┣ /sp2 <id> - Spam nội dung
┣ /spicon <số> - Spam icon
┣ /spnd <nd> - Spam treo
┣ /spstick <số> - Spam sticker
┗ /spcall <id> - Spam call

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
┣ /clear2 - Xoá tin nhắn bot
┗ /logout - Thoát acc

👤 **Admin:** [HQUY CUTI](tg://user?id=7153197678)
"""

def _logic(c, u_i):
    # Khai báo các trạng thái cho client này
    s_t[u_i] = False
    cl_t[u_i] = False

    async def _sd(cid, ct, tid=None):
        s_t[u_i] = True
        inf = isinstance(ct, str)
        ls = ct if not inf else [ct]
        while s_t.get(u_i):
            for m in ls:
                if not s_t.get(u_i): break
                try:
                    # Gửi tin nhắn từ acc cá nhân đã login
                    fm = f"{m.strip()} [\u200b](tg://user?id={tid})" if tid else m.strip()
                    await c.send_message(cid, fm, parse_mode='markdown')
                    await asyncio.sleep(0.3)
                except FloodWaitError as e: await asyncio.sleep(e.seconds + 1)
                except: break
            if not inf: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/info(?:\s+(.+))?'))
    async def _inf(e):
        target = e.pattern_match.group(1)
        try:
            if target: user = await c.get_entity(int(target) if target.isdigit() else target)
            elif e.is_reply: user = await c.get_entity((await e.get_reply_message()).sender_id)
            else: user = await c.get_me()
            await e.edit(f"👤 **Name:** {user.first_name}\n🆔 **ID:** `{user.id}`\n🏷 **User:** @{user.username if user.username else 'N/A'}")
        except: await e.edit("❌ Không thấy!")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp1(e):
        t = int(e.pattern_match.group(1))
        await e.delete()
        if os.path.exists('chui.txt'):
            with open('chui.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                await _sd(e.chat_id, lines, t)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e):
        s_t[u_i] = False
        cl_t[u_i] = False
        await e.edit("🛑 **STOPPED**")
        await asyncio.sleep(1)
        await e.delete()

    @c.on(events.NewMessage(outgoing=True, pattern=r'/voice (.+)'))
    async def _v(e):
        t = e.pattern_match.group(1)
        await e.delete()
        p = f"v_{u_i}.mp3"
        try:
            communicate = edge_tts.Communicate(t, "vi-VN-NamMinhNeural", rate="-15%")
            await communicate.save(p)
            await c.send_file(e.chat_id, p, voice_note=True)
        except: pass
        if os.path.exists(p): os.remove(p)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/fake(?:\s+(.+))?'))
    async def _fk(e):
        t = e.pattern_match.group(1)
        try:
            if t: target = await c.get_entity(int(t) if t.isdigit() else t)
            elif e.is_reply: target = await c.get_entity((await e.get_reply_message()).sender_id)
            else: return await e.edit("⚠️ Tag hoặc Reply!")
            await e.edit("🔄 Đang fake...")
            await c(functions.account.UpdateProfileRequest(first_name=target.first_name, last_name=target.last_name or ""))
            await e.edit(f"🎭 Đã fake thành: {target.first_name}")
        except: await e.edit("❌ Lỗi!")

@bot.on(events.CallbackQuery(data="login"))
async def _lf(ev):
    u = ev.sender_id
    if u in b_u: return
    async with bot.conversation(u) as cv:
        try:
            await cv.send_message("📱 **LOGIN ACC CÁ NHÂN**\nNhập SĐT (+84...):")
            p = (await cv.get_response()).text.strip().replace(" ", "")
            c = TelegramClient(StringSession(), A_ID, A_HS)
            await c.connect()
            r = await c.send_code_request(p)
            await cv.send_message("📩 Nhập OTP (Dạng 1.2.3.4.5):")
            o = (await cv.get_response()).text.strip().replace(".", "")
            await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[u] = c
            _logic(c, u)
            await cv.send_message("✅ **LOGIN THÀNH CÔNG!**")
        except Exception as e: await cv.send_message(f"❌ {str(e)}")

@bot.on(events.NewMessage(pattern='/start'))
async def _st(ev):
    _su(ev.sender_id)
    await ev.respond(M_T, buttons=[[Button.inline("📱 LOGIN", data="login")]])

@bot.on(events.NewMessage(pattern=r'/tb\s+([\s\S]+)'))
async def _tb(e):
    if e.sender_id != O_ID: return
    msg = e.pattern_match.group(1)
    if not os.path.exists(F1): return
    with open(F1, "r") as f: ids = f.read().splitlines()
    await e.respond(f"📢 Đang gửi TB cho {len(ids)} người...")
    for uid in ids:
        try:
            await bot.send_message(int(uid), f"📢 **TB:** {msg}")
            await asyncio.sleep(0.3)
        except: continue
    await e.respond("✅ Hoàn tất!")

if __name__ == '__main__':
    print("REX SYSTEM IS READY.")
    bot.run_until_disconnected()


