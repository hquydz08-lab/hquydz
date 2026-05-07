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
current_delay = 1.0

# ===== BỘ NGÔN NHAY TAG (MỖI CÂU 1 DÒNG) =====
NGON_NHAY_TAG = [
    "123 con chó cùng sủa =))",
    "con gái mẹ mày làm đĩ từ lúc sống đến khi chết mà 🤣",
    "con đĩ phàn kháng cha được không ấy",
    "thằng cha mày gánh lúa cho mày đi đú à :))",
    "mẹ đĩ mày dắt mày vô sàn à :))",
    "con điếm bị bố sỉ nhục",
    "không phục à",
    "phản kháng lại những câu sỉ vả của cha xem :))",
    "con chó học cách làm người à 👉🤣",
    "con chó ăn cứt :))",
    "phế phẩm vậy em",
    "con chó mồ côi 🤙",
    "mày ngu vậy sao không off mxh luôn đi 🤣👋",
    "max speed được không ấy con chó ei 👉🤪",
    "lại phải win à 😁",
    "sồn mau không con đĩ mẹ m chết",
    "thằng cặc bất hiếu",
    "mẹ mày bị anh chơi suốt năm suốt tháng mà 😛",
    "sồn để cứu con mẹ mày mau🥺👋",
    "cha win cmnr :))",
    "bố cầm shotgun bắn thủng não con đĩ ngu :))",
    "mặt cứt mày phế phẩm vậy em",
    "con chó đú ửa à 🤪",
    "thằng ngu ei 👉😛",
    "phản kháng bố mau 😒",
    "còn sự sống không ấy thằng nqu ei :))",
    "mxh là cách duy nhất để mày sống ak :))",
    "thua bố không phục ak :))",
    "đĩ lồn ăn cứt trâu để sống qua ngày à 🤣",
    "thằng ngu cố nhai nốt mấy câu để cầu cứu con gái mẹ m nha :))",
    "thằng óc cứt ảo war ae ơi :))",
    "ôm hận bố cmnr :))",
    "óc cứt múa may quay cuồng để bị cha sỉ vả vào cái mặt cứt mày à :))",
    "ngôn như con cặc thêm cái mặt cặc mày để bố buồn nôn à :))",
    "bố đái vào cái bàn thờ thờ tổ tiên 3 đời con chó ngu ăn cứt :))",
    "thằng em bị bố gõ cho hồn bay phách lạc đi cùng con mẹ mày rồi ak 🤪",
    "thấy bố là mày câm à :))",
    "bố chưa cho mày chạy mà :))",
    "con chó cố gắng hăng 1 tí được không :))",
    "mẹ mày trông khá ngon 🤪🤙",
    "nhìn mặt mày cay cay bố lắm rồi ak 🤣",
    "bố mà tung skill sút mày là tỉ lệ tử vong của mày là 100% =)))",
    "chó home cặc tập đú war kìa ae làng nước ơi =)))",
    "thằng não tật chỉ biết câm nín nhìn bố sỉ vả 👉😒",
    "alo alo :))",
    "chọn cách im lặng để bố tha cho mẹ đĩ mày à :))",
    "sao sao :))",
    "tnh bại kìa :))",
    "bố lại win à :))",
    "con chó ngu đú đú ôm hận bố đến cuối đời :))",
    "chó đú ảo war r ak 🤣🤙",
    "ê ê :))",
    "trông ngôn mày phèn như quần áo con gái mẹ mày mặc cộng vô đell nổi 50k :))",
    "óc chó bị sỉ vả đang nghĩ cách phục thù bố đoá 😁✌️",
    "mẹ mày trông nứng ghê vậy :))",
    "mẹ mày làm đĩ từ tuổi 16 bán dâm kiếm tiền cho thằng bại não mày lên đây đú đú kiếm fame từ bố ak 🤣",
    "đĩ ngu cầu xin bố tha mạng à =))",
    "gào thét trong vô vọng cmnr à :))",
    "bố xuất tinh vào não mẹ đĩ mày cmnr :))",
    "ơ ơ nổi điên rồi à :))",
    "học cách phản kháng bố để giải cứu con mẹ mày xem =))",
    "tk óc choá :)))",
    "đừng làm cha chú ý bằng những câu phèn cặc mày lấy trên mạng :))",
    "con đ/ĩ mẹ mày bị tao cầm đinh ba xiên chết tại chỗ thằng bố mày ôm hận tao qua báo thù cho con mẹ nó còn không xong bị tao cầm phóng lợn xiên qua đầu của bố mày máu rơi như tinh trùng bố của mày bắn vào lỗ l/ồ/n mẹ mày🤣🤣❓️",
    "con chó ngu mày thích ăn vạ bố k bố lại đấm cho 1 cái bây giờ :))",
    "anh đâm thủng lỗ lồn gái mẹ mày giờ chứ thích sủa với bố k :))",
    "chill tí sớ sủng với bố nổi không thằng cặc ei :))",
    "thằng óc cặc lgbt mày đang sủa ai cho mày câm :))",
    "mày ngưng là con mẹ đĩ nhà m đột tử liền mà :))",
    "thằng bất hiếu thấy mẹ chết không cứu :))",
    "mày chống cự bố mau không bố lấy noti mày bố đem lên tbg up cho mọi người đều biết thằng mặt cặc đâm cha giết mẹ đang tỏ ra ổn nhưng sâu trong cái mặt cặc nó đang run sợ cha 😛😛😛",
    "con chó speed tí được không ấy slow là con mẹ mày đột tử chết ngay trước mặt mày giờ 🥺🙏",
    "bố nhét cặc vào trong lồn mẹ mày xem cái mặt gái mẹ mày làm đĩ trông như nào :))",
    "đụ con gái mẹ mày trông thế nào nhỉ :))",
    "mày không repply bố là bố phi dao đâm thủng não mẹ m liền nè :))",
    "mày trông ngôn mày có tí sát thương nào với bố k :))",
    "bố tung 1% sức mạnh là đủ để con mẹ mày chết liền mà :))",
    "ngăn cản t giết mẹ m đi con chó ngu :))",
    "mẹ đĩ mày sống được 50 tuổi không ấy :))",
    "con chó ngu mày loạn luân cả với mẹ mày à =))",
    "con chó bất hiếu bà nó u90 rồi mà nó còn k tha :))",
    "cận cảnh thằng cặc bị bố sỉ vả đến nổi off mxh :))",
    "mày bỏ lại mẹ mày theo dì mày à 🤣",
    "bố tung skill 1 sút là con mẹ mày chết liền lun 🤪👊",
    "tỉ lệ win war của mày khi đối đầu với bố là 0% :))",
    "mày nhai ngôn là con ĩ ẹ m chết ngay lập tức 👎",
    "bọn bố bá vcl :))",
    "thằng ngu home cặc ghẻ định đối đầu với anh à :))",
    "mày thua bố cmnr không phục ak :))",
    "Chết mẹ đi cho đỡ chật đất em ak :))",
    "mặt lồn mày sủa được câu nào có tí dame được k ấy :))",
    "m có đủ ảnh hưởng để khiến bố care mày ak 🤣🫵",
    "a mới gõ có vài câu mà con mẹ mày đã k ngồi yên được r à 😛🤟",
    "thằng culi mặt cứt chỉ biết ngồi nghe bố chửi à :))",
    "bố băm đầu từng con chó nhà mày 😁👎",
    "cố làm bố cay à 🤪🤙",
    "con chó mặt cứt buông thả r ak :))",
    "mặt lồn mày sao k 44 theo mẹ m đi :))",
    "bất lực vì bị bố rb r ak :))",
    "bố chat war cũng đủ để con mẹ mày 44 😛👌",
    "con chó ghen tị vì t có bame à :))",
    "thằng đĩ mồ côi lại còn bất hiếu được nhận nuôi cô nhi viện mà lại ăn cháo đá bát đốt nhà à 🤣🫵",
    "ủa rồi mày gạ bố gõ chi để rồi lộ cái mặt cặc béo phì kèm não 1 nửa của m :))",
    "t chôn xác con gái mẹ m ngay dưới giường m đó 😛👎",
    "m speed lên tí được không ấy thấy m slow v sao cứu được bà già m đây :))",
    "bố gõ cho m k còn đường mà siêu sinh 😛🫵",
    "bố quá mạnh khiến con mẹ m van xin quỳ lạy 3 ngày 3 đêm lun 😒👌",
    "con đĩ già m bị t đụ chán chê xong ôm hận mà qua đời mà =))",
    "t hoá đấng tối cao cầm phóng đâm vào loz con gái mẹ m mà =))",
    "thằng cặc ai cho m đú ngôn =))",
    "t tung skill sút 1 phát khiến mu loz mẹ m k còn mà 🥺🙏",
    "con mồ côi m mà rớt t là t lấy noti m lên chà đạp vào loz gái mẹ m bây h đó 🤪👎",
    "hôm nay thay trời hành đạo nha ae :))",
    "bố hoá songoku chưởng 1 cái khiến mẹ m tắc thở ngay lập tức 😂👊",
    "gặp bố mà k chào là bố sút vô đầu chó của mẹ đĩ m liền nè :))",
    "thằng cặc m sủa câu nào có tí dame tí được không ấy :))",
    "con chó ngu rớt rớt bố xong giả điên loạn để bố tha cho bà già nó hay sao 🤪👊",
    "con chó bel phj da đen m thích câm k 🤣🙏",
    "t là phật tổ dơ tay 1 phát là mẹ m chết liền :))",
    "não cún bất lực vì mẹ m bị t giết à :))",
    "m cố phản kháng bố tí :))",
    "bọn cha lại win à :))",
    "thằng não tàn 1 bên não m bị chó tha mất hay sao mà idea m hạn hẹp chỉ có 1% v=)))",
    "m là rác thải sinh học k được xử lí mà trôi dạt sang mxh làm 1 con chó culi tập đú làm trò hề cho bố xem à 😂🤙",
    "con ngu t xem m cầu cứu được ai :))",
    "m đoán xem tỉ lệ win của m khi đối đầu với bố là bao nhiêu % còn bố nghĩ là 0% =)))",
    "m nhìn bố chửi với những ngôn từ thượng đẳng cho lũ hạ cấp m nghe mà chỉ biết ôm hận bố 👊👊👊",
    "thu đi để lại lá vàng mẹ m đi để lại thằng cặc đú war à 🤣🤣🤣👌",
    "m làm màu chi để r bị bố sỉ nhục như lúc con gái mẹ m quỳ lạy van xin t tha cho gia đình m 😛🤙",
    "ae ơi ra coi nó phản kháng vùng vẫy trong vô vọng kìa 🤣🤣",
    "đcm con chó mồ côi :))",
    "thằng óc cứt mặt cặc m van xin bố mau :))",
    "sủa điên loạn kìa :))",
    "trông m non nớt như gái mẹ m 😂👌",
    "mới đó đã chạy bố cmnr :))",
    "chạy là t tung cú sút ngàn cân sút nát đầu chó bà già m liền 🥺🙏",
    "coi cái con ngu cặc slow vc :))",
    "trông t khá cool còn m khá gà :))",
    "slow 1 chút là mẹ m chết :))",
    "t lỡ cho con mẹ m bú cu r sướng vãi cặc 🤣👌",
    "lêu lêu thằng ngu cặc bất lực đứng nhìn t đụ mẹ m mà k làm được gì à đừng có uất hận bố nha 😎🤟",
    "văn thơ anh lai láng đủ để làm mẹ m dạng háng mỗi đêm =)))",
    "qua sống phải bắc cầu kiều con mẹ muốn làm đĩ thì phải chiều các cha 🤣🤣🤣👊👊👊",
    "con ngu này đi đường bị bố úp sọt khóc huhu về méc mẹ 👉🤣",
    "alo alo đừng hận bố mà 44 mà :))",
    "m ngoi lên đây mau để coi t giết cha má m nè 🤟🤟🤟",
    "đĩ mẹ m chết kìa cứu mau đi 🤣🤙",
    "ngôn như cứt t 🤪",
    "con đĩ mẹ m khổ vì m ghê :))",
    "má m bị t đầu độc đến chết 🤣👊",
    "m đàn ông hay đàn bà mà yếu đuối vậy 👉😒",
    "m cầu cứu bạn bè m cho đông đông 1 tí nào 🤣🤟",
    "k có câu nào có tí dame với bọn bố à 👉🤪",
    "thằng nứng cặc đến bà hàng xóm nó gần đất xa trời 90 tuổi nó còn chơi 3 tiếng làm bả gần tắc thở 😒👌",
    "con chó làm trò để làm cha cay à =))",
    "anh bá vcl lỡ đá chết con mẹ m r 😝👋",
    "mẹ m bị bọn a thay nhau đụ từ bắc đến nam mà 😂👊",
    "thằng ngu này bị bố chà đạp bắt ăn cứt phải khen ngon mà hay là món sở trường của nó là ăn cứt vậy ae =))",
    "không chịu được vì bị bố sỉ nhục à 👉🤣",
    "con điếm phò bị cha cầm gậy chọc vô mu lồn mẹ nó nè :))",
    "chó ngu ăn cứt các cha :))",
    "mỗi lần gặp bọn a là trứng dái m còn phải từ biệt m mà :))",
    "con chó mặt cứt m bị cô lập từ ngoài đời lẫn mxh :))",
    "t lấy ô tô đâm thằng vào mu loz con mẹ m thằng chó súc vật 😂🤙",
    "m làm trò gì vậy :))",
    "m có tin là bố chỉ cần 1 nốt nhạc là địt chết con mẹ m k :)))",
    "thằng cha m bị yếu sinh lý hay sao mà con mẹ m mút cặc t như chưa từng được mút 👉🤪",
    "người yêu m còn chấp nhận bỏ m theo t vì t cak to mà 👉😝",
    "cha m hận t lắm chỉ biết đứng nhìn con cặc 30cm của t rã thẳng vô lôz mẹ nó mà 🤪🤟",
    "t ỉa lên bàn thờ nhà m mà mẹ m còn bênh vực t khiến m ôm hận t mãi mà =))",
    "má m mỗi tháng là phải xịt máu lồn cho cha m uống k là cha m bỏ mẹ m theo bà hàng xóm à 🤣",
    "lên mạng tạo nét để bị cha sút vào mu loz r khóc ăn vạ bố à :))",
    "con chó phế vật thấy bố mạnh quá là làm thân 😒😒😒😒",
    "bị bố chửi mà m tăng cả huyết áp khiến bà già m phải bú cu a cầu xin à 😝🫵",
    "mẹ m làm búp bê tình dục cho a thì mỗi đêm a đỡ phải lục đục đi tìm =))",
    "thằng bất hiếu chấp nhận bán rẻ mẹ nó cho t vì t cho nó 20k mua mì tôm :))",
    "nhìn mặt cứt m mà cũng tập đú ak =)))",
    "thằng mặt cặc bị t hạ đo ván sau 1 cút sút ngoạn mục 🤣🤣🤣🤪🤪🤪",
    "óc cứt tập đú để bị bố chửi mếu máo đi ăn vạ khắp nơi:))",
    "mẹ đĩ m bán trinh chỉ để đổi lấy 100k :))",
    "m nhìn t chửi mà chỉ biết câm lặng k nổi 1 lời phản kháng à :))",
    "kính lão đắc thọ còn mẹ m thì xóc lọ cho t :))",
    "a là cha dượng của m đây thằng ngu bú cứt :))",
    "t là phật tổ dơ tay 1 phát là mẹ m chết liền :))",
    "thấy bố mạnh quá con chó phải van xin à :))",
    "lêu lêu con chó mếu r kìa 🤣😒🤣",
    "bị t khủng bố quá nát mẹ hộp sọ 20iq của m r à 😝🤟🤟",
    "thằng đầu đinh ở nhà lá ước mơ duy nhất là ở biệt thự như tụi a 👉😏😏😏",
    "culi bị bố chửi mất xác lìa cổ r kìa 🤣🤣🤣🤣😏😏😏",
    "thằng ngu phải giết cha đụ má để cầu win bố à 🤣👌",
    "giấc mơ làm dân war của nó bị dập tắt sau khi sủa loạn trước mặt t :))",
    "mẹ m phải nằm bò trước cửa nhà t làm con chó để kiếm tí cơm mà 👉😛",
    "ngôn m bao giờ cao siêu được như tụi a 🤪🤪🤪🤪🤪",
    "thằng ngu hồi chiều mới mạnh miệng là dân war đến khi gặp a là tối đến lại chùm trăn khóc huhu =))",
    "mẹ đĩ m bất lực nằm bò khi bị t sỉ vả về cái bản mặt với hoàn cảnh gia đình khó khăn của m mà 🥺🙏",
    "thằng cha m đã vô dụng còn con mẹ m cũng bất tài 🤪🤟",
    "con chó nghiện sex thú đang cố vùng vẫy à 🤪👊👊",
    "con ngu đi bộ mơ ước đi xe như tụi a à :))",
    "hôm nay làm việc thiện quét rác thải mxh nha ae 😏",
    "cả họ hàng m phải xếp hàng lần lượt để được bú dái anh mà 🤪🤪👌",
    "đẹp trai 2 mái đái vô bàn thờ nhà m 👉🤣",
    "thằng cặc bất lực chứng kiến cảnh t cầm bật lửa đốt từng sợi lông loz mẹ nó 👉😏🤙",
    "mẹ m bị t địt rách cả màng trinh mà 🤪🤪",
    "thằng ba nó còn chứng kiến cảnh nó loạn luân với mẹ nó mà 😒🤟",
    "m k còn câu nào có sát thương hả th loz đâm cha đụ má 🤣👊",
    "sao anh vừa đến là m rụng lun z 🤪🤙",
    "cn đĩ óc loz vô gia cư lên mạng phông bạt bị bố bóc trần sự thật ak 🤣🤟",
    "cn culi ai cho m slow v 🤣👌👌",
    "thằng cặc bệnh hoạn giết cha giết mẹ để sĩ đời 😝👊👊",
    "con chó m sủa liên tục mau lên 🤣🤟",
    "tung hết kĩ năng m ra phản kháng bố đê 🤪👌",
    "đột tử chết cmm r ak 🤣🤣🤣",
    "cố gắng phản kháng bố 1 chút để giữ lấy danh dự cho con mẹ m dưới kia đê 😂🙏",
    "hăng hái 1 tí lên bố xem 🤣🤟",
    "m gặp t như gặp cha khép nép cái mõm loz k dám sủa bậy ak 😝👊",
    "thằng béo mỡ bị t đâm chết tươi 🤣👌",
    "cha thánh chửi mà t chửi chết cả nhà m lun 🤪👊👊",
    "thời gian trôi qua để m cảm nhận nỗi đau mồ côi à =))",
    "trong cơn phê đá m cầm dao giết mẹ m à =))",
    "thằng ngu thèm cứt bố lắm à 🤣👊",
    "con chó nhà nghèo đú đởn mơ ước với tới bọn anh à 🤣🤟",
    "ngôn từ m hạ đẳng v sao mà gây dame với bố đây :))",
    "con quái thai dị dạng 2 lỗ đít :))",
    "lỗ loz mẹ m t chui đầu vô còn vừa nữa mà 🤪👊👊👊",
    "Ngu hết phần thiên hạ ngu chuyện lạ dân gian ngu vượt ngàn con chó à :))",
    "anh gõ cho m thân tàn ma dại a đụ vô cái đầu chó m xuất tinh liên tục vào lỗ loz mẹ m khiến mẹ đĩ m luôn ghi nhớ khuôn mặt của bố mà 🤣👌",
    "m lên đây xàm loz với tụi a thì cũng có khiến mẹ đĩ m sống dậy được k zay tk loz 🤪👊👊",
    "thằng bê đê bất lực vì mẹ nó bị đụ tung cái lồn:)))",
    "quá khứ m đen tối thì tương lai m cũng vậy vì m đối đầu với cha m =))",
    "con choá hăng mau lên =))",
    "bố cho m hăng mà 😎👎",
    "slow 1 tí là con mẹ m bị t bóp cổ chết nghẹn bây giờ 👉🤣🤣",
    "thằng mặt loz hãm cak bạn bè ai cũng xa lánh chỉ sợ bị chửi vạ lây 👉🤪",
    "bị anh mày sỉ vả mà chỉ biết câm lặng tỏ ra mình ngôn nhưng sâu trong tâm trí là nước mắt biển rộng 👉🤪",
    "mặt loz m sống như cak qua cầu rút ván y chang con đĩ mẹ m bú cu xong là tự mặt k nhận cha dượng cho m ak 🤣🤣👎👎",
    "lương cha già m ba cọc ba đồng để cho m lên đây đú đởn với cha ak 👉🤣",
    "Cầm cái bản sớ ngon từ thời thằng cha con đĩ meh mày về mà dắt đầu chăn cỏ cho thằngđĩ ms àmy thêm cái nỏii lòng tâm can coi thử ổng có cầm cái điếu cày điếu đổ ổng phang vo đầu mày cái bốp hôn con đỉ má th lang thang ngoau đường kiềm tiền mưu sinh co mặt lol mày ở đây kiếm chiện một hồi là tao báo chánh quyền xuông tống cố thằng cha con đĩ meh mày liền nè thằng bê đê xe cán 🖕🏻😓😓😓",
    "Súc sinh k trình mà đòi bem anh hả th đú🤣👎👎👎👎",
    "thằng bê đê bất lực vì mẹ nó bị đụ tung cái lồn🤣🤣👎",
    "con đĩ mẹ mày bất lực vì bị tao chửi mà chỉ biết câm lặng 😂😂🤙🤙🤙",
    "làm màu mà bị tao chửi rung cái con cặc 👉🤪",
    "thằng bê đê ảo cặc đòi cân và cái kết=)))",
    "con đĩ mẹ của mày thèm cứt tao dữ lắm 👉😂😂",
    "chậm vậy sao cứu được con đĩ mẹ mày nhanh lên đi chứ 👉🤪🤪",
    "ai cho mày sủa tao cho mày sủa chưa 🤣🤣👎👎",
    "mày mà ngưng một giây là con đĩ mẹ mày bả tắt đường thở á =)))",
    "mẹ đĩ của m dắt m vào sàn à=)))",
    "mẹ mày bú cặc t để m được vào sàn mà 😂😂🤟🤟🤟",
    "đập đá hít cần sa nhiều xong sủa bậy à👉👉🤣🤣",
    "mẹ mày bị tao dã vào lồn=)))",
    "địt mẹ mày sướng tê con cặc=)))",
    "mẹ mày bị tao địt rên ư ử=)))",
    "tao địt mẹ mày nát lồn mà=)))",
    "mẹ mày bị tao cưỡng hiếp=)))",
    "sao mày lề mề dị con 🥺🙏🙏",
    "ko cảm hứng để hăng à 🤣🤟",
    "nghèo k có nghi lực à =)))",
    "m thèm cứt t mà 😏🫵",
    "chối t giết cha má m nè:)))",
    "k lên t tuyệt chủng m nhen cn thú=)))",
    "mày ngưng là con đĩ mẹ mày chết?",
    "Cha mày đụ chó sinh ra mày đk dog :))",
    "bị tao chọc cay hơn con chó luôn=)))",
    "Mẹ Mày bị t địt sập cầu sập cống",
    "Súc sinh k trình mà đòi bem anh hả th đú:))))",
    "Cay cú anh trong lòng mà không làm đc gì😒🫵",
    "Cái con không có địa vị bằng 1 cn súc vật nữa😝👌",
    "Mày bị cha hành cho cay cú mà",
    "Gõ sồn máu lồn mày lên=)))",
    "Lgbt bày binh bố trận dồn cha hả 🤣🤙🤙",
    "Cha mày bón cứt dô mõm m nè:)))",
    "Cha mày bón cứt dô mõm m nè=)))",
    "Bị cha mày đọa đày xuống diêm la địa phủ🤪👎👎",
    "Để đầu thai chuyển kiếp thành súc vật🤪🤙🤙",
    "Cay quá nên uống nc đái chó cho đỡ cay đi em =))",
    "Bị cha cho tha hóa thành cchó ngu dốt👉🤪",
    "Mày bần hèn vậy à thằng óc cứt=)))",
    "Tk não vô sinh ngu ngục quỳ lạy bố đê Kiếm ngôn nào sát thương tí dc k =)))",
    "Tk não vô sinh ngu ngục quỳ lạy bố đê kkk 👉😏🫵",
    "sợ bố mà xạo lồn à con =)))",
    "nổ trứng dái chưa em :)))",
    "M có ổn k đó :))",
    "Tổ cha m con nghiệt súc :)))",
    "Ăn hại lên phím phản kháng à :))",
    "Vùng vẫy trước cái chết à :))",
    "Nổi kh đó tk ngu :))",
    "T thấy m hơi bất ổn r đấy :))",
    "Chọc tí đã cay r ak :))",
    "Nóng tính thế đã xiên cha mẹ phát nào chưa :))",
    "Lô lô cái tk ngu học :))",
    "Lương 3 cọc lên mạng sĩ gì v em :))",
    "Bật đt lên là thấy m tru tréo y như là con cầy :))",
    "Nhảm nhảm t đá vào họng m nhen :))",
    "Phảng kháng gì yếu vậy tk ăn hại :))",
    "M làm được việc k thế :))",
    "M cay lắm r à :))",
    "Cay r mày làm gì được t không :))",
    "Ăn vạ tao à :))",
    "Mxh rách còn thua thì m định làm ăn gì cho đời :))",
    "Chết mẹ đi cho đỡ chật đất em ak :))",
    "Bất lực lắm r à tk ku :))",
    "Kệ con mẹ m bố cứ dập ấy :))",
    "T dập m như t dập mẹ m tối qua mà :))",
    "T chọc có tí sao nổ dái r thế :))",
    "Có phải họ gọi tao là bố mày nên mày suốt ngày tìm đến tao :))",
    "Bố nói kh nghe à bướng hả con zai :))",
    "Tk mất dạy chửi bố nó kìa ae :))",
    "Trình quèn thể hiện văn thơ à :))",
    "Văn thì cũ vần thì ngu m định cầm đến để tấu hài à :))",
    "Vl khỉ thành tinh à :))",
    "123 lalala 456 địt cha nhà m :))",
    "Con chó con mèo con ghẹ nhưng tao chỉ thích con mẹ m thôi :))",
    "Cái đù mẹ tk ngu tung skill gì đây :))",
    "T đạp cho mấy phát hết mẹ skill bh :))",
    "Ngày anh sinh ra là ngày mày có thêm 1 người bố à :))",
    "Cố làm anh cay à :))",
    "Anh không cay là con mẹ m nằm trên đường ray nhen :))",
    "Anh chửi bừa mấy câu bằng mẹ nó kiến thức cả đời m rồi à :))",
    "Không phản bác được à :))",
    "Không sủa nổi cút ra chỗ khác chơi :))",
    "M chĩa mõm về t vì chó sắp ra đi thì mõm nó chĩa về chủ à :))",
    "Bọn trộm chó nhìn mặt m còn khinh :))",
    "Phế vật sủa không nổi à :))",
    "Câm lặng rồi à :))",
    "Câm bố vẫn chửi đấy :))",
    "Làm cc gì dc bố kh ấy :))",
    "Coi tk ngu cay t kìa ae :))",
    "nay làm việc thiện dọn rác nhé :))",
    "ngoan nằm im anh quét đi nào :))",
    "nhai luôn cũng dc nhé :))",
    "nhà anh nuôi mỗi m thôi nhai cho hết đi đừng để lại :))",
    "thua không phục à :))",
    "cáu anh lắm à :))",
    "tức anh lắm à :))",
    "kệ con mẹ m chứ :))",
    "siêu sinh về với vùng cực lạc chứ :)))"
]

