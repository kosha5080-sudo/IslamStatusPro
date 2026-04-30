# =========================
# حالات واتس اب اسلاميه PRO MAX
# =========================

import os
import random
import datetime
import shutil
import json

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

from content import AYAT_AR, AHADITH_AR, AZKAR_AR, DOAA_AR

try:
    import arabic_reshaper
except:
    arabic_reshaper = None


# =========================
# إعدادات
# =========================

Window.clearcolor = (0.02, 0.02, 0.02, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
SETTINGS_FILE = "settings.json"

FONT_PATH = resource_find(FONT_FILE) or FONT_FILE

try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
    UI_FONT = "ArabicFont"
except:
    UI_FONT = None


# =========================
# أدوات
# =========================

def ar(text):
    if arabic_reshaper:
        try:
            return arabic_reshaper.reshape(text)[::-1]
        except:
            return text[::-1]
    return text[::-1]


def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def date_text():
    today = datetime.date.today()
    months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
    days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
    return f"{ar(days[today.weekday()])} - {today.day} {ar(months[today.month-1])} {today.year}"


def wrap_text(text, limit=18):
    words = text.split()
    lines = []
    line = ""

    for w in words:
        test = (line + " " + w).strip()
        if len(test) <= limit:
            line = test
        else:
            lines.append(line)
            line = w

    if line:
        lines.append(line)

    return lines


def draw_text(draw, x, y, text, font, color):
    draw.text((x, y), ar(text), fill=color, font=font, anchor="mm")


# =========================
# التصميمات
# =========================

def theme_colors(design):
    if design == 1:
        return (0,22,13), (210,170,80), (245,245,245)
    elif design == 2:
        return (5,5,5), (230,185,75), (240,240,240)
    else:
        return (242,238,228), (145,105,45), (30,30,30)


# =========================
# إنشاء الصورة
# =========================

def make_status(path, design=1):

    w, h = 1080, 1920
    bg, gold, white = theme_colors(design)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(60)
    text_font = get_font(48)
    small_font = get_font(30)

    all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
    text = random.choice(all_data)

    draw_text(draw, 540, 200, "حالات واتس اب اسلاميه", title_font, gold)
    draw_text(draw, 540, 300, date_text(), small_font, white)

    y = 700
    for line in wrap_text(text):
        draw_text(draw, 540, y, line, text_font, white)
        y += 80

    img.save(path)


# =========================
# التطبيق
# =========================

class IslamApp(App):

    def build(self):

        self.design = 1
        self.temp_path = "preview.jpg"

        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.img = Image()

        row = BoxLayout(size_hint=(1,0.1))

        btn1 = Button(text="تصميم 1")
        btn2 = Button(text="تصميم 2")
        btn3 = Button(text="تصميم 3")

        btn1.bind(on_press=lambda x: self.set_design(1))
        btn2.bind(on_press=lambda x: self.set_design(2))
        btn3.bind(on_press=lambda x: self.set_design(3))

        row.add_widget(btn1)
        row.add_widget(btn2)
        row.add_widget(btn3)

        self.btn_generate = Button(text="إنشاء حالة")
        self.btn_save = Button(text="حفظ في المعرض")

        self.btn_generate.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save_img)

        root.add_widget(self.img)
        root.add_widget(row)
        root.add_widget(self.btn_generate)
        root.add_widget(self.btn_save)

        self.generate()

        return root

    def set_design(self, d):
        self.design = d
        self.generate()

    def generate(self, *args):
        make_status(self.temp_path, self.design)
        self.img.source = self.temp_path
        self.img.reload()

    def save_img(self, *args):
        os.makedirs(SAVE_DIR, exist_ok=True)
        path = os.path.join(SAVE_DIR, f"status_{int(datetime.datetime.now().timestamp())}.jpg")
        shutil.copy(self.temp_path, path)


IslamApp().run()
