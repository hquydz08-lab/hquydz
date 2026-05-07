import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 

# 1. String Session MỚI của ông (Đã bao bọc bằng dấu ngoặc kép)
SESSION_STR = "1BVtsOL0Buxx2VVdubrOn5Gwh3ZO9MWJ8BQuolTkymPcDyFnwCGYUeHUu2UdLabIVwjf_rizS42f8bMUd9NxAgL75n2Nqjssyjd1RJBn7_sYjoZMFSnOE19RMUau8-cjpOftvCUgmlK7X2SLoMi0jqrPNlPCvqF2imKuz5TcZrBbgOpFy5Rz4sYQshpds3xK6-0-eDTkEjz8hPbjRhixob_XUSTWQjQ8Sdk-XcSb-RgfCNQPF6RbLJ3gTMzJR9GRUmlN3RkLi-mfy-3obJWKz1rFayRESpDfGOF64dCiqWgPGxZLqcF047zZdnqMueLcXA_A8yT8Up2UgE5FPocxVufdEMdohedA="

# 2. Token Bot War của ông
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"

# --- HÀM TỰ ĐỘNG BÙ PADDING (FIX LỖI RENDER SẬP) ---
def fix_padding(s):
    s = s.strip()
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return s

# --- KHỞI TẠO CLIENT ---
client = TelegramClient(StringSession(fix_padding(SESSION_STR)), API_ID, API_HASH)

# --- BỘ NGÔN 500 DÒNG ---
NGON_NHAY = ["cn choa ei=))=))=))", "m chay anh cmnr=))=))=))", "đứng lại cho bố=))", "go di m=))", "sao im r con cho=))"] * 100
NGON_NHAYTAG = ["mẹ m bị t cho ăn gậy vào mồm à con súc vật=))", "sao r con chó mồ côi eii=))", "cay r à con chó=))", "sủa tiếp đi m=))"] * 125

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
global_delay = 0.5 

def check_auth(uid):
    if uid == BOSS_ID or uid in data["admins"]: return True
    uid_str = str(uid)
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien" or (isinstance(expiry, (int, float)) and time.time() < expiry): return True
    return False

# --- MENU CHÍNH & BẢNG GIÁ KEY (KHI NGƯỜI LẠ START) ---
@client.on(events.NewMessage(pattern=r'^/menu$|^/start$'))
async def cmd_menu(e):
    if check_auth(e.sender_id):
        await e.reply("""✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
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
        await e.reply("""📣 XÁC THỰC NGƯỜI DÙNG
──────────────────────────
💰 BẢNG GIÁ KEY REX SPAM:
🎫 KEY NGÀY: 2.000 VNĐ
🎫 KEY TUẦN: 10.000 VNĐ
🎫 KEY THÁNG: 30.000 VNĐ
🎫 VĨNH VIỄN: 70.000 VNĐ
──────────────────────────
📝 Nhập key: /nhapkey <mã_key>
👑 Mua key tại: @hquycute""")

# --- LOGIC SPAM 500 DÒNG ---
@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    await e.reply("🚀 BẮT ĐẦU NHÂY 500 CÂU!")
    for sentence in NGON_NHAY:
        if not tasks["nhay"].get(e.chat_id): break
        await client.send_message(e.chat_id, sentence)
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

# Flask duy trì server Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

# Khởi động Bot
print("🚀 Bot đang lên sóng...")
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
