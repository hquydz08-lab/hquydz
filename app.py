import os, asyncio, threading, time, json, random
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from datetime import datetime, timedelta
from flask import Flask

# ===== CẤU HÌNH =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0Bu58Jr7-lsWHDO3waK6zC3u_f2_fOBnBR7jWd9litQGbKTvcwAFdSKWCx5WZYSdgittvv7qAS8EbarEuyFEUn_nx7H-hCCy1n8x22F9Ar9nmgMrgnCYHrfiKp6FufesRoLsmwxWskmN82h1YSrEl_xQXamc8JkrRUv22MPC385FT6UIlt9KkO1c3pFBHITY9fgipaFAPg8FSB66pcZ-Uv-2MIcupeVYOBzDRUxU6NB9VTF9dCXnSXgPCliCNxfiLvrhCYWMG6U8S110YP98pH1_GRl7VcZ6ZmunHPBRZAB5lCFPg6pn_jSpLVpVEBmOri-sq1gCp57bRsefmh_eRE73E="

# Quản lý dữ liệu Key
# data["users"] giờ sẽ lưu: {"ID_USER": "Ngày_Hết_Hạn"}
data = {"users": {}, "keys": {}, "admins": [7153197678], "delay": 0.5}
tasks = {"spam": {}}

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

# --- MENU & BẢNG GIÁ HÀNG DỌC ---
BANG_GIA = """📣 BẢNG GIÁ KEY REX SPAM
──────────────────────────
🎫 KEY NGÀY: 2.000 VNĐ
🎫 KEY TUẦN: 10.000 VNĐ
🎫 KEY THÁNG: 30.000 VNĐ
🎫 VĨNH VIỄN: 70.000 VNĐ
──────────────────────────
👑 Mua tại: @hquycute
ADMIN:HQUY"""

MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây
🤬 /nhaytag - Nhây tag chửi
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Danh sách admin
🔑 /newkey - Tạo key (Tên + Time)
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Văn bản sang Voice
🛑 /stop - SPAM OFF
🔴 /stopxoa - Dừng xoá tin bot
🚀 /start - Khởi động lại bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

@client.on(events.NewMessage)
async def main_handler(e):
    if not e.text: return
    args = e.text.split()
    cmd = args[0].lower()
    uid = e.sender_id
    
    # Kiểm tra hạn dùng
    now = datetime.now()
    is_vip = False
    if uid == BOSS_ID or uid in data["admins"]:
        is_vip = True
    elif str(uid) in data["users"]:
        expiry = datetime.strptime(data["users"][str(uid)], "%Y-%m-%d %H:%M:%S")
        if now < expiry:
            is_vip = True
        else:
            del data["users"][str(uid)] # Hết hạn thì xóa

    # 1. LỆNH CÔNG KHAI
    if cmd == '/start':
        await e.reply(MENU_VIP if is_vip else BANG_GIA)
        return

    if cmd == '/nhapkey':
        if len(args) < 2: return await e.reply("⚠️ Nhập: `/nhapkey TÊN-KEY`")
        key_name = args[1]
        if key_name in data["keys"]:
            days = data["keys"][key_name]
            expiry_date = now + timedelta(days=days)
            data["users"][str(uid)] = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
            del data["keys"][key_name]
            await e.reply(f"✅ VIP ACTIVE!\nHạn dùng đến: {data['users'][str(uid)]}\nADMIN:HQUY")
        else: await e.reply("❌ Key sai hoặc đã dùng!")
        return

    # 2. LỆNH CHO ADMIN / BOSS
    if is_vip:
        # Cấu trúc: /newkey [tên] [thời gian: day/week/month/forever]
        if cmd == '/newkey' and uid == BOSS_ID:
            if len(args) < 3:
                return await e.reply("⚠️ Cú pháp: `/newkey [tên] [day/week/month/forever]`")
            
            name = args[1]
            duration = args[2].lower()
            days = 0
            
            if duration == 'day': days = 1
            elif duration == 'week': days = 7
            elif duration == 'month': days = 30
            elif duration == 'forever': days = 36500
            else: return await e.reply("❌ Thời gian không hợp lệ (day/week/month/forever)")
            
            data["keys"][name] = days
            await e.reply(f"🔑 ĐÃ TẠO KEY:\n🏷 Tên: `{name}`\n⏰ Hạn: {duration}\nADMIN:HQUY")

        elif cmd == '/info':
            target = (await e.get_reply_message()).sender_id if e.is_reply else uid
            await e.reply(f"👻 ID: `{target}`\nADMIN:HQUY")

        elif cmd == '/stop':
            tasks["spam"][e.chat_id] = False
            await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

        elif cmd == '/nhay':
            tasks["spam"][e.chat_id] = True
            await e.reply("🚀 BẮT ĐẦU...")
            while tasks["spam"].get(e.chat_id):
                await client.send_message(e.chat_id, "đmm sủa tiếp đi con chó mồ côi=))")
                await asyncio.sleep(data["delay"])

# Flask
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
