import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER GIỮ BOT SỐNG ---
app = Flask('')
@app.route('/')
def home(): return "REX SYSTEM LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_final_fix', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.2}
user_sessions = {}
login_step = {}
spam_running = {} 

# --- GIAO DIỆN CHUẨN ---
BANG_GIA = """📣 **XÁC THỰC NGƯỜI DÙNG**
━━━━━━━━━━━━━━━
💰 **BẢNG GIÁ DỊCH VỤ**
🎫 **2K   | DAY**
🎫 **10K  | WEEK**
🎫 **20K  | MONTH**
🎫 **70K  | VĨNH VIỄN**
━━━━━━━━━━━━━━━
🔑 Nhập key: `/nhapkey <key>`
👑 **ADMIN: @hquycute**"""

MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: VIP VÔ HẠN

🔥 **DANH SÁCH 15 LỆNH:**
🤬 /sp - Chửi nhây 4500 câu (Userbot)
🤬 /spnd - Spam nội dung tự chọn
🤬 /spicon - Spam icon liên tục
📞 /call - Spam Call nạn nhân
⚡ /setdelay - Chỉnh tốc độ (giây)
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin đối thủ
👑 /xoaall - Xóa sạch tin nhắn bot
👻 /info - Lấy ID người dùng
💎 /voice - Chửi bằng Voice gắt
🛑 /stop - DỪNG SPAM NGAY LẬP TỨC
🔴 /stopxoa - Dừng chế độ xóa bot
🚀 /start - Xem lại Menu
👑 /login - Log acc Tele để spam hộ
✈️ /loguot - Thoát tài khoản Tele
✨ ────────────────────────── ✨
ADMIN:HQUY"""

AD_MENU = """👑 **QUẢN TRỊ ẨN**
━━━━━━━━━━━━━━━
➕ /addadm <id> | ➖ /xoaadm <id>
➕ /newkey <mã> | 📋 /listkey
📢 /tb <nội dung>
━━━━━━━━━━━━━━━
ADMIN:HQUY"""

def get_bullets():
    g = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "tuoi lon", "nhoc con", "duoi vl"]
    s = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
    return [f"{random.choice(g)} {random.choice(s)} {random.choice(s)}" for _ in range(4500)]

@bot.on(events.NewMessage)
async def handle(e):
    u, t, cid = e.sender_id, e.text.strip() if e.text else "", e.chat_id
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # 1. LỆNH STOP (PHẢI ĐẶT ĐẦU TIÊN)
    if t == '/stop':
        spam_running[cid] = False
        await e.reply("🛑 **SPAM OFF**\nĐã cưỡng chế dừng luồng!\nADMIN:HQUY")
        return

    # 2. LỆNH ẨN & START
    if (is_o or is_a) and t == '/ad':
        await e.reply(AD_MENU); return
    if t == '/start':
        await e.reply(MENU_USER if is_v else BANG_GIA); return

    # 3. QUY TRÌNH LOGIN (HỖ TRỢ OTP 1.2.3.4.5)
    if t == '/login' and is_v:
        login_step[u] = {'step': 'phone'}; await e.reply("📱 Nhập SĐT (+84...):"); return
    
    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ',''); cl = TelegramClient(StringSession(), API_ID, API_HASH); await cl.connect()
            try:
                h = await cl.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': cl, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 Nhập OTP (Kiểu 1.2.3.4.5):")
            except: await e.reply("❌ Lỗi SĐT!"); del login_step[u]
            return
        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', ''); cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_sessions[u] = cl.session.save(); await e.reply("✅ **LOGIN OK!** Giờ gõ /sp bot sẽ dùng acc này."); del login_step[u]
            except: await e.reply("❌ Sai OTP!"); del login_step[u]
            return

    if not is_v:
        if t.startswith('/nhapkey'):
            k = t.split()[1] if len(t.split()) > 1 else ""
            if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!")
        return

    # 4. THỰC THI 15 LỆNH CHIẾN ĐẤU
    if t == '/sp':
        spam_running[cid] = True; await e.reply("🚀 Rex nã đạn...")
        client_to_use = bot
        if u in user_sessions:
            uc = TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH)
            await uc.connect(); client_to_use = uc
        
        for msg in get_bullets():
            if spam_running.get(cid) == False: break
            try:
                await client_to_use.send_message(cid, msg)
                await asyncio.sleep(db["delay"])
            except: break

    elif t.startswith('/spnd'):
        spam_running[cid] = True; nd = t.replace('/spnd','').strip() or "Sủa e"
        for _ in range(500):
            if spam_running.get(cid) == False: break
            await bot.send_message(cid, nd); await asyncio.sleep(db["delay"])

    elif t == '/spicon':
        spam_running[cid] = True; ic = ["🤡","💩","🔥","⚡"]
        for _ in range(500):
            if spam_running.get(cid) == False: break
            await bot.send_message(cid, random.choice(ic)); await asyncio.sleep(db["delay"])

    elif t == '/xoaall':
        await e.reply("👑 Đang dọn dẹp...")
        async for m in bot.iter_messages(cid, from_user='me'):
            try: await m.delete()
            except: pass

    elif t == '/voice':
        try:
            tts = gTTS(text="địt mẹ mày con chó, cha hắc quy nồ một vả chết cụ mày luôn", lang='vi')
            tts.save("v.ogg"); await bot.send_file(cid, "v.ogg", voice_note=True); os.remove("v.ogg")
        except: pass

    elif t.startswith('/setdelay'):
        try: db["delay"] = float(t.split()[1]); await e.reply(f"⚡ Delay: {db['delay']}s")
        except: pass

    elif t == '/info': await e.reply(f"👤: {e.sender.first_name}\n🆔: {u}\nADMIN:HQUY")

    # LỆNH ADMIN (OWNER ONLY)
    if is_o:
        if t.startswith('/addadm'):
            try: aid = int(t.split()[1]); db["admins"].append(aid); await e.reply(f"✅ Add Admin {aid}")
            except: pass
        elif t.startswith('/newkey'):
            nk = t.split()[1]; db["keys"].append(nk); await e.reply(f"🔑 Key: {nk}")

if __name__ == '__main__':
    bot.run_until_disconnected()
