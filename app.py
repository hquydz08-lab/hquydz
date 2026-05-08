import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from flask import Flask

# ===== CẤU HÌNH =====
API_ID = 34619338
API_HASH = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678 
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
SESSION_STR = "1BVtsOL0Bu58Jr7-lsWHDO3waK6zC3u_f2_fOBnBR7jWd9litQGbKTvcwAFdSKWCx5WZYSdgittvv7qAS8EbarEuyFEUn_nx7H-hCCy1n8x22F9Ar9nmgMrgnCYHrfiKp6FufesRoLsmwxWskmN82h1YSrEl_xQXamc8JkrRUv22MPC385FT6UIlt9KkO1c3pFBHITY9fgipaFAPg8FSB66pcZ-Uv-2MIcupeVYOBzDRUxU6NB9VTF9dCXnSXgPCliCNxfiLvrhCYWMG6U8S110YP98pH1_GRl7VcZ6ZmunHPBRZAB5lCFPg6pn_jSpLVpVEBmOri-sq1gCp57bRsefmh_eRE73E="

client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

# --- BỘ NGÔN 1000 DÒNG ---
BO_NGON_1 = [f"Dòng {i+1}: cn choa ei=)) sủa đi" for i in range(500)]
BO_NGON_2 = [f"Dòng {i+1}: mẹ m bị t cho ăn gậy=))" for i in range(500)]

tasks = {"spam": {}}

# --- MENU 18 LỆNH HÀNG DỌC (ÉP HIỆN) ---
MENU_VIP = """✨ ────────────────────────── ✨
Rex Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 DANH SÁCH MENU
🤬 /nhay - Trêu nhây (500 dòng)
🤬 /nhaytag - Nhây tag chửi (500 dòng)
📞 /call - Spam Call + ID
⚡ /setdelay - Chỉnh tốc độ
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin
➕ /addadm - Thêm quản trị viên
➖ /xoadm - Xóa quản trị viên
📜 /listadm - Xem danh sách admin
🔑 /newkey - Tạo key hệ thống
🔑 /nhapkey - Kích hoạt key
❌ /xoakey - Xóa key
👑 /xoaall - Xoá sạch spam
👻 /info - Check ID người dùng
💎 /voice - Chuyển sang Voice
🛑 /stop - Dừng tất cả (SPAM OFF)
🔴 /stopxoa - Dừng xóa bot
🚀 /start - Khởi động bot
✨ ────────────────────────── ✨
ADMIN:HQUY"""

@client.on(events.NewMessage)
async def catch_all(e):
    # LOG NÀY ĐỂ ÔNG XEM TRÊN RENDER: NẾU HIỆN DÒNG NÀY MÀ BOT KHÔNG REP LÀ DO TOKEN CHẾT
    print(f"📩 Nhận tin: {e.text} từ ID: {e.sender_id}")
    
    cmd = e.text.lower() if e.text else ""
    
    if cmd in ['/menu', '/start']:
        await e.reply(MENU_VIP)

    if cmd == '/nhay':
        if e.sender_id != BOSS_ID: return
        tasks["spam"][e.chat_id] = True
        await e.reply("🚀 VĂNG 500 DÒNG!")
        for msg in BO_NGON_1:
            if not tasks["spam"].get(e.chat_id): break
            await client.send_message(e.chat_id, msg)
            await asyncio.sleep(0.5)

    if cmd == '/stop':
        tasks["spam"][e.chat_id] = False
        await e.reply("🛑 **SPAM OFF**\nADMIN:HQUY")

# Flask duy trì cho Render
app = Flask(__name__)
@app.route('/')
def h(): return "Bot Live"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

print("🚀 BOT ĐANG CHẠY... ÔNG GÕ /MENU ĐI!")
client.start(bot_token=BOT_TOKEN)
client.run_until_disconnected()
