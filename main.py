import os
import random
import datetime

from kivy.app import App
from kivy.core.window import Window
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


Window.clearcolor = (0, 0, 0, 1)

SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
FONT_FILE = "arabic.ttf"

APP_TITLE_AR = "حالات واتس اب اسلاميه"
APP_TITLE_EN = "Islamic WhatsApp Status"


# ==========================
# DATA
# ==========================

AYAT_AR = [
"ألا بذكر الله تطمئن القلوب",
"إن مع العسر يسرا",
"واستعينوا بالصبر والصلاة",
"وقل رب زدني علما",
"فاذكروني أذكركم",
"ادعوني أستجب لكم",
"ومن يتوكل على الله فهو حسبه",
"إن الله يحب المحسنين",
"إن الله مع الصابرين",
"والله خير الرازقين"
] * 5

AHADITH_AR = [
"إنما الأعمال بالنيات",
"الدين النصيحة",
"الكلمة الطيبة صدقة",
"تبسمك في وجه أخيك صدقة",
"لا تغضب",
"يسروا ولا تعسروا",
"الطهور شطر الإيمان",
"خيركم من تعلم القرآن وعلمه",
"المؤمن للمؤمن كالبنيان",
"من حسن إسلام المرء تركه ما لا يعنيه"
] * 5

AZKAR_AR = [
"سبحان الله",
"الحمد لله",
"الله أكبر",
"لا إله إلا الله",
"سبحان الله وبحمده",
"سبحان الله العظيم",
"أستغفر الله",
"لا حول ولا قوة إلا بالله",
"حسبي الله ونعم الوكيل",
"اللهم صل وسلم على نبينا محمد"
] * 5

DOAA_AR = [
"اللهم اغفر لي ولوالدي",
"اللهم ارزقني من حيث لا أحتسب",
"اللهم فرج همي ويسر أمري",
"اللهم ثبت قلبي على دينك",
"اللهم اجعل القرآن ربيع قلبي",
"اللهم اشف مرضانا",
"اللهم اجعلني من الصالحين",
"اللهم اهدني واهد بي",
"اللهم ارزقني حسن الخاتمة",
"اللهم ارزقني راحة القلب"
] * 5


AYAT_EN = [
"Indeed, with hardship comes ease.",
"Remember Allah often.",
"Call upon Me; I will respond.",
"Allah is with the patient.",
"Allah loves the doers of good."
] * 10

AHADITH_EN = [
"Actions are judged by intentions.",
"A good word is charity.",
"Do not become angry.",
"Make things easy.",
"Purity is half of faith."
] * 10

AZKAR_EN = [
"Glory be to Allah.",
"All praise is due to Allah.",
"Allah is the Greatest.",
"There is no god but Allah.",
"I seek forgiveness from Allah."
] * 10

DOAA_EN = [
"O Allah forgive me.",
"O Allah guide me.",
"O Allah grant me peace.",
"O Allah bless my day.",
"O Allah accept my prayer."
] * 10


# ==========================
# HELPERS
# ==========================

def reshape_ar(text):
    if arabic_reshaper:
        try:
            return arabic_reshaper.reshape(text)[::-1]
        except:
            return text[::-1]
    return text[::-1]


def get_font(size):
    path = resource_find(FONT_FILE)
    if path:
        try:
            return ImageFont.truetype(path, size)
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

        day_name = reshape_ar(days[today.weekday()])
        month_name = reshape_ar(months[today.month - 1])

        return f"{today.year} {month_name} {today.day} - {day_name}"

    return today.strftime("%A - %d %B %Y")


def draw_center(draw, x, y, text, font, color, lang="ar", plain=False):
    if lang == "ar" and not plain:
        text = reshape_ar(text)

    draw.text((x, y), text, fill=color, font=font, anchor="mm")


def wrap_text(text, limit=20):
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


def scan_gallery(path):
    try:
        from jnius import autoclass

        MediaScannerConnection = autoclass(
            "android.media.MediaScannerConnection"
        )
        PythonActivity = autoclass(
            "org.kivy.android.PythonActivity"
        )

        MediaScannerConnection.scanFile(
            PythonActivity.mActivity,
            [path],
            ["image/jpeg"],
            None
        )
    except:
        pass


def get_random_content(lang, ctype):
    if lang == "ar":
        source = {
            "ayah": ("آية اليوم", random.choice(AYAT_AR), "آية قرآنية"),
            "hadith": ("حديث اليوم", random.choice(AHADITH_AR), "حديث شريف"),
            "dhikr": ("ذكر اليوم", random.choice(AZKAR_AR), "ذكر"),
            "dua": ("دعاء اليوم", random.choice(DOAA_AR), "دعاء")
        }
    else:
        source = {
            "ayah": ("Daily Verse", random.choice(AYAT_EN), "Quran"),
            "hadith": ("Daily Hadith", random.choice(AHADITH_EN), "Hadith"),
            "dhikr": ("Daily Dhikr", random.choice(AZKAR_EN), "Dhikr"),
            "dua": ("Daily Dua", random.choice(DOAA_EN), "Dua")
        }

    if ctype == "random":
        ctype = random.choice(["ayah", "hadith", "dhikr", "dua"])

    return source[ctype]


# ==========================
# IMAGE MAKER
# ==========================

