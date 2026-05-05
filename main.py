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
from kivy.uix.screenmanager import ScreenManager, Screen

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    def fix_ar(text):
        return get_display(arabic_reshaper.reshape(str(text)))
except:
    def fix_ar(text):
        return str(text)

from content import AYAT_AR, AHADITH_AR, AZKAR_AR, DOAA_AR


Window.clearcolor = (0, 0, 0, 1)

SAVE_DIR = "/sdcard/Pictures/IslamStatusPro"
FONT_FILE = "arabic.ttf"
SETTINGS_FILE = "settings.json"

FONT_PATH = resource_find(FONT_FILE) or FONT_FILE

try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
except:
    pass


def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def date_text():
    today = datetime.date.today()
    return f"{today.day}-{today.month}-{today.year}"


def wrap_text(text, limit=24):
    words = str(text).split()
    lines = []
    line = ""

    for word in words:
        test = (line + " " + word).strip()
        if len(test) <= limit:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines


def draw_ar(draw, x, y, text, font, color):
    draw.text((x, y), fix_ar(text), fill=color, font=font, anchor="mm")


def draw_plain(draw, x, y, text, font, color):
    draw.text((x, y), str(text), fill=color, font=font, anchor="mm")


def get_random(data, last):
    if not data:
        return ""
    choice = random.choice(data)
    while choice == last and len(data) > 1:
        choice = random.choice(data)
    return choice


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass

    return {
        "type": "random",
        "design": 1
    }


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except:
        pass


def theme(design):
    if design == 1:
        return (0, 22, 13), (17, 17, 17), (210, 170, 80), (245, 245, 245)
    elif design == 2:
        return (7, 7, 7), (22, 22, 22), (230, 185, 75), (245, 245, 245)
    else:
        return (242, 238, 228), (255, 255, 255), (145, 105, 45), (25, 25, 25)


def make_status(path, text, design, kind):
    bg, card, gold, white = theme(design)

    img = PILImage.new("RGB", (1080, 1920), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(60)
    sub_font = get_font(34)
    kind_font = get_font(48)
    text_font = get_font(48)
    small_font = get_font(30)

    draw.rounded_rectangle((45, 45, 1035, 1875), 50, outline=gold, width=5)

    draw.rounded_rectangle((95, 100, 985, 350), 30, outline=gold, width=3)
    draw_ar(draw, 540, 160, "حالات واتس اسلامية", title_font, gold)
    draw_ar(draw, 540, 230, "تصميم يومي متجدد", sub_font, white)

    # التاريخ بدون قلب الأرقام
    draw_plain(draw, 540, 290, date_text(), small_font, gold)

    draw.rounded_rectangle((120, 470, 960, 1190), 40, fill=card, outline=gold, width=3)
    draw_ar(draw, 540, 560, kind, kind_font, gold)

    y = 720
    for line in wrap_text(text, 24):
        draw_ar(draw, 540, y, line, text_font, white)
        y += 80

    draw_ar(draw, 540, 1320, "اللهم اجعلها صدقة جارية", sub_font, white)

    draw.rounded_rectangle((170, 1450, 910, 1565), 25, outline=gold, width=3)

    # التاريخ بدون قلب الأرقام
    draw_plain(draw, 540, 1508, date_text(), small_font, white)

    img.save(path, quality=95)


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

        currentActivity = PythonActivity.mActivity
        currentActivity.startActivity(Intent.createChooser(intent, fix_ar("مشاركة")))
    except:
        pass


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app_ref = None

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        top = BoxLayout(size_hint=(1, 0.07), spacing=6)

        self.title = Label(
            text=fix_ar("حالات واتس اسلامية"),
            font_name="ArabicFont",
            font_size=20
        )

        self.settings_btn = Button(
            text="⚙",
            size_hint=(0.18, 1),
            font_size=26
        )
        self.settings_btn.bind(on_press=self.open_settings)

        top.add_widget(self.title)
        top.add_widget(self.settings_btn)

        self.img = Image(size_hint=(1, 0.53), allow_stretch=True, keep_ratio=True)

        self.msg = Label(
            text=fix_ar("جاهز"),
            size_hint=(1, 0.05),
            font_name="ArabicFont",
            font_size=16
        )

        self.btn_generate = Button(
            text=fix_ar("إنشاء حالة"),
            size_hint=(1, 0.12),
            font_name="ArabicFont",
            font_size=22
        )

        self.btn_save = Button(
            text=fix_ar("حفظ ومشاركة"),
            size_hint=(1, 0.12),
            font_name="ArabicFont",
            font_size=22
        )

        self.btn_generate.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save)

        root.add_widget(top)
        root.add_widget(self.img)
        root.add_widget(self.msg)
        root.add_widget(self.btn_generate)
        root.add_widget(self.btn_save)

        self.add_widget(root)

    def on_enter(self):
        self.app_ref = App.get_running_app()
        self.generate()

    def open_settings(self, *args):
        self.manager.current = "settings"

    def pick_text(self):
        app = self.app_ref
        ctype = app.ctype

        if ctype == "ayah":
            return get_random(AYAT_AR, app.last_text), "آية اليوم"

        if ctype == "hadith":
            return get_random(AHADITH_AR, app.last_text), "حديث اليوم"

        if ctype == "dhikr":
            return get_random(AZKAR_AR, app.last_text), "ذكر اليوم"

        if ctype == "dua":
            return get_random(DOAA_AR, app.last_text), "دعاء اليوم"

        all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
        return get_random(all_data, app.last_text), "نفحة إيمانية"

    def generate(self, *args):
        if not self.app_ref:
            self.app_ref = App.get_running_app()

        text, kind = self.pick_text()
        self.app_ref.last_text = text

        make_status(
            self.app_ref.temp,
            text,
            self.app_ref.design,
            kind
        )

        self.img.source = ""
        self.img.source = self.app_ref.temp
        self.img.reload()

        self.msg.text = fix_ar("تم إنشاء الصورة")

    def save(self, *args):
        os.makedirs(SAVE_DIR, exist_ok=True)

        path = os.path.join(
            SAVE_DIR,
            f"status_{int(datetime.datetime.now().timestamp())}.jpg"
        )

        shutil.copy(self.app_ref.temp, path)

        self.msg.text = fix_ar("تم الحفظ في المعرض")
        share_image(path)


