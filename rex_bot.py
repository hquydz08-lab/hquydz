import os, asyncio, random
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER GIỮ BOT SỐNG ---
app = Flask('')
@app.route('/')
def home(): return "REX ADMIN LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 
bot = TelegramClient('rex_final', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "delay": 0.2}
st = {}

# --- GIAO DIỆN CHUẨN ---
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

MENU = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn

🔥 DANH SÁCH MENU
🤬 /sp -> Trêu nhây 200 câu cực gắt
🤬 /spnd -> Spam nội dung tự chọn
🤬 /spicon -> Spam icon liên tục
📞 /call -> Spam Call + ID
⚡ /setdelay -> Chỉnh tốc độ
🚫 /anti -> Tự xóa tin đối thủ
✅ /unanti -> Ngừng xóa tin
👑 /xoaall -> Xoá sạch spam bot
👻 /info -> Check ID người dùng
💎 /voice -> Chuyển sang Voice
🛑 /stop -> Dừng tất cả (SPAM OFF)
🔴 /stopxoa -> Dừng xóa bot
🚀 /start -> Khởi động bot
👑 /login -> Đăng nhập acc
✈️ /loguot -> Thoát acc bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

# --- MENU ẨN (CHỈ OWNER THẤY) ---
AD_MENU = """👑 ADMIN PANEL (OWNER ONLY)
━━━━━━━━━━━━━━━
➕ /addkey <mã> - Thêm key
📋 /listkey - Danh sách key
📢 /tb <nội dung> - Thông báo hệ thống
💀 /listvic - Danh sách nạn nhân
━━━━━━━━━━━━━━━"""

@bot.on(events.NewMessage)
async def handle(e):
    u, t = e.sender_id, e.text.strip() if e.text else ""
    is_o = (u == OWNER_ID)
    is_v = (u in db["auth"] or is_o)

    # 1. PHẢN HỒI LỆNH CƠ BẢN
    if t == '/start':
        await e.reply(MENU if is_v else BANG_GIA)
        return

    # 2. LỆNH ẨN /ad (CHỈ CHỦ NHÂN MỚI HIỆN BẢNG QUẢN TRỊ)
    if t == '/ad':
        if is_o:
            await e.reply(AD_MENU)
        else:
            # Người thường gõ /ad sẽ bị bơ hoặc hiện menu thường
            pass 
        return
    
    # 3. QUẢN LÝ KEY (CHỈ OWNER)
    if is_o:
        if t.startswith('/addkey'):
            nk = t.split()[1] if len(t.split()) > 1 else ""
            if nk: db["keys"].append(nk); await e.reply(f"✅ Thêm key: {nk}")
        elif t == '/listkey':
            await e.reply(f"📋 Danh sách key: {db['keys']}")
        elif t.startswith('/tb'):
            msg = t.replace('/tb','').strip()
            for x in list(set(db["auth"]+[OWNER_ID])):
                try: await bot.send_message(x, f"📢 **TB TỪ ADMIN**\n\n{msg}\n\nADMIN:HQUY")
                except: pass
            await e.reply("✅ Đã gửi thông báo!")

    if not is_v: return

    # 4. NHẬP KEY
    if t.startswith('/nhapkey'):
        k = t.split()[1] if len(t.split()) > 1 else ""
        if k in db["keys"]:
            db["auth"].append(u); await e.reply("✅ VIP ĐÃ BẬT! Gõ /start")
        else: await e.reply("❌ Key không tồn tại!")

    # 5. VOICE VÀ SPAM
    if t == '/voice':
        try:
            tts = gTTS(text="địt mẹ mày cha hắc quy nồ một vả chết cụ mày luôn", lang='vi')
            tts.save("v.ogg")
            await bot.send_file(e.chat_id, "v.ogg", voice_note=True)
            os.remove("v.ogg")
        except: pass

    if t == '/sp':
        st[e.chat_id] = True
        g = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "yeu ot", "speed lun", "tuoi lon"]
        d = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
        await e.reply("🚀 Rex nã 200 đạn...")
        for _ in range(200):
            if not st.get(e.chat_id): break
            await bot.send_message(e.chat_id, f"{random.choice(g)} {random.choice(d)}")
            await asyncio.sleep(db["delay"])
            
    elif t == '/stop':
        st[e.chat_id] = False; await e.reply("🛑 SPAM OFF\nADMIN:HQUY")

if __name__ == '__main__':
    bot.run_until_disconnected()

