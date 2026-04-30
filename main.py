# =========================
# حالات واتس اب اسلاميه - Store Edition
# =========================

import os
import random
import datetime
import shutil
import json

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

from content import AYAT_AR, AHADITH_AR, AZKAR_AR, DOAA_AR

Window.clearcolor = (0.02, 0.02, 0.02, 1)

SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
SETTINGS_FILE = "settings.json"

FONT_FILE = "arabic.ttf"


# =========================
# أدوات
# =========================

def get_font(size):
    try:
        return ImageFont.truetype(FONT_FILE, size)
    except:
        return ImageFont.load_default()


def date_text():
    today = datetime.date.today()
    return f"{today.day}-{today.month}-{today.year}"


def wrap_text(text, limit=18):
    words = text.split()
    lines = []
    line = ""

    for w in words:
        if len(line + " " + w) <= limit:
            line += " " + w
        else:
            lines.append(line.strip())
            line = w

    if line:
        lines.append(line)

    return lines


def draw_text(draw, x, y, text, font, color):
    draw.text((x, y), text, fill=color, font=font, anchor="mm")


# =========================
# اختيار نص بدون تكرار
# =========================

def get_random(data, last):
    choice = random.choice(data)
    while choice == last:
        choice = random.choice(data)
    return choice


# =========================
# تصميمات
# =========================

def theme(design):
    if design == 1:
        return (0,22,13), (210,170,80), (255,255,255)
    if design == 2:
        return (10,10,10), (230,185,75), (240,240,240)
    return (242,238,228), (145,105,45), (20,20,20)


# =========================
# إنشاء صورة
# =========================

def make_status(path, text, design):

    bg, gold, white = theme(design)

    img = PILImage.new("RGB", (1080, 1920), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(60)
    text_font = get_font(48)

    draw_text(draw, 540, 200, "حالات واتس اب اسلاميه", title_font, gold)

    y = 700
    for line in wrap_text(text):
        draw_text(draw, 540, y, line, text_font, white)
        y += 80

    draw_text(draw, 540, 1600, date_text(), get_font(28), gold)

    img.save(path)


# =========================
# التطبيق
# =========================

class IslamApp(App):

    def build(self):

        self.design = 1
        self.last_text = ""

        self.temp = "preview.jpg"

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.img = Image()

        # النوع
        row_type = BoxLayout(size_hint=(1,0.1))

        self.type = "random"

        for name in ["random","ayah","hadith","dhikr","dua"]:
            btn = Button(text=name)
            btn.bind(on_press=lambda x, n=name: self.set_type(n))
            row_type.add_widget(btn)

        # التصميم
        row_design = BoxLayout(size_hint=(1,0.1))

        for i in [1,2,3]:
            btn = Button(text=f"Design {i}")
            btn.bind(on_press=lambda x, d=i: self.set_design(d))
            row_design.add_widget(btn)

        self.btn_generate = Button(text="Generate")
        self.btn_save = Button(text="Save")

        self.btn_generate.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save)

        root.add_widget(self.img)
        root.add_widget(row_type)
        root.add_widget(row_design)
        root.add_widget(self.btn_generate)
        root.add_widget(self.btn_save)

        self.generate()

        return root

    def set_type(self, t):
        self.type = t
        self.generate()

    def set_design(self, d):
        self.design = d
        self.generate()

    def pick_text(self):

        if self.type == "ayah":
            return get_random(AYAT_AR, self.last_text)
        if self.type == "hadith":
            return get_random(AHADITH_AR, self.last_text)
        if self.type == "dhikr":
            return get_random(AZKAR_AR, self.last_text)
        if self.type == "dua":
            return get_random(DOAA_AR, self.last_text)

        all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
        return get_random(all_data, self.last_text)

    def generate(self, *args):

        text = self.pick_text()
        self.last_text = text

        make_status(self.temp, text, self.design)

        self.img.source = self.temp
        self.img.reload()

    def save(self, *args):

        os.makedirs(SAVE_DIR, exist_ok=True)

        path = os.path.join(
            SAVE_DIR,
            f"status_{int(datetime.datetime.now().timestamp())}.jpg"
        )

        shutil.copy(self.temp, path)


IslamApp().run()
