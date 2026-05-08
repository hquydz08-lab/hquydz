import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH HỆ THỐNG =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678  # Kiểm tra đúng ID này để hiện Menu VIP
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0Bu58Jr7-lsWHDO3waK6zC3u_f2_fOBnBR7jWd9litQGbKTvcwAFdSKWCx5WZYSdgittvv7qAS8EbarEuyFEUn_nx7H-hCCy1n8x22F9Ar9nmgMrgnCYHrfiKp6FufesRoLsmwxWskmN82h1YSrEl_xQXamc8JkrRUv22MPC385FT6UIlt9KkO1c3pFBHITY9fgipaFAPg8FSB66pcZ-Uv-2MIcupeVYOBzDRUxU6NB9VTF9dCXnSXgPCliCNxfiLvrhCYWMG6U8S110YP98pH1_GRl7VcZ6ZmunHPBRZAB5lCFPg6pn_jSpLVpVEBmOri-sq1gCp57bRsefmh_eRE73E="

def fix_padding(s):
    s = s.strip().replace(" ", "")
    return s + "=" * (-len(s) % 4)

client = TelegramClient(StringSession(fix_padding(SESSION_STR)), API_ID, API_HASH)

# --- 2 BỘ VĂN BẢN (TỔNG 1000 DÒNG) ---
BO_NHAY_1 = [f"Dòng {i+1}: cn choa ei=)) sủa tiếp đi con cún" for i in range(500)]
BO_NHAY_2 = [f"Dòng {i+1}: mẹ m bị t cho ăn gậy=)) cay không con súc vật" for i in range(500)]

tasks = {"spam": {}}

# --- HỆ THỐNG MENU & LỆNH HÀNG DỌC ---
MENU_VIP = """✨ ────────────────────────── ✨
🦖 Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây (500 dòng)
🤬 /nhaytag - Nhây tag chửi (500 dòng)
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ spam
🚫 /anti - Tự xóa tin nhắn đối thủ
✅ /unanti - Ngừng xóa tin nhắn
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key (ngày/tuần/tháng/vv)
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key hệ thống
👑 /xoaall - Xoá sạch tin nhắn spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển văn bản thành voice
🛑 /stop - Dừng SPAM (SPAM OFF)
🔴 /stopxoa - Dừng xóa tin nhắn bot
🚀 /start - Khởi động lại bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

BANG_GIA = """📣 BẢNG GIÁ KEY REX SPAM
──────────────────────────
🎫 KEY NGÀY: 2.000 VNĐ
🎫 KEY TUẦN: 10.000 VNĐ
🎫 KEY THÁNG: 30.000 VNĐ
🎫 VĨNH VIỄN: 70.000 VNĐ
──────────────────────────
👑 Mua tại: @hquycute
ADMIN:HQUY"""

@client.on(events.NewMessage(pattern=r'^/menu$|^/start$'))
async def cmd_start(e):
    if e.sender_id == BOSS_ID:
        await e.reply(MENU_VIP)
    else:
        await e.reply(BANG_GIA)

@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def run_nhay1(e):
    if e.sender_id != BOSS_ID: return
    tasks["spam"][e.chat_id] = True
    await e.reply("🚀 BẮT ĐẦU NHÂY BỘ 1 (500 DÒNG)!")
    for msg in BO_NHAY_1:
        if not tasks["spam"].get(e.chat_id): break
        await client.send_message(e.chat_id, msg)
        await asyncio.sleep(0.5)

@client.on(events.NewMessage(pattern=r'^/nhaytag$'))
async def run_nhay2(e):
    if e.sender_id != BOSS_ID: return
    tasks["spam"][e.chat_id] = True
    await e.reply("🔥 BẮT ĐẦU NHÂY BỘ 2 (500 DÒNG)!")
    for msg in BO_NHAY_2:
        if not tasks["spam"].get(e.chat_id): break
        await client.send_message(e.chat_id, msg)
        await asyncio.sleep(0.5)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def run_stop(e):
    tasks["spam"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

# Flask cho Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
