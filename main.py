import os
import random
import datetime
import shutil

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.resources import resource_find
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from PIL import Image as PILImage
from PIL import ImageDraw, ImageFont

try:
    import arabic_reshaper

    def fix_ar(text):
        return arabic_reshaper.reshape(str(text))[::-1]
except:
    def fix_ar(text):
        return str(text)[::-1]

from content import AYAT_AR, AHADITH_AR, AZKAR_AR, DOAA_AR


Window.clearcolor = (0, 0, 0, 1)

SAVE_DIR = "/sdcard/Pictures/IslamStatusPro"
FONT_FILE = "arabic.ttf"
FONT_PATH = resource_find(FONT_FILE) or FONT_FILE
SETTINGS_FILE = "settings.json"

try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
except:
    pass


def ui(text):
    return fix_ar(text)


def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()


def date_text():
    today = datetime.date.today()
    return f"{today.day}-{today.month}-{today.year}"


def wrap_text(text, limit=22):
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

    draw.rounded_rectangle((45, 45, 1035, 1875), radius=50, outline=gold, width=5)

    draw.rounded_rectangle((95, 100, 985, 350), radius=30, outline=gold, width=3)
    draw_ar(draw, 540, 160, "حالات واتس اسلامية", title_font, gold)
    draw_ar(draw, 540, 230, "تصميم يومي متجدد", sub_font, white)
    draw_plain(draw, 540, 290, date_text(), small_font, gold)

    draw.rounded_rectangle((120, 470, 960, 1190), radius=40, fill=card, outline=gold, width=3)
    draw_ar(draw, 540, 560, kind, kind_font, gold)

    y = 720
    for line in wrap_text(text, 24):
        draw_ar(draw, 540, y, line, text_font, white)
        y += 80

    draw_ar(draw, 540, 1320, "اللهم اجعلها صدقة جارية", sub_font, white)

    draw.rounded_rectangle((170, 1450, 910, 1565), radius=25, outline=gold, width=3)
    draw_plain(draw, 540, 1508, date_text(), small_font, white)

    img.save(path, quality=95)


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
    except:
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

        currentActivity = PythonActivity.mActivity
        currentActivity.startActivity(Intent.createChooser(intent, fix_ar("مشاركة")))

    except:
        pass


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app_ref = None

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        top = BoxLayout(size_hint=(1, 0.06), spacing=5)

        self.title = Label(
            text=ui("حالات واتس اسلامية"),
            font_name="ArabicFont",
            font_size=18
        )

        self.settings_btn = Button(
            text="⚙",
            size_hint=(0.18, 1),
            font_size=24
        )
        self.settings_btn.bind(on_press=self.open_settings)

        top.add_widget(self.title)
        top.add_widget(self.settings_btn)

        self.img = Image(size_hint=(1, 0.52), allow_stretch=True, keep_ratio=True)

        self.msg = Label(
            text=ui("جاهز"),
            size_hint=(1, 0.05),
            font_name="ArabicFont",
            font_size=18
        )

        self.btn_generate = Button(
            text=ui("إنشاء حالة"),
            size_hint=(1, 0.11),
            font_name="ArabicFont",
            font_size=22
        )

        self.btn_save = Button(
            text=ui("حفظ في المعرض"),
            size_hint=(1, 0.11),
            font_name="ArabicFont",
            font_size=22
        )

        self.btn_share = Button(
            text=ui("مشاركة"),
            size_hint=(1, 0.11),
            font_name="ArabicFont",
            font_size=22
        )

        self.btn_generate.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save_only)
        self.btn_share.bind(on_press=self.share_only)

        root.add_widget(top)
        root.add_widget(self.img)
        root.add_widget(self.msg)
        root.add_widget(self.btn_generate)
        root.add_widget(self.btn_save)
        root.add_widget(self.btn_share)

        self.add_widget(root)

    def open_settings(self, *args):
        self.manager.current = "settings"

    def on_pre_enter(self):
        self.app_ref = App.get_running_app()
        self.generate()

    def pick_text(self):
        t = self.app_ref.content_type

        if t == "ayah":
            return get_random(AYAT_AR, self.app_ref.last_text), "آية اليوم"

        if t == "hadith":
            return get_random(AHADITH_AR, self.app_ref.last_text), "حديث اليوم"

        if t == "dhikr":
            return get_random(AZKAR_AR, self.app_ref.last_text), "ذكر اليوم"

        if t == "dua":
            return get_random(DOAA_AR, self.app_ref.last_text), "دعاء اليوم"

        all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
        return get_random(all_data, self.app_ref.last_text), "نفحة إيمانية"

    def generate(self, *args):
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

        self.msg.text = ui("تم إنشاء الصورة")

    def save_only(self, *args):
        os.makedirs(SAVE_DIR, exist_ok=True)

        path = os.path.join(
            SAVE_DIR,
            f"status_{int(datetime.datetime.now().timestamp())}.jpg"
        )

        shutil.copy(self.app_ref.temp, path)
        scan_gallery(path)

        self.app_ref.last_saved_path = path
        self.msg.text = ui("تم الحفظ في المعرض")

    def share_only(self, *args):
        if not self.app_ref.last_saved_path or not os.path.exists(self.app_ref.last_saved_path):
            self.save_only()

        share_image(self.app_ref.last_saved_path)


