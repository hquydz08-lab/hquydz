import os, asyncio, random
from telethon import TelegramClient, events
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER GIỮ BOT SỐNG ---
app = Flask('')
@app.route('/')
def home(): return "REX FIX BOARD LIVE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_perfect', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.15}
st = {}

# --- BẢNG GIÁ CHUẨN THỨ TỰ (FIXED) ---
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

# --- MENU 15 LỆNH ---
MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn

🔥 DANH SÁCH MENU
🤬 /sp -> Trêu nhây 4500 câu cực gắt
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

# --- MENU QUẢN TRỊ ẨN ---
AD_MENU = """👑 HỆ THỐNG QUẢN TRỊ ẨN
━━━━━━━━━━━━━━━
⭐ QUYỀN OWNER:
➕ /addadm <id> | ➖ /xoaadm <id>
📋 /listadm

🔥 QUYỀN ADMIN:
➕ /newkey <mã> | ➖ /xoakey <mã>
📋 /listkey | 📢 /tb <nội dung>
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

    # 1. ƯU TIÊN LỆNH ẨN /ad (CHỈ OWNER/ADMIN MỚI THẤY)
    if t == '/ad':
        if is_o or is_a: await e.reply(AD_MENU)
        return

    # 2. LỆNH START (PHÂN QUYỀN HIỂN THỊ)
    if t == '/start':
        await e.reply(MENU_USER if is_v else BANG_GIA)
        return

    # 3. QUẢN TRỊ ADMIN (CHỈ OWNER)
    if is_o:
        if t.startswith('/addadm'):
            try: aid = int(t.split()[1]); db["admins"].append(aid); await e.reply(f"✅ Thêm Admin: {aid}")
            except: pass
        elif t.startswith('/xoaadm'):
            try: aid = int(t.split()[1]); db["admins"].remove(aid); await e.reply(f"➖ Xóa Admin: {aid}")
            except: pass
        elif t == '/listadm': await e.reply(f"📋 Admin: {db['admins']}")

    # 4. QUẢN TRỊ KEY (ADMIN & OWNER)
    if is_a or is_o:
        if t.startswith('/newkey'):
            nk = t.split()[1]; db["keys"].append(nk); await e.reply(f"🔑 Key mới: {nk}")
        elif t.startswith('/xoakey'):
            nk = t.split()[1]; db["keys"].remove(nk); await e.reply(f"➖ Xóa Key: {nk}")
        elif t == '/listkey': await e.reply(f"📋 List Key: {db['keys']}")
        elif t.startswith('/tb'):
            msg = t.replace('/tb','').strip()
            for x in list(set(db["auth"] + db["admins"])):
                try: await bot.send_message(x, f"📢 TB: {msg}\nADMIN:HQUY")
                except: pass

    # 5. LỆNH NGƯỜI DÙNG VIP (SAU KHI NHẬP KEY)
    if not is_v:
        if t.startswith('/nhapkey'):
            k = t.split()[1] if len(t.split()) > 1 else ""
            if k in db["keys"]:
                db["auth"].append(u); await e.reply("✅ XÁC THỰC VIP THÀNH CÔNG!")
            else: await e.reply("❌ Key sai!")
        return

    # THỰC THI 15 LỆNH
    if t == '/sp':
        st[e.chat_id] = True; await e.reply("🚀 Rex nã 4500 phát đạn cũ...")
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
        await e.reply("👑 Đang dọn dẹp..."); async for msg in bot.iter_messages(e.chat_id, from_user='me'): await msg.delete()
    elif t == '/spicon':
        st[e.chat_id] = True; icons = ["🤡","💩","🔥","⚡"]
        for _ in range(100):
            if not st.get(e.chat_id): break
            await bot.send_message(e.chat_id, random.choice(icons)); await asyncio.sleep(db["delay"])
    elif t == '/login': await e.reply("👑 Gửi SĐT (+84...) để Login...")
    elif t == '/loguot': await e.reply("✈️ Đã Logout tất cả!")

if __name__ == '__main__':
    bot.run_until_disconnected()

