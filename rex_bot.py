import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "REX FULL SYSTEM LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_full_15', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.3}
user_sessions = {} 
login_step = {}
spam_running = {}

# --- KHO ĐẠN SỚ NGÔN (1 DÒNG DÀI) ---
NEW_BULLETS = [
    "123 con chó cùng sủa =))", "con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣",
    "thằng cha mày gánh lúa cho mày đi đú à :))", "con điếm bị bố sỉ nhục",
    "bố đái vào cái bàn thờ thờ tổ tiên 3 đời con chó ngu ăn cứt :))",
    "thằng em bị bố gõ cho hồn bay phách lạc đi cùng con mẹ mày rồi ak 🤪",
    "bố mà tung skill sút mày là tỉ lệ tử vong của mày là 100% =)))",
    "con đ/ĩ mẹ mày bị tao cầm đinh ba xiên chết tại chỗ thằng bố mày ôm hận tao qua báo thù",
    "bố nhét cặc vào trong lồn mẹ mày xem cái mặt gái mẹ mày làm đĩ trông như nào :))",
    "mày nhai ngôn là con ĩ ẹ m chết ngay lập tức 👎", "bọn bố bá vcl :))",
    "mẹ m bị bọn a thay nhau đụ từ bắc đến nam mà 😂👊", "con chó m sủa liên tục mau lên 🤣🤟"
]

def get_rex_bullets():
    bullets = []
    for _ in range(2000):
        raw_msg = random.choice(NEW_BULLETS)
        one_line_msg = " ".join([raw_msg for _ in range(12)]) 
        bullets.append(one_line_msg)
    return bullets

# --- GIAO DIỆN HỆ THỐNG ---
MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: VIP VÔ HẠN

🔥 **DANH SÁCH 15 LỆNH CHIẾN ĐẤU:**
🤬 /sp - Spam sớ ngôn 1 dòng (Userbot)
🤬 /spnd - Spam nội dung tự chọn 1 dòng
🤬 /spicon - Spam icon liên tục
📞 /call - Spam Call nạn nhân
⚡ /setdelay - Chỉnh tốc độ (giây)
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin đối thủ
👑 /xoaall - Xóa sạch tin nhắn bot
👻 /info - Lấy ID người dùng (Kèm @)
💎 /voice - Chửi bằng Voice gắt
🛑 /stop - SPAM OFF (Dừng luồng)
🔴 /stopxoa - Dừng chế độ xóa bot
🚀 /start - Xem lại Menu
👑 /login - Log acc Tele để mượn xác
✈️ /loguot - Thoát tài khoản
✨ ────────────────────────── ✨
ADMIN:HQUY"""

AD_MENU = """👑 **QUẢN TRỊ ẨN (HQUY ONLY)**
━━━━━━━━━━━━━━━
➕ /addadm | ➖ /xoaadm
📋 /listadm | ➕ /newkey
📋 /listkey | 📢 /tb <nội dung>
━━━━━━━━━━━━━━━
ADMIN:HQUY"""

@bot.on(events.NewMessage)
async def handle(e):
    u, t, cid = e.sender_id, e.text.strip() if e.text else "", e.chat_id
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # LỆNH DỪNG KHẨN CẤP
    if t == '/stop':
        spam_running[cid] = False
        await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY"); return

    if t == '/start':
        await e.reply(MENU_USER if is_v else "🎫 Nhập key: `/nhapkey <key>`"); return

    if (is_o or is_a) and t == '/ad':
        await e.reply(AD_MENU); return

    if not is_v:
        if t.startswith('/nhapkey'):
            k = t.split()[1] if len(t.split()) > 1 else ""
            if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!")
        return

    # 1. LOGIN USERBOT
    if t == '/login':
        login_step[u] = {'step': 'phone'}; await e.reply("📱 Nhập SĐT (+84...):"); return
    
    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ',''); cl = TelegramClient(StringSession(), API_ID, API_HASH); await cl.connect()
            try:
                h = await cl.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': cl, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 Nhập OTP (dạng 1.2.3.4.5):")
            except: await e.reply("❌ Lỗi!"); del login_step[u]
            return
        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', ''); cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_sessions[u] = cl.session.save(); await e.reply("✅ **LOGIN THÀNH CÔNG!**"); del login_step[u]
            except: await e.reply("❌ Sai OTP!"); del login_step[u]
            return

    # 2. THỰC THI 15 LỆNH (CHỈ DÙNG ACC USER ĐÃ LOGIN)
    if t == '/sp':
        if u not in user_sessions: await e.reply("❌ Cần `/login` để nã đạn!"); return
        spam_running[cid] = True
        async with TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH) as uc:
            for msg in get_rex_bullets():
                if not spam_running.get(cid): break
                try: await uc.send_message(cid, msg); await asyncio.sleep(db["delay"])
                except: break

    elif t.startswith('/spnd'):
        if u not in user_sessions: await e.reply("❌ Cần `/login`!"); return
        spam_running[cid] = True; nd = t.replace('/spnd','').strip() or "gay"
        msg = " ".join([nd for _ in range(15)])
        async with TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH) as uc:
            for _ in range(1000):
                if not spam_running.get(cid): break
                try: await uc.send_message(cid, msg); await asyncio.sleep(db["delay"])
                except: break

    elif t == '/info':
        # Code lấy ID người dùng khác qua @mention
        target = t.split()[1] if len(t.split()) > 1 else "me"
        try:
            entity = await bot.get_entity(target)
            await e.reply(f"👤 Tên: {entity.first_name}\n🆔 ID: `{entity.id}`\nADMIN:HQUY")
        except: await e.reply("❌ Không tìm thấy người này!")

    elif t == '/voice':
        try:
            tts = gTTS(text="địt mẹ mày con chó, cha hắc quy nồ một vả chết cụ mày luôn", lang='vi')
            tts.save("v.ogg"); await bot.send_file(cid, "v.ogg", voice_note=True); os.remove("v.ogg")
        except: pass

    elif t == '/xoaall':
        await e.reply("👑 Đang dọn dẹp tin nhắn của bot..."); async for m in bot.iter_messages(cid, from_user='me'): await m.delete()

    # CÁC LỆNH ADMIN ẨN
    if is_o:
        if t.startswith('/addadm'):
            aid = int(t.split()[1]); db["admins"].append(aid); await e.reply(f"✅ Đã thêm Admin: {aid}")
        elif t.startswith('/newkey'):
            nk = t.split()[1]; db["keys"].append(nk); await e.reply(f"🔑 Key mới: `{nk}`")

if __name__ == '__main__':
    bot.run_until_disconnected()
