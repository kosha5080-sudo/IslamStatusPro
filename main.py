import os, random, datetime, math
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

Window.clearcolor = (0.02, 0.025, 0.02, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"

TEXTS = [
    ("آية اليوم", "واذكروا الله كثيرا لعلكم تفلحون", "سورة الأنفال"),
    ("آية اليوم", "إن مع العسر يسرا", "سورة الشرح"),
    ("آية اليوم", "ألا بذكر الله تطمئن القلوب", "سورة الرعد"),
    ("حديث اليوم", "من دل على خير فله مثل أجر فاعله", "رواه مسلم"),
    ("حديث اليوم", "الكلمة الطيبة صدقة", "متفق عليه"),
    ("دعاء اليوم", "اللهم إني أسألك الهدى والتقى والعفاف والغنى", "دعاء نبوي"),
    ("دعاء اليوم", "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار", "دعاء قرآني"),
    ("ذكر اليوم", "سبحان الله وبحمده سبحان الله العظيم", "ذكر عظيم"),
    ("ذكر اليوم", "لا إله إلا الله وحده لا شريك له", "ذكر اليوم"),
]

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

def wrap_words(text, max_len=18):
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

def arabic_date():
    today = datetime.date.today()
    months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    return f"{days[today.weekday()]} - {today.day} {months[today.month-1]} {today.year}"

def draw_center(draw, xy, text, font, fill):
    draw.text(xy, ar(text), font=font, fill=fill, anchor="mm")

def make_image(path, design=1):
    w, h = 1080, 1920

    if design == 1:
        bg = (8, 32, 20)
        card = (24, 26, 24)
        gold = (215, 174, 88)
        white = (245, 245, 235)
    elif design == 2:
        bg = (238, 227, 206)
        card = (252, 246, 232)
        gold = (150, 105, 45)
        white = (25, 55, 35)
    else:
        bg = (5, 6, 7)
        card = (18, 18, 18)
        gold = (225, 178, 70)
        white = (245, 245, 245)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    big = get_font(78)
    title_font = get_font(64)
    mid = get_font(50)
    small = get_font(36)
    tiny = get_font(30)

    kind, text, ref = random.choice(TEXTS)

    draw.rounded_rectangle((45, 45, w-45, h-45), radius=45, outline=gold, width=5)
    draw.rounded_rectangle((80, 95, w-80, 380), radius=38, outline=gold, width=3)

    draw_center(draw, (w/2, 175), "حالات واتس اب اسلاميه", title_font, gold)
    draw_center(draw, (w/2, 260), "تصميم يومي متجدد", small, white)
    draw_center(draw, (w/2, 325), arabic_date(), tiny, gold)

    draw.rounded_rectangle((135, 520, w-135, 1180), radius=40, fill=card, outline=gold, width=3)
    draw_center(draw, (w/2, 615), kind, mid, gold)

    y = 790
    for line in wrap_words(text, 18):
        draw_center(draw, (w/2, y), line, mid, white)
        y += 95

    draw_center(draw, (w/2, 1105), ref, small, gold)

    draw.line((260, 1300, 820, 1300), fill=gold, width=3)
    draw_center(draw, (w/2, 1390), "اللهم اجعلها صدقة جارية", small, white)

    draw.rounded_rectangle((150, 1500, w-150, 1625), radius=30, outline=gold, width=3)
    draw_center(draw, (w/2, 1562), arabic_date(), small, white)

    draw_center(draw, (w/2, 1775), "ISLAM STATUS PRO VIP", tiny, gold)

    img.save(path, quality=95)

class MyApp(App):
    def build(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.design = 1
        self.last_path = ""

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        self.preview = Image(size_hint=(1, 0.78), allow_stretch=True, keep_ratio=True)
        self.msg = Label(text="VIP Ready", size_hint=(1, 0.06), font_size=18)

        row = BoxLayout(size_hint=(1, 0.08), spacing=6)

        for i in [1, 2, 3]:
            b = Button(text=f"Design {i}", font_size=16)
            b.bind(on_press=lambda x, d=i: self.generate_design(d))
            row.add_widget(b)

        btn_new = Button(text="Create New VIP Status", size_hint=(1, 0.08), font_size=20)
        btn_new.bind(on_press=self.generate_random)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(row)
        root.add_widget(btn_new)

        self.generate_design(1)
        return root

    def make_path(self, design):
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(SAVE_DIR, f"islam_status_vip_{design}_{now}.jpg")

    def generate_design(self, design):
        try:
            self.design = design
            path = self.make_path(design)
            make_image(path, design)
            self.last_path = path
            self.preview.source = path
            self.preview.reload()
            self.msg.text = f"Saved Design {design} in Pictures/IslamStatusPro"
        except Exception as e:
            self.msg.text = "Error: " + str(e)

    def generate_random(self, *args):
        self.generate_design(random.choice([1, 2, 3]))

MyApp().run()
