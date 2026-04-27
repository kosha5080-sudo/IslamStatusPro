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
except Exception:
    arabic_reshaper = None

Window.clearcolor = (0.03, 0.04, 0.03, 1)

APP_NAME = "Islamic WhatsApp Status"
FONT_FILE = "arabic.ttf"

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

def wrap_text(text, max_len=18):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if len(test) <= max_len:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def font(size):
    f = resource_find(FONT_FILE)
    if f and os.path.exists(f):
        return ImageFont.truetype(f, size)
    return ImageFont.load_default()

def greg_date():
    today = datetime.date.today()
    months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    return f"{days[today.weekday()]} - {today.day} {months[today.month-1]} {today.year}"

def make_status(design, save_dir):
    os.makedirs(save_dir, exist_ok=True)

    w, h = 1080, 1920
    if design == 1:
        bg, gold, white = (9,35,22), (212,170,82), (245,245,235)
    elif design == 2:
        bg, gold, white = (238,226,205), (150,105,45), (20,45,30)
    else:
        bg, gold, white = (8,9,10), (225,177,75), (245,245,245)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    font_big = font(92)
    font_mid = font(58)
    font_small = font(38)
    font_tiny = font(30)

    kind, main_text, ref = TEXTS[datetime.date.today().toordinal() % len(TEXTS)]

    draw.rounded_rectangle((55, 80, w-55, h-80), radius=45, outline=gold, width=5)
    draw.rounded_rectangle((95, 670, w-95, 1180), radius=35, fill=(35,35,35) if design != 2 else (250,244,232), outline=gold, width=3)

    draw.text((w/2, 170), ar("التقويم الهجري"), fill=gold, font=font_big, anchor="mm")
    draw.text((w/2, 270), ar("١٤٤٧ هـ"), fill=gold, font=font_mid, anchor="mm")
    draw.text((w/2, 330), ar("حسب تقويم أم القرى"), fill=white, font=font_small, anchor="mm")

    draw.rounded_rectangle((340, 430, 740, 510), radius=35, fill=gold)
    draw.text((w/2, 470), ar(kind), fill=(10,25,15), font=font_small, anchor="mm")

    y = 780
    for line in wrap_text(main_text, 18):
        draw.text((w/2, y), ar(line), fill=white, font=font_mid, anchor="mm")
        y += 90

    draw.text((w/2, 1120), ar(ref), fill=gold, font=font_small, anchor="mm")

    draw.rounded_rectangle((95, 1390, 985, 1570), radius=30, outline=gold, width=3)
    draw.text((w/2, 1445), ar(greg_date()), fill=white, font=font_small, anchor="mm")
    draw.text((w/2, 1515), ar("حالات واتس اب اسلاميه"), fill=gold, font=font_small, anchor="mm")

    draw.text((w/2, 1785), "ISLAM STATUS PRO", fill=gold, font=font_tiny, anchor="mm")

    path = os.path.join(save_dir, f"islam_status_design_{design}.jpg")
    img.save(path, quality=95)
    return path

class AppUI(App):
    def build(self):
        self.save_dir = self.user_data_dir

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.title = Label(text="Islamic WhatsApp Status", font_size=24, size_hint_y=None, height=55)
        self.preview = Image(size_hint_y=1, allow_stretch=True, keep_ratio=True)

        row = BoxLayout(size_hint_y=None, height=65, spacing=8)
        for i in [1, 2, 3]:
            btn = Button(text=f"Design {i}", font_size=18)
            btn.bind(on_press=lambda x, d=i: self.create(d))
            row.add_widget(btn)

        save = Button(text="Create Today Status", font_size=20, size_hint_y=None, height=65)
        save.bind(on_press=lambda x: self.create(random.randint(1, 3)))

        self.msg = Label(text="Ready", font_size=15, size_hint_y=None, height=40)

        root.add_widget(self.title)
        root.add_widget(self.preview)
        root.add_widget(row)
        root.add_widget(save)
        root.add_widget(self.msg)

        self.create(1)
        return root

    def create(self, design):
        try:
            path = make_status(design, self.save_dir)
            self.preview.source = path
            self.preview.reload()
            self.msg.text = "Image created successfully"
        except Exception as e:
            self.msg.text = "Error: " + str(e)

AppUI().run()
