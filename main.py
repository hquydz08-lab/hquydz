import multiprocessing
import time
import json
import random
import os
import ssl
import base64
import requests
import threading
import urllib3
from flask import Flask
from zlapi import ZaloAPI, ThreadType, Message, Mention, MultiMsgStyle, MessageStyle
from colorama import Fore, Style, init
from pystyle import Colors, Colorate, Write

# --- CẤU HÌNH WEB SERVER ĐỂ TREO RENDER 24/7 ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Zalo & Discord All-In-One đang Live!"

def run_flask():
    # Render yêu cầu port 10000
    app.run(host='0.0.0.0', port=10000)

# Chạy Flask trong một luồng riêng để không chặn code Bot
threading.Thread(target=run_flask).start()

# --- CẤU HÌNH HỆ THỐNG ---
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- THÔNG TIN ĐĂNG NHẬP (HẢI QUÝ ĐIỀN VÀO ĐÂY) ---
# Dán Cookie (dạng dict hoặc chuỗi) vào đây
USER_COOKIE = "DÁN_COOKIE_CỦA_ÔNG_VÀO_ĐÂY"
# IMEI Zalo của ông
USER_IMEI = "DÁN_IMEI_CỦA_ÔNG_VÀO_ĐÂY"
# Mã zpw_sek tôi đã giải mã sạch từ link cho ông
ZPW_SEK = "yK7vmxBmw10Uq5+2ha+og+zqGgFVejjeyzGZCVJMgJ8iqAXrOG8hFLNsopcy5TopFwNcOvOBGHX6BcEWiYm90hBhdk9D/3/lKYoBluQBTp9E7fl2askrfzlU7a9khXGc"

# --- TIỆN ÍCH HIỂN THỊ RAINBOW ---
def get_banner():
    banner = r"""
    ██╗  ██╗ ██████╗  █████╗ ███╗   ██╗ ██████╗ 
    ██║ ██╔╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝ 
    █████╔╝ ██║   ██║███████║██╔██╗ ██║██║  ███╗
    ██╔═██╗ ██║   ██║██╔══██║██║╚██╗██║██║   ██║
    ██║  ██╗╚██████╔╝██║  ██║██║ ╚████║╚██████╔╝
    ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
         ZALO & DISCORD ALL-IN-ONE V11.0 [VIP]
    """
    return Colorate.Horizontal(Colors.rainbow, banner)

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

# (Giữ nguyên các hàm doc_file_noi_dung, get_image_files, phan_tich_lua_chon của ông ở đây)
def doc_file_noi_dung(ten_file):
    try:
        with open(ten_file, "r", encoding="utf-8") as file:
            return [dong.strip() for dong in file if dong.strip()]
    except Exception as e:
        print(Fore.RED + f"Lỗi đọc file {ten_file}: {e}")
        return []

def get_image_files(directory):
    try:
        supported = ('.jpg', '.jpeg', '.png', '.gif')
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(supported)]
    except: return []

def phan_tich_lua_chon(chuoi_nhap, so_luong_toi_da):
    try:
        cac_so = [int(i.strip()) for i in chuoi_nhap.split(',')]
        return [n for n in cac_so if 1 <= n <= so_luong_toi_da]
    except: return []

# --- LỚP BOT ZALO TỔNG HỢP ---
class ZaloBotFull(ZaloAPI):
    def __init__(self, imei, session_cookies, delay_min, delay_max=None):
        # Tự động gán zpw_sek vào cookies
        if isinstance(session_cookies, dict):
            session_cookies['zpw_sek'] = ZPW_SEK
        
        super().__init__('api_key', 'secret_key', imei, session_cookies)
        self.delay_min = delay_min
        self.delay_max = delay_max if delay_max else delay_min
        self.color_map = {1: "#db342e", 2: "#f27806", 3: "#f7b503", 4: "#15a85f", 5: "#ffffff"}

    # (Giữ nguyên logic run_tag_all, run_treo_ngon, fetch_groups_list của ông)
    def run_tag_all(self, id_nhom, file_nguon, co_chay):
        noi_dung_list = doc_file_noi_dung(file_nguon)
        while co_chay.value:
            try:
                tin_nhan = random.choice(noi_dung_list) + " @All"
                self.setTyping(id_nhom, ThreadType.GROUP)
                time.sleep(1)
                mention = Mention(uid="-1", length=4, offset=len(tin_nhan)-4)
                self.send(Message(text=tin_nhan, mention=mention), id_nhom, ThreadType.GROUP)
                print(Fore.GREEN + f"[TAG ALL] Group {id_nhom}: {tin_nhan[:20]}...")
            except Exception as e: print(Fore.RED + f"Lỗi Tag: {e}")
            time.sleep(random.uniform(self.delay_min, self.delay_max))

    def run_treo_ngon(self, id_nhom, msg_text, color_choices, media_type, media_source, co_chay, ttl=None):
        color_idx = 0
        while co_chay.value:
            try:
                self.setTyping(id_nhom, ThreadType.GROUP)
                if media_type == "image":
                    imgs = get_image_files(media_source)
                    if imgs: self.sendLocalImage(random.choice(imgs), id_nhom, ThreadType.GROUP, ttl=ttl)
                elif media_type == "video":
                    vids = doc_file_noi_dung(media_source)
                    if vids: self.sendRemoteVideo(random.choice(vids), "https://files.catbox.moe/bvw84b.jpg", duration="100000", thread_id=id_nhom, thread_type=ThreadType.GROUP, ttl=ttl)
                
                color = self.color_map[color_choices[color_idx % len(color_choices)]]
                style = MultiMsgStyle([
                    MessageStyle(offset=0, length=1000, style="color", color=color),
                    MessageStyle(offset=0, length=1000, style="font", size="40")
                ])
                mention = Mention("-1", length=len(msg_text), offset=0)
                self.send(Message(text=msg_text, mention=mention, style=style), id_nhom, ThreadType.GROUP, ttl=ttl)
                print(Fore.CYAN + f"[TREO NGÔN] Group {id_nhom} | Màu: {color}")
                color_idx += 1
            except Exception as e: print(Fore.RED + f"Lỗi Ngôn: {e}")
            time.sleep(self.delay_min)

    def fetch_groups_list(self):
        try:
            res = self.fetchAllGroups()
            return [{'id': gid, 'name': self.fetchGroupInfo(gid).gridInfoMap[gid]["name"]} for gid in res.gridVerMap.keys()]
        except: return []

