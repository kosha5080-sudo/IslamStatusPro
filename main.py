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

Window.clearcolor = (0.03, 0.04, 0.03, 1)
FONT_FILE = "arabic.ttf"

TEXTS = [
    ("آية اليوم", "واذكروا الله كثيرا لعلكم تفلحون"),
    ("حديث اليوم", "من دل على خير فله مثل أجر فاعله"),
    ("دعاء اليوم", "اللهم إني أسألك الهدى والتقى والعفاف والغنى"),
    ("ذكر اليوم", "سبحان الله وبحمده سبحان الله العظيم"),
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

def make_image(path):
    w, h = 1080, 1920
    img = PILImage.new("RGB", (w, h), (12, 28, 18))
    draw = ImageDraw.Draw(img)

    gold = (212,170,82)
    white = (245,245,235)

    big = get_font(70)
    mid = get_font(45)
    small = get_font(34)

    kind, text = random.choice(TEXTS)

    draw.rounded_rectangle((40,40,w-40,h-40), radius=40, outline=gold, width=5)

    draw.text((w/2,150), ar("حالات واتس اب اسلاميه"), fill=gold, font=big, anchor="mm")

    draw.rounded_rectangle((120,500,w-120,1200), radius=35, fill=(25,25,25), outline=gold, width=3)

    draw.text((w/2,600), ar(kind), fill=gold, font=mid, anchor="mm")
    draw.text((w/2,850), ar(text), fill=white, font=mid, anchor="mm")

    today = datetime.date.today().strftime("%d / %m / %Y")
    draw.text((w/2,1500), today, fill=white, font=small, anchor="mm")

    draw.text((w/2,1780), "ISLAM STATUS PRO", fill=gold, font=small, anchor="mm")

    img.save(path, quality=95)

class MyApp(App):
    def build(self):
        self.save_dir = "/storage/emulated/0/Pictures"
        os.makedirs(self.save_dir, exist_ok=True)

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.preview = Image(size_hint=(1,0.8), allow_stretch=True)
        self.msg = Label(text="Ready", size_hint=(1,0.08))

        btn = Button(text="Create New Status", size_hint=(1,0.12))
        btn.bind(on_press=self.generate)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(btn)

        self.generate()
        return root

    def generate(self, *args):
        try:
            path = os.path.join(self.save_dir, "islam_status.jpg")
            make_image(path)
            self.preview.source = path
            self.preview.reload()
            self.msg.text = "Saved in Pictures/islam_status.jpg"
        except Exception as e:
            self.msg.text = str(e)

MyApp().run()
