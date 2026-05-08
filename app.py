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

# --- BỘ VĂN BẢN 1000 DÒNG (DÒNG NÀO RA DÒNG ĐÓ) ---
NGON_CHUI = [
    "đmm sủa tiếp đi con chó", "mồ côi thì im mồm", "cay à con cún", 
    "sao im r con súc vật", "mẹ m bị t cho ăn gậy vào mồm à",
    "óc chó sủa đi", "loại mồ côi", "bố vả vỡ mồm", "nhây với bố à", 
    "câm như hến vậy con", "sủa mạnh lên xem nào", "bố m cân tất"
] * 100 # Nhân lên cho đủ 1000+ dòng

db = {"users": {}, "keys": {}, "admins": [7153197678], "delay": 0.5}
tasks = {"spam": {}, "anti": {}}

client = TelegramClient(StringSession(SESSION_STR.strip()), API_ID, API_HASH)

# --- GIAO DIỆN MENU VIP ---
MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH 20 LỆNH
🤬 /sp - Trêu nhây (Tách dòng)
🤬 /spnd - Spam nội dung (Tách dòng)
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key hệ thống
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xoa key
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng xóa bot
🚀 /start - Khởi động bot
⚙️ /restart - Khởi động lại hệ thống
🗑 /clean - Dọn dẹp bộ nhớ
✨ ────────────────────────── ✨
ADMIN:HQUY"""

@client.on(events.NewMessage)
async def main_handler(e):
    if not e.text: return
    args = e.text.split()
    cmd = args[0].lower()
    uid = e.sender_id
    is_vip = (uid == BOSS_ID or uid in db["admins"] or str(uid) in db["users"])

    if cmd == '/start':
        await e.reply(MENU_VIP if is_vip else "Gõ /nhapkey để dùng bot.\nADMIN:HQUY")
        return

    if is_vip:
        # 1. Spam Trêu Nhây (Từng dòng)
        if cmd == '/sp' and len(args) > 1:
            target = args[1]
            tasks["spam"][e.chat_id] = True
            for line in NGON_CHUI:
                if not tasks["spam"].get(e.chat_id): break
                await client.send_message(e.chat_id, f"{line} [{target}](tg://user?id={target})")
                await asyncio.sleep(db["delay"])

        # 2. Spam Nội Dung (Mỗi câu 1 dòng)
        elif cmd == '/spnd' and len(args) > 1:
            nd_full = e.text.replace(args[0], '').strip()
            lines = nd_full.split('\n')
            tasks["spam"][e.chat_id] = True
            while tasks["spam"].get(e.chat_id):
                for line in lines:
                    if not tasks["spam"].get(e.chat_id): break
                    if line.strip():
                        await client.send_message(e.chat_id, line.strip())
                        await asyncio.sleep(db["delay"])

        # 3. Các lệnh quản trị & Tiện ích
        elif cmd == '/voice' and len(args) > 1:
            text = e.text.replace(args[0], '').strip()
            gTTS(text, lang='vi').save("v.mp3")
            await client.send_file(e.chat_id, "v.mp3", voice_note=True)
            os.remove("v.mp3")
        elif cmd == '/stop': tasks["spam"][e.chat_id] = False; await e.reply("🛑 **SPAM OFF**")
        elif cmd == '/setdelay': db["delay"] = float(args[1]); await e.reply(f"⚡ Delay: {db['delay']}s")
        elif cmd == '/info':
            user = (await e.get_reply_message()).sender_id if e.is_reply else uid
            await e.reply(f"👻 ID: `{user}`")
        elif cmd == '/newkey' and uid == BOSS_ID:
            k = args[1] if len(args) > 1 else str(random.randint(1000,9999))
            db["keys"][k] = True; await e.reply(f"🔑 Key: `{k}`")
        elif cmd == '/addadm' and uid == BOSS_ID:
            new_adm = (await e.get_reply_message()).sender_id if e.is_reply else int(args[1])
            db["admins"].append(new_adm); await e.reply("✅ Added Admin")
        # (Thêm các logic lệnh khác vào đây tương tự...)

# Flask
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

async def run_bot():
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 REX SPAM FULL 20 LỆNH ONLINE!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(run_bot())
