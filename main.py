
import asyncio, os, random, datetime, edge_tts, re, glob, requests
from telethon import TelegramClient, events, Button, functions, types
from telethon.errors import FloodWaitError, RPCError, PremiumAccountRequiredError
from telethon.sessions import StringSession

# --- CẤU HÌNH HỆ THỐNG ---
A_ID = 34619338
A_HS = '0f9eb480f7207cf57060f2f35c0ba137'
B_TK = '8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4'
O_ID = 7153197678 

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
u_c, s_t, c_b, c_i, s_l, o_f, o_m = {}, {}, {}, {}, {}, {}, {}

F1, F2 = "bot_users.txt", "banned_users.txt"
if os.path.exists(F2):
    with open(F2, "r") as f: b_u = set(int(l.strip()) for l in f if l.strip())
else: b_u = set()

def _su(u):
    if not os.path.exists(F1): open(F1, "w").close()
    with open(F1, "r") as f: us = f.read().splitlines()
    if str(u) not in us:
        with open(F1, "a") as f: f.write(f"{u}\n")

# --- GIAO DIỆN MENU CHUẨN SẾP YÊU CẦU ---
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
┗ /logout - Thoát acc

👤 **ADMIN: Hquy**"""

def _logic(c, u_i):
    @c.on(events.NewMessage(outgoing=True, pattern=r'/sp (\d+)'))
    async def _sp1(e):
        t = int(e.pattern_match.group(1)); s_t[u_i] = True; await e.delete()
        delay = 2.0 if s_l.get(u_i) else 0.3
        if os.path.exists('chui.txt'):
            lines = open('chui.txt', 'r', encoding='utf-8').readlines()
            while s_t.get(u_i):
                for m in lines:
                    if not s_t.get(u_i): break
                    try:
                        await c.send_message(e.chat_id, f"{m.strip()} [\u200b](tg://user?id={t})", parse_mode='markdown')
                        await asyncio.sleep(delay)
                    except: break

    @c.on(events.NewMessage(outgoing=True, pattern=r'/spslow (on|off)'))
    async def _slow(e):
        mode = e.pattern_match.group(1) == 'on'
        s_l[u_i] = mode
        await e.edit(f"✅ Spam chậm: {'BẬT' if mode else 'TẮT'}")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/setoff (.+)'))
    async def _soff(e):
        o_m[u_i] = e.pattern_match.group(1)
        await e.edit("✅ Đã đặt tin nhắn bận!")

    @c.on(events.NewMessage(outgoing=True, pattern=r'/off (on|off)'))
    async def _offm(e):
        o_f[u_i] = e.pattern_match.group(1) == 'on'
        await e.edit(f"✅ Chế độ bận: {'BẬT' if o_f[u_i] else 'TẮT'}")

    @c.on(events.NewMessage(incoming=True))
    async def _auto_off(e):
        if o_f.get(u_i) and e.is_private:
            msg = o_m.get(u_i, "Hiện tại mình đang bận, sry!")
            await e.respond(msg)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/clear'))
    async def _clr(e):
        await e.edit("🧹 Đang dọn dẹp..."); msgs = []
        async for m in c.iter_messages(e.chat_id, limit=100, from_user='me'): msgs.append(m.id)
        if msgs: await c.delete_messages(e.chat_id, msgs)

    @c.on(events.NewMessage(outgoing=True, pattern=r'/stop'))
    async def _stp(e):
        s_t[u_i] = False; await e.edit("🛑 **HỆ THỐNG DỪNG**"); await asyncio.sleep(1); await e.delete()

    @c.on(events.NewMessage(outgoing=True, pattern=r'/fake(?:\s+(.+))?'))
    async def _fk(e):
        t = e.pattern_match.group(1)
        try:
            if t: target = await c.get_entity(int(t) if t.isdigit() else t)
            elif e.is_reply: target = await c.get_entity((await e.get_reply_message()).sender_id)
            await e.edit("🔄 Đang fake...")
            await c(functions.account.UpdateProfileRequest(first_name=target.first_name))
            await e.edit(f"🎭 Fake thành công: {target.first_name}")
        except: await e.edit("❌ Lỗi fake!")

@bot.on(events.CallbackQuery(data="login"))
async def _lf(ev):
    u = ev.sender_id
    async with bot.conversation(u) as cv:
        try:
            await cv.send_message("📱 SĐT (+84...):")
            p = (await cv.get_response()).text.strip().replace(" ", "")
            c = TelegramClient(StringSession(), A_ID, A_HS); await c.connect()
            r = await c.send_code_request(p)
            await cv.send_message("📩 OTP (1.2.3.4.5):")
            o = (await cv.get_response()).text.strip().replace(".", "")
            await c.sign_in(p, o, phone_code_hash=r.phone_code_hash)
            u_c[u] = c; _logic(c, u); await cv.send_message("✅ ĐÃ KẾT NỐI!")
        except Exception as e: await cv.send_message(f"❌ {str(e)}")

@bot.on(events.NewMessage(pattern='/start'))
async def _st(ev):
    _su(ev.sender_id)
    await ev.respond(M_T, buttons=[[Button.inline("📱 LOGIN", data="login")]])

if __name__ == '__main__':
    bot.run_until_disconnected()


