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

# Quản lý dữ liệu (Lưu tạm thời)
data = {"users": [], "keys": {}, "admins": [7153197678], "delay": 0.5}
tasks = {"spam": {}, "anti": {}}

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

# --- BẢNG GIÁ HÀNG DỌC ---
BANG_GIA = """📣 BẢNG GIÁ KEY REX SPAM
──────────────────────────
🎫 KEY NGÀY: 2.000 VNĐ
🎫 KEY TUẦN: 10.000 VNĐ
🎫 KEY THÁNG: 30.000 VNĐ
🎫 VĨNH VIỄN: 70.000 VNĐ
──────────────────────────
👑 Mua tại: @hquycute
ADMIN:HQUY"""

# --- MENU VIP HÀNG DỌC ---
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
🔑 /newkey - Tạo key hệ thống
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
    is_vip = (uid == BOSS_ID or uid in data["admins"] or str(uid) in data["users"])

    # 1. Start & Menu
    if cmd == '/start':
        await e.reply(MENU_VIP if is_vip else BANG_GIA)
        return
    if cmd == '/menu' and is_vip:
        await e.reply(MENU_VIP)
        return

    # 2. Các lệnh hệ thống (Chỉ Boss/Admin)
    if is_vip:
        if cmd == '/newkey' and uid == BOSS_ID:
            k = f"REX-{random.randint(1000,9999)}"
            data["keys"][k] = True
            await e.reply(f"🔑 KEY MỚI: `{k}`\nADMIN:HQUY")
        
        elif cmd == '/nhapkey':
            k = args[1] if len(args) > 1 else ""
            if k in data["keys"]:
                data["users"].append(str(uid))
                del data["keys"][k]
                await e.reply("✅ KÍCH HOẠT VIP THÀNH CÔNG!\nADMIN:HQUY")
            else: await e.reply("❌ Key không tồn tại!")

        elif cmd == '/listadm':
            await e.reply(f"📜 Danh sách Admin: `{data['admins']}`\nADMIN:HQUY")

        elif cmd == '/info':
            target = (await e.get_reply_message()).sender_id if e.is_reply else uid
            await e.reply(f"👻 ID của đối tượng: `{target}`\nADMIN:HQUY")

        elif cmd == '/xoaall':
            await e.reply("👑 Đang xoá sạch tin nhắn spam...")
            # Logic xóa (tùy quyền admin group)

        elif cmd == '/xoakey' and uid == BOSS_ID:
            data["keys"] = {}
            await e.reply("❌ Đã xoá sạch kho key hệ thống!\nADMIN:HQUY")

        elif cmd == '/voice':
            await e.reply("💎 Tính năng Voice đang được bảo trì!\nADMIN:HQUY")

        elif cmd == '/addadm' and uid == BOSS_ID:
            new_adm = int(args[1]) if len(args) > 1 else None
            if new_adm:
                data["admins"].append(new_adm)
                await e.reply(f"➕ Đã thêm `{new_adm}` làm Admin.")

        # Lệnh Spam
        elif cmd == '/nhay' or cmd == '/nhaytag':
            tasks["spam"][e.chat_id] = True
            await e.reply("🚀 BẮT ĐẦU NHÂY...")
            while tasks["spam"].get(e.chat_id):
                await client.send_message(e.chat_id, "đmm sủa tiếp đi con chó mồ côi=))")
                await asyncio.sleep(data["delay"])

        elif cmd == '/stop':
            tasks["spam"][e.chat_id] = False
            await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

# Flask
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
