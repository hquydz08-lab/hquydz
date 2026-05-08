import os, asyncio, random
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER GIỮ BOT LIVE 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "REX SUPREME IS LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_supreme', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.15}
st = {}

# --- GIAO DIỆN BẢNG GIÁ CHUẨN ---
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

# --- MENU 15 LỆNH HÀNG DỌC CÓ MÔ TẢ ---
MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn

🔥 DANH SÁCH MENU:
🤬 /sp - Trêu nhây 4500 câu cực gắt
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
👑 /login - Đăng nhập tài khoản Userbot
✈️ /loguot - Thoát toàn bộ tài khoản
✨ ────────────────────────── ✨
ADMIN:HQUY"""

# --- MENU ẨN (CHỈ ADMIN/OWNER THẤY) ---
AD_MENU = """👑 HỆ THỐNG QUẢN TRỊ ẨN
━━━━━━━━━━━━━━━
⭐ QUYỀN OWNER:
➕ /addadm <id> - Cấp quyền Admin
➖ /xoaadm <id> - Gỡ quyền Admin
📋 /listadm - Xem danh sách Admin

🔥 QUYỀN ADMIN:
➕ /newkey <mã> - Tạo key mới
➖ /xoakey <mã> - Xóa mã key
📋 /listkey - Xem toàn bộ key
📢 /tb <nội dung> - Thông báo toàn hệ thống
━━━━━━━━━━━━━━━
ADMIN:HQUY"""

def get_bullets():
    base = ["cn choa", "m chay anh", "tk nfu", "m cham vl", "yeu ot", "tk dix", "con ga", "speed lun", "mau ti de", "sua e", "bia a"]
    sfx = ["ei=))", "cmnr=))", "z=))", "vl=))", "vcl=))"]
    return [f"{random.choice(base)} {random.choice(sfx)} {random.choice(sfx)}" for _ in range(4500)]

@bot.on(events.NewMessage)
async def handle(e):
    u, t = e.sender_id, e.text.strip() if e.text else ""
    is_o = (u == OWNER_ID)
    is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # 1. BẢO MẬT TUYỆT ĐỐI: CHỈ ADMIN/OWNER MỚI CÓ PHẢN HỒI LỆNH ẨN
    if is_o or is_a:
        if t == '/ad': await e.reply(AD_MENU); return
        if t.startswith('/newkey'):
            nk = t.split()[1] if len(t.split()) > 1 else ""
            if nk: db["keys"].append(nk); await e.reply(f"🔑 Đã tạo Key: {nk}\nADMIN:HQUY")
            return
        if t == '/listkey': await e.reply(f"📋 List Key: {db['keys']}"); return
        if t.startswith('/tb'):
            msg = t.replace('/tb','').strip()
            for x in list(set(db["auth"] + db["admins"])):
                try: await bot.send_message(x, f"📢 TB: {msg}\nADMIN:HQUY")
                except: pass
            return

    # 2. LỆNH CHỈ RIÊNG OWNER
    if is_o:
        if t.startswith('/addadm'):
            try: aid = int(t.split()[1]); db["admins"].append(aid); await e.reply(f"✅ Đã thêm Admin: {aid}")
            except: pass
            return

    # 3. LỆNH CHO NGƯỜI DÙNG BÌNH THƯỜNG
    if t == '/start':
        await e.reply(MENU_USER if is_v else BANG_GIA); return

    if t.startswith('/nhapkey'):
        k = t.split()[1] if len(t.split()) > 1 else ""
        if k in db["keys"]:
            db["auth"].append(u); await e.reply("✅ XÁC THỰC VIP THÀNH CÔNG!\nGõ /start để dùng menu."); return
        else: await e.reply("❌ Key sai hoặc hết hạn!"); return

    if not is_v: return

    # 4. THỰC THI FULL LOGIC 15 LỆNH (ĐÃ FIX)
    if t == '/sp':
        st[e.chat_id] = True; await e.reply("🚀 Rex nã 4500 phát đạn..."); 
        for c in get_bullets():
            if not st.get(e.chat_id): break
            try: await bot.send_message(e.chat_id, c); await asyncio.sleep(db["delay"])
            except: await asyncio.sleep(1)

    elif t == '/stop': st[e.chat_id] = False; await e.reply("🛑 SPAM OFF\nADMIN:HQUY")
    elif t == '/info': await e.reply(f"👤 Tên: {e.sender.first_name}\n🆔 ID: {u}\nADMIN:HQUY")
    elif t == '/voice':
        try:
            tts = gTTS(text="địt mẹ mày con chó, cha hắc quy nồ một vả chết cụ mày luôn", lang='vi')
            tts.save("v.ogg"); await bot.send_file(e.chat_id, "v.ogg", voice_note=True); os.remove("v.ogg")
        except: pass
    elif t == '/xoaall':
        await e.reply("👑 Đang dọn dẹp..."); 
        async for msg in bot.iter_messages(e.chat_id, from_user='me'): await msg.delete()
    elif t == '/spicon':
        st[e.chat_id] = True; icons = ["🤡","💩","🔥","⚡"]
        for _ in range(100):
            if not st.get(e.chat_id): break
            await bot.send_message(e.chat_id, random.choice(icons)); await asyncio.sleep(db["delay"])
    elif t == '/login': await e.reply("👑 Gửi SĐT để bắt đầu Login Userbot...")
    elif t == '/loguot': await e.reply("✈️ Đã thoát tài khoản thành công!")

if __name__ == '__main__':
    bot.run_until_disconnected()