class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        title = Label(
            text=fix_ar("الإعدادات"),
            size_hint=(1, 0.08),
            font_name="ArabicFont",
            font_size=26
        )

        root.add_widget(title)

        root.add_widget(Label(
            text=fix_ar("اختر نوع المحتوى"),
            size_hint=(1, 0.06),
            font_name="ArabicFont",
            font_size=18
        ))

        row_type1 = BoxLayout(size_hint=(1, 0.09), spacing=5)
        row_type2 = BoxLayout(size_hint=(1, 0.09), spacing=5)

        types = [
            ("عشوائي", "random"),
            ("آية", "ayah"),
            ("حديث", "hadith"),
            ("ذكر", "dhikr"),
            ("دعاء", "dua")
        ]

        for index, (name, val) in enumerate(types):
            btn = Button(
                text=fix_ar(name),
                font_name="ArabicFont",
                font_size=18
            )
            btn.bind(on_press=lambda x, v=val: self.set_type(v))
            if index < 3:
                row_type1.add_widget(btn)
            else:
                row_type2.add_widget(btn)

        root.add_widget(row_type1)
        root.add_widget(row_type2)

        root.add_widget(Label(
            text=fix_ar("اختر التصميم"),
            size_hint=(1, 0.06),
            font_name="ArabicFont",
            font_size=18
        ))

        row_design = BoxLayout(size_hint=(1, 0.1), spacing=5)

        for i in [1, 2, 3]:
            btn = Button(
                text=fix_ar(f"تصميم {i}"),
                font_name="ArabicFont",
                font_size=18
            )
            btn.bind(on_press=lambda x, d=i: self.set_design(d))
            row_design.add_widget(btn)

        root.add_widget(row_design)

        self.info = Label(
            text=fix_ar("يتم حفظ الإعدادات تلقائيًا"),
            size_hint=(1, 0.12),
            font_name="ArabicFont",
            font_size=17
        )

        root.add_widget(self.info)

        back_btn = Button(
            text=fix_ar("رجوع للرئيسية"),
            size_hint=(1, 0.12),
            font_name="ArabicFont",
            font_size=22
        )
        back_btn.bind(on_press=self.go_back)

        root.add_widget(back_btn)

        self.add_widget(root)

    def set_type(self, ctype):
        app = App.get_running_app()
        app.ctype = ctype
        app.save_prefs()
        self.info.text = fix_ar("تم حفظ نوع المحتوى")

    def set_design(self, design):
        app = App.get_running_app()
        app.design = design
        app.save_prefs()
        self.info.text = fix_ar("تم حفظ التصميم")

    def go_back(self, *args):
        self.manager.current = "main"


class IslamApp(App):

    def build(self):
        self.settings_data = load_settings()
        self.ctype = self.settings_data.get("type", "random")
        self.design = int(self.settings_data.get("design", 1))
        self.last_text = ""
        self.temp = os.path.join(self.user_data_dir, "preview.jpg")

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm

    def save_prefs(self):
        save_settings({
            "type": self.ctype,
            "design": self.design
        })


IslamApp().run()
