import os, random, datetime
from PIL import Image as PILImage, ImageDraw, ImageFont

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window

try:
    import arabic_reshaper
except Exception:
    arabic_reshaper = None

Window.clearcolor = (0.03, 0.04, 0.03, 1)

APP_NAME = "حالات واتس اب اسلاميه"
FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"

TEXTS = [
    ("آية اليوم", "وَاذْكُرُوا اللَّهَ كَثِيرًا لَعَلَّكُمْ تُفْلِحُونَ", "سورة الأنفال - الآية 45"),
    ("حديث اليوم", "مَنْ دَلَّ عَلَى خَيْرٍ فَلَهُ مِثْلُ أَجْرِ فَاعِلِهِ", "رواه مسلم"),
    ("دعاء اليوم", "اللهم إني أسألك الهدى والتقى والعفاف والغنى", "دعاء نبوي"),
    ("ذكر اليوم", "سُبْحَانَ اللَّهِ وَبِحَمْدِهِ، سُبْحَانَ اللَّهِ الْعَظِيمِ", "ذكر عظيم"),
]

def ar(text):
    if arabic_reshaper:
        return arabic_reshaper.reshape(text)[::-1]
    return text[::-1]

def greg_date():
    today = datetime.date.today()
    months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    return f"{days[today.weekday()]} - {today.day} {months[today.month-1]} {today.year}"

def make_status(design=1):
    os.makedirs(SAVE_DIR, exist_ok=True)

    w, h = 1080, 1920
    if design == 1:
        bg = (9, 35, 22)
        gold = (212, 170, 82)
        white = (245, 245, 235)
    elif design == 2:
        bg = (238, 226, 205)
        gold = (150, 105, 45)
        white = (20, 45, 30)
    else:
        bg = (8, 9, 10)
        gold = (225, 177, 75)
        white = (245, 245, 245)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype(FONT_FILE, 92)
    font_mid = ImageFont.truetype(FONT_FILE, 58)
    font_small = ImageFont.truetype(FONT_FILE, 38)
    font_tiny = ImageFont.truetype(FONT_FILE, 30)

    kind, main_text, ref = TEXTS[datetime.date.today().toordinal() % len(TEXTS)]

    # frame
    draw.rounded_rectangle((55, 80, w-55, h-80), radius=45, outline=gold, width=5)
    draw.rounded_rectangle((95, 670, w-95, 1180), radius=35, fill=(35, 35, 35) if design != 2 else (250, 244, 232), outline=gold, width=3)

    # header
    draw.text((w/2, 170), ar("التقويم الهجري"), fill=gold, font=font_big, anchor="mm")
    draw.text((w/2, 270), ar("١٤٤٧ هـ"), fill=gold, font=font_mid, anchor="mm")
    draw.text((w/2, 330), ar("حسب تقويم أم القرى"), fill=white, font=font_small, anchor="mm")

    # badge
    draw.rounded_rectangle((360, 430, 720, 505), radius=35, fill=gold)
    draw.text((w/2, 468), ar(kind), fill=(10, 25, 15), font=font_small, anchor="mm")

    # text
    y = 780
    for line in wrap_ar(main_text, 18):
        draw.text((w/2, y), ar(line), fill=white, font=font_mid, anchor="mm")
        y += 85

    draw.text((w/2, 1120), ar(ref), fill=gold, font=font_small, anchor="mm")

    # date boxes
    draw.rounded_rectangle((95, 1390, 985, 1570), radius=30, outline=gold, width=3)
    draw.text((w/2, 1445), ar(greg_date()), fill=white, font=font_small, anchor="mm")
    draw.text((w/2, 1515), ar("حالات واتس اب اسلاميه"), fill=gold, font=font_small, anchor="mm")

    draw.text((w/2, 1785), "ISLAM STATUS PRO", fill=gold, font=font_tiny, anchor="mm")

    path = os.path.join(SAVE_DIR, f"islam_status_{design}.jpg")
    img.save(path, quality=95)
    return path

def wrap_ar(text, max_len):
    words = text.split()
    lines, line = [], ""
    for word in words:
        if len(line + " " + word) <= max_len:
            line += " " + word
        else:
            lines.append(line.strip())
            line = word
    if line:
        lines.append(line.strip())
    return lines

class AppUI(App):
    def build(self):
        self.current = None

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title = Label(text="Islamic WhatsApp Status", font_size=24, size_hint_y=None, height=55)
        self.preview = Image(size_hint_y=1)

        row = BoxLayout(size_hint_y=None, height=65, spacing=8)
        for i in [1, 2, 3]:
            btn = Button(text=f"Design {i}", font_size=18)
            btn.bind(on_press=lambda x, d=i: self.create(d))
            row.add_widget(btn)

        save = Button(text="Create & Save Today Status", font_size=20, size_hint_y=None, height=65)
        save.bind(on_press=lambda x: self.create(random.randint(1, 3)))

        self.msg = Label(text="Saved image will be in Pictures/IslamStatusPro", font_size=15, size_hint_y=None, height=40)

        root.add_widget(self.title)
        root.add_widget(self.preview)
        root.add_widget(row)
        root.add_widget(save)
        root.add_widget(self.msg)

        self.create(1)
        return root

    def create(self, design):
        try:
            path = make_status(design)
            self.preview.source = path
            self.preview.reload()
            self.msg.text = "Saved: Pictures/IslamStatusPro"
        except Exception as e:
            self.msg.text = str(e)

AppUI().run()
