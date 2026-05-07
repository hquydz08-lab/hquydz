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
SESSION_STR = "1BVtsOL0Bu4qv-2Kt7PD7f4XQKW22mcgaZTh56Xr6uLc4qAX-eJWivCgQfMNhmQmAxNN5_uxEobvPj5se_yT4a9wSY4Tgw..." 

DATA_FILE = "data_hquy.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"keys": {}, "user_keys": {}, "admins": [7153197678]}

data = load_data()
def save_data():
    with open(DATA_FILE, "w") as f: json.dump(data, f)

tasks = {"nhay": {}, "nhaytag": {}}
ANTI_LIST = {}
global_delay = 0.5 

# ===== BỘ NGÔN (500 DÒNG NHÂN BẢN) =====
NGON_NHAY = [
    "cn choa ei=))=))=))=))", "123=))=))=))=))", "m chay anh cmnr=))=))=))=))=))", "m yeu ot z tk nfu=))=))=))=))=))",
    "m cham vl e=))=))=))", "slow lun e=))=))=))=))", "yeu z cn dix=))=))=))=))", "tk 3de=))=))=))=))=))",
    "tk dix lgbt=))=))=))=))", "cn choa nfu=))=))=))=))=))", "deo co canh lun e=))=))=))=))", "m cham vl e=))=))=))=))",
    "m yeu v=))=))=))=))=))=))", "yeu ro=))=))=))=))=))=))", "bia a=))=))=))=))", "tk dix=))=))=))=))"
] * 30 

NGON_NHAYTAG = [
    "123 con chó cùng sủa =))", "con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣", "con đĩ phàn kháng cha được không ấy",
    "thằng cha mày gánh lúa cho mày đi đú à :))", "mẹ đĩ mày dắt mày vô sàn à :))", "con điếm bị bố sỉ nhục", "không phục à",
    "phản kháng lại những câu sỉ vả của cha xem :))"
] * 60

client = TelegramClient(StringSession(SESSION_STR), api_id, api_hash)

# ===== HỆ THỐNG KIỂM TRA KEY =====
def check_auth(uid):
    uid_str = str(uid)
    if uid in data["admins"] or uid == BOSS_ID: return True
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien": return True
        if time.time() < expiry: return True
        else:
            del data["user_keys"][uid_str]
            save_data()
    return False

# --- QUẢN LÝ KEY (LỆNH MỚI) ---
@client.on(events.NewMessage(pattern=r'^/newkey (day|week|month|vinhvien)'))
async def cmd_newkey(e):
    if e.sender_id != BOSS_ID and e.sender_id not in data["admins"]: return
    duration = e.pattern_match.group(1)
    key = f"HQUY-{random.randint(1000, 9999)}"
    
    if duration == "day": expire_in = 86400
    elif duration == "week": expire_in = 604800
    elif duration == "month": expire_in = 2592000
    else: expire_in = "vinhvien"

    data["keys"][key] = expire_in
    save_data()
    await e.reply(f"🔑 Key mới ({duration}): `{key}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/nhapkey (\S+)'))
async def cmd_nhapkey(e):
    key = e.pattern_match.group(1)
    if key in data["keys"]:
        expire_val = data["keys"][key]
        if expire_val == "vinhvien":
            data["user_keys"][str(e.sender_id)] = "vinhvien"
        else:
            data["user_keys"][str(e.sender_id)] = time.time() + expire_val
        del data["keys"][key]
        save_data()
        await e.reply("✅ Kích hoạt Key thành công!\nADMIN:HQUY")
    else:
        await e.reply("❌ Key không tồn tại hoặc đã hết hạn.")

# --- LỆNH SPAM ---
@client.on(events.NewMessage(pattern=r'^/nhaytag (\S+)'))
async def cmd_nhaytag(e):
    if not check_auth(e.sender_id): return
    target = e.pattern_match.group(1)
    tasks["nhaytag"][e.chat_id] = True
    while tasks["nhaytag"].get(e.chat_id):
        await client.send_message(e.chat_id, f"{target} {random.choice(NGON_NHAYTAG)}")
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    while tasks["nhay"].get(e.chat_id):
        await client.send_message(e.chat_id, random.choice(NGON_NHAY))
        await asyncio.sleep(global_delay)

# --- MENU SIÊU VIP ---
@client.on(events.NewMessage(pattern=r'^/menu$'))
async def cmd_menu(e):
    await e.reply("""✨ ────────────────────────── ✨
🦖 Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây 
🤬 /nhaytag - Nhây tag chửi 
📞 /call - Gọi điện xuyên giáp
⚡ /setdelay - Chỉnh tốc độ spam
🚫 /anti - Tự xóa tin nhắn đối thủ
✅ /unanti - Ngừng xóa tin nhắn
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey (day/week/month/vinhvien)
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch tin nhắn spam
👻 /info - Check ID
💎 /voice - CHUYEN VAN BAN THANH VOICE
🛑 /stop - Dừng tất cả
🔴 /stopxoa - dừng xoá tin nhắn bot spam
✨ ────────────────────────── ✨
ADMIN:HQUY""")

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    tasks["nhay"][e.chat_id] = False
    tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/stopxoa$'))
async def cmd_stopxoa(e):
    await e.reply("🔴 Đã dừng xoá tin nhắn bot spam.\nADMIN:HQUY")

# Flask Server
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
