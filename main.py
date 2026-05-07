import multiprocessing
import time
import json
import random
import os
import threading
import urllib3
from flask import Flask
from zlapi import ZaloAPI, ThreadType, Message, Mention, MultiMsgStyle, MessageStyle
from colorama import Fore, init

# --- WEB SERVER CHO RENDER ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot Live"
def run_flask(): app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_flask).start()

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- THÔNG TIN CỦA ÔNG ---
USER_COOKIE = {
    "__zi": "3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1",
    "__zi-legacy": "3000.SSZejyD6zOgdh2mtnLQWYQN_RAG01ICFj1.1",
    "zlang": "vn",
    "zpw_sek": "yK7vmxBmw10Uq5+2ha+og+zqGgFVejjeyzGZCVJMgJ8iqAXrOG8hFLNsopcy5TopFwNcOvOBGHX6BcEWiYm90hBhdk9D/3/lKYoBluQBTp9E7fl2askrfzlU7a9khXGc"
}
USER_IMEI = "c5f107db-982e-4875-92d6-1352876c8433-4c998e5f5ff75020ed6dad16881af41d"

class ZaloBotFull(ZaloAPI):
    def __init__(self, imei, session_cookies):
        super().__init__('api_key', 'secret_key', imei, session_cookies)
        self.running_processes = {}

    def onMessage(self, mid, author_id, message, message_type, group_id, metadata, thread_id, thread_type):
        if not message: return
        msg = message.lower().strip()

        # LỆNH .MENU
        if msg == ".menu":
            menu_text = (
                "--- ADMIN:HQUY ---\n"
                "📜 DANH SÁCH LỆNH:\n"
                "1️⃣ .menu : Xem tất cả lệnh\n"
                "2️⃣ .on : Bật Nhây @All (Nhóm)\n"
                "3️⃣ .ngon : Bật Treo Ngôn Màu\n"
                "4️⃣ .info : Check ID (Tag để check người khác)\n"
                "5️⃣ .off : Dừng tất cả (SPAM OFF)"
            )
            self.send(Message(text=menu_text), thread_id, thread_type)

        # LỆNH .INFO
        elif msg.startswith(".info"):
            target_id = author_id
            if metadata and "mentions" in metadata:
                try:
                    target_id = json.loads(metadata["mentions"])[0]["uid"]
                except: pass
            
            info_text = f"✨ THÔNG TIN:\n🆔 ID: {target_id}\n👤 Tên: {self.fetchUserInfo(target_id).changedProfiles[target_id].displayName}"
            self.send(Message(text=info_text), thread_id, thread_type)

        # LỆNH .ON
        elif msg == ".on" and thread_type == ThreadType.GROUP:
            if thread_id not in self.running_processes:
                p = multiprocessing.Process(target=self.run_tag_all, args=(thread_id,))
                p.start()
                self.running_processes[thread_id] = p
                self.send(Message(text="Đã bật Nhây @All!"), thread_id, thread_type)

        # LỆNH .NGON
        elif msg == ".ngon":
            if thread_id not in self.running_processes:
                p = multiprocessing.Process(target=self.run_treo_ngon, args=(thread_id,))
                p.start()
                self.running_processes[thread_id] = p
                self.send(Message(text="Đã bật Treo Ngôn Màu!"), thread_id, thread_type)

        # LỆNH .OFF (DỪNG TẤT CẢ)
        elif msg == ".off":
            if thread_id in self.running_processes:
                self.running_processes[thread_id].terminate()
                del self.running_processes[thread_id]
                self.send(Message(text="SPAM OFF"), thread_id, thread_type)

    def run_tag_all(self, id_nhom):
        noi_dung = ["Sủa tiếp đi con chó", "Khóc to lên", "Nhây tí cho vui", "Gà vcl"]
        while True:
            try:
                txt = random.choice(noi_dung) + " @All"
                mention = Mention(uid="-1", length=4, offset=len(txt)-4)
                self.send(Message(text=txt, mention=mention), id_nhom, ThreadType.GROUP)
            except: pass
            time.sleep(2)

    def run_treo_ngon(self, id_nhom):
        colors = ["#db342e", "#f27806", "#f7b503", "#15a85f"]
        while True:
            try:
                color = random.choice(colors)
                style = MultiMsgStyle([MessageStyle(offset=0, length=100, style="color", color=color)])
                self.send(Message(text="🔥 TREO NGÔN MÀU 🔥", style=style), id_nhom, ThreadType.GROUP)
            except: pass
            time.sleep(1.5)

# --- CHẠY BOT ---
if __name__ == "__main__":
    client = ZaloBotFull(USER_IMEI, USER_COOKIE)
    print("ADMIN:HQUY - Bot đang nghe lệnh...")
    client.listen()
