import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
SESSION_STR = "1BVtsOL0Bu4qv-2Kt7PD7f4XQKW22mcgaZTh56Xr6uLc4qAX-eJWivCgQfMNhmQmAxNN5_uxEobvPj5se_yT4a9wSY4TgwSjAkYp1MwrLMPn8y04m3tKwmrCkouFBDrR7vihqk4-ZCg6kKzJaAkYu4Z960SdBK7DNzoRMXCFrMTxi80pqi0OK95BBjcto5w0WVNH1XJikycoNa7bmNPYrXMQyRx3QkJkyVXxh5nmGo4AKTPzht9yqHTj7jx-pCS68Aj0yJxGZmcryReEdRejpq1ibTDJx6Uyd_FZkgWUY9CuFvFwyLNy4F_Uivi2ng8IsawIwJW8JiLTXkbz5vMvWsA0xelch42HGvGZgqXCnpQK8mV3WPy6YjEXCIJEwMFWiGPv-SjD1ISUGBcl2sACEn-DxzWS5S5dbR9AJI7TknkG5QbrBv4="

# ===== BỘ NGÔN 500 DÒNG =====
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
ANTI_LIST = {}
global_delay = 0.5 

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def check_auth(uid):
    if uid == BOSS_ID or uid in data["admins"]: return True
    uid_str = str(uid)
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien" or (isinstance(expiry, (int, float)) and time.time() < expiry): return True
    return False

# --- MENU ĐÚNG MẪU HÀNG DỌC ---
@client.on(events.NewMessage(pattern=r'^/menu$'))
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
        await e.reply("📣 XÁC THỰC NGƯỜI DÙNG\n🎫 2K/DAY | 10K/WEEK | 70K/VV\n📝 Nhập key: /nhapkey <key>\n👑 ADMIN: @hquycute")

# --- FIX CÁC LỆNH HỆ THỐNG ---

@client.on(events.NewMessage(pattern=r'^/addadm (\d+)'))
async def cmd_addadm(e):
    if e.sender_id != BOSS_ID: return
    aid = int(e.pattern_match.group(1))
    if aid not in data["admins"]: data["admins"].append(aid); save_data()
    await e.reply(f"➕ Đã thêm Admin: `{aid}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/listadm$'))
async def cmd_listadm(e):
    if not check_auth(e.sender_id): return
    msg = "📜 DANH SÁCH ADMIN:\n" + "\n".join([f"• `{a}`" for a in data["admins"]])
    await e.reply(f"{msg}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/newkey (day|week|month|vinhvien)'))
async def cmd_newkey(e):
    if not check_auth(e.sender_id): return
    dur = e.pattern_match.group(1)
    k = f"HQUY-{random.randint(1000,9999)}"
    vals = {"day": 86400, "week": 604800, "month": 2592000, "vinhvien": "vinhvien"}
    data["keys"][k] = vals[dur]; save_data()
    await e.reply(f"🔑 Key ({dur}): `{k}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/setdelay (\d+(\.\d+)?)'))
async def cmd_delay(e):
    if not check_auth(e.sender_id): return
    global global_delay
    global_delay = float(e.pattern_match.group(1))
    await e.reply(f"⚡ Đã chỉnh Delay: {global_delay}s\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/anti$'))
async def cmd_anti(e):
    if not check_auth(e.sender_id) or not e.is_reply: return
    msg = await e.get_reply_message()
    target = msg.sender_id
    if e.chat_id not in ANTI_LIST: ANTI_LIST[e.chat_id] = []
    ANTI_LIST[e.chat_id].append(target)
    await e.reply(f"🚫 Đã bật diệt đối thủ: `{target}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/unanti$'))
async def cmd_unanti(e):
    if not check_auth(e.sender_id): return
    ANTI_LIST[e.chat_id] = []
    await e.reply("✅ Đã ngừng diệt tin nhắn.\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoaall$'))
async def cmd_xoaall(e):
    if not check_auth(e.sender_id): return
    async for m in client.iter_messages(e.chat_id, from_user='me', limit=100):
        await m.delete()
    await e.respond("👑 Đã dọn sạch tin nhắn spam!\nADMIN:HQUY")

# --- LOGIC SPAM 500 DÒNG ---
@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    for sentence in NGON_NHAY:
        if not tasks["nhay"].get(e.chat_id): break
        await client.send_message(e.chat_id, sentence)
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/nhaytag (\S+)'))
async def cmd_nhaytag(e):
    if not check_auth(e.sender_id): return
    target = e.pattern_match.group(1)
    tasks["nhaytag"][e.chat_id] = True
    for sentence in NGON_NHAYTAG:
        if not tasks["nhaytag"].get(e.chat_id): break
        await client.send_message(e.chat_id, f"{target} {sentence}")
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

# Flask duy trì server
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
