import os, random, asyncio, threading, json, time
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
BOSS_ID = 7153197678  # ID CỦA ÔNG
SESSION_STR = "1BVtsOL0Bu3ftXep1MwrLMPn8yO4m3tKwmrCkouFBDrR7vihqk4-ZCg6kK-zJaAkYu4Z96OSdBK7DNzoRMXCFrMTxi80pqi0OK95BBjcto5w0WVNHlXJikycoNa7bmNPYrXMQyRx3QkJkYVXxH5nmGo4AKTPzht9yqHTj7jx-pCS68Aj0yJxGZmcryReEdREjpq1ibTDJx6Uyd_FZkgWUY9CuFvFwyLNy4F_Uivi2ng8IsawIwJW8JiLtXkbz5vMvWsA0xelcH42HGvGZgqXCnpQK8mV3WpY6YjEXCIJEwMFWiGPv-SjD1ISUGBcl2sACEn-DxzWS5S5dbR9AJI7TknKG5QbrBv4=" 

DATA_FILE = "data_hquy.json"
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f: return json.load(f)
        except: pass
    # Mặc định admin là ID của ông
    return {"keys": {}, "user_keys": {}, "admins": [7153197678]}

data = load_data()
def save_data():
    with open(DATA_FILE, "w") as f: json.dump(data, f)

tasks = {"nhay": {}, "nhaytag": {}}
ANTI_LIST = {}
global_delay = 0.5 

# ===== BỘ NGÔN (DÀI 500+ DÒNG) =====
NGON_NHAY = [
    "cn choa ei=))=))=))=))", "123=))=))=))=))", "m chay anh cmnr=))=))=))=))=))", "m yeu ot z tk nfu=))=))=))=))=))",
    "m cham vl e=))=))=))", "slow lun e=))=))=))=))", "yeu z cn dix=))=))=))=))", "tk 3de=))=))=))=))=))",
    "tk dix lgbt=))=))=))=))", "cn choa nfu=))=))=))=))=))", "deo co canh lun e=))=))=))=))", "m cham vl e=))=))=))=))",
    "m yeu v=))=))=))=))=))=))", "yeu ro=))=))=))=))=))=))", "bia a=))=))=))=))", "tk dix=))=))=))=))", "mau k=))=))=))=))"
] * 30 

NGON_NHAYTAG = [
    "123 con chó cùng sủa =))", "con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣", "con đĩ phàn kháng cha được không ấy",
    "thằng cha mày gánh lúa cho mày đi đú à :))", "mẹ đĩ mày dắt mày vô sàn à :))", "con điếm bị bố sỉ nhục", "không phục à",
    "phản kháng lại những câu sỉ vả của cha xem :))", "con chó học cách làm người à 👉🤣", "con chó ăn cứt :))",
    "con chó mồ côi 🤙", "mày ngu vậy sao không off mxh luôn đi 🤣👋", "sồn mau không con đĩ mẹ m chết"
] * 40

client = TelegramClient(StringSession(SESSION_STR), api_id, api_hash)

# --- KIỂM TRA QUYỀN HẠN ---
def check_auth(uid):
    if uid == 7153197678 or uid in data["admins"]: return True
    uid_str = str(uid)
    if uid_str in data["user_keys"]:
        expiry = data["user_keys"][uid_str]
        if expiry == "vinhvien" or time.time() < expiry: return True
    return False

# --- HỆ THỐNG 17 LỆNH ---
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

@client.on(events.NewMessage(pattern=r'^/setdelay (\d+(\.\d+)?)'))
async def cmd_delay(e):
    if not check_auth(e.sender_id): return
    global global_delay
    global_delay = float(e.pattern_match.group(1))
    await e.reply(f"⚡ Đã chỉnh delay về: {global_delay}s\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/anti (\S+)'))
async def cmd_anti(e):
    if not check_auth(e.sender_id): return
    u = await client.get_entity(e.pattern_match.group(1))
    if e.chat_id not in ANTI_LIST: ANTI_LIST[e.chat_id] = []
    if u.id not in ANTI_LIST[e.chat_id]: ANTI_LIST[e.chat_id].append(u.id)
    await e.reply(f"🚫 Đã khóa mục tiêu: {u.id}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/unanti (\S+)'))
async def cmd_unanti(e):
    if not check_auth(e.sender_id): return
    u = await client.get_entity(e.pattern_match.group(1))
    if e.chat_id in ANTI_LIST and u.id in ANTI_LIST[e.chat_id]:
        ANTI_LIST[e.chat_id].remove(u.id)
    await e.reply(f"✅ Đã gỡ khóa: {u.id}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/addadm (\d+)'))
async def cmd_addadm(e):
    if e.sender_id != 7153197678: return
    aid = int(e.pattern_match.group(1))
    if aid not in data["admins"]: data["admins"].append(aid); save_data()
    await e.reply(f"➕ Đã thêm Admin: {aid}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoadm (\d+)'))
async def cmd_xoadm(e):
    if e.sender_id != 7153197678: return
    aid = int(e.pattern_match.group(1))
    if aid in data["admins"]: data["admins"].remove(aid); save_data()
    await e.reply(f"➖ Đã xóa Admin: {aid}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/listadm$'))
async def cmd_listadm(e):
    await e.reply(f"📜 Danh sách Admin: {data['admins']}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/newkey (day|week|month|vinhvien)'))
async def cmd_newkey(e):
    if not check_auth(e.sender_id): return
    dur = e.pattern_match.group(1)
    k = f"HQUY-{random.randint(100,999)}"
    vals = {"day": 86400, "week": 604800, "month": 2592000, "vinhvien": "vinhvien"}
    data["keys"][k] = vals[dur]; save_data()
    await e.reply(f"🔑 Key mới ({dur}): `{k}`\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/nhapkey (\S+)'))
async def cmd_nhapkey(e):
    k = e.pattern_match.group(1)
    if k in data["keys"]:
        exp = data["keys"][k]
        data["user_keys"][str(e.sender_id)] = "vinhvien" if exp == "vinhvien" else time.time() + exp
        del data["keys"][k]; save_data()
        await e.reply("✅ Kích hoạt thành công!\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/xoakey (\S+)'))
async def cmd_xoakey(e):
    if not check_auth(e.sender_id): return
    k = e.pattern_match.group(1)
    if k in data["keys"]: 
        del data["keys"][k]; save_data()
        await e.reply("❌ Đã xóa Key hệ thống.")

@client.on(events.NewMessage(pattern=r'^/info$'))
async def cmd_info(e):
    await e.reply(f"👻 ID Của Bạn: {e.sender_id}\nID Chat: {e.chat_id}\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    tasks["nhay"][e.chat_id] = tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

@client.on(events.NewMessage(pattern=r'^/stopxoa$'))
async def cmd_stopxoa(e):
    await e.reply("🔴 Đã dừng xoá tin nhắn bot spam.\nADMIN:HQUY")

# Lệnh rỗng chờ cập nhật
@client.on(events.NewMessage(pattern=r'^/(call|voice|xoaall)'))
async def placeholders(e):
    await e.reply("💎 Chức năng đang được OWNER bảo trì...\nADMIN:HQUY")

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

@client.on(events.NewMessage())
async def auto_delete_handler(e):
    if e.chat_id in ANTI_LIST and e.sender_id in ANTI_LIST[e.chat_id]:
        try: await e.delete()
        except: pass

app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Online"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
