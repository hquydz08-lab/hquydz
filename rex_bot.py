import os, asyncio, random, re
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "REX USERBOT LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_main_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.15}
user_sessions = {} # Lưu session của từng người dùng: {user_id: StringSession}
login_step = {} # Trạng thái login

# --- GIAO DIỆN BẢNG GIÁ ĐÚNG THỨ TỰ ---
BANG_GIA = """📣 XÁC THỰC NGƯỜI DÙNG
━━━━━━━━━━━━━━━
💰 BẢNG GIÁ
🎫 2K/DAY
🎫 10K/WEEK
🎫 20K/MONTH
🎫 70K/VV
━━━━━━━━━━━━━━━
🔑 Vui lòng nhập key để sử dụng bot
📝 /nhapkey <key>
━━━━━━━━━━━━━━━
👑 ADMIN: @hquycute"""

MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn

🔥 DANH SÁCH MENU:
🤬 /sp - Dùng Acc đã login nã 4500 câu
🤬 /spnd - Spam nội dung tự chọn
🤬 /spicon - Spam icon liên tục
📞 /call - Spam Call + ID nạn nhân
⚡ /setdelay - Điều chỉnh tốc độ spam
🚫 /anti - Tự động xóa tin đối thủ
✅ /unanti - Ngừng chế độ xóa tin
👑 /xoaall - Xoá sạch tin nhắn spam
👻 /info - Kiểm tra ID người dùng
💎 /voice - Chuyển văn bản sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng lệnh xóa bot
🚀 /start - Khởi động lại bot
👑 /login - Đăng nhập tài khoản Tele để spam
✈️ /loguot - Thoát tài khoản Tele
✨ ────────────────────────── ✨
ADMIN:HQUY"""

# --- HÀM CHỬI 4500 CÂU ---
def get_bullets():
    base = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "yeu ot", "tk dix", "con ga", "tuoi lon", "nhoc con", "duoi vl"]
    sfx = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
    return [f"{random.choice(base)} {random.choice(sfx)} {random.choice(sfx)}" for _ in range(4500)]

@bot.on(events.NewMessage)
async def handle(e):
    u, t = e.sender_id, e.text.strip() if e.text else ""
    is_o = (u == OWNER_ID)
    is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # LỆNH ẨN /ad CHỈ OWNER/ADMIN THẤY
    if (is_o or is_a) and t == '/ad':
        await e.reply("👑 QUẢN TRỊ: /addadm | /listadm | /newkey | /listkey | /tb\nADMIN:HQUY"); return

    # XỬ LÝ LOGIN (DÙNG TELETHON ĐỂ LOG VÀO ACC NGƯỜI DÙNG)
    if t == '/login' and is_v:
        login_step[u] = {'step': 'phone'}
        await e.reply("📱 **BƯỚC 1:** Nhập Số điện thoại (VD: +84987654321)"); return

    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ', '')
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            try:
                code_hash = await client.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': client, 'phone': phone, 'hash': code_hash.phone_code_hash}
                await e.reply("📩 **BƯỚC 2:** Nhập mã OTP theo dạng `1.2.3.4.5` để đăng nhập."); return
            except Exception as ex:
                await e.reply(f"❌ Lỗi: {str(ex)}"); del login_step[u]; return

        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', '')
            client = login_step[u]['client']
            try:
                await client.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_sessions[u] = client.session.save() # Lưu lại session
                await e.reply("✅ **LOGIN THÀNH CÔNG!**\nBây giờ gõ /sp để acc này đi war.\nADMIN:HQUY")
                del login_step[u]; return
            except Exception as ex:
                await e.reply(f"❌ OTP Sai: {str(ex)}"); del login_step[u]; return

    # LỆNH START & KEY
    if t == '/start': await e.reply(MENU_USER if is_v else BANG_GIA); return
    if t.startswith('/nhapkey'):
        k = t.split()[1] if len(t.split()) > 1 else ""
        if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!"); return
        else: await e.reply("❌ Sai key!"); return

    if not is_v: return

    # LỆNH SPAM (DÙNG CHÍNH ACC ĐÃ LOGIN NẾU CÓ)
    if t == '/sp':
        st[e.chat_id] = True
        await e.reply("🚀 Rex đang nã 4500 phát đạn... Đợi tí!")
        
        # Kiểm tra xem có session login chưa, nếu có thì dùng acc đó gửi
        sender = bot
        if u in user_sessions:
            user_client = TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH)
            await user_client.connect()
            sender = user_client

        for c in get_bullets():
            if not st.get(e.chat_id): break
            try:
                await sender.send_message(e.chat_id, c)
                await asyncio.sleep(db["delay"])
            except errors.FloodWaitError as f: await asyncio.sleep(f.seconds)
            except: break

    elif t == '/stop': st[e.chat_id] = False; await e.reply("🛑 SPAM OFF\nADMIN:HQUY")
    elif t == '/loguot':
        if u in user_sessions: del user_sessions[u]; await e.reply("✈️ Đã gỡ tài khoản Tele!"); 
        else: await e.reply("❌ Chưa login acc nào!")

if __name__ == '__main__':
    bot.run_until_disconnected()
