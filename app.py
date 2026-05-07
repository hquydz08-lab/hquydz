import os, random, asyncio, threading, json, time
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
BOSS_ID = 7153197678  
SESSION_STR = "1BVtsOL0Bu3ftXep1MwrLMPn8yO4m3tKwmrCkouFBDrR7vihqk4-ZCg6kK-zJaAkYu4Z96OSdBK7DNzoRMXCFrMTxi80pqi0OK95BBjcto5w0WVNHlXJikycoNa7bmNPYrXMQyRx3QkJkYVXxH5nmGo4AKTPzht9yqHTj7jx-pCS68Aj0yJxGZmcryReEdREjpq1ibTDJx6Uyd_FZkgWUY9CuFvFwyLNy4F_Uivi2ng8IsawIwJW8JiLtXkbz5vMvWsA0xelcH42HGvGZgqXCnpQK8mV3WpY6YjEXCIJEwMFWiGPv-SjD1ISUGBcl2sACEn-DxzWS5S5dbR9AJI7TknKG5QbrBv4=" 

DATA_FILE = "data_hquy.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"keys": {}, "user_keys": {}, "admins": [7153197678]}

data = load_data()
def save_data():
    with open(DATA_FILE, "w") as f: json.dump(data, f)

tasks = {"nhay": {}, "nhaytag": {}}
ANTI_LIST = {}
global_delay = 0.5 

# --- BỘ NGÔN SPAM ---
NGON_NHAY = ["cn choa ei=))=))=))=))", "m chay anh cmnr=))=))=))=))"] * 100
NGON_NHAYTAG = ["con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣"] * 100

client = TelegramClient(StringSession(SESSION_STR), api_id, api_hash)

# --- KIỂM TRA QUYỀN ---
def check_auth(uid):
    if uid == 7153197678 or uid in data["admins"]: return True
    uid_str = str(uid)
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien" or time.time() < expiry: return True
    return False

# --- LỆNH MENU (PHÂN QUYỀN) ---
@client.on(events.NewMessage(pattern=r'^/menu$'))
async def cmd_menu(e):
    if check_auth(e.sender_id):
        # Menu khi ĐÃ CÓ KEY hoặc là ADMIN
        await e.reply("""✨ ────────────────────────── ✨
🦖 Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây 
🤬 /nhaytag - Nhây tag chửi 
📞 /call - SPAMCALL+ID
⚡ /setdelay - Chỉnh tốc độ spam
🚫 /anti - Tự xóa tin nhắn đối thủ
✅ /unanti - Ngừng xóa tin nhắn
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key (day/week/month/vinhvien)
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch tin nhắn spam
👻 /info - Check ID
💎 /voice - CHUYEN VAN BAN THANH VOICE
🛑 /stop - Dừng tất cả
🔴 /stopxoa - dừng xoá tin nhắn bot spam
✨ ────────────────────────── ✨
ADMIN:HQUY""")
    else:
        # Menu khi CHƯA CÓ KEY
        await e.reply("""📣 XÁC THỰC NGƯỜI DÙNG
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
👑 ADMIN: @hquycute""")

# --- CÁC LỆNH HỆ THỐNG ---
@client.on(events.NewMessage(pattern=r'^/nhapkey (\S+)'))
async def cmd_nhapkey(e):
    k = e.pattern_match.group(1)
    if k in data["keys"]:
        exp = data["keys"][k]
        data["user_keys"][str(e.sender_id)] = "vinhvien" if exp == "vinhvien" else time.time() + exp
        del data["keys"][k]; save_data()
        await e.reply("✅ Kích hoạt thành công! Gõ /menu để bắt đầu.")
    else:
        await e.reply("❌ Key không hợp lệ hoặc đã sử dụng.")

@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    while tasks["nhay"].get(e.chat_id):
        await client.send_message(e.chat_id, random.choice(NGON_NHAY))
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/nhaytag (\S+)'))
async def cmd_nhaytag(e):
    if not check_auth(e.sender_id): return
    target = e.pattern_match.group(1)
    tasks["nhaytag"][e.chat_id] = True
    while tasks["nhaytag"].get(e.chat_id):
        await client.send_message(e.chat_id, f"{target} {random.choice(NGON_NHAYTAG)}")
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/info$'))
async def cmd_info(e):
    await e.reply(f"👻 ID: `{e.sender_id}`")

# Flask duy trì server
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
