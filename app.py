import os, asyncio, threading, time, json, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from gtts import gTTS
from flask import Flask

# ===== CẤU HÌNH =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0BuxqW2IARcbqCT-8hxCtwMS3cNSRFvKTdWRD4J0B54iss_sM2bNqcnUkHRkbtKflVVhbWcMoDrIStGFXjZZomp7QdlVwI74Q-Cf2OBJGZOZatvpGtZWVcX69iRJBfyPq0t5-zKMJgLCeDdrUnJIfYL6CFRzSrMb-Qrje87_1IRZH_KoWhj5PSoOJZCjPZWRH3rONJQxp5b1MSDyNEIH7iA2RBzG-ME1gQEbA9txIEGPVrEymLlyIGp4kV8p1GZWtbDKp7MXAlHcCwIgjlmeRlYaDg0TFDujHDJuCh7uc-5X8xbbrOUKmNWLvj7TuTqBhBzLwJxB21TLAym4xG9dlLJSc=" 

# --- BỘ NGÔN 1000 DÒNG ---
NGON_1000 = ["đmm sủa tiếp đi con chó", "mồ côi thì im mồm", "cay à con cún", "sao im r con súc vật", "mẹ m bị t cho ăn gậy vào mồm à"] * 200
NGON_500 = NGON_1000[:500]

db = {"users": {}, "keys": {}, "admins": [7153197678], "delay": 0.5}
tasks = {"spam": {}, "anti": {}}

client = TelegramClient(StringSession(SESSION_STR.strip()), API_ID, API_HASH)

# --- GIAO DIỆN BẢNG GIÁ (HIỆN KHI /START HOẶC /NHAPKEY TRỐNG) ---
BANG_GIA = """📣 𝗫𝗔𝗖 𝗧𝗛𝗨𝗖 𝗡𝗚𝗨𝗢𝗜 𝗗𝗨𝗡𝗚
━━━━━━━━━━━━━━━━━━
💰 𝗕𝗔𝗡𝗚 𝗚𝗜𝗔
━━━━━━━━━━━━━━━━━━
🎫 2K/DAY | 10K/WEEK
🎫 20K/MONTH | 70K/VV
━━━━━━━━━━━━━━━━━━
🔑 Vui lòng nhập key để sử dụng bot
📝 /nhapkey <key>
━━━━━━━━━━━━━━━━━━
👑 ADMIN: @hquycute
ADMIN:HQUY"""

# --- MENU VIP CHUẨN ---
MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /sp - Trêu nhây 
🤬 /spnd - spam + nội dung 
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key hệ thống
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng xóa bot
🚀 /start - Khởi động bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

@client.on(events.NewMessage)
async def main_handler(e):
    if not e.text: return
    args = e.text.split()
    cmd = args[0].lower()
    uid = e.sender_id
    is_vip = (uid == BOSS_ID or uid in db["admins"] or str(uid) in db["users"])

    # 1. Start & Nhapkey trống
    if cmd == '/start' or (cmd == '/nhapkey' and len(args) < 2):
        await e.reply(MENU_VIP if is_vip else BANG_GIA)
        return

    # 2. Nhập key có mã
    if cmd == '/nhapkey' and len(args) >= 2:
        if args[1] in db["keys"]:
            db["users"][str(uid)] = "active"
            await e.reply("✅ VIP ACTIVE!\nADMIN:HQUY")
        else: await e.reply("❌ Key không tồn tại!")
        return

    # 3. Lệnh VIP
    if is_vip:
        if cmd == '/spnd' and len(args) > 1:
            nd = e.text.replace(args[0], '').strip()
            tasks["spam"][e.chat_id] = True
            while tasks["spam"].get(e.chat_id):
                await client.send_message(e.chat_id, nd)
                await asyncio.sleep(db["delay"])

        elif cmd == '/sp' and len(args) > 1:
            target = args[1]
            tasks["spam"][e.chat_id] = True
            for line in NGON_500:
                if not tasks["spam"].get(e.chat_id): break
                await client.send_message(e.chat_id, f"{line} [{target}](tg://user?id={target})")
                await asyncio.sleep(db["delay"])

        elif cmd == '/voice' and len(args) > 1:
            text = e.text.replace(args[0], '').strip()
            gTTS(text, lang='vi').save("v.mp3")
            await client.send_file(e.chat_id, "v.mp3", voice_note=True)
            os.remove("v.mp3")

        elif cmd == '/stop':
            tasks["spam"][e.chat_id] = False
            await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

        elif cmd == '/info':
            user = (await e.get_reply_message()).sender_id if e.is_reply else uid
            await e.reply(f"👻 ID: `{user}`\nADMIN:HQUY")

        elif cmd == '/newkey' and uid == BOSS_ID:
            k = args[1] if len(args) > 1 else str(random.randint(1000,9999))
            db["keys"][k] = True
            await e.reply(f"🔑 Key: `{k}`\nADMIN:HQUY")

# Flask duy trì Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
