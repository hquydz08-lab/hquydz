import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 #
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4" #

# Session mới nhất của ông
SESSION_STR = "1BVtsOL0Bu58Jr7-lsWHDO3waK6zC3u_f2_fOBnBR7jWd9litQGbKTvcwAFdSKWCx5WZYSdgittvv7qAS8EbarEuyFEUn_nx7H-hCCy1n8x22F9Ar9nmgMrgnCYHrfiKp6FufesRoLsmwxWskmN82h1YSrEl_xQXamc8JkrRUv22MPC385FT6UIlt9KkO1c3pFBHITY9fgipaFAPg8FSB66pcZ-Uv-2MIcupeVYOBzDRUxU6NB9VTF9dCXnSXgPCliCNxfiLvrhCYWMG6U8S110YP98pH1_GRl7VcZ6ZmunHPBRZAB5lCFPg6pn_jSpLVpVEBmOri-sq1gCp57bRsefmh_eRE73E=" #

def fix_padding(s):
    if not s: return ""
    s = s.strip().replace(" ", "").replace("\n", "")
    return s + "=" * (-len(s) % 4)

client = None
try:
    client = TelegramClient(StringSession(fix_padding(SESSION_STR)), API_ID, API_HASH)
except Exception as e:
    print(f"❌ LỖI SESSION: {e}")

# --- 2 BỘ NGÔN MỖI BỘ 500 DÒNG ---
BO_1 = ["cn choa ei=))", "m chay di con kiki=))", "đứng lại cho bố bảo=))", "sao im r con súc vật=))", "cay à con cún=))"] * 100
BO_2 = ["mẹ m bị t cho ăn gậy vào mồm à=))", "sao r con chó mồ côi eii=))", "cay r à con súc vật=))", "sủa tiếp đi m=))", "mồ côi thì im mồm vào=))"] * 100

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

# --- HỆ THỐNG LỆNH ---
if client:
    # LỆNH KIỂM TRA PHẢN HỒI (MỚI THÊM)
    @client.on(events.NewMessage(pattern=r'^/check$'))
    async def cmd_check(e):
        await e.reply(f"✅ Bot Live!\n👤 ID của ông: `{e.sender_id}`\n🛡 ID Boss: `7153197678`\nADMIN:HQUY")

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
ADMIN:HQUY""") #
        else:
            await e.reply("💰 BẢNG GIÁ KEY REX SPAM:\n🎫 DAY: 2K | WEEK: 10K | VV: 70K\n👑 Mua tại: @hquycute")

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
        await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY") #

# Flask duy trì cho Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

if client:
    print("🚀 Bot đang khởi động...")
    client.start(bot_token=BOT_TOKEN)
    client.run_until_disconnected()
else:
    while True: time.sleep(5)
