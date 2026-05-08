import os, asyncio, threading, time, json, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0Bu58Jr7-lsWHDO3waK6zC3u_f2_fOBnBR7jWd9litQGbKTvcwAFdSKWCx5WZYSdgittvv7qAS8EbarEuyFEUn_nx7H-hCCy1n8x22F9Ar9nmgMrgnCYHrfiKp6FufesRoLsmwxWskmN82h1YSrEl_xQXamc8JkrRUv22MPC385FT6UIlt9KkO1c3pFBHITY9fgipaFAPg8FSB66pcZ-Uv-2MIcupeVYOBzDRUxU6NB9VTF9dCXnSXgPCliCNxfiLvrhCYWMG6U8S110YP98pH1_GRl7VcZ6ZmunHPBRZAB5lCFPg6pn_jSpLVpVEBmOri-sq1gCp57bRsefmh_eRE73E="

# --- BỘ NGÔN 1000 DÒNG (ĐÃ XOÁ "DÒNG X:") ---
BO_1 = ["cn choa ei=)) sủa tiếp đi con cún", "đứng lại cho bố bảo=))", "sao im r con súc vật=))", "cay à con cún=))", "mẹ m bị t cho ăn gậy vào mồm à=))"] * 100
BO_2 = ["mồ côi thì im mồm vào=))", "cay r à con súc vật=))", "sủa tiếp đi m=))", "mẹ m bị t cho ăn gậy vào mồm à=))", "sao r con chó mồ côi eii=))"] * 100

# Quản lý Key & Task
data = {"users": [], "keys": {}, "admins": [7153197678], "delay": 0.5}
tasks = {"spam": {}, "anti": {}}

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

# --- MENU & BẢNG GIÁ ---
MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: VIP (Đã Có Key)

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây
🤬 /nhaytag - Nhây tag chửi
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ spam
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin nhắn
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key hệ thống
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch tin nhắn spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển văn bản thành voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng xoá tin bot
🚀 /start - Khởi động lại bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

BANG_GIA = """📣 BẢNG GIÁ KEY REX SPAM
──────────────────────────
🎫 KEY NGÀY: 2.000 VNĐ
🎫 KEY TUẦN: 10.000 VNĐ
🎫 KEY THÁNG: 30.000 VNĐ
🎫 VĨNH VIỄN: 70.000 VNĐ
──────────────────────────
👑 Mua tại: @hquycute
ADMIN:HQUY"""

@client.on(events.NewMessage)
async def main_handler(e):
    if not e.text: return
    cmd = e.text.lower().split()[0]
    uid = e.sender_id
    is_vip = (uid == BOSS_ID or uid in data["admins"] or str(uid) in data["users"])

    # --- LỆNH CƠ BẢN ---
    if cmd in ['/start', '/menu']:
        await e.reply(MENU_VIP if is_vip else BANG_GIA)

    elif cmd == '/info':
        user_target = (await e.get_reply_message()).sender_id if e.is_reply else uid
        await e.reply(f"🆔 ID: `{user_target}`\nADMIN:HQUY")

    # --- HỆ THỐNG KEY ---
    elif cmd == '/newkey' and uid == BOSS_ID:
        k = f"REX-{random.randint(1000,9999)}"
        data["keys"][k] = True
        await e.reply(f"🔑 KEY: `{k}`\nADMIN:HQUY")

    elif cmd == '/nhapkey':
        k = e.text.split()[1] if len(e.text.split()) > 1 else ""
        if k in data["keys"]:
            data["users"].append(str(uid))
            del data["keys"][k]
            await e.reply("✅ KÍCH HOẠT VIP THÀNH CÔNG!\nADMIN:HQUY")
        else: await e.reply("❌ Key sai hoặc đã dùng!")

    # --- CÁC LỆNH SPAM (CHỈ VIP) ---
    if not is_vip: return

    if cmd == '/nhay':
        tasks["spam"][e.chat_id] = True
        for m in BO_1:
            if not tasks["spam"].get(e.chat_id): break
            await client.send_message(e.chat_id, m)
            await asyncio.sleep(data["delay"])

    elif cmd == '/nhaytag':
        tasks["spam"][e.chat_id] = True
        for m in BO_2:
            if not tasks["spam"].get(e.chat_id): break
            await client.send_message(e.chat_id, m)
            await asyncio.sleep(data["delay"])

    elif cmd == '/setdelay':
        try:
            data["delay"] = float(e.text.split()[1])
            await e.reply(f"⚡ Đã chỉnh delay: {data["delay"]}s")
        except: pass

    elif cmd == '/stop':
        tasks["spam"][e.chat_id] = False
        await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

    elif cmd == '/anti':
        tasks["anti"][e.chat_id] = True
        await e.reply("🚫 ANTI ON - Đã kích hoạt tự xoá tin nhắn!")

    elif cmd == '/unanti':
        tasks["anti"][e.chat_id] = False
        await e.reply("✅ ANTI OFF!")

# Auto-Delete cho Anti
@client.on(events.NewMessage)
async def anti_delete(e):
    if tasks["anti"].get(e.chat_id) and e.sender_id != BOSS_ID:
        try: await e.delete()
        except: pass

# Flask duy trì Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