# ===== QUẢN LÝ ADMIN =====
def load_admins():
    if not os.path.exists("admins.json"):
        with open("admins.json", "w") as f: json.dump([7153197678], f)
        return [7153197678]
    try:
        with open("admins.json", "r") as f: 
            data = json.load(f)
            if BOSS_ID not in data: data.append(7153197678)
            return data
    except: return [7153197678  ]

def save_admins(data):
    with open("admins.json", "w") as f: json.dump(data, f, indent=4)

sub_admins = load_admins()
def is_admin(uid): return uid in sub_admins or uid == BOSS_ID

# ================= LỆNH QUẢN TRỊ =================
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
    if target == BOSS_ID: return await e.reply("❌ Boss bất tử!")
    if target in sub_admins:
        sub_admins.remove(target)
        save_admins(sub_admins)
        await e.reply(f"🗑 Đã xóa Admin: `{target}`")

@client.on(events.NewMessage(pattern=r'^/info\s+(.+)'))
async def get_info(e):
    if not is_admin(e.sender_id): return
    target = e.pattern_match.group(1)
    try:
        user = await client.get_entity(target)
        await e.reply(f"👤 User: {target}\n🆔 ID: `{user.id}`")
    except: await e.reply("❌ Không thấy!")

# ================= ANTI & DELAY =================
anti_list = set()
@client.on(events.NewMessage(pattern=r'^/anti\s+(.+)'))
async def anti_on(e):
    if not is_admin(e.sender_id): return
    try:
        u = await client.get_entity(e.pattern_match.group(1))
        anti_list.add(u.id); await e.reply(f"💀 Đã Anti: `{u.id}`")
    except: await e.reply("❌ Lỗi")