class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=10, spacing=8)

        title = Label(
            text=ui("الإعدادات"),
            size_hint=(1, 0.08),
            font_name="ArabicFont",
            font_size=24
        )

        root.add_widget(title)

        root.add_widget(Label(
            text=ui("نوع المحتوى"),
            size_hint=(1, 0.06),
            font_name="ArabicFont",
            font_size=18
        ))

        row_type = BoxLayout(size_hint=(1, 0.1), spacing=4)

        types = [
            ("عشوائي", "random"),
            ("آية", "ayah"),
            ("حديث", "hadith"),
            ("ذكر", "dhikr"),
            ("دعاء", "dua")
        ]

        for name, val in types:
            b = Button(text=ui(name), font_name="ArabicFont")
            b.bind(on_press=lambda x, v=val: self.set_content(v))
            row_type.add_widget(b)

        root.add_widget(row_type)

        root.add_widget(Label(
            text=ui("التصميم"),
            size_hint=(1, 0.06),
            font_name="ArabicFont",
            font_size=18
        ))

        row_design = BoxLayout(size_hint=(1, 0.1), spacing=4)

        for i in [1, 2, 3]:
            b = Button(text=ui(f"تصميم {i}"), font_name="ArabicFont")
            b.bind(on_press=lambda x, d=i: self.set_design(d))
            row_design.add_widget(b)

        root.add_widget(row_design)

        root.add_widget(Label(
            text=ui("الإشعارات"),
            size_hint=(1, 0.06),
            font_name="ArabicFont",
            font_size=18
        ))

        row_notify = BoxLayout(size_hint=(1, 0.1), spacing=4)

        self.notify_btn = Button(text=ui("الإشعار: إيقاف"), font_name="ArabicFont")
        self.notify_btn.bind(on_press=self.toggle_notify)

        self.hour_btn = Button(text=ui("الساعة: 9"), font_name="ArabicFont")
        self.hour_btn.bind(on_press=self.change_hour)

        row_notify.add_widget(self.notify_btn)
        row_notify.add_widget(self.hour_btn)

        root.add_widget(row_notify)

        self.status = Label(
            text=ui("تم حفظ الإعدادات تلقائياً"),
            size_hint=(1, 0.08),
            font_name="ArabicFont",
            font_size=16
        )

        root.add_widget(self.status)

        back = Button(
            text=ui("رجوع"),
            size_hint=(1, 0.12),
            font_name="ArabicFont",
            font_size=22
        )
        back.bind(on_press=self.go_back)

        root.add_widget(back)

        self.add_widget(root)

    def on_pre_enter(self):
        app = App.get_running_app()
        self.notify_btn.text = ui("الإشعار: تشغيل") if app.notify else ui("الإشعار: إيقاف")
        self.hour_btn.text = ui(f"الساعة: {app.notify_hour}")

    def set_content(self, value):
        app = App.get_running_app()
        app.content_type = value
        app.save_settings()
        self.status.text = ui("تم حفظ نوع المحتوى")

    def set_design(self, value):
        app = App.get_running_app()
        app.design = value
        app.save_settings()
        self.status.text = ui("تم حفظ التصميم")

    def toggle_notify(self, *args):
        app = App.get_running_app()
        app.notify = not app.notify
        app.save_settings()
        self.notify_btn.text = ui("الإشعار: تشغيل") if app.notify else ui("الإشعار: إيقاف")
        self.status.text = ui("تم حفظ الإشعارات")

    def change_hour(self, *args):
        app = App.get_running_app()
        app.notify_hour += 1
        if app.notify_hour > 23:
            app.notify_hour = 0
        app.save_settings()
        self.hour_btn.text = ui(f"الساعة: {app.notify_hour}")
        self.status.text = ui("تم حفظ الساعة")

    def go_back(self, *args):
        self.manager.current = "main"


class IslamApp(App):

    def build(self):
        self.store = JsonStore(SETTINGS_FILE)

        self.design = 1
        self.content_type = "random"
        self.notify = False
        self.notify_hour = 9
        self.last_text = ""
        self.last_saved_path = ""

        self.temp = os.path.join(self.user_data_dir, "preview.jpg")

        self.load_settings()

        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm

    def load_settings(self):
        if self.store.exists("prefs"):
            prefs = self.store.get("prefs")
            self.design = prefs.get("design", 1)
            self.content_type = prefs.get("content_type", "random")
            self.notify = prefs.get("notify", False)
            self.notify_hour = prefs.get("notify_hour", 9)

    def save_settings(self):
        self.store.put(
            "prefs",
            design=self.design,
            content_type=self.content_type,
            notify=self.notify,
            notify_hour=self.notify_hour
        )


IslamApp().run()
