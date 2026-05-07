import os, random, asyncio, threading, json, time
from datetime import datetime
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
# DÁN SESSION CỦA ÔNG VÀO ĐÂY
SESSION_STR = "1BVtsOL0Bu4qv-2Kt7PD7f4XQKW22mcgaZTh56Xr6uLc4qAX-eJWivCgQfMNhmQmAxNN5_uxEobvPj5se_yT4a9wSY4TgwSjAkYp1MwrLMPn8y04m3tKwmrCkouFBDrR7vihqk4-ZCg6kKzJaAkYu4Z960SdBK7DNzoRMXCFrMTxi80pqi0OK95BBjcto5w0WVNH1XJikycoNa7bmNPYrXMQyRx3QkJkyVXxh5nmGo4AKTPzht9yqHTj7jx-pCS68Aj0yJxGZmcryReEdRejpq1ibTDJx6Uyd_FZkgWUY9CuFvFwyLNy4F_Uivi2ng8IsawIwJW8JiLTXkbz5vMvWsA0xelch42HGvGZgqXCnpQK8mV3WPy6YjEXCIJEwMFWiGPv-SjD1ISUGBcl2sACEn-DxzWS5S5dbR9AJI7TknkG5QbrBv4="

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
STOP_XOA = False
global_delay = 0.5 

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

def check_auth(uid):
    if uid == BOSS_ID or uid in data["admins"]: return True
    uid_str = str(uid)
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien" or (isinstance(expiry, (int, float)) and time.time() < expiry): return True
    return False

# --- HỆ THỐNG 17 LỆNH HOÀN CHỈNH ---

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
📞 /call - Gọi điện xuyên giáp
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
💎 /voice - CHUYỂN VĂN BẢN THÀNH VOICE
🛑 /stop - Dừng tất cả
🔴 /stopxoa - Dừng xoá tin nhắn bot
✨ ────────────────────────── ✨
ADMIN:HQUY""")
    else:
        await e.reply("📣 XÁC THỰC NGƯỜI DÙNG\n🎫 2K/DAY | 10K/WEEK | 70K/VV\n📝 Nhập key: /nhapkey <key>\n👑 ADMIN: @hquycute")

@client.on(events.NewMessage(pattern=r'^/addadm (\d+)'))
async def cmd_addadm(e):
    if e.sender_id != BOSS_ID: return
    aid = int(e.pattern_match.group(1))
    if aid not in data["admins"]: data["admins"].append(aid); save_data()
    await e.reply(f"➕ Đã thêm Admin: `{aid}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoadm (\d+)'))
async def cmd_xoadm(e):
    if e.sender_id != BOSS_ID: return
    aid = int(e.pattern_match.group(1))
    if aid in data["admins"]: data["admins"].remove(aid); save_data()
    await e.reply(f"➖ Đã xóa Admin: `{aid}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/newkey (day|week|month|vinhvien)'))
async def cmd_newkey(e):
    if not check_auth(e.sender_id): return
    dur = e.pattern_match.group(1)
    k = f"HQUY-{random.randint(1000,9999)}"
    vals = {"day": 86400, "week": 604800, "month": 2592000, "vinhvien": "vinhvien"}
    data["keys"][k] = vals[dur]; save_data()
    await e.reply(f"🔑 Key ({dur}): `{k}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoakey (\S+)'))
async def cmd_xoakey(e):
    if not check_auth(e.sender_id): return
    k = e.pattern_match.group(1)
    if k in data["keys"]: del data["keys"][k]; save_data(); await e.reply("❌ Đã xóa key hệ thống.")

@client.on(events.NewMessage(pattern=r'^/setdelay (\d+(\.\d+)?)'))
async def cmd_delay(e):
    if not check_auth(e.sender_id): return
    global global_delay
    global_delay = float(e.pattern_match.group(1))
    await e.reply(f"⚡ Tốc độ: {global_delay}s\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/anti$'))
async def cmd_anti(e):
    if not check_auth(e.sender_id) or not e.is_reply: return
    msg = await e.get_reply_message()
    target = msg.sender_id
    if e.chat_id not in ANTI_LIST: ANTI_LIST[e.chat_id] = []
    ANTI_LIST[e.chat_id].append(target)
    await e.reply(f"🚫 Đã bật diệt đối thủ: `{target}`")

@client.on(events.NewMessage(pattern=r'^/unanti$'))
async def cmd_unanti(e):
    if not check_auth(e.sender_id): return
    ANTI_LIST[e.chat_id] = []
    await e.reply("✅ Đã dọn dẹp danh sách diệt.")

@client.on(events.NewMessage(pattern=r'^/info$'))
async def cmd_info(e):
    await e.reply(f"👻 ID: `{e.sender_id}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/stopxoa$'))
async def cmd_stopxoa(e):
    if not check_auth(e.sender_id): return
    global STOP_XOA
    STOP_XOA = True
    await e.reply("🔴 Đã dừng xoá tin nhắn bot.\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoaall$'))
async def cmd_xoaall(e):
    if not check_auth(e.sender_id): return
    async for msg in client.iter_messages(e.chat_id, from_user='me', limit=100):
        await msg.delete()
    await e.respond("👑 Đã dọn sạch bãi chiến trường!\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/call$'))
async def cmd_call(e):
    if not check_auth(e.sender_id): return
    await e.reply("📞 Đang kết nối cuộc gọi xuyên giáp...\nADMIN:HQUY")

@client.on(events.NewMessage())
async def auto_delete(e):
    if e.chat_id in ANTI_LIST and e.sender_id in ANTI_LIST[e.chat_id]:
        await e.delete()

# --- CÁC LỆNH NHÂY ---
@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    while tasks["nhay"].get(e.chat_id):
        await client.send_message(e.chat_id, "cn choa ei=))=))=))")
        await asyncio.sleep(global_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    if not check_auth(e.sender_id): return
    tasks["nhay"][e.chat_id] = tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
