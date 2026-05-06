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


STRINGS = {
    "ar": {
        "app_title": "حالات واتس اسلامية",
        "daily": "تصميم يومي متجدد",
        "settings": "الإعدادات",
        "language": "اللغة",
        "arabic": "عربي",
        "english": "English",
        "content_type": "نوع المحتوى",
        "random": "عشوائي",
        "ayah": "آية",
        "hadith": "حديث",
        "dhikr": "ذكر",
        "dua": "دعاء",
        "design": "التصميم",
        "design_1": "تصميم 1",
        "design_2": "تصميم 2",
        "design_3": "تصميم 3",
        "notifications": "الإشعارات",
        "notify_on": "الإشعار: تشغيل",
        "notify_off": "الإشعار: إيقاف",
        "hour": "الساعة",
        "saved_settings": "تم حفظ الإعدادات",
        "back": "رجوع",
        "ready": "جاهز",
        "created": "تم إنشاء الصورة",
        "create": "إنشاء حالة",
        "save": "حفظ في المعرض",
        "share": "مشاركة واتساب",
        "saved": "تم الحفظ في المعرض",
        "share_fail": "تعذر فتح واتساب",
        "charity": "اللهم اجعلها صدقة جارية",
        "kind_ayah": "آية اليوم",
        "kind_hadith": "حديث اليوم",
        "kind_dhikr": "ذكر اليوم",
        "kind_dua": "دعاء اليوم",
        "kind_random": "نفحة إيمانية",
    },
    "en": {
        "app_title": "Islamic WhatsApp Status",
        "daily": "Daily New Design",
        "settings": "Settings",
        "language": "Language",
        "arabic": "Arabic",
        "english": "English",
        "content_type": "Content Type",
        "random": "Random",
        "ayah": "Ayah",
        "hadith": "Hadith",
        "dhikr": "Dhikr",
        "dua": "Dua",
        "design": "Design",
        "design_1": "Design 1",
        "design_2": "Design 2",
        "design_3": "Design 3",
        "notifications": "Notifications",
        "notify_on": "Notification: On",
        "notify_off": "Notification: Off",
        "hour": "Hour",
        "saved_settings": "Settings saved",
        "back": "Back",
        "ready": "Ready",
        "created": "Image created",
        "create": "Create Status",
        "save": "Save to Gallery",
        "share": "Share WhatsApp",
        "saved": "Saved to gallery",
        "share_fail": "Could not open WhatsApp",
        "charity": "May it be ongoing charity",
        "kind_ayah": "Daily Ayah",
        "kind_hadith": "Daily Hadith",
        "kind_dhikr": "Daily Dhikr",
        "kind_dua": "Daily Dua",
        "kind_random": "Daily Inspiration",
    }
}


def t(key, lang="ar"):
    return STRINGS.get(lang, STRINGS["ar"]).get(key, key)


def ui(text, lang="ar"):
    return fix_ar(text) if lang == "ar" else str(text)


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


def draw_text(draw, x, y, text, font, color, lang="ar"):
    final = fix_ar(text) if lang == "ar" else str(text)
    draw.text((x, y), final, fill=color, font=font, anchor="mm")


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


def make_status(path, text, design, kind, lang):
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
    draw_text(draw, 540, 160, t("app_title", lang), title_font, gold, lang)
    draw_text(draw, 540, 230, t("daily", lang), sub_font, white, lang)
    draw_plain(draw, 540, 290, date_text(), small_font, gold)

    draw.rounded_rectangle((120, 470, 960, 1190), radius=40, fill=card, outline=gold, width=3)
    draw_text(draw, 540, 560, kind, kind_font, gold, lang)

    y = 720
    for line in wrap_text(text, 24):
        draw_text(draw, 540, y, line, text_font, white, lang)
        y += 80

    draw_text(draw, 540, 1320, t("charity", lang), sub_font, white, lang)

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


