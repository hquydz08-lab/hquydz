import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions, types
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "REX SYSTEM LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_war_final', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": {}, "auth": [], "admins": [OWNER_ID], "delay": 0.3, "anti": False}
user_clients = {} 
login_step = {}
spam_running = {}

# --- GIAO DIỆN CHUẨN CỦA ÔNG ---
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
🤬 /sp - Trêu nhây 
🤬 /spnd - spam + nội dung 
🤬 /spicon - spam icon bất kì
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng xóa bot
🚀 /start - Khởi động bot
👑 /login - log acc
✈️ /loguot - thoát acc
🎭 /fake - mượn xác người khác
✨ ────────────────────────── ✨
ADMIN:HQUY"""

AD_MENU = """👑 **QUẢN TRỊ VIÊN**
━━━━━━━━━━━━━━━
➕ /addadm - Thêm Admin
➖ /xoaadm - Xoá Admin
📜 /listadm - Xem ds Admin
🔑 /newkey - Tạo key mới
❌ /xoakey - Xoá key
📢 /tb - Thông báo người dùng
━━━━━━━━━━━━━━━
ADMIN:HQUY"""

# --- KHO ĐẠN SỚ NGÔN ---
DAN_DUOC = [
    "cn choa ei=))=))=))=))", "123=))=))=))=))", "m chay anh cmnr=))=))=))=))=))",
    "m yeu ot z tk nfu=))=))=))=))=))", "m cham vl e=))=))=))", "slow lun e=))=))=))=))",
    "yeu z cn dix=))=))=))=))", "tk 3de=))=))=))=))=))", "tk dix lgbt=))=))=))=))",
    "cn choa nfu=))=))=))=))=))", "deo co canh lun e=))=))=))=))"
]

@bot.on(events.NewMessage)
async def handle(e):
    u, t, cid = e.sender_id, e.text.strip() if e.text else "", e.chat_id
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    if not is_v and not t.startswith('/nhapkey'):
        await e.reply(BANG_GIA); return

    if t == '/ad' and (is_o or is_a):
        await e.reply(AD_MENU); return

    if t == '/start' or t == '/menu':
        await e.reply(MENU_VIP); return

    # --- HỆ THỐNG QUẢN TRỊ ---
    if is_o or is_a:
        if t.startswith('/addadm'):
            aid = int(t.split()[1]); db["admins"].append(aid); await e.reply(f"✅ Thêm Admin {aid}")
        elif t.startswith('/newkey'):
            k = t.split()[1]; db["keys"][k] = "forever"; await e.reply(f"🔑 Key: `{k}`")
        elif t.startswith('/tb'):
            msg = t.replace('/tb', '').strip()
            for user in set(db["auth"] + db["admins"]):
                try: await bot.send_message(user, f"📢 **TB:** {msg}\nADMIN:HQUY")
                except: pass

    # --- LOGIN OTP 1.2345 ---
    if t == '/login':
        login_step[u] = {'step': 'phone'}; await e.reply("📱 Nhập SĐT (VD: +84...):")
    elif u in login_step:
        if login_step[u]['step'] == 'phone':
            cl = TelegramClient(StringSession(), API_ID, API_HASH); await cl.connect()
            h = await cl.send_code_request(t.replace(' ',''))
            login_step[u] = {'step': 'otp', 'client': cl, 'phone': t, 'hash': h.phone_code_hash}
            await e.reply("📩 Nhập OTP (VD: 1.2345):")
        elif login_step[u]['step'] == 'otp':
            try:
                cl = login_step[u]['client']
                await cl.sign_in(login_step[u]['phone'], t.replace('.',''))
                user_clients[u] = cl; await e.reply("✅ **LOGIN OK!** Acc chính đã sẵn sàng."); del login_step[u]
            except: await e.reply("❌ Lỗi!"); del login_step[u]
        return

    # --- LỆNH FAKE ---
    if t.startswith('/fake'):
        if u not in user_clients: await e.reply("❌ Cần /login!"); return
        try:
            uc = user_clients[u]; target = t.split()[1]
            ent = await uc.get_entity(target)
            await uc(functions.account.UpdateProfileRequest(first_name=ent.first_name, last_name=ent.last_name or ""))
            await e.reply(f"🎭 Đã fake thành: {ent.first_name}"); return
        except: await e.reply("❌ Lỗi fake!"); return

    # --- THỰC THI SPAM (ACC BẠN SPAM) ---
    if t == '/sp':
        if u not in user_clients: await e.reply("❌ Cần /login!"); return
        spam_running[cid] = True; uc = user_clients[u]
        # Lấy đúng ID phòng chat để không bị spam vào lưu trữ
        peer = await uc.get_input_entity(cid)
        while spam_running.get(cid):
            for msg in DAN_DUOC:
                if not spam_running.get(cid): break
                try: await uc.send_message(peer, msg); await asyncio.sleep(db["delay"])
                except: break

    if t == '/stop':
        spam_running[cid] = False; await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY"); return

    if t.startswith('/voice'):
        txt = t.replace('/voice','').strip() or "sủa mau"
        gTTS(text=txt, lang='vi').save("v.ogg")
        await bot.send_file(cid, "v.ogg", voice_note=True); os.remove("v.ogg")

if __name__ == '__main__':
    bot.run_until_disconnected()
