import os, asyncio, threading, time, json, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from gtts import gTTS
from flask import Flask

# ===== CẤU HÌNH GỐC =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0BuxqW2IARcbqCT-8hxCtwMS3cNSRFvKTdWRD4J0B54iss_sM2bNqcnUkHRkbtKflVVhbWcMoDrIStGFXjZZomp7QdlVwI74Q-Cf2OBJGZOZatvpGtZWVcX69iRJBfyPq0t5-zKMJgLCeDdrUnJIfYL6CFRzSrMb-Qrje87_1IRZH_KoWhj5PSoOJZCjPZWRH3rONJQxp5b1MSDyNEIH7iA2RBzG-ME1gQEbA9txIEGPVrEymLlyIGp4kV8p1GZWtbDKp7MXAlHcCwIgjlmeRlYaDg0TFDujHDJuCh7uc-5X8xbbrOUKmNWLvj7TuTqBhBzLwJxB21TLAym4xG9dlLJSc="

# Database tạm thời
db = {"users": {}, "keys": {}, "admins": [7153197678], "delay": 0.5, "anti": False, "stopxoa": False}
tasks = {"spam": {}}

# Văn bản chửi (Mỗi câu 1 dòng)
NGON_CHUI = ["đmm sủa tiếp đi con chó", "mồ côi thì im mồm", "cay à con cún", "óc chó sủa đi", "nhây với bố à", "câm mồm đi con súc vật", "bố m vả cho rụng răng", "sủa mạnh lên con"] * 100

client = TelegramClient(StringSession(SESSION_STR.strip()), API_ID, API_HASH)

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

    # 1. /start
    if cmd == '/start':
        await e.reply(MENU_VIP if is_vip else "⚠️ Bạn chưa có quyền VIP. Liên hệ @hquycute để mua key!")
        return

    # 2. /nhapkey (Dành cho người chưa là VIP)
    if cmd == '/nhapkey':
        if len(args) < 2:
            await e.reply("💰 **BẢNG GIÁ VIP**\n🎫 2K/DAY | 10K/WEEK | 70K/VV\n📝 Cú pháp: `/nhapkey <key>`\nADMIN:HQUY")
            return
        key = args[1]
        if key in db["keys"]:
            db["users"][str(uid)] = "active"
            del db["keys"][key]
            await e.reply("✅ VIP ACTIVE! Gõ /start để xem menu mới.\nADMIN:HQUY")
        else: await e.reply("❌ Key sai hoặc đã hết hạn!")

    if not is_vip: return

    # --- NHÓM LỆNH SPAM (TÁCH DÒNG) ---
    if cmd == '/sp' and len(args) > 1:
        target = args[1]
        tasks["spam"][e.chat_id] = True
        for line in NGON_CHUI:
            if not tasks["spam"].get(e.chat_id): break
            await client.send_message(e.chat_id, f"{line} [{target}](tg://user?id={target})")
            await asyncio.sleep(db["delay"])

    elif cmd == '/spnd' and len(args) > 1:
        nd = e.text.replace(args[0], '').strip()
        lines = nd.split('\n')
        tasks["spam"][e.chat_id] = True
        while tasks["spam"].get(e.chat_id):
            for line in lines:
                if not tasks["spam"].get(e.chat_id): break
                await client.send_message(e.chat_id, line.strip())
                await asyncio.sleep(db["delay"])

    elif cmd == '/call':
        target = args[1] if len(args) > 1 else "Người dùng"
        await e.reply(f"📞 Đang thực hiện cuộc gọi ảo tới `{target}`...\nADMIN:HQUY")

    elif cmd == '/stop':
        tasks["spam"][e.chat_id] = False
        await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

    elif cmd == '/setdelay' and len(args) > 1:
        db["delay"] = float(args[1])
        await e.reply(f"⚡ Tốc độ mới: {db['delay']}s")

    # --- NHÓM LỆNH ADMIN ---
    elif cmd == '/addadm' and uid == BOSS_ID:
        target = (await e.get_reply_message()).sender_id if e.is_reply else int(args[1])
        db["admins"].append(target); await e.reply(f"✅ Đã thêm Admin `{target}`")

    elif cmd == '/xoadm' and uid == BOSS_ID:
        target = (await e.get_reply_message()).sender_id if e.is_reply else int(args[1])
        if target in db["admins"]: db["admins"].remove(target)
        await e.reply(f"❌ Đã xóa Admin `{target}`")

    elif cmd == '/listadm':
        await e.reply(f"📜 Danh sách Admin: `{db['admins']}`")

    elif cmd == '/newkey' and uid == BOSS_ID:
        k = args[1] if len(args) > 1 else str(random.randint(1000, 9999))
        db["keys"][k] = True; await e.reply(f"🔑 Key mới: `{k}`")

    elif cmd == '/xoakey' and len(args) > 1:
        if args[1] in db["keys"]: del db["keys"][args[1]]; await e.reply("🗑 Đã xóa key.")

    # --- NHÓM LỆNH TIỆN ÍCH ---
    elif cmd == '/info':
        target_id = uid
        if e.is_reply: target_id = (await e.get_reply_message()).sender_id
        elif len(args) > 1:
            try: target_id = (await client.get_entity(args[1])).id
            except: pass
        await e.reply(f"👻 ID: `{target_id}`\nADMIN:HQUY")

    elif cmd == '/voice' and len(args) > 1:
        txt = e.text.replace(args[0], '').strip()
        gTTS(txt, lang='vi').save("v.mp3")
        await client.send_file(e.chat_id, "v.mp3", voice_note=True)
        os.remove("v.mp3")

    elif cmd == '/anti': db["anti"] = True; await e.reply("🚫 **ANTI ON** - Sẽ xóa tin đối thủ.")
    elif cmd == '/unanti': db["anti"] = False; await e.reply("✅ **ANTI OFF**")
    elif cmd == '/stopxoa': db["stopxoa"] = True; await e.reply("🔴 Đã dừng xóa bot.")
    elif cmd == '/xoaall':
        await e.reply("👑 Đang xóa sạch dấu vết spam...")
        # Giả lập xóa sạch (hoặc logic thực tế nếu bot có quyền xóa tin nhắn cũ)

# --- XỬ LÝ ANTI (XÓA TIN ĐỐI THỦ) ---
@client.on(events.NewMessage)
async def handler_anti(e):
    if db["anti"] and not e.out and e.sender_id not in db["admins"] and e.sender_id != BOSS_ID:
        try: await e.delete()
        except: pass

# --- KEEP ALIVE ---
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

async def run():
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 REX SPAM FULL 20 LỆNH ĐÃ SẴN SÀNG!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(run())