def share_whatsapp(path):
    try:
        from jnius import autoclass

        Intent = autoclass("android.content.Intent")
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        Uri = autoclass("android.net.Uri")
        File = autoclass("java.io.File")

        intent = Intent(Intent.ACTION_SEND)
        intent.setType("image/*")
        intent.setPackage("com.whatsapp")

        uri = Uri.fromFile(File(path))
        intent.putExtra(Intent.EXTRA_STREAM, uri)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

        currentActivity = PythonActivity.mActivity
        currentActivity.startActivity(intent)
        return True

    except:
        return False


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        top = BoxLayout(size_hint=(1, 0.06), spacing=5)

        self.title = Label(
            text="",
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
            text="",
            size_hint=(1, 0.05),
            font_name="ArabicFont",
            font_size=18
        )

        self.btn_generate = Button(size_hint=(1, 0.11), font_name="ArabicFont", font_size=22)
        self.btn_save = Button(size_hint=(1, 0.11), font_name="ArabicFont", font_size=22)
        self.btn_share = Button(size_hint=(1, 0.11), font_name="ArabicFont", font_size=22)

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

    def refresh_ui(self):
        app = App.get_running_app()
        lang = app.lang

        self.title.text = ui(t("app_title", lang), lang)
        self.msg.text = ui(t("ready", lang), lang)
        self.btn_generate.text = ui(t("create", lang), lang)
        self.btn_save.text = ui(t("save", lang), lang)
        self.btn_share.text = ui(t("share", lang), lang)

    def open_settings(self, *args):
        self.manager.current = "settings"

    def on_pre_enter(self):
        self.refresh_ui()
        self.generate()

    def pick_text(self):
        app = App.get_running_app()

        if app.content_type == "ayah":
            return get_random(AYAT_AR, app.last_text), t("kind_ayah", app.lang)

        if app.content_type == "hadith":
            return get_random(AHADITH_AR, app.last_text), t("kind_hadith", app.lang)

        if app.content_type == "dhikr":
            return get_random(AZKAR_AR, app.last_text), t("kind_dhikr", app.lang)

        if app.content_type == "dua":
            return get_random(DOAA_AR, app.last_text), t("kind_dua", app.lang)

        all_data = AYAT_AR + AHADITH_AR + AZKAR_AR + DOAA_AR
        return get_random(all_data, app.last_text), t("kind_random", app.lang)

    def generate(self, *args):
        app = App.get_running_app()

        text, kind = self.pick_text()
        app.last_text = text

        make_status(app.temp, text, app.design, kind, app.lang)

        self.img.source = ""
        self.img.source = app.temp
        self.img.reload()

        self.msg.text = ui(t("created", app.lang), app.lang)

    def save_only(self, *args):
        app = App.get_running_app()

        os.makedirs(SAVE_DIR, exist_ok=True)

        path = os.path.join(
            SAVE_DIR,
            f"status_{int(datetime.datetime.now().timestamp())}.jpg"
        )

        shutil.copy(app.temp, path)
        scan_gallery(path)

        app.last_saved_path = path
        self.msg.text = ui(t("saved", app.lang), app.lang)

    def share_only(self, *args):
        app = App.get_running_app()

        if not app.last_saved_path or not os.path.exists(app.last_saved_path):
            self.save_only()

        ok = share_whatsapp(app.last_saved_path)

        if not ok:
            self.msg.text = ui(t("share_fail", app.lang), app.lang)


class SettingsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root_box = BoxLayout(orientation="vertical", padding=10, spacing=8)

        self.title = Label(size_hint=(1, 0.08), font_name="ArabicFont", font_size=24)
        self.root_box.add_widget(self.title)

        self.lang_label = Label(size_hint=(1, 0.06), font_name="ArabicFont", font_size=18)
        self.root_box.add_widget(self.lang_label)

        row_lang = BoxLayout(size_hint=(1, 0.1), spacing=4)
        self.btn_ar = Button(font_name="ArabicFont")
        self.btn_en = Button(font_name="ArabicFont")
        self.btn_ar.bind(on_press=lambda x: self.set_language("ar"))
        self.btn_en.bind(on_press=lambda x: self.set_language("en"))
        row_lang.add_widget(self.btn_ar)
        row_lang.add_widget(self.btn_en)
        self.root_box.add_widget(row_lang)

        self.type_label = Label(size_hint=(1, 0.06), font_name="ArabicFont", font_size=18)
        self.root_box.add_widget(self.type_label)

        row_type = BoxLayout(size_hint=(1, 0.1), spacing=4)

        self.type_buttons = []
        for key, val in [
            ("random", "random"),
            ("ayah", "ayah"),
            ("hadith", "hadith"),
            ("dhikr", "dhikr"),
            ("dua", "dua")
        ]:
            b = Button(font_name="ArabicFont")
            b.bind(on_press=lambda x, v=val: self.set_content(v))
            row_type.add_widget(b)
            self.type_buttons.append((b, key))

        self.root_box.add_widget(row_type)

        self.design_label = Label(size_hint=(1, 0.06), font_name="ArabicFont", font_size=18)
        self.root_box.add_widget(self.design_label)

        row_design = BoxLayout(size_hint=(1, 0.1), spacing=4)

        self.design_buttons = []
        for i in [1, 2, 3]:
            b = Button(font_name="ArabicFont")
            b.bind(on_press=lambda x, d=i: self.set_design(d))
            row_design.add_widget(b)
            self.design_buttons.append((b, i))

        self.root_box.add_widget(row_design)

        self.notify_label = Label(size_hint=(1, 0.06), font_name="ArabicFont", font_size=18)
        self.root_box.add_widget(self.notify_label)

        row_notify = BoxLayout(size_hint=(1, 0.1), spacing=4)

        self.notify_btn = Button(font_name="ArabicFont")
        self.notify_btn.bind(on_press=self.toggle_notify)

        self.hour_btn = Button(font_name="ArabicFont")
        self.hour_btn.bind(on_press=self.change_hour)

        row_notify.add_widget(self.notify_btn)
        row_notify.add_widget(self.hour_btn)
        self.root_box.add_widget(row_notify)

        self.status = Label(size_hint=(1, 0.08), font_name="ArabicFont", font_size=16)
        self.root_box.add_widget(self.status)

        self.back_btn = Button(size_hint=(1, 0.12), font_name="ArabicFont", font_size=22)
        self.back_btn.bind(on_press=self.go_back)

        self.root_box.add_widget(self.back_btn)

        self.add_widget(self.root_box)

    def on_pre_enter(self):
        self.refresh_ui()

    def refresh_ui(self):
        app = App.get_running_app()
        lang = app.lang

        self.title.text = ui(t("settings", lang), lang)
        self.lang_label.text = ui(t("language", lang), lang)
        self.btn_ar.text = ui(t("arabic", lang), lang)
        self.btn_en.text = t("english", lang)

        self.type_label.text = ui(t("content_type", lang), lang)

        for b, key in self.type_buttons:
            b.text = ui(t(key, lang), lang)

        self.design_label.text = ui(t("design", lang), lang)

        for b, i in self.design_buttons:
            b.text = ui(t(f"design_{i}", lang), lang)

        self.notify_label.text = ui(t("notifications", lang), lang)
        self.notify_btn.text = ui(t("notify_on" if app.notify else "notify_off", lang), lang)
        self.hour_btn.text = ui(f"{t('hour', lang)}: {app.notify_hour}", lang)

        self.status.text = ui(t("saved_settings", lang), lang)
        self.back_btn.text = ui(t("back", lang), lang)

    def set_language(self, lang):
        app = App.get_running_app()
        app.lang = lang
        app.save_settings()
        self.refresh_ui()

    def set_content(self, value):
        app = App.get_running_app()
        app.content_type = value
        app.save_settings()
        self.status.text = ui(t("saved_settings", app.lang), app.lang)

    def set_design(self, value):
        app = App.get_running_app()
        app.design = value
        app.save_settings()
        self.status.text = ui(t("saved_settings", app.lang), app.lang)

    def toggle_notify(self, *args):
        app = App.get_running_app()
        app.notify = not app.notify
        app.save_settings()
        self.refresh_ui()

    def change_hour(self, *args):
        app = App.get_running_app()
        app.notify_hour = (int(app.notify_hour) + 1) % 24
        app.save_settings()
        self.refresh_ui()

    def go_back(self, *args):
        self.manager.current = "main"


class IslamApp(App):

    def build(self):
        self.store = JsonStore(SETTINGS_FILE)

        self.lang = "ar"
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
            self.lang = prefs.get("lang", "ar")
            self.design = int(prefs.get("design", 1))
            self.content_type = prefs.get("content_type", "random")
            self.notify = bool(prefs.get("notify", False))

            try:
                self.notify_hour = int(prefs.get("notify_hour", 9))
            except:
                self.notify_hour = 9

            if self.notify_hour < 0 or self.notify_hour > 23:
                self.notify_hour = 9

            if self.lang not in ["ar", "en"]:
                self.lang = "ar"

    def save_settings(self):
        self.store.put(
            "prefs",
            lang=self.lang,
            design=self.design,
            content_type=self.content_type,
            notify=self.notify,
            notify_hour=self.notify_hour
        )


IslamApp().run()
