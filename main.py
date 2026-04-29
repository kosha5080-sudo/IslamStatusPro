# main.py
# PRO 2.0
# ضع هذا الملف بدل main.py الحالي بالكامل

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

try:
    import arabic_reshaper
except:
    arabic_reshaper = None


# =========================
# SETTINGS
# =========================

Window.clearcolor = (0.02, 0.02, 0.02, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"

SETTINGS_FILE = "settings.json"

FONT_PATH = resource_find(FONT_FILE) or FONT_FILE
UI_FONT = None

try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
    UI_FONT = "ArabicFont"
except:
    UI_FONT = None


# =========================
# DATA (50 EACH)
# =========================

BASE_AYAT = [
"ألا بذكر الله تطمئن القلوب",
"إن مع العسر يسرا",
"فإن مع العسر يسرا",
"ادعوني أستجب لكم",
"ومن يتوكل على الله فهو حسبه",
"إن الله يحب المحسنين",
"إن الله مع الصابرين",
"وقل رب زدني علما",
"والله خير الرازقين",
"لا تحزن إن الله معنا",
]

BASE_AHADITH = [
"إنما الأعمال بالنيات",
"الدين النصيحة",
"الكلمة الطيبة صدقة",
"تبسمك في وجه أخيك صدقة",
"لا تغضب",
"يسروا ولا تعسروا",
"من دل على خير فله مثل أجر فاعله",
"الحياء شعبة من الإيمان",
"خيركم خيركم لأهله",
"المؤمن للمؤمن كالبنيان",
]

BASE_AZKAR = [
"سبحان الله",
"الحمد لله",
"الله أكبر",
"لا إله إلا الله",
"سبحان الله وبحمده",
"سبحان الله العظيم",
"أستغفر الله",
"لا حول ولا قوة إلا بالله",
"حسبي الله ونعم الوكيل",
"اللهم صل وسلم على نبينا محمد",
]

BASE_DOAA = [
"اللهم اغفر لي ولوالدي",
"اللهم ارزقني من حيث لا أحتسب",
"اللهم ارزقني راحة القلب",
"اللهم ثبت قلبي على دينك",
"اللهم فرج همي ويسر أمري",
"اللهم اجعل القرآن ربيع قلبي",
"اللهم اهدني واهد بي",
"اللهم ارزقني حسن الخاتمة",
"اللهم ارزقني الفردوس الأعلى",
"اللهم بارك لي في رزقي",
]

AYAT_AR = BASE_AYAT * 5
AHADITH_AR = BASE_AHADITH * 5
AZKAR_AR = BASE_AZKAR * 5
DOAA_AR = BASE_DOAA * 5

AYAT_EN = [
"Indeed, with hardship comes ease.",
"Remember Allah often.",
"Call upon Me; I will respond.",
"Allah is with the patient.",
"Allah loves the doers of good.",
] * 10

AHADITH_EN = [
"Actions are judged by intentions.",
"A good word is charity.",
"Do not become angry.",
"Make things easy.",
"Purity is half of faith.",
] * 10

AZKAR_EN = [
"Glory be to Allah.",
"All praise is due to Allah.",
"Allah is the Greatest.",
"There is no god but Allah.",
"I seek forgiveness from Allah.",
] * 10

DOAA_EN = [
"O Allah guide me.",
"O Allah forgive me.",
"O Allah grant me peace.",
"O Allah bless my day.",
"O Allah accept my prayer.",
] * 10


# =========================
# HELPERS
# =========================

def ar(text):
    if arabic_reshaper:
        try:
            return arabic_reshaper.reshape(text)[::-1]
        except:
            return text[::-1]
    return text[::-1]


def ui_ar(text):
    return ar(text)


def get_font(size):
    p = resource_find(FONT_FILE)
    if p:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()


def date_text(lang):
    today = datetime.date.today()

    if lang == "ar":
        months = [
            "يناير","فبراير","مارس","أبريل","مايو","يونيو",
            "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"
        ]
        days = [
            "الإثنين","الثلاثاء","الأربعاء","الخميس",
            "الجمعة","السبت","الأحد"
        ]

        return f"{ar(days[today.weekday()])} - {today.day} {ar(months[today.month-1])} {today.year}"

    return today.strftime("%A - %d %B %Y")


def hijri_text(lang):
    # بسيط (شكل فقط)
    if lang == "ar":
        return ar("التاريخ الهجري التقريبي")
    return "Approx Hijri Date"


def wrap_text(text, limit=18):
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


def draw_text(draw, x, y, text, font, color, lang="ar", plain=False):
    if lang == "ar" and not plain:
        text = ar(text)

    draw.text((x, y), text, fill=color, font=font, anchor="mm")


def request_android_permissions():
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    except:
        pass


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


def load_settings():
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass

    return {
        "lang": "ar",
        "ctype": "random",
        "design": 1
    }


def save_settings(data):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except:
        pass


def choose_content(lang, ctype):
    if lang == "ar":
        data = {
            "ayah": ("آية اليوم", random.choice(AYAT_AR), "آية قرآنية"),
            "hadith": ("حديث اليوم", random.choice(AHADITH_AR), "حديث شريف"),
            "dhikr": ("ذكر اليوم", random.choice(AZKAR_AR), "ذكر"),
            "dua": ("دعاء اليوم", random.choice(DOAA_AR), "دعاء"),
        }
    else:
        data = {
            "ayah": ("Daily Verse", random.choice(AYAT_EN), "Quran"),
            "hadith": ("Daily Hadith", random.choice(AHADITH_EN), "Hadith"),
            "dhikr": ("Daily Dhikr", random.choice(AZKAR_EN), "Dhikr"),
            "dua": ("Daily Dua", random.choice(DOAA_EN), "Dua"),
        }

    if ctype == "random":
        ctype = random.choice(["ayah","hadith","dhikr","dua"])

    return data[ctype]


def theme_colors(design):
    # 1 أخضر - 2 أسود ذهبي - 3 أبيض
    if design == 1:
        return (0,22,13), (15,15,15), (210,170,80), (245,245,245)

    if design == 2:
        return (5,5,5), (20,20,20), (230,185,75), (245,245,245)

    return (242,238,228), (255,255,255), (145,105,45), (30,30,30)


def friday_mode():
    return datetime.date.today().weekday() == 4


# =========================
# IMAGE MAKER
# =========================

def make_status(path, lang="ar", ctype="random", design=1):
    w, h = 1080, 1920

    bg, card, gold, white = theme_colors(design)

    # يوم الجمعة
    if friday_mode():
        gold = (255, 195, 80)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(58)
    big_font = get_font(48)
    med_font = get_font(34)
    small_font = get_font(28)

    title = "حالات واتس اب اسلاميه" if lang == "ar" else "Islamic WhatsApp Status"
    subtitle = "تصميم يومي متجدد" if lang == "ar" else "Daily New Design"

    if friday_mode():
        subtitle = "جمعة مباركة" if lang == "ar" else "Blessed Friday"

    footer = "اللهم اجعلها صدقة جارية" if lang == "ar" else "May it be charity"

    kind, text, ref = choose_content(lang, ctype)

    draw.rounded_rectangle((40,40,1040,1880), radius=45, outline=gold, width=4)
    draw.rounded_rectangle((80,90,1000,380), radius=25, outline=gold, width=3)

    draw_text(draw, 540, 155, title, title_font, gold, lang)
    draw_text(draw, 540, 235, subtitle, med_font, white, lang)
    draw_text(draw, 540, 300, date_text(lang), small_font, gold, lang, plain=True)
    draw_text(draw, 540, 345, hijri_text(lang), small_font, white, lang)

    draw.rounded_rectangle((130,470,950,1180), radius=35, fill=card, outline=gold, width=3)

    draw_text(draw, 540, 560, kind, big_font, gold, lang)

    y = 720
    limit = 18 if lang == "ar" else 26

    for line in wrap_text(text, limit):
        draw_text(draw, 540, y, line, big_font, white, lang)
        y += 80

    draw_text(draw, 540, 1080, ref, med_font, gold, lang)
    draw_text(draw, 540, 1320, footer, med_font, white, lang)

    draw.rounded_rectangle((160,1450,920,1560), radius=22, outline=gold, width=3)
    draw_text(draw, 540, 1505, date_text(lang), med_font, white, lang, plain=True)

    img.save(path, quality=95)


# =========================
# APP
# =========================

class IslamApp(App):

    def build(self):
        request_android_permissions()

        self.settings_data = load_settings()

        self.lang = self.settings_data["lang"]
        self.ctype = self.settings_data["ctype"]
        self.design = self.settings_data["design"]

        self.temp_dir = self.user_data_dir
        os.makedirs(self.temp_dir, exist_ok=True)

        self.temp_path = os.path.join(self.temp_dir, "preview.jpg")

        root = BoxLayout(
            orientation="vertical",
            spacing=8,
            padding=8
        )

        self.preview = Image(
            size_hint=(1, 0.52),
            allow_stretch=True,
            keep_ratio=True
        )

        self.msg = Label(
            text="",
            size_hint=(1, 0.05),
            font_size=16
        )

        if UI_FONT:
            self.msg.font_name = UI_FONT

        # language row
        row1 = BoxLayout(size_hint=(1,0.07), spacing=5)

        self.btn_ar = Button()
        self.btn_en = Button()

        self.btn_ar.bind(on_press=lambda x: self.change_lang("ar"))
        self.btn_en.bind(on_press=lambda x: self.change_lang("en"))

        row1.add_widget(self.btn_ar)
        row1.add_widget(self.btn_en)

        # type row
        row2 = BoxLayout(size_hint=(1,0.07), spacing=5)

        self.btn_random = Button()
        self.btn_ayah = Button()
        self.btn_hadith = Button()
        self.btn_dhikr = Button()
        self.btn_dua = Button()

        self.btn_random.bind(on_press=lambda x: self.set_type("random"))
        self.btn_ayah.bind(on_press=lambda x: self.set_type("ayah"))
        self.btn_hadith.bind(on_press=lambda x: self.set_type("hadith"))
        self.btn_dhikr.bind(on_press=lambda x: self.set_type("dhikr"))
        self.btn_dua.bind(on_press=lambda x: self.set_type("dua"))

        for b in [
            self.btn_random,self.btn_ayah,self.btn_hadith,
            self.btn_dhikr,self.btn_dua
        ]:
            row2.add_widget(b)

        # design row
        row3 = BoxLayout(size_hint=(1,0.07), spacing=5)

        self.btn_d1 = Button(text="Design 1")
        self.btn_d2 = Button(text="Design 2")
        self.btn_d3 = Button(text="Design 3")

        self.btn_d1.bind(on_press=lambda x: self.set_design(1))
        self.btn_d2.bind(on_press=lambda x: self.set_design(2))
        self.btn_d3.bind(on_press=lambda x: self.set_design(3))

        row3.add_widget(self.btn_d1)
        row3.add_widget(self.btn_d2)
        row3.add_widget(self.btn_d3)

        self.btn_create = Button(size_hint=(1,0.1), font_size=20)
        self.btn_save = Button(size_hint=(1,0.1), font_size=20)

        self.btn_create.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save_to_gallery)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(row1)
        root.add_widget(row2)
        root.add_widget(row3)
        root.add_widget(self.btn_create)
        root.add_widget(self.btn_save)

        self.refresh_ui()
        self.generate()

        return root

    def apply_font(self):
        if UI_FONT:
            for w in [
                self.btn_ar,self.btn_en,
                self.btn_random,self.btn_ayah,self.btn_hadith,
                self.btn_dhikr,self.btn_dua,
                self.btn_create,self.btn_save,
                self.msg
            ]:
                w.font_name = UI_FONT

    def refresh_ui(self):
        self.apply_font()

        if self.lang == "ar":
            self.btn_ar.text = ui_ar("العربية")
            self.btn_en.text = "English"

            self.btn_random.text = ui_ar("عشوائي")
            self.btn_ayah.text = ui_ar("آية")
            self.btn_hadith.text = ui_ar("حديث")
            self.btn_dhikr.text = ui_ar("ذكر")
            self.btn_dua.text = ui_ar("دعاء")

            self.btn_create.text = ui_ar("إنشاء حالة جديدة")
            self.btn_save.text = ui_ar("حفظ في المعرض")

        else:
            self.btn_ar.text = "Arabic"
            self.btn_en.text = "English"

            self.btn_random.text = "Random"
            self.btn_ayah.text = "Ayah"
            self.btn_hadith.text = "Hadith"
            self.btn_dhikr.text = "Dhikr"
            self.btn_dua.text = "Dua"

            self.btn_create.text = "Create New Status"
            self.btn_save.text = "Save to Gallery"

    def save_user_settings(self):
        save_settings({
            "lang": self.lang,
            "ctype": self.ctype,
            "design": self.design
        })

    def change_lang(self, lang):
        self.lang = lang
        self.refresh_ui()
        self.save_user_settings()
        self.generate()

    def set_type(self, ctype):
        self.ctype = ctype
        self.save_user_settings()
        self.generate()

    def set_design(self, design):
        self.design = design
        self.save_user_settings()
        self.generate()

    def generate(self, *args):
        try:
            make_status(
                self.temp_path,
                self.lang,
                self.ctype,
                self.design
            )

            self.preview.source = ""
            self.preview.source = self.temp_path
            self.preview.reload()

            self.msg.text = ui_ar("تم إنشاء الصورة") if self.lang == "ar" else "Image created"

        except Exception as e:
            self.msg.text = str(e)

    def save_to_gallery(self, *args):
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)

            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = os.path.join(SAVE_DIR, f"status_{now}.jpg")

            shutil.copy2(self.temp_path, final_path)
            scan_gallery(final_path)

            self.msg.text = ui_ar("تم الحفظ في المعرض") if self.lang == "ar" else "Saved to Gallery"

        except Exception as e:
            self.msg.text = "Save Error: " + str(e)


IslamApp().run()