def make_status(path, lang="ar", ctype="random"):
    w, h = 1080, 1920

    img = PILImage.new("RGB", (w, h), (0, 20, 12))
    draw = ImageDraw.Draw(img)

    gold = (210, 170, 80)
    white = (245, 245, 245)
    dark = (15, 15, 15)

    title_font = get_font(58)
    big_font = get_font(48)
    med_font = get_font(34)
    small_font = get_font(28)

    draw.rounded_rectangle((40, 40, 1040, 1880), radius=45, outline=gold, width=4)
    draw.rounded_rectangle((80, 90, 1000, 340), radius=25, outline=gold, width=3)

    title = APP_TITLE_AR if lang == "ar" else APP_TITLE_EN
    sub = "تصميم يومي متجدد" if lang == "ar" else "Daily New Design"

    draw_center(draw, 540, 155, title, title_font, gold, lang)
    draw_center(draw, 540, 235, sub, med_font, white, lang)
    draw_center(draw, 540, 300, date_text(lang), small_font, gold, lang, plain=True)

    draw.rounded_rectangle((130, 470, 950, 1180), radius=35, fill=dark, outline=gold, width=3)

    kind, text, ref = get_random_content(lang, ctype)

    draw_center(draw, 540, 560, kind, big_font, gold, lang)

    y = 720
    limit = 18 if lang == "ar" else 26

    for line in wrap_text(text, limit):
        draw_center(draw, 540, y, line, big_font, white, lang)
        y += 80

    draw_center(draw, 540, 1080, ref, med_font, gold, lang)

    footer = "اللهم اجعلها صدقة جارية" if lang == "ar" else "May it be charity"
    draw_center(draw, 540, 1320, footer, med_font, white, lang)

    draw.rounded_rectangle((160, 1450, 920, 1560), radius=22, outline=gold, width=3)
    draw_center(draw, 540, 1505, date_text(lang), med_font, white, lang, plain=True)

    img.save(path, quality=95)


# ==========================
# APP
# ==========================

class IslamApp(App):

    def build(self):
        os.makedirs(SAVE_DIR, exist_ok=True)

        self.lang = "ar"
        self.ctype = "random"

        root = BoxLayout(
            orientation="vertical",
            spacing=8,
            padding=8
        )

        self.preview = Image(
            size_hint=(1, 0.62),
            allow_stretch=True,
            keep_ratio=True
        )

        self.msg = Label(
            text="Ready",
            size_hint=(1, 0.05),
            font_size=18
        )

        # لغة
        row1 = BoxLayout(size_hint=(1, 0.08), spacing=5)

        self.btn_ar = Button(text="العربية")
        self.btn_en = Button(text="English")

        self.btn_ar.bind(on_press=lambda x: self.change_lang("ar"))
        self.btn_en.bind(on_press=lambda x: self.change_lang("en"))

        row1.add_widget(self.btn_ar)
        row1.add_widget(self.btn_en)

        # نوع
        row2 = BoxLayout(size_hint=(1, 0.08), spacing=5)

        self.btn_random = Button(text="عشوائي")
        self.btn_ayah = Button(text="آية")
        self.btn_hadith = Button(text="حديث")
        self.btn_dhikr = Button(text="ذكر")
        self.btn_dua = Button(text="دعاء")

        self.btn_random.bind(on_press=lambda x: self.set_type("random"))
        self.btn_ayah.bind(on_press=lambda x: self.set_type("ayah"))
        self.btn_hadith.bind(on_press=lambda x: self.set_type("hadith"))
        self.btn_dhikr.bind(on_press=lambda x: self.set_type("dhikr"))
        self.btn_dua.bind(on_press=lambda x: self.set_type("dua"))

        row2.add_widget(self.btn_random)
        row2.add_widget(self.btn_ayah)
        row2.add_widget(self.btn_hadith)
        row2.add_widget(self.btn_dhikr)
        row2.add_widget(self.btn_dua)

        # زر إنشاء
        self.btn_create = Button(
            text="إنشاء حالة جديدة",
            size_hint=(1, 0.12),
            font_size=22
        )

        self.btn_create.bind(on_press=self.generate)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(row1)
        root.add_widget(row2)
        root.add_widget(self.btn_create)

        self.refresh_ui()
        self.generate()

        return root

    def refresh_ui(self):
        if self.lang == "ar":
            self.btn_ar.text = "العربية"
            self.btn_en.text = "English"

            self.btn_random.text = "عشوائي"
            self.btn_ayah.text = "آية"
            self.btn_hadith.text = "حديث"
            self.btn_dhikr.text = "ذكر"
            self.btn_dua.text = "دعاء"

            self.btn_create.text = "إنشاء حالة جديدة"

        else:
            self.btn_ar.text = "Arabic"
            self.btn_en.text = "English"

            self.btn_random.text = "Random"
            self.btn_ayah.text = "Ayah"
            self.btn_hadith.text = "Hadith"
            self.btn_dhikr.text = "Dhikr"
            self.btn_dua.text = "Dua"

            self.btn_create.text = "Create New Status"

    def change_lang(self, lang):
        self.lang = lang
        self.refresh_ui()
        self.generate()

    def set_type(self, ctype):
        self.ctype = ctype
        self.generate()

    def generate(self, *args):
        try:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(SAVE_DIR, f"status_{now}.jpg")

            make_status(path, self.lang, self.ctype)

            scan_gallery(path)

            self.preview.source = path
            self.preview.reload()

            if self.lang == "ar":
                self.msg.text = "تم الحفظ داخل المعرض / Pictures/IslamStatusPro"
            else:
                self.msg.text = "Saved in Gallery / Pictures/IslamStatusPro"

        except Exception as e:
            self.msg.text = str(e)


IslamApp().run()
