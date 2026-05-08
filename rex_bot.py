import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions
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

bot = TelegramClient('rex_main_fix', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.15}
active_userbots = {} 
login_step = {}
st = {}

# --- BẢNG GIÁ CHUẨN THỨ TỰ ---
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
👑 /login - Đăng nhập acc để bot chửi hộ
✈️ /loguot - Thoát tài khoản Tele
✨ ────────────────────────── ✨
ADMIN:HQUY"""

def get_bullets():
    base = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "yeu ot", "tk dix", "con ga", "tuoi lon", "nhoc con", "duoi vl"]
    sfx = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
    return [f"{random.choice(base)} {random.choice(sfx)} {random.choice(sfx)}" for _ in range(4500)]

@bot.on(events.NewMessage)
async def handle(e):
    u, t = e.sender_id, e.text.strip() if e.text else ""
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    if (is_o or is_a) and t == '/ad':
        await e.reply("👑 QUẢN TRỊ: /addadm | /listadm | /newkey | /listkey | /tb\nADMIN:HQUY"); return

    if t == '/login' and is_v:
        login_step[u] = {'step': 'phone'}
        await e.reply("📱 **BƯỚC 1:** Nhập Số điện thoại (VD: +84987654321)"); return

    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ', '')
            client = TelegramClient(StringSession(), API_ID, API_HASH)
            await client.connect()
            try:
                h = await client.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': client, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 **BƯỚC 2:** Nhập OTP kiểu `1.2.3.4.5`."); return
            except Exception as ex: await e.reply(f"❌ Lỗi: {ex}"); del login_step[u]; return

        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', '')
            cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                active_userbots[u] = cl
                await e.reply("✅ **LOGIN THÀNH CÔNG!** Có thể dùng /call ngay."); 
                del login_step[u]; return
            except Exception as ex: await e.reply(f"❌ OTP Sai: {ex}"); del login_step[u]; return

    if t == '/start': await e.reply(MENU_USER if is_v else BANG_GIA); return
    
    if t.startswith('/nhapkey'):
        k = t.split()[1] if len(t.split()) > 1 else ""
        if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!"); return
        else: await e.reply("❌ Sai key!"); return

    if not is_v: return

    # --- LỆNH SPAM CALL (DÀNH CHO USERBOT) ---
    if t.startswith('/call'):
        if u not in active_userbots:
            await e.reply("❌ Ông phải /login tài khoản Tele trước mới dùng được lệnh này!"); return
        
        target = t.split()[1] if len(t.split()) > 1 else None
        if not target:
            await e.reply("⚠️ Vui lòng nhập ID hoặc Username nạn nhân: `/call @username` hoặc `/call 123456`."); return
        
        st[e.chat_id] = True
        await e.reply(f"📞 Đang bắt đầu Spam Call nạn nhân {target}...")
        user_cl = active_userbots[u]
        
        for _ in range(50): # Spam 50 cuộc gọi
            if not st.get(e.chat_id): break
            try:
                # Logic: Tạo cuộc gọi rồi ngắt ngay để làm phiền nạn nhân
                res = await user_cl(functions.phone.RequestCallRequest(
                    user_id=target,
                    random_id=random.randint(0, 0x7fffffff),
                    g_a_hash=b'123',
                    protocol=functions.phone.PhoneCallProtocol(
                        udp_p2p=True, udp_reflector=True,
                        min_layer=65, max_layer=65,
                        library_versions=['1.0.0']
                    )
                ))
                await asyncio.sleep(2) # Đợi chuông reo
                await user_cl(functions.phone.DiscardCallRequest(peer=res.phone_call.id, reason=functions.phone.PhoneCallDiscardReasonDisconnect(), duration=0, connection_id=0))
                await asyncio.sleep(db["delay"])
            except: 
                await asyncio.sleep(5); continue

    # --- CÁC LỆNH KHÁC ---
    elif t == '/sp':
        st[e.chat_id] = True; await e.reply("🚀 Rex nã 4500 phát đạn cũ..."); 
        for c in get_bullets():
            if not st.get(e.chat_id): break
            try: await bot.send_message(e.chat_id, c); await asyncio.sleep(db["delay"])
            except: break

    elif t == '/stop': st[e.chat_id] = False; await e.reply("🛑 SPAM OFF\nADMIN:HQUY")
    
    elif t.startswith('/spnd'):
        st[e.chat_id] = True; nd = t.replace('/spnd','').strip() or "Sủa e"
        for _ in range(500):
            if not st.get(e.chat_id): break
            await bot.send_message(e.chat_id, nd); await asyncio.sleep(db["delay"])

    elif t == '/xoaall':
        await e.reply("👑 Đang dọn dẹp..."); 
        async for m in bot.iter_messages(e.chat_id, from_user='me'): await m.delete()

    elif t == '/voice':
        try:
            tts = gTTS(text="địt mẹ mày con chó, cha hắc quy nồ một vả chết cụ mày luôn", lang='vi')
            tts.save("v.ogg"); await bot.send_file(e.chat_id, "v.ogg", voice_note=True); os.remove("v.ogg")
        except: pass

if __name__ == '__main__':
    bot.run_until_disconnected()
