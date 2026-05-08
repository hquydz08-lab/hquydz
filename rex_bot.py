import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "REX USERBOT IS LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_bot_only', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": {}, "auth": [], "admins": [OWNER_ID], "delay": 0.3, "anti": False}
user_clients = {} 
login_step = {}
spam_running = {}

# --- GIAO DIỆN ---
BANG_GIA = """📣 XÁC THỰC NGƯỜI DÙNG
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

MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /sp - Trêu nhây (Acc bạn spam)
🤬 /spnd - Spam nội dung (Acc bạn spam)
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🚀 /start - Khởi động bot
👑 /login - Log acc cá nhân
✈️ /loguot - Thoát acc
✨ ────────────────────────── ✨
ADMIN:HQUY"""

AD_MENU = """👑 **MENU QUẢN TRỊ VIÊN**
━━━━━━━━━━━━━━━
➕ /addadm | ➖ /xoaadm
📜 /listadm | 🔑 /newkey
📢 /tb <nội dung>
━━━━━━━━━━━━━━━
ADMIN:HQUY"""

# --- KHO KẸO (1 CÂU 1 DÒNG) ---
DAN_DUOC = [
    "cn choa ei=))=))=))=))", "123=))=))=))=))", "m chay anh cmnr=))=))=))=))=))",
    "m yeu ot z tk nfu=))=))=))=))=))", "m cham vl e=))=))=))", "slow lun e=))=))=))=))",
    "yeu z cn dix=))=))=))=))", "tk 3de=))=))=))=))=))", "tk dix lgbt=))=))=))=))",
    "cn choa nfu=))=))=))=))=))", "deo co canh lun e=))=))=))=))", "m cham vl e=))=))=))=))",
    "m yeu v=))=))=))=))=))=))", "yeu ro=))=))=))=))=))=))", "bia a=))=))=))=))",
    "tk dix=))=))=))=))", "mau k=))=))=))=))", "mau de=))=))=))=))=))",
    "cham a=))=))=))=))=))=))", "tk nfu =))=))=))=))=))", "mau ti de=))=))=))=))",
    "yeu ot vcl=))=))=))=))", "cmm dot tu kia=))=))=))", "lien tuc de=))=))=))=))=))"
]

@bot.on(events.NewMessage)
async def handle(e):
    u, t, cid = e.sender_id, e.text.strip() if e.text else "", e.chat_id
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # 1. CHẶN NGƯỜI LẠ (CHỈ HIỆN BẢNG GIÁ)
    if not is_v and not t.startswith('/nhapkey'):
        await e.reply(BANG_GIA); return

    # 2. LỆNH /ad (CHỈ ADMIN THẤY)
    if t == '/ad' and (is_o or is_a):
        await e.reply(AD_MENU); return

    # 3. LỆNH CÔNG KHAI CHO NGƯỜI CÓ KEY
    if t == '/start' or t == '/menu':
        await e.reply(MENU_VIP); return

    if t.startswith('/nhapkey'):
        try:
            k = t.split()[1]
            if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!"); return
            else: await e.reply("❌ Key sai!"); return
        except: pass

    # 4. CƠ CHẾ LOGIN (USERBOT - QUAN TRỌNG)
    if t == '/login':
        login_step[u] = {'step': 'phone'}; await e.reply("📱 Nhập SĐT (VD: +84987654321):"); return

    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ','')
            cl = TelegramClient(StringSession(), API_ID, API_HASH); await cl.connect()
            try:
                h = await cl.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': cl, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 Nhập OTP (VD mã 12345 nhập là 1.2345):")
            except: await e.reply("❌ Lỗi SĐT!"); del login_step[u]
            return
        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', '') # Tự động bỏ dấu chấm để lấy mã chuẩn
            cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_clients[u] = cl # Lưu Client đã login
                await e.reply("✅ **LOGIN THÀNH CÔNG!**\nBây giờ dùng `/sp` acc bạn sẽ tự spam."); del login_step[u]
            except: await e.reply("❌ OTP Sai!"); del login_step[u]
            return

    # 5. THỰC THI SPAM (CHỈ DÙNG ACC ĐÃ LOGIN)
    if t == '/sp':
        if u not in user_clients:
            await e.reply("❌ Bạn chưa `/login` acc cá nhân!"); return
        
        spam_running[cid] = True
        uc = user_clients[u] # Lấy acc cá nhân ra để spam
        await e.reply("🚀 **ĐANG DÙNG ACC BẠN ĐỂ CHIẾN...**")
        
        while spam_running.get(cid):
            for msg in DAN_DUOC:
                if not spam_running.get(cid): break
                try:
                    await uc.send_message(cid, msg) # ACC CÁ NHÂN GỬI TIN
                    await asyncio.sleep(db["delay"])
                except: break

    elif t == '/stop':
        spam_running[cid] = False; await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

    # (Các lệnh quản trị ẩn /newkey, /tb, /addadm nằm ở đây...)
    if is_o or is_a:
        if t.startswith('/newkey'):
            args = t.split(); k = args[1]; db["keys"][k] = "forever"; await e.reply(f"🔑 Key: `{k}`")
        elif t.startswith('/tb'):
            msg = t.replace('/tb','').strip()
            for user in set(db["auth"] + db["admins"]):
                try: await bot.send_message(user, f"📢 TB: {msg}")
                except: pass

if __name__ == '__main__':
    bot.run_until_disconnected()