# (Giữ nguyên lớp DiscordFullSpammer của ông)
class DiscordFullSpammer:
    def __init__(self, messages, channels, tokens):
        self.messages = messages
        self.channels = channels
        self.tokens = tokens
        self.running = True

    def batch_send(self, token, delay):
        session = requests.Session()
        while self.running:
            for channel in self.channels:
                payload = {"content": random.choice(self.messages), "tts": False, "nonce": str(int(time.time()*1000)), "flags": 0}
                headers = {"Authorization": token, "Content-Type": "application/json"}
                try:
                    res = session.post(f"https://discord.com/api/v10/channels/{channel}/messages", headers=headers, json=payload)
                    if res.status_code == 200:
                        print(Fore.GREEN + f"[DISCORD] SUCCESS | Token: {token[:6]} | Channel: {channel}")
                    elif res.status_code == 429:
                        time.sleep(res.json().get('retry_after', 2))
                except: pass
                time.sleep(delay)

def menu_zalo():
    cls()
    print(get_banner())
    print(Colorate.Horizontal(Colors.rainbow, "1. Chế độ Treo Ngôn (Màu sắc, Media, TTL)"))
    print(Colorate.Horizontal(Colors.rainbow, "2. Chế độ Treo Tag All (@All Nhây Box)"))
    mode = input("\nChọn (1/2): ")
    
    # Sử dụng thông tin cấu hình sẵn ở trên
    cookie_dict = USER_COOKIE if isinstance(USER_COOKIE, dict) else eval(USER_COOKIE)
    bot = ZaloBotFull(USER_IMEI, cookie_dict, 0)
    
    groups = bot.fetch_groups_list()
    if not groups:
        print(Fore.RED + "Không thể lấy danh sách nhóm. Kiểm tra lại Cookie/zpw_sek!")
        return

    for i, g in enumerate(groups, 1): print(f"{i}. {g['name']} ({g['id']})")
    
    sel = phan_tich_lua_chon(input("Chọn nhóm (vd: 1,3): "), len(groups))
    gids = [groups[i-1]['id'] for i in sel]
    
    # ... (Giữ nguyên phần xử lý mode 1/2 của ông)
    if mode == '1':
        msg_file = input("File nội dung spam (.txt): ")
        msg_text = "\n".join(doc_file_noi_dung(msg_file))
        delay = float(input("Delay (giây): "))
        colors = phan_tich_lua_chon(input("Màu (1:Đỏ, 2:Cam, 3:Vàng, 4:Xanh, 5:Trắng): "), 5)
        ttl_choice = input("Bật TTL? (Y/N): ").lower()
        ttl = int(float(input("Giây TTL: "))*1000) if ttl_choice == 'y' else None
        
        media_choice = input("Treo Ảnh (Y), Video (N), hay Không (O): ").lower()
        m_type, m_src = "text", ""
        if media_choice == 'y': m_type, m_src = "image", input("Thư mục ảnh: ")
        elif media_choice == 'n': m_type, m_src = "video", input("File URL video: ")

        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_treo_ngon, args=(gid, msg_text, colors, m_type, m_src, flag, ttl)).start()
    else:
        msg_file = input("File nội dung nhây (.txt): ")
        d_min = float(input("Delay Min: "))
        d_max = float(input("Delay Max: "))
        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_tag_all, args=(gid, msg_file, flag)).start()

# ... (Giữ nguyên hàm menu_discord và main)
def menu_discord():
    cls()
    print(get_banner())
    t_file = input("File Token: ")
    c_id = input("ID Kênh: ")
    m_file = input("File tin nhắn: ")
    delay = float(input("Delay: "))
    
    tokens = doc_file_noi_dung(t_file)
    msgs = doc_file_noi_dung(m_file)
    
    spammer = DiscordFullSpammer(msgs, [c_id], tokens)
    for t in tokens:
        threading.Thread(target=spammer.batch_send, args=(t, delay), daemon=True).start()
    input("\nDiscord đang chạy... Enter để thoát.")

def main():
    while True:
        cls()
        print(get_banner())
        print(Colorate.Horizontal(Colors.rainbow, "1. ZALO MULTI-FUNCTION (V11.0)"))
        print(Colorate.Horizontal(Colors.rainbow, "2. DISCORD SPAMMER (T.PY)"))
        print(Colorate.Horizontal(Colors.rainbow, "0. THOÁT"))
        
        cmd = input("\nLựa chọn: ")
        if cmd == '1': menu_zalo()
        elif cmd == '2': menu_discord()
        elif cmd == '0': break

if __name__ == "__main__":
    main()
