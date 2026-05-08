import os, asyncio, random, re
from telethon import TelegramClient, events, errors, functions
from telethon.sessions import StringSession
from flask import Flask
from threading import Thread
from gtts import gTTS

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "REX SYSTEM MAX POWER"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- CONFIG ---
API_ID, API_HASH = 34619338, "0f9eb480f7207cf57060f2f35c0ba137"
BOT_TOKEN = "8628695487:AAGBj8QL8ZWEEoTxMNx6CJ3ZMVKohzI68C4"
OWNER_ID = 7153197678 

bot = TelegramClient('rex_final_boss', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
db = {"keys": ["REX-HQUY"], "auth": [], "admins": [OWNER_ID], "delay": 0.2}
user_sessions = {} 
login_step = {}
spam_running = {} 

# --- KHO ĐẠN MỚI CỦA ÔNG (1 CÂU = 1 DÒNG DÀI) ---
def get_rex_bullets():
    NEW_BULLETS = [
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
        "thằng óc cứt ảo war ae ơi :))", "ôm hận bố cmnr :))",
        "óc cứt múa may quay cuồng để bị cha sỉ vả vào cái mặt cứt mày à :))",
        "ngôn như con cặc thêm cái mặt cặc mày để bố buồn nôn à :))",
        "bố đái vào cái bàn thờ thờ tổ tiên 3 đời con chó ngu ăn cứt :))",
        "thằng em bị bố gõ cho hồn bay phách lạc đi cùng con mẹ mày rồi ak 🤪",
        "thấy bố là mày câm à :))", "bố chưa cho mày chạy mà :))",
        "con chó cố gắng hăng 1 tí được không :))", "mẹ mày trông khá ngon 🤪🤙",
        "nhìn mặt mày cay cay bố lắm rồi ak 🤣", "bố mà tung skill sút mày là tỉ lệ tử vong của mày là 100% =)))",
        "chó home cặc tập đú war kìa ae làng nước ơi =)))", "thằng não tật chỉ biết câm nín nhìn bố sỉ vả 👉😒",
        "alo alo :))", "chọn cách im lặng để bố tha cho mẹ đĩ mày à :))", "sao sao :))",
        "tnh bại kìa :))", "bố lại win à :))", "con chó ngu đú đú ôm hận bố đến cuối đời :))",
        "chó đú ảo war r ak 🤣🤙", "ê ê :))", "trông ngôn mày phèn như quần áo con gái mẹ mày mặc cộng vô đell nổi 50k :))",
        "óc chó bị sỉ vả đang nghĩ cách phục thù bố đoá 😁✌️", "mẹ mày trông nứng ghê vậy :))",
        "mẹ mày làm đĩ từ tuổi 16 bán dâm kiếm tiền cho thằng bại não mày lên đây đú đú kiếm fame từ bố ak 🤣",
        "đĩ ngu cầu xin bố tha mạng à =))", "gào thét trong vô vọng cmnr à :))",
        "bố xuất tinh vào não mẹ đĩ mày cmnr :))", "ơ ơ nổi điên rồi à :))",
        "học cách phản kháng bố để giải cứu con mẹ mày xem =))", "tk óc choá :)))",
        "đừng làm cha chú ý bằng những câu phèn cặc mày lấy trên mạng :))",
        "con đ/ĩ mẹ mày bị tao cầm đinh ba xiên chết tại chỗ thằng bố mày ôm hận tao qua báo thù cho con mẹ nó còn không xong bị tao cầm phóng lợn xiên qua đầu của bố mày máu rơi như tinh trùng bố của mày bắn vào lỗ l/ồ/n mẹ mày🤣🤣❓️",
        "con chó ngu mày thích ăn vạ bố k bố lại đấm cho 1 cái bây giờ :))",
        "anh đâm thủng lỗ lồn gái mẹ mày giờ chứ thích sủa với bố k :))", "chill tí sớ sủng với bố nổi không thằng cặc ei :))",
        "thằng óc cặc lgbt mày đang sủa ai cho mày câm :))", "mày ngưng là con mẹ đĩ nhà m đột tử liền mà :))",
        "thằng bất hiếu thấy mẹ chết không cứu :))", "con chó speed tí được không ấy slow là con mẹ mày đột tử chết ngay trước mặt mày giờ 🥺🙏",
        "bố nhét cặc vào trong lồn mẹ mày xem cái mặt gái mẹ mày làm đĩ trông như nào :))", "đụ con gái mẹ mày trông thế nào nhỉ :))",
        "mày không repply bố là bố phi dao đâm thủng não mẹ m liền nè :))", "mày trông ngôn mày có tí sát thương nào với bố k :))",
        "bố tung 1% sức mạnh là đủ để con mẹ mày chết liền mà :))", "ngăn cản t giết mẹ m đi con chó ngu :))",
        "mẹ đĩ mày sống được 50 tuổi không ấy :))", "con chó ngu mày loạn luân cả với mẹ mày à =))",
        "con chó bất hiếu bà nó u90 rồi mà nó còn k tha :))", "cận cảnh thằng cặc bị bố sỉ vả đến nổi off mxh :))",
        "mày bỏ lại mẹ mày theo dì mày à 🤣", "bố tung skill 1 sút là con mẹ mày chết liền lun 🤪👊",
        "tỉ lệ win war của mày khi đối đầu với bố là 0% :))", "mày nhai ngôn là con ĩ ẹ m chết ngay lập tức 👎",
        "bọn bố bá vcl :))", "thằng ngu home cặc ghẻ định đối đầu với anh à :))",
        "mày thua bố cmnr không phục ak :))", "Chết mẹ đi cho đỡ chật đất em ak :))",
        "mặt lồn mày sủa được câu nào có tí dame được k ấy :))", "m có đủ ảnh hưởng để khiến bố care mày ak 🤣🫵",
        "thằng culi mặt cứt chỉ biết ngồi nghe bố chửi à :))", "bố băm đầu từng con chó nhà mày 😁👎",
        "con chó mặt cứt buông thả r ak :))", "mặt lồn mày sao k 44 theo mẹ m đi :))",
        "bất lực vì bị bố rb r ak :))", "bố chat war cũng đủ để con mẹ mày 44 😛👌",
        "con chó ghen tị vì t có bame à :))", "t chôn xác con gái mẹ m ngay dưới giường m đó 😛👎",
        "bố gõ cho m k còn đường mà siêu sinh 😛🫵", "bố quá mạnh khiến con mẹ m van xin quỳ lạy 3 ngày 3 đêm lun 😒👌",
        "thằng cặc ai cho m đú ngôn =))", "hôm nay thay trời hành đạo nha ae :))",
        "thằng cặc m sủa câu nào có tí dame tí được không ấy :))", "con chó ảo war lên đây ngồi xàm loz cho t đụ vô loz bà già nó hay sao mà nó cứ nhảm nhảm đú gì 🤣🙏",
        "bọn cha lại win à :))", "con ngu t xem m cầu cứu được ai :))",
        "thu đi để lại lá vàng mẹ m đi để lại thằng cặc đú war à 🤣🤣🤣👌", "đcm con chó mồ côi :))",
        "thằng óc cứt mặt cặc m van xin bố mau :))", "sủa điên loạn kìa :))", "moi tay r ak :))",
        "mới đó đã chạy bố cmnr :))", "coi cái con ngu cặc slow vc :))", "slow 1 chút là mẹ m chết :))",
        "ngôn như cứt t 🤪", "con đĩ mẹ m khổ vì m ghê :))", "mẹ m bị bọn a thay nhau đụ từ bắc đến nam mà 😂👊",
        "không chịu được vì bị bố sỉ nhục à 👉🤣", "chó ngu ăn cứt các cha :))", "m làm trò gì vậy :))",
        "con chó phế vật thấy bố mạnh quá là làm thân 😒😒😒😒", "nhìn mặt cứt m mà cũng tập đú ak =)))",
        "a là cha dượng của m đây thằng ngu bú cứt :))", "lêu lêu con chó mếu r kìa 🤣😒🤣",
        "con ngu này đi bộ mơ ước đi xe như tụi a à :))", "ngôn m bao giờ cao siêu được như tụi a 🤪🤪🤪🤪🤪",
        "đẹp trai 2 mái đái vô bàn thờ nhà m 👉🤣", "con chó m sủa liên tục mau lên 🤣🤟",
        "đột tử chết cmm r ak 🤣🤣🤣", "thằng béo mỡ bị t đâm chết tươi 🤣👌",
        "con chó nhà nghèo đú đởn mơ ước với tới bọn anh à 🤣🤟", "con quái thai dị dạng 2 lỗ đít :))",
        "Ăn hại lên phím phản kháng à :))", "Vùng vẫy trước cái chết à :))", "M cay lắm r à :))",
        "Ăn vạ tao à :))", "Bố nói kh nghe à bướng hả con zai :))", "M chĩa mõm về t vì chó sắp ra đi thì mõm nó chĩa về chủ à :))"
    ]
    
    bullets = []
    for _ in range(4500):
        raw_msg = random.choice(NEW_BULLETS)
        # Nối lại thành 1 dòng siêu dài (nhân bản 15 lần để tràn màn hình)
        one_line_msg = " ".join([raw_msg for _ in range(15)]) 
        bullets.append(one_line_msg)
    return bullets

# --- MENU & LỆNH ---
MENU_USER = """✨ ────────────────────────── ✨
👤 OWNER: Hai Quy ⚡️
🚀 QUYỀN HẠN: VIP VÔ HẠN

🔥 **15 LỆNH CHIẾN ĐẤU:**
🤬 /sp - Spam đạn MỚI (1 dòng cực dài)
🤬 /spnd - Spam nội dung tự chọn 1 dòng
🤬 /spicon - Spam icon 1 dòng
📞 /call - Spam Call nạn nhân
⚡ /setdelay - Chỉnh tốc độ (giây)
🚫 /anti - Tự xóa tin đối thủ
✅ /unanti - Ngừng xóa tin đối thủ
👑 /xoaall - Xóa sạch tin nhắn bot
👻 /info - Check ID người dùng
💎 /voice - Chửi bằng Voice gắt
🛑 /stop - DỪNG SPAM (FIX CỨNG)
🔴 /stopxoa - Dừng xóa bot
🚀 /start - Xem Menu
👑 /login - Log acc Tele để spam hộ
✈️ /loguot - Thoát tài khoản
✨ ────────────────────────── ✨
ADMIN:HQUY"""

@bot.on(events.NewMessage)
async def handle(e):
    u, t, cid = e.sender_id, e.text.strip() if e.text else "", e.chat_id
    is_o = (u == OWNER_ID); is_a = (u in db["admins"])
    is_v = (u in db["auth"] or is_o or is_a)

    # LỆNH STOP PHẢI ƯU TIÊN SỐ 1
    if t == '/stop':
        spam_running[cid] = False
        await e.reply("🛑 **SPAM OFF**\nĐã cắt tiết luồng thành công!\nADMIN:HQUY"); return

    if t == '/start': await e.reply(MENU_USER if is_v else "🎫 Nhập key: `/nhapkey <key>`"); return
    
    if (is_o or is_a) and t == '/ad':
        await e.reply("👑 **ADMIN MENU:** /addadm, /newkey, /listkey, /tb"); return

    if not is_v:
        if t.startswith('/nhapkey'):
            k = t.split()[1] if len(t.split()) > 1 else ""
            if k in db["keys"]: db["auth"].append(u); await e.reply("✅ VIP ON!")
        return

    # LOGIN USERBOT
    if t == '/login':
        login_step[u] = {'step': 'phone'}; await e.reply("📱 Nhập SĐT (+84...):"); return
    
    if u in login_step:
        if login_step[u]['step'] == 'phone':
            phone = t.replace(' ',''); cl = TelegramClient(StringSession(), API_ID, API_HASH); await cl.connect()
            try:
                h = await cl.send_code_request(phone)
                login_step[u] = {'step': 'otp', 'client': cl, 'phone': phone, 'hash': h.phone_code_hash}
                await e.reply("📩 Nhập OTP (1.2.3.4.5):")
            except: await e.reply("❌ Lỗi!"); del login_step[u]; return
        elif login_step[u]['step'] == 'otp':
            otp = t.replace('.', ''); cl = login_step[u]['client']
            try:
                await cl.sign_in(login_step[u]['phone'], otp, phone_code_hash=login_step[u]['hash'])
                user_sessions[u] = cl.session.save(); await e.reply("✅ **LOGIN OK!**"); del login_step[u]; return
            except: await e.reply("❌ Sai OTP!"); del login_step[u]; return

    # THỰC THI SPAM
    if t == '/sp':
        if u not in user_sessions: await e.reply("❌ Cần `/login` trước!"); return
        spam_running[cid] = True
        uc = TelegramClient(StringSession(user_sessions[u]), API_ID, API_HASH); await uc.connect()
        await e.reply("🚀 Rex nã đạn MỚI - 1 DÒNG DÀI...")
        for msg in get_rex_bullets():
            if spam_running.get(cid) == False: break
            try: await uc.send_message(cid, msg); await asyncio.sleep(db["delay"])
            except: break

    elif t.startswith('/spnd'):
        spam_running[cid] = True; nd = t.replace('/spnd','').strip() or "Sủa"
        msg = " ".join([nd for _ in range(15)])
        for _ in range(500):
            if spam_running.get(cid) == False: break
            await bot.send_message(cid, msg); await asyncio.sleep(db["delay"])

if __name__ == '__main__':
    bot.run_until_disconnected()
