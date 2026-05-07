from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio, random, os, threading, json
from flask import Flask

# ===== WEB SERVER GIỮ SỐNG =====
app = Flask(__name__)
@app.route('/')
def home(): return "SYSTEM ONLINE"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ===== CẤU HÌNH =====
api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"
BOSS_ID = 7153197678  
STRING_SESSION = "1BVtsOL0Bu4qv-2Kt7PD7f4XQKW22mcgaZTh56Xr6uLc4qAX-eJWivCgQfMNhmQmAxNN5_uxEobvPj5se_yT4a9wSY4Tgwz15QlsCxOoC3VdWluVQzYnHPYs1cczjwN7JZvKXcTQxXrsNpj6FglIq_UO5sxHxAkd21z-cN7IEv2dbY8Dg4ahNWTAZeZQOAIR6ZXmuYLC55qSzPCbPHJlrtvNolkqOrzw_WHsEnRhfX6AyHK7CTQJ9mGl4FOOEYjP28cTHmyOeTiZMQR702UeOIDHsYOhgSZpac9pxhKrcczeyjxVk4HHsZeXRkSSklp0xTbEF7zZ0juFlTCpwj4rTi918cKcJoUA="

client = TelegramClient(StringSession(STRING_SESSION), api_id, api_hash)

# Biến delay mặc định
current_delay = 1.0

# ===== QUẢN LÝ ADMIN =====
def load_admins():
    if not os.path.exists("admins.json"):
        with open("admins.json", "w") as f: json.dump([7153197678], f)
        return [7153197678]
    try:
        with open("admins.json", "r") as f: 
            data = json.load(f)
            if BOSS_ID not in data: data.append(BOSS_ID)
            return data
    except: return [BOSS_ID]

sub_admins = load_admins()
def is_admin(uid): return uid in sub_admins or uid == BOSS_ID

def load_file(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f: f.write("😈")
        return ["😈"]
    with open(file, "r", encoding="utf-8") as f:
        return [i.strip() for i in f if i.strip()]

# ================= LỆNH SET DELAY =================
@client.on(events.NewMessage(pattern=r'^/setdelay (\d+(\.\d+)?)$'))
async def set_delay(e):
    if not is_admin(e.sender_id): return
    global current_delay
    val = float(e.pattern_match.group(1))
    if 0.001 <= val <= 3.0:
        current_delay = val
        await e.reply(f"✅ Đã cập nhật Delay: `{current_delay}`s")
    else:
        await e.reply("❌ Vui lòng nhập từ 0.001 đến 3.0")

# ================= LỆNH MENU =================
@client.on(events.NewMessage(pattern=r'^/menu$'))
async def menu(e):
    if not is_admin(e.sender_id): return
    help_text = f"""⚡ **VIP USERBOT - ADMIN: HQUY** ⚡
---
💬 **LỆNH SPAM (Delay: {current_delay}s):**
• `/nhay` : Nhây tin nhắn
• `/nhaytag [tag]` : Tag kẻ thù
• `/setdelay [số]` : Chỉnh tốc độ (0.001-3.0)
• `/stop` : **SPAM OFF**

🗑 **LỆNH XOÁ:**
• `/xoaall` | `/stopxoa`

🛡 **LỆNH ANTI:**
• `/anti` | `/unanti` [id]

👤 **QUẢN TRỊ:**
• `/info` | `/addadm` | `/xoaadm`
---
🆔 My ID: `7153197678`"""
    await e.reply(help_text)

# ================= LOGIC SPAM & XOÁ =================
nhay_tasks, tag_tasks, delete_tasks = {}, {}, {}
anti_list = set()

@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def nhay(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id
    msgs = load_file("nhay.txt")
    nhay_tasks[cid] = True
    await e.reply(f"💬 Nhây ON | {current_delay}s")
    while nhay_tasks.get(cid):
        await client.send_message(cid, random.choice(msgs))
        await asyncio.sleep(current_delay)

@client.on(events.NewMessage(pattern=r'^/nhaytag (.+)'))
async def nhaytag(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id; users_in = e.text.split()[1:]
    users = []
    for u in users_in:
        try: users.append(await client.get_entity(u))
        except: pass
    tag_tasks[cid] = True
    await e.reply(f"🔥 Nhây Tag ON | {current_delay}s")
    while tag_tasks.get(cid):
        mentions = "".join([f"<a href='tg://user?id={u.id}'>‎</a> " for u in users])
        await client.send_message(cid, f"{mentions}\n{random.choice(load_file('nhaytag.txt'))}", parse_mode="html")
        await asyncio.sleep(current_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def stop_all(e):
    cid = e.chat_id
    nhay_tasks[cid] = tag_tasks[cid] = False
    await e.reply("🛑 SPAM OFF")

@client.on(events.NewMessage(pattern=r'^/xoaall$'))
async def xoa(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id; delete_tasks[cid] = True
    async for m in client.iter_messages(cid):
        if not delete_tasks.get(cid): break
        try: await m.delete()
        except: pass

@client.on(events.NewMessage(pattern=r'^/stopxoa$'))
async def stopx(e): delete_tasks[e.chat_id] = False; await e.reply("🛑 Dừng xoá")

@client.on(events.NewMessage(pattern=r'^/anti (\S+)'))
async def anti_on(e):
    if not is_admin(e.sender_id): return
    try:
        u = await client.get_entity(e.pattern_match.group(1))
        anti_list.add(u.id); await e.reply(f"💀 Đã Anti ID: {u.id}")
    except: await e.reply("❌ Lỗi")

@client.on(events.NewMessage(incoming=True))
async def anti_handler(e):
    if e.sender_id in anti_list:
        try: await e.delete()
        except: pass

# ================= KHỞI CHẠY =================
async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
