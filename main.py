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
    app.run(host='0.0.0.0', port=10000)

threading.Thread(target=run_flask).start()

# --- CẤU HÌNH HỆ THỐNG ---
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- DỮ LIỆU CỦA HẢI QUÝ ---
USER_COOKIE = {
    "__zi": "3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1",
    "__zi-legacy": "3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1",
    "zlang": "vn",
    "_ga": "GA1.2.655939952.1778083101",
    "_gid": "GA1.2.744731849.1778083101",
    "zpsrc": "",
    "zputm_campaign": "",
    "zputm_medium": "",
    "zputm_source": "",
    "zpw_sek": "yK7vmxBmw10Uq5+2ha+og+zqGgFVejjeyzGZCVJMgJ8iqAXrOG8hFLNsopcy5TopFwNcOvOBGHX6BcEWiYm90hBhdk9D/3/lKYoBluQBTp9E7fl2askrfzlU7a9khXGc"
}
USER_IMEI = "c5f107db-982e-4875-92d6-1352876c8433-4c998e5f5ff75020ed6dad16881af41d"

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
        super().__init__('api_key', 'secret_key', imei, session_cookies)
        self.delay_min = delay_min
        self.delay_max = delay_max if delay_max else delay_min
        self.color_map = {1: "#db342e", 2: "#f27806", 3: "#f7b503", 4: "#15a85f", 5: "#ffffff"}

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

# --- LOGIC DISCORD ---
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
                except: pass
                time.sleep(delay)

# --- MENU VÀ MAIN ---
def menu_zalo():
    cls()
    print(get_banner())
    print("1. Chế độ Treo Ngôn")
    print("2. Chế độ Treo Tag All")
    mode = input("\nChọn (1/2): ")
    
    bot = ZaloBotFull(USER_IMEI, USER_COOKIE, 0)
    groups = bot.fetch_groups_list()
    if not groups:
        print(Fore.RED + "Lỗi: Không lấy được danh sách nhóm!")
        return

    for i, g in enumerate(groups, 1): print(f"{i}. {g['name']} ({g['id']})")
    sel = phan_tich_lua_chon(input("Chọn nhóm: "), len(groups))
    gids = [groups[i-1]['id'] for i in sel]
    
    if mode == '1':
        msg_file = input("File nội dung: ")
        msg_text = "\n".join(doc_file_noi_dung(msg_file))
        delay = float(input("Delay: "))
        colors = phan_tich_lua_chon(input("Màu (1-5): "), 5)
        ttl_choice = input("Bật TTL? (Y/N): ").lower()
        ttl = int(float(input("Giây TTL: "))*1000) if ttl_choice == 'y' else None
        
        m_type, m_src = "text", ""
        choice = input("Ảnh (Y), Video (N), Không (O): ").lower()
        if choice == 'y': m_type, m_src = "image", input("Thư mục ảnh: ")
        elif choice == 'n': m_type, m_src = "video", input("File URL video: ")

        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_treo_ngon, args=(gid, msg_text, colors, m_type, m_src, flag, ttl)).start()
    else:
        msg_file = input("File nhây: ")
        d_min = float(input("Delay Min: "))
        d_max = float(input("Delay Max: "))
        for gid in gids:
            flag = multiprocessing.Value('b', True)
            multiprocessing.Process(target=bot.run_tag_all, args=(gid, msg_file, flag)).start()

def main():
    while True:
        cls()
        print(get_banner())
        print("1. ZALO MULTI-FUNCTION")
        print("2. DISCORD SPAMMER")
        cmd = input("\nLựa chọn: ")
        if cmd == '1': menu_zalo()
        elif cmd == '2': # Thêm logic gọi menu_discord của ông vào đây
            pass
        elif cmd == '0': break

if __name__ == "__main__":
    main()
