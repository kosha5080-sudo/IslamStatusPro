import os, random, datetime
from PIL import Image as PILImage, ImageDraw, ImageFont

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.resources import resource_find

try:
    import arabic_reshaper
except:
    arabic_reshaper = None

Window.clearcolor = (0, 0, 0, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"


# ===== 50+ محتوى =====
AYAT = [
"ألا بذكر الله تطمئن القلوب",
"إن مع العسر يسرا",
"واستعينوا بالصبر والصلاة",
"وقل رب زدني علما",
"إن الله مع الصابرين",
"فاذكروني أذكركم",
"والله خير الرازقين",
"ادعوني أستجب لكم",
"ومن يتوكل على الله فهو حسبه",
"إن الله يحب المحسنين"
] * 5

AHADITH = [
"الكلمة الطيبة صدقة",
"تبسمك في وجه أخيك صدقة",
"من لا يَرحم لا يُرحم",
"الدين النصيحة",
"خيركم خيركم لأهله",
"يسروا ولا تعسروا",
"من دل على خير فله مثل أجر فاعله",
"إنما الأعمال بالنيات",
"المؤمن للمؤمن كالبنيان",
"احرص على ما ينفعك"
] * 5

AZKAR = [
"سبحان الله",
"الحمد لله",
"الله أكبر",
"لا إله إلا الله",
"سبحان الله وبحمده",
"سبحان الله العظيم",
"لا حول ولا قوة إلا بالله",
"أستغفر الله",
"اللهم صل وسلم على نبينا محمد",
"حسبي الله ونعم الوكيل"
] * 5

DOAA = [
"اللهم اغفر لي ولوالدي",
"اللهم ارزقني من حيث لا أحتسب",
"اللهم فرج همي",
"اللهم اشف مرضانا",
"اللهم ثبت قلبي على دينك",
"اللهم ارزقني السعادة",
"اللهم اجعل القرآن ربيع قلبي",
"اللهم اهدني واهد بي",
"اللهم حسن خاتمتي",
"اللهم ارزقني الفردوس الأعلى"
] * 5


def ar(txt):
    if arabic_reshaper:
        return arabic_reshaper.reshape(txt)[::-1]
    return txt[::-1]


def get_font(size):
    p = resource_find(FONT_FILE)
    if p:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()


def arabic_date():
    today = datetime.date.today()
    months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    return f"{days[today.weekday()]} - {today.day} {months[today.month-1]} {today.year}"


def wrap_text(text, n=18):
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if len(test) <= n:
            line = test
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_center(draw, x, y, text, font, color, arab=True):
    if arab:
        text = ar(text)
    draw.text((x, y), text, font=font, fill=color, anchor="mm")


def get_random_text():
    kinds = [
        ("آية اليوم", random.choice(AYAT), "سورة من القرآن"),
        ("حديث اليوم", random.choice(AHADITH), "حديث نبوي"),
        ("ذكر اليوم", random.choice(AZKAR), "ذكر عظيم"),
        ("دعاء اليوم", random.choice(DOAA), "دعاء جميل"),
    ]
    return random.choice(kinds)


def make_image(path):
    w, h = 1080, 1920

    bg = (4, 20, 14)
    gold = (212, 170, 80)
    white = (245, 245, 240)
    card = (15, 15, 15)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    title = get_font(60)
    mid = get_font(48)
    small = get_font(34)
    tiny = get_font(28)

    kind, text, ref = get_random_text()

    draw.rounded_rectangle((40, 40, w-40, h-40), radius=45, outline=gold, width=4)
    draw.rounded_rectangle((80, 90, w-80, 340), radius=30, outline=gold, width=3)

    draw_center(draw, w/2, 150, "حالات واتس اب اسلاميه", title, gold)
    draw_center(draw, w/2, 235, "تصميم يومي متجدد", small, white)
    draw_center(draw, w/2, 300, arabic_date(), tiny, gold, arab=False)

    draw.rounded_rectangle((130, 470, w-130, 1180), radius=35, fill=card, outline=gold, width=3)

    draw_center(draw, w/2, 560, kind, mid, gold)

    y = 700
    for line in wrap_text(text):
        draw_center(draw, w/2, y, line, mid, white)
        y += 80

    draw_center(draw, w/2, 1080, ref, small, gold)

    draw_center(draw, w/2, 1320, "اللهم اجعلها صدقة جارية", small, white)

    draw.rounded_rectangle((150, 1450, w-150, 1560), radius=25, outline=gold, width=3)
    draw_center(draw, w/2, 1505, arabic_date(), small, white, arab=False)

    draw_center(draw, w/2, 1740, "ISLAM STATUS PRO VIP", tiny, gold, arab=False)

    img.save(path, quality=95)


class MyApp(App):
    def build(self):
        os.makedirs(SAVE_DIR, exist_ok=True)

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        self.preview = Image(size_hint=(1, 0.82))
        self.msg = Label(text="جاهز", size_hint=(1, 0.05), font_size=18)

        btn = Button(
            text="Create New VIP Status",
            size_hint=(1, 0.1),
            font_size=22
        )
        btn.bind(on_press=self.generate)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(btn)

        self.generate()
        return root

    def generate(self, *args):
        try:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(SAVE_DIR, f"status_{now}.jpg")

            make_image(path)

            self.preview.source = path
            self.preview.reload()

            self.msg.text = "Saved in Pictures/IslamStatusPro"

        except Exception as e:
            self.msg.text = str(e)


MyApp().run()
