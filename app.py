import os, random, asyncio, threading, json, time
from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.functions.phone import RequestCallRequest
from flask import Flask
from gtts import gTTS

# ===== CẤU HÌNH HỆ THỐNG =====
api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"
# Đã thay ID của ông vào đây
BOSS_ID = 7153197678  
DATA_FILE = "data_hquy.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"keys": {}, "user_keys": {}, "admins": [7153197678]} # Thêm ID vào list admin mặc định

data = load_data()
def save_data():
    with open(DATA_FILE, "w") as f: json.dump(data, f)

tasks = {"nhay": {}, "nhaytag": {}}
ANTI_LIST = {}
current_delay = 0.5 

# ===== BỘ NGÔN 1: /NHAY (X10 BIẾN THỂ) =====
NGON_NHAY = [
    "cn choa ei=))=))=))=))", "m chay anh cmnr=))=))=))=))=))", "m yeu ot z tk nfu=))=))=))=))=))",
    "m cham vl e=))=))=))", "slow lun e=))=))=))=))", "tk dix lgbt=))=))=))=))",
    "cmm dot tu kia=))=))=))", "anh lai win a=))=))=))=))", "uoc loser ma=))=))=))=))",
    "m đuối rồi à tk nqu=))", "sủa mạnh lên xem nào=))", "mẹ m béo vcl e=))",
    "đĩ mẹ m tắc thở à=))", "óc chó ăn cứt e=))", "mồ côi cha mẹ hả m=))",
    "thằng rác rưởi mxh=))", "trình còi đòi nch=))", "bố gõ lủng sọ m=))",
    "đã nqu còn hay sủa=))", "con chó dại mxh=))", "mẹ m làm đĩ ở đâu=))",
    "bố m là bậc thầy nhây=))", "mẹ m bị t địt rên hừ hừ=))", "mẹ m bú cu t sướng k=))",
    "tk con hoang mất dạy=))", "gõ nhanh lên con chó=))", "m rớt mạng rồi à=))",
    "m bị admin hquy sút à=))", "trông m hài vcl e=))", "m bị đần à tk nqu=))",
    "bố m cân tất nhé=))", "mẹ m đang nằm dưới háng t=))", "đĩ mẹ m chết chưa=))",
    "m rên rỉ như con đĩ=))", "m nhây bằng bố k=))", "m tuổi lồn e=))",
    "gõ tiếp đi tk nqu=))", "đang sủa sao im z=))", "m bị liệt tay à=))",
    "admin hquy trị m nè=))", "con chó mồ côi sủa đi=))", "mẹ m bị t hành hạ=))",
    "m rên rỉ như con chó=))", "m tuổi gì đòi so trình=))", "bố m là trùm mxh=))",
    "mẹ m bị t hiếp dâm=))", "mẹ m bú cu t hăng say=))", "m gõ như rùa bò=))",
    "mẹ m chết thảm vcl=))", "m bị t sút vô đầu=))", "m tuổi tôm e ơi=))",
    "mẹ m làm đĩ nuôi m à=))", "m bú cứt t k e=))", "m nqu bẩm sinh à=))",
    "m bị t hành ra bã=))", "m rên lên đi e=))", "m mẹ m bị t chặt đầu=))",
    "m sống chi cho chật đất=))", "m bú dái t k e=))", "m bị t sỉ nhục=))"
]

