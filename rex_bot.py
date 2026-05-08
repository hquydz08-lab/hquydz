import os, asyncio, random
from telethon import TelegramClient, events, errors
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER GIỮ BOT SỐNG ---
app = Flask('')
@app.route('/')
def home(): return "REX SYSTEM FIXED"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

# Khởi tạo Bot chính
bot = TelegramClient('rex_bot_main', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.15}
user_sessions = {} # {user_id: session_string}
login_step = {} # {user_id: {'step': '...', 'client': ...}}
st = {}

# --- GIAO DIỆN CHUẨN ---
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
🤬 /sp - Trêu nhây 4500 câu cực gắt
🤬 /spnd - Spam nội dung tự chọn
🤬 /spicon - Spam icon liên tục
📞 /call - Spam Call (Yêu cầu login)
⚡ /setdelay - Chỉnh tốc độ (giây)
🚫 /anti - Tự xóa tin nhắn đối thủ
✅ /unanti - Ngừng xóa tin đối thủ
👑 /xoaall - Xóa sạch tin nhắn của bot
👻 /info - Lấy ID người dùng nhanh
💎 /voice - Chuyển văn bản sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng chế độ xóa bot
🚀 /start - Xem lại bảng menu này
👑 /login - Đăng nhập acc Tele để spam
✈️ /loguot - Thoát tài khoản Tele
✨ ────────────────────────── ✨
ADMIN:HQUY"""

def get_bullets():
    base = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "yeu ot", "tk dix", "con ga", "tuoi lon", "nhoc con"]
    sfx = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
    return [f"{random.choice(base)} {random.choice(sfx)} {random.choice(sfx)}" for _ in range(4500)]

# --- XỬ LÝ LỆNH TỪ BOT ---
@bot.on(events.NewMessage)
async def bot_handler(e):
    u, t = e.sender_id, e.text.strip() if e.text else ""
    is_o = (u == OWNER_ID)
    is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # 1. Start & Bảng giá (FIXED - Gõ phát ra luôn)
    if t == '/start':
        await e.reply(MENU_USER if is_v else BANG_GIA)
        return

    # 2. Nhập Key
    if t.startswith('/nhapkey'):
        k = t.split()[1] if len(t.split()) > 1 else ""
        if k in db["keys"]:
            db["auth"].append(u); await e.reply("✅ XÁC THỰC VIP THÀNH CÔNG! Gõ /start để thấy Menu.")
        else: await e.reply("❌ Sai key rồi con trai!")
        return

    if not is_v: return

    # 3. Lệnh ẩn /ad
    if (is_o or is_a) and t == '/ad':
        await e.reply("👑 QUẢN TRỊ: /addadm | /listadm | /newkey | /listkey | /tb\nADMIN:HQUY"); return

    # 4. Quy trình Login (FIXED - Nhập OTP kiểu 1.2.3.4.5)
    if t == '/login':
        login_step[u] = {'step': 'phone'}
        await e.reply("📱 **BƯỚC 1:** Gửi SĐT (VD: +84987654321)")
        return

    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ', '')
            cl = TelegramClient(StringSession(), API_ID, API_HASH)
            await cl.connect()
            try:
                h = await cl.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': cl, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 **BƯỚC 2:** Nhập OTP kiểu `1.2.3.4.5` để bot log vào acc.")
            except Exception as ex: await e.reply(f"❌ Lỗi: {ex}"); del login_step[u]
            return

        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', '')
            cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_sessions[u] = cl.session.save()
                await e.reply("✅ **LOGIN THÀNH CÔNG!** Bây giờ gõ /sp, bot sẽ dùng acc này để nã đạn.")
                
                # Kích hoạt Radar Auto-War cho acc vừa log
                @cl.on(events.NewMessage(outgoing=True))
                async def user_auto_sp(ev):
                    if ev.text.startswith('/sp'):
                        for c in get_bullets():
                            try: await ev.respond(c); await asyncio.sleep(db["delay"])
                            except: break
                del login_step[u]
            except Exception as ex: await e.reply(f"❌ OTP Sai: {ex}"); del login_step[u]
            return

    # 5. Các lệnh Spam
    if t == '/sp':
        st[e.chat_id] = True
        # Nếu đã login acc tele, dùng acc đó spam, nếu chưa dùng bot
        target_client = bot
        if u in user_sessions:
            cl_user = TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH)
            await cl_user.connect()
            target_client = cl_user
            
        await e.reply("🚀 Rex nã 4500 phát đạn... BẮT ĐẦU!")
        for c in get_bullets():
            if not st.get(e.chat_id): break
            try: await target_client.send_message(e.chat_id, c); await asyncio.sleep(db["delay"])
            except: break

    elif t == '/stop': 
        st[e.chat_id] = False; await e.reply("🛑 SPAM OFF\nADMIN:HQUY")

    elif t == '/info': 
        await e.reply(f"👤 Tên: {e.sender.first_name}\n🆔 ID: {u}\nADMIN:HQUY")

if __name__ == '__main__':
    bot.run_until_disconnected()
