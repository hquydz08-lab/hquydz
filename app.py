from telethon import TelegramClient, events
import asyncio, random, os, threading, json
from flask import Flask

# ===== WEB SERVER GIỮ SỐNG (DÀNH CHO RENDER) =====
app = Flask(__name__)
@app.route('/')
def home(): return "SYSTEM ONLINE"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ===== CẤU HÌNH ID CHÍNH CHỦ =====
api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"
session_name = "vip_userbot"
BOSS_ID = 7153197678  # ID CỦA ÔNG ĐÃ ĐƯỢC THÊM TẠI ĐÂY

client = TelegramClient(session_name, api_id, api_hash)

# ===== QUẢN LÝ QUYỀN ADMIN =====
def load_admins():
    if not os.path.exists("admins.json"):
        # Mặc định thêm ID của ông vào file admin nếu chưa có
        with open("admins.json", "w") as f: json.dump([BOSS_ID], f)
        return [BOSS_ID]
    try:
        with open("admins.json", "r") as f: 
            data = json.load(f)
            if BOSS_ID not in data: data.append(BOSS_ID)
            return data
    except: return [BOSS_ID]

def save_admins(data):
    with open("admins.json", "w") as f: json.dump(data, f, indent=4)

sub_admins = load_admins()

def is_admin(uid):
    return uid in sub_admins or uid == BOSS_ID

def load_file(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f: f.write("😈")
        return ["😈"]
    with open(file, "r", encoding="utf-8") as f:
        return [i.strip() for i in f if i.strip()]

# ================= LỆNH MENU (XEM TẤT CẢ LỆNH) =================
@client.on(events.NewMessage(pattern=r'^/menu$'))
async def menu(e):
    if not is_admin(e.sender_id): return
    help_text = """⚡ **VIP USERBOT - ADMIN: HQUY** ⚡
---
💬 **LỆNH SPAM:**
• `/nhay [delay]` : Nhây tin nhắn
• `/nhaytag [tag] [delay]` : Tag kẻ thù
• `/treongon [delay]` : Treo văn bản dài
• `/stop` : **SPAM OFF**

🗑 **LỆNH XOÁ:**
• `/xoaall` : Xoá sạch tin nhắn nhóm
• `/stopxoa` : Dừng xoá

🛡 **LỆNH ANTI:**
• `/anti [username/id]` : Bật Anti
• `/unanti [username/id]` : Tắt Anti

👤 **QUẢN TRỊ:**
• `/info [username]` : Lấy ID nhanh
• `/addadm [id]` : Thêm Admin (Boss dùng)
• `/xoaadm [id]` : Xoá Admin (Boss dùng)
---
🆔 My ID: `7153197678`"""
    await e.reply(help_text)

# ================= LỆNH QUẢN LÝ (CHỈ ÔNG DÙNG ĐƯỢC) =================
@client.on(events.NewMessage(pattern=r'^/addadm (\d+)'))
async def add_adm(e):
    if e.sender_id != BOSS_ID: return
    new_id = int(e.pattern_match.group(1))
    if new_id not in sub_admins:
        sub_admins.append(new_id)
        save_admins(sub_admins)
        await e.reply(f"✅ Đã thêm Admin: `{new_id}`")

@client.on(events.NewMessage(pattern=r'^/xoaadm (\d+)'))
async def del_adm(e):
    if e.sender_id != BOSS_ID: return
    target = int(e.pattern_match.group(1))
    if target == BOSS_ID: return await e.reply("❌ Ông không thể tự xoá chính mình!")
    if target in sub_admins:
        sub_admins.remove(target)
        save_admins(sub_admins)
        await e.reply(f"🗑 Đã xóa Admin: `{target}`")

# ================= LỆNH INFO (LẤY ID QUA USERNAME) =================
@client.on(events.NewMessage(pattern=r'^/info (@\S+)'))
async def get_info(e):
    if not is_admin(e.sender_id): return
    username = e.pattern_match.group(1)
    try:
        user = await client.get_entity(username)
        await e.reply(f"👤 User: {username}\n🆔 ID: `{user.id}`")
    except:
        await e.reply("❌ Không tìm thấy user này!")

# ================= LOGIC SPAM & XOÁ (GIỮ NGUYÊN) =================
nhay_tasks, tag_tasks, treo_tasks, delete_tasks = {}, {}, {}, {}
anti_list = set()

@client.on(events.NewMessage(pattern=r'^/nhay (\d+)'))
async def nhay(e):
    if not is_admin(e.sender_id): return
    delay, cid = int(e.pattern_match.group(1)), e.chat_id
    msgs = load_file("nhay.txt")
    nhay_tasks[cid] = True
    await e.reply(f"💬 Nhây ON | {delay}s")
    while nhay_tasks.get(cid):
        await client.send_message(cid, random.choice(msgs))
        await asyncio.sleep(delay)

@client.on(events.NewMessage(pattern=r'^/nhaytag (.+) (\d+)'))
async def nhaytag(e):
    if not is_admin(e.sender_id): return
    parts = e.text.split(); delay = int(parts[-1]); users_in = parts[1:-1]; cid = e.chat_id
    users = []
    for u in users_in:
        try: users.append(await client.get_entity(u))
        except: pass
    tag_tasks[cid] = True
    await e.reply(f"🔥 Nhây Tag ON | {delay}s")
    while tag_tasks.get(cid):
        mentions = "".join([f"<a href='tg://user?id={u.id}'>‎</a> " for u in users])
        await client.send_message(cid, f"{mentions}\n{random.choice(load_file('nhaytag.txt'))}", parse_mode="html")
        await asyncio.sleep(delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def stop_all(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id
    nhay_tasks[cid] = tag_tasks[cid] = treo_tasks[cid] = False
    await e.reply("🛑 SPAM OFF")

@client.on(events.NewMessage(pattern=r'^/xoaall$'))
async def xoa(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id; delete_tasks[cid] = True
    await e.reply("🗑 Đang xoá tin nhắn...")
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

@client.on(events.NewMessage(pattern=r'^/unanti (\S+)'))
async def anti_off(e):
    if not is_admin(e.sender_id): return
    try:
        u = await client.get_entity(e.pattern_match.group(1))
        anti_list.discard(u.id); await e.reply(f"😇 Đã Unanti ID: {u.id}")
    except: await e.reply("❌ Lỗi")

@client.on(events.NewMessage(incoming=True))
async def anti_handler(e):
    if e.sender_id in anti_list:
        try: await e.delete()
        except: pass

# ================= KHỞI CHẠY =================
async def main():
    await client.start()
    print(f"Bot Online! Boss ID: {BOSS_ID}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