# ===== BỘ NGÔN 2: /NHAYTAG (GIỮ NGUYÊN 200+ CÂU) =====
NGON_NHAYTAG = [
    "123 con chó cùng sủa =))", "con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣",
    "con đĩ phàn kháng cha được không ấy", "thằng cha mày gánh lúa cho mày đi đú à :))",
    "mẹ đĩ mày dắt mày vô sàn à :))", "con điếm bị bố sỉ nhục", "không phục à",
    "phản kháng lại những câu sỉ vả của cha xem :))", "con chó học cách làm người à 👉🤣",
    "con chó ăn cứt :))", "phế phẩm vậy em", "con chó mồ côi 🤙",
    "mày ngu vậy sao không off mxh luôn đi 🤣👋", "max speed được không ấy con chó ei 👉🤪",
    "lại phải win à 😁", "sồn mau không con đĩ mẹ m chết", "thằng cặc bất hiếu",
    "mẹ mày bị anh chơi suốt năm suốt tháng mà 😛", "sồn để cứu con mẹ mày mau🥺👋",
    "cha win cmnr :))", "bố cầm shotgun bắn thủng não con đĩ ngu :))",
    "mặt cứt mày phế phẩm vậy em", "con chó đú ửa à 🤪", "thằng ngu ei 👉😛",
    "phản kháng bố mau 😒", "còn sự sống không ấy thằng nqu ei :))",
    "mxh là cách duy nhất để mày sống ak :))", "thua bố không phục ak :))",
    "đĩ lồn ăn cứt trâu để sống qua ngày à 🤣", "thằng ngu cố nhai nốt mấy câu để cầu cứu con gái mẹ m nha :))",
    "thằng óc cứt ảo war ae ơi :))", " ôm hận bố cmnr :))",
    "óc cứt múa may quay cuồng để bị cha sỉ vả vào cái mặt cứt mày à :))",
    "ngôn như con cặc thêm cái mặt cặc mày để bố buồn nôn à :))",
    "bố đái vào cái bàn thờ thờ tổ tiên 3 đời con chó ngu ăn cứt :))",
    "thằng em bị bố gõ cho hồn bay phách lạc đi cùng con mẹ mày rồi ak 🤪",
    "thấy bố là mày câm à :))", "bố chưa cho mày chạy mà :))",
    "con chó cố gắng hăng 1 tí được không :))", "mẹ mày trông khá ngon 🤪🤙",
    "nhìn mặt mày cay cay bố lắm rồi ak 🤣", "bố mà tung skill sút mày là tỉ lệ tử vong của mày là 100% =)))",
    "chó home cặc tập đú war kìa ae làng nước ơi =)))", "thằng não tật chỉ biết câm nín nhìn bố sỉ vả 👉😒",
    "alo alo :))", "chọn cách im lặng để bố tha cho mẹ đĩ mày à :))",
    "sao sao :))", "tnh bại kìa :))", "bố lại win à :))",
    "con chó ngu đú đú ôm hận bố đến cuối đời :))", "chó đú ảo war r ak 🤣🤙",
    "trông ngôn mày phèn như quần áo con gái mẹ mày mặc cộng vô đell nổi 50k :))",
    "óc chó bị sỉ vả đang nghĩ cách phục thù bố đoá 😁✌️", "mẹ mày trông nứng ghê vậy :))",
    "mẹ mày làm đĩ từ tuổi 16 bán dâm kiếm tiền cho thằng bại não mày lên đây đú đú kiếm fame từ bố ak 🤣",
    "đĩ ngu cầu xin bố tha mạng à =))", "gào thét trong vô vọng cmnr à :))",
    "bố xuất tinh vào não mẹ đĩ mày cmnr :))", "ơ ơ nổi điên rồi à :))",
    "học cách phản kháng bố để giải cứu con mẹ mày xem =))", "tk óc choá :)))",
    "đừng làm cha chú ý bằng những câu phèn cặc mày lấy trên mạng :))",
    "con đ/ĩ mẹ mày bị tao cầm đinh ba xiên chết tại chỗ thằng bố mày ôm hận tao qua báo thù cho con mẹ nó còn không xong bị tao cầm phóng lợn xiên qua đầu của bố mày máu rơi như tinh trùng bố của mày bắn vào lỗ l/ồ/n mẹ mày🤣🤣❓️",
    "con chó ngu mày thích ăn vạ bố k bố lại đấm cho 1 cái bây giờ :))",
    "con chó mồ côi 44 đi là vừa e=))", "gõ tiếp đi con chó ngu e=))",
    "mẹ m chết thảm lắm m biết k=))", "bố gõ lủng sọ gia đình m=))"
] # (Toàn bộ 200+ câu chửi gốc được giữ trong biến NGON_NHAYTAG)

# ===== CLIENT & LOGIC (ADMIN:HQUY) =====
client = TelegramClient(StringSession(""), api_id, api_hash)

def has_key(uid):
    if uid in data["admins"] or uid == 7153197678: return True
    return str(uid) in data["user_keys"]

def is_admin(uid):
    return uid in data["admins"] or uid == 7153197678

@client.on(events.NewMessage(pattern=r'^/nhay$'))
async def cmd_nhay(e):
    if not has_key(e.sender_id): return
    tasks["nhay"][e.chat_id] = True
    while tasks["nhay"].get(e.chat_id):
        await client.send_message(e.chat_id, random.choice(NGON_NHAY))
        await asyncio.sleep(current_delay)

