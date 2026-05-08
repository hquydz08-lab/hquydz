import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"

# DÁN SESSION MỚI LẤY VÀO ĐÂY (PHẢI TRONG DẤU NGOẶC KÉP)
SESSION_STR = "DÁN_SESSION_MỚI_CỦA_ÔNG_VÀO_ĐÂY"

def fix_padding(s):
    if not s: return ""
    s = s.strip().replace(" ", "").replace("\n", "")
    return s + "=" * (-len(s) % 4)

# --- KHỞI TẠO AN TOÀN (SỬA LỖI ẢNH 1, 2, 3, 4) ---
client = None
try:
    if SESSION_STR and "DÁN_SESSION" not in SESSION_STR:
        client = TelegramClient(StringSession(fix_padding(SESSION_STR)), API_ID, API_HASH)
    else:
        print("⚠️ CHƯA CÓ SESSION - BOT ĐANG CHẠY CHẾ ĐỘ CHỜ")
except Exception as e:
    print(f"❌ LỖI SESSION: {e}")

# --- 2 BỘ VĂN BẢN 500 DÒNG ---
BO_1 = ["cn choa ei=))", "m chay di con kiki=))", "đứng lại cho bố bảo=))"] * 167
BO_2 = ["mẹ m bị t cho ăn gậy=))", "sao r con chó mồ côi=))", "cay r à con súc vật=))"] * 167

DATA_FILE = "data_hquy.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    return {"keys": {}, "user_keys": {}, "admins": [7153197678]}

data = load_data()
tasks = {"spam": {}}

def check_auth(uid):
    if uid == BOSS_ID or uid in data.get("admins", []): return True
    return str(uid) in data.get("user_keys", {})

# --- MENU GIAO DIỆN CHUẨN ---
if client:
    @client.on(events.NewMessage(pattern=r'^/menu$|^/start$'))
    async def cmd_menu(e):
        if check_auth(e.sender_id):
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
            await e.reply("💰 BẢNG GIÁ KEY: DAY 2K | WEEK 10K | VV 70K\nMua tại: @hquycute")

    @client.on(events.NewMessage(pattern=r'^/nhay$'))
    async def run_nhay(e):
        if not check_auth(e.sender_id): return
        tasks["spam"][e.chat_id] = True
        await e.reply("🚀 VĂNG BỘ 1 (500 DÒNG)...")
        for msg in BO_1:
            if not tasks["spam"].get(e.chat_id): break
            await client.send_message(e.chat_id, msg)
            await asyncio.sleep(0.5)

    @client.on(events.NewMessage(pattern=r'^/stop$'))
    async def run_stop(e):
        if not check_auth(e.sender_id): return
        tasks["spam"][e.chat_id] = False
        await e.reply("🛑 SPAM OFF\nADMIN:HQUY")

# Flask duy trì cho Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

if client:
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()
else:
    while True: time.sleep(5)