@client.on(events.NewMessage(pattern=r'^/unanti\s+(.+)'))
async def anti_off(e):
    if not is_admin(e.sender_id): return
    try:
        u = await client.get_entity(e.pattern_match.group(1))
        anti_list.discard(u.id); await e.reply(f"😇 Đã Unanti: `{u.id}`")
    except: await e.reply("❌ Lỗi")

@client.on(events.NewMessage(pattern=r'^/setdelay (\d+(\.\d+)?)$'))
async def set_delay(e):
    if not is_admin(e.sender_id): return
    global current_delay
    val = float(e.pattern_match.group(1))
    if 0.001 <= val <= 3.0:
        current_delay = val
        await e.reply(f"✅ Delay: `{current_delay}`s")

# ================= SPAM LOGIC =================
nhay_tasks, tag_tasks, delete_tasks = {}, {}, {}

@client.on(events.NewMessage(pattern=r'^/menu$'))
async def menu(e):
    if not is_admin(e.sender_id): return
    help_text = f"""⚡ **VIP USERBOT - HQUY** ⚡
---
💬 **SPAM ({current_delay}s):**
• `/nhay` | `/nhaytag [tag]` | `/stop`
• `/setdelay [số]` (0.001-3.0)

🛡 **ANTI:**
• `/anti [tag/id]` | `/unanti [tag/id]`

👤 **ADMIN:**
• `/info [tag]` | `/addadm` | `/xoaadm`
---
🆔 My ID: `7153197678`"""
    await e.reply(help_text)

@client.on(events.NewMessage(pattern=r'^/nhaytag (.+)'))
async def nhaytag(e):
    if not is_admin(e.sender_id): return
    cid = e.chat_id; users_in = e.text.split()[1:]; tag_tasks[cid] = True
    users = []
    for u in users_in:
        try: users.append(await client.get_entity(u))
        except: pass
    await e.reply(f"🔥 Tag ON | {current_delay}s")
    while tag_tasks.get(cid):
        # Tạo chuỗi tag ẩn cho tất cả đối tượng
        mentions = "".join([f"<a href='tg://user?id={u.id}'>‎</a> " for u in users])
        # Lấy ngẫu nhiên 1 câu trong bộ ngôn
        msg = random.choice(NGON_NHAY_TAG)
        await client.send_message(cid, f"{mentions}\n{msg}", parse_mode="html")
        await asyncio.sleep(current_delay)

@client.on(events.NewMessage(pattern=r'^/stop$'))
async def stop_all(e):
    if not is_admin(e.sender_id): return
    tag_tasks[e.chat_id] = False
    await e.reply("🛑 SPAM OFF")

@client.on(events.NewMessage(incoming=True))
async def handler(e):
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