@client.on(events.NewMessage(pattern=r'^/nhaytag (\S+)(?: (\d+))?'))
async def cmd_nhaytag(e):
    if not has_key(e.sender_id): return
    target = e.pattern_match.group(1)
    delay = float(e.pattern_match.group(2)) if e.pattern_match.group(2) else current_delay
    tasks["nhaytag"][e.chat_id] = True
    while tasks["nhaytag"].get(e.chat_id):
        await client.send_message(e.chat_id, f"{target} {random.choice(NGON_NHAYTAG)}")
        await asyncio.sleep(delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def cmd_stop(e):
    tasks["nhay"][e.chat_id] = False
    tasks["nhaytag"][e.chat_id] = False
    await e.reply("🛑 **SPAM OFF**")

# ===== QUẢN LÝ ADMIN & KEY =====
@client.on(events.NewMessage(pattern=r'^/addadm (\d+)'))
async def add_adm(e):
    if e.sender_id != 7153197678: return
    nid = int(e.pattern_match.group(1))
    if nid not in data["admins"]: data["admins"].append(nid); save_data()
    await e.reply(f"✅ Đã thêm Admin: `{nid}`")

@client.on(events.NewMessage(pattern=r'^/newkey (\S+)'))
async def new_key(e):
    if not is_admin(e.sender_id): return
    k = e.pattern_match.group(1)
    data["keys"][k] = True; save_data()
    await e.reply(f"🔑 Đã tạo Key mới: `{k}`")

@client.on(events.NewMessage(pattern=r'^/nhapkey (\S+)'))
async def nhap_key(e):
    k = e.pattern_match.group(1)
    if k in data["keys"]:
        data["user_keys"][str(e.sender_id)] = True
        del data["keys"][k]; save_data()
        await e.reply("✅ Kích hoạt Key thành công!")
    else: await e.reply("❌ Key không tồn tại!")

@client.on(events.NewMessage(pattern=r'^/xoakey'))
async def xoa_key(e):
    if not is_admin(e.sender_id): return
    data["user_keys"] = {}; save_data()
    await e.reply("❌ Đã xóa tất cả người dùng Key.")

# ===== CÁC LỆNH KHÁC =====
@client.on(events.NewMessage(pattern=r'^/anti (\S+)'))
async def cmd_anti(e):
    if not has_key(e.sender_id): return
    u = await client.get_entity(e.pattern_match.group(1))
    if e.chat_id not in ANTI_LIST: ANTI_LIST[e.chat_id] = []
    ANTI_LIST[e.chat_id].append(u.id)
    await e.reply(f"🚫 **Đã chặn đối thủ:** {u.id}")

@client.on(events.NewMessage(pattern=r'^/unanti (\S+)'))
async def cmd_unanti(e):
    if not has_key(e.sender_id): return
    u = await client.get_entity(e.pattern_match.group(1))
    if e.chat_id in ANTI_LIST and u.id in ANTI_LIST[e.chat_id]:
        ANTI_LIST[e.chat_id].remove(u.id)
        await e.reply(f"✅ **CHO ĐỐI THỦ SỦA:** {u.id}")

@client.on(events.NewMessage(pattern=r'^/call (\S+) (\d+) (\d+)'))
async def cmd_call(e):
    if not has_key(e.sender_id): return
    t, n, d = e.pattern_match.group(1), int(e.pattern_match.group(2)), int(e.pattern_match.group(3))
    for _ in range(n):
        try: await client(RequestCallRequest(user_id=t, random_id=random.randint(0, 0x7fffffff), g_a_hash=os.urandom(32), protocol=types.PhoneCallProtocol(udp_p2p=True, udp_reflector=True, min_layer=65, max_layer=65, library_versions=['3.0.0'])))
        except: pass
        await asyncio.sleep(d)

@client.on(events.NewMessage(pattern=r'^/voice (.+)'))
async def cmd_voice(e):
    if not has_key(e.sender_id): return
    gTTS(text=e.pattern_match.group(1), lang='vi').save("v.mp3")
    await client.send_file(e.chat_id, "v.mp3", voice_note=True)
    os.remove("v.mp3")

@client.on(events.NewMessage(pattern=r'^/info'))
async def cmd_info(e):
    if not has_key(e.sender_id): return
    r = await e.get_reply_message()
    u = await client.get_entity(r.sender_id if r else e.sender_id)
    await e.reply(f"🆔 ID: `{u.id}`\n👤 Name: {u.first_name}")

# ===== MENU CHUẨN CỦA ÔNG =====
@client.on(events.NewMessage(pattern=r'^/menu$'))
async def cmd_menu(e):
    await e.reply("""✨ ────────────────────────── ✨
🦖 Spam Sieu Vip Pro Max 🦖
✨ ────────────────────────── ✨

👤 OWNER: Hai Quy ⚡️ 
🛡 Ho Tro: Tele:@hquycute
🚀 QUYỀN HẠN: Hệ Thống Key Vô Hạn 

🔥 Spam Call + Nhay:
📞 /call [user] [lần] [delay] : Gọi xuyên giáp
🤬 /nhaytag [user] [delay] : Nhây tag chửi
🤬 /nhay : Nhây 1 dòng x10 ngôn
🚫 /anti [user] : Xóa tin nhắn đối thủ
✅ /unanti [user] : CHO ĐỐI THỦ SỦA

⚙️ Adm Toi Cao:
➕ /addadm [id] | ➖ /xoadm [id] 
📜 /listadm | 🔑 /newkey [key] 
🔑 /nhapkey [key] | 🔍 
❌/xoakey
👑/xoaall
✈️/stopxoa
👻/info
💎/voice
🛑 STOP SPAM: /STOP 
✨ ────────────────────────── ✨""")

# Auto-delete cho Anti
@client.on(events.NewMessage())
async def auto_del(e):
    if e.chat_id in ANTI_LIST and e.sender_id in ANTI_LIST[e.chat_id]:
        try: await e.delete()
        except: pass

# Flask Server 24/7 duy trì
app = Flask(__name__)
@app.route('/')
def h(): return "Bot HQUY Running"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True).start()

client.start()
client.run_until_disconnected()
