import os
import random
import datetime
import shutil
import traceback

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
    from bidi.algorithm import get_display
except Exception:
    arabic_reshaper = None
    get_display = None


Window.clearcolor = (0, 0, 0, 1)

SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
FONT_FILE = "arabic.ttf"
FONT_PATH = resource_find(FONT_FILE) or FONT_FILE

try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
    UI_FONT = "ArabicFont"
except Exception:
    UI_FONT = None


def fix_ar(text):
    try:
        if arabic_reshaper and get_display:
            return get_display(arabic_reshaper.reshape(text))
        return text
    except Exception:
        return text


def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def date_text():
    today = datetime.date.today()
    return f"{today.day}-{today.month}-{today.year}"


def wrap_text(text, limit=22):
    words = text.split()
    lines = []
    line = ""
    for w in words:
        test = (line + " " + w).strip()
        if len(test) <= limit:
            line = test
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_text(draw, x, y, text, font, color):
    draw.text((x, y), fix_ar(text), fill=color, font=font, anchor="mm")


def theme(design):
    if design == 1:
        return (0, 22, 13), (18, 18, 18), (210, 170, 80), (245, 245, 245)
    if design == 2:
        return (5, 5, 5), (22, 22, 22), (230, 185, 75), (245, 245, 245)
    return (242, 238, 228), (255, 255, 255), (145, 105, 45), (25, 25, 25)


def make_status(path, text, design, kind):
    bg, card, gold, white = theme(design)

    img = PILImage.new("RGB", (1080, 1920), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(60)
    sub_font = get_font(34)
    text_font = get_font(46)
    small_font = get_font(28)

    draw.rounded_rectangle((45, 45, 1035, 1875), radius=48, outline=gold, width=5)

    draw.rounded_rectangle((95, 100, 985, 340), radius=30, outline=gold, width=3)
    draw_text(draw, 540, 165, "حالات واتس اب اسلاميه", title_font, gold)
    draw_text(draw, 540, 245, "تصميم يومي متجدد", sub_font, white)
    draw_text(draw, 540, 300, date_text(), small_font, gold)

    draw.rounded_rectangle((120, 470, 960, 1180), radius=42, fill=card, outline=gold, width=3)
    draw_text(draw, 540, 565, kind, sub_font, gold)

    y = 720
    for line in wrap_text(text, 24):
        draw_text(draw, 540, y, line, text_font, white)
        y += 78

    draw_text(draw, 540, 1325, "اللهم اجعلها صدقة جارية", sub_font, white)

    draw.rounded_rectangle((170, 1450, 910, 1565), radius=25, outline=gold, width=3)
    draw_text(draw, 540, 1508, date_text(), small_font, white)

    img.save(path, quality=95)


def get_random(data, last):
    if not data:
        return "سبحان الله"
    choice = random.choice(data)
    while choice == last and len(data) > 1:
        choice = random.choice(data)
    return choice


def scan_gallery(path):
    try:
        from jnius import autoclass
        MediaScannerConnection = autoclass("android.media.MediaScannerConnection")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        MediaScannerConnection.scanFile(
            PythonActivity.mActivity,
            [path],
            ["image/jpeg"],
            None
        )
    except Exception:
        pass


def share_image(path):
    try:
        from jnius import autoclass
        Intent = autoclass("android.content.Intent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Uri = autoclass("android.net.Uri")
        File = autoclass("java.io.File")

        intent = Intent(Intent.ACTION_SEND)
        intent.setType("image/*")
        uri = Uri.fromFile(File(path))
        intent.putExtra(Intent.EXTRA_STREAM, uri)

        PythonActivity.mActivity.startActivity(Intent.createChooser(intent, "مشاركة"))
    except Exception:
        pass


class IslamApp(App):

    def build(self):
        try:
            self.design = 1
            self.last_text = ""
            self.type = "random"
            self.temp = os.path.join(self.user_data_dir, "preview.jpg")

            root = BoxLayout(orientation="vertical", padding=8, spacing=8)

            self.img = Image(size_hint=(1, 0.55), allow_stretch=True, keep_ratio=True)

            self.msg = Label(
                text=fix_ar("جاري التجهيز"),
                size_hint=(1, 0.05),
                font_name=UI_FONT if UI_FONT else None
            )

            row_type = BoxLayout(size_hint=(1, 0.08), spacing=4)

            types = [
                ("عشوائي", "random"),
                ("آية", "ayah"),
                ("حديث", "hadith"),
                ("ذكر", "dhikr"),
                ("دعاء", "dua")
            ]

            for name, val in types:
                btn = Button(text=fix_ar(name))
                if UI_FONT:
                    btn.font_name = UI_FONT
                btn.bind(on_press=lambda x, v=val: self.set_type(v))
                row_type.add_widget(btn)

            row_design = BoxLayout(size_hint=(1, 0.08), spacing=4)

            for i in [1, 2, 3]:
                btn = Button(text=fix_ar(f"تصميم {i}"))
                if UI_FONT:
                    btn.font_name = UI_FONT
                btn.bind(on_press=lambda x, d=i: self.set_design(d))
                row_design.add_widget(btn)

            self.btn_generate = Button(text=fix_ar("إنشاء حالة جديدة"), size_hint=(1, 0.1), font_size=20)
            self.btn_save = Button(text=fix_ar("حفظ ومشاركة"), size_hint=(1, 0.1), font_size=20)

            if UI_FONT:
                self.btn_generate.font_name = UI_FONT
                self.btn_save.font_name = UI_FONT

            self.btn_generate.bind(on_press=self.generate)
            self.btn_save.bind(on_press=self.save)

            root.add_widget(self.img)
            root.add_widget(self.msg)
            root.add_widget(row_type)
            root.add_widget(row_design)
            root.add_widget(self.btn_generate)
            root.add_widget(self.btn_save)

            self.generate()
            return root

        except Exception:
            error = traceback.format_exc()
            return Label(text=error)

    def set_type(self, t):
        self.type = t
        self.generate()

    def set_design(self, d):
        self.design = d
        self.generate()

    def pick_text(self):
        if self.type == "ayah":
            return get_random(AYAT_AR, self.last_text), "آية اليوم"
        if self.type == "hadith":
            return get_random(AHADITH_AR, self.last_text), "حديث اليوم"
        if self.type == "dhikr":
            return get_random(AZKAR_AR, self.last_text), "ذكر اليوم"
        if self.type == "dua":
            return get_random(DOAA_AR, self.last_text), "دعاء اليوم"

        all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
        return get_random(all_data, self.last_text), "نفحة إيمانية"

    def generate(self, *args):
        try:
            text, kind = self.pick_text()
            self.last_text = text

            make_status(self.temp, text, self.design, kind)

            self.img.source = ""
            self.img.source = self.temp
            self.img.reload()

            self.msg.text = fix_ar("تم إنشاء الصورة")
        except Exception as e:
            self.msg.text = "Error: " + str(e)

    def save(self, *args):
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)

            path = os.path.join(
                SAVE_DIR,
                f"status_{int(datetime.datetime.now().timestamp())}.jpg"
            )

            shutil.copy(self.temp, path)
            scan_gallery(path)
            self.msg.text = fix_ar("تم الحفظ في المعرض")
            share_image(path)

        except Exception as e:
            self.msg.text = "Save Error: " + str(e)


IslamApp().run()
