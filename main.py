import os
import random
import datetime
import shutil

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

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
TEMP_DIR = "/storage/emulated/0/Android/data/com.islam.halatwatssislamia/files"


AYAT_AR = ["ألا بذكر الله تطمئن القلوب", "إن مع العسر يسرا", "ادعوني أستجب لكم"] * 17
AHADITH_AR = ["الكلمة الطيبة صدقة", "إنما الأعمال بالنيات", "تبسمك في وجه أخيك صدقة"] * 17
AZKAR_AR = ["سبحان الله وبحمده", "أستغفر الله العظيم", "لا إله إلا الله"] * 17
DOAA_AR = ["اللهم اغفر لي ولوالدي", "اللهم ارزقني راحة القلب", "اللهم ثبت قلبي على دينك"] * 17

AYAT_EN = ["Indeed, with hardship comes ease.", "Remember Allah often.", "Call upon Me; I will respond."] * 17
AHADITH_EN = ["A good word is charity.", "Actions are judged by intentions.", "Do not become angry."] * 17
AZKAR_EN = ["Glory be to Allah.", "All praise is due to Allah.", "I seek forgiveness from Allah."] * 17
DOAA_EN = ["O Allah guide me.", "O Allah forgive me.", "O Allah grant me peace."] * 17


def ar(text):
    if arabic_reshaper:
        return arabic_reshaper.reshape(text)[::-1]
    return text[::-1]


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
        months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
        days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
        return f"{today.year} {ar(months[today.month-1])} {today.day} - {ar(days[today.weekday()])}"
    return today.strftime("%A - %d %B %Y")


def draw_text(draw, x, y, text, font, color, lang="ar", plain=False):
    if lang == "ar" and not plain:
        text = ar(text)
    draw.text((x, y), text, fill=color, font=font, anchor="mm")


def wrap_text(text, limit=20):
    words = text.split()
    lines, line = [], ""
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


def get_content(lang, ctype):
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
        ctype = random.choice(["ayah", "hadith", "dhikr", "dua"])

    return data[ctype]


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


def make_status(path, lang="ar", ctype="random"):
    w, h = 1080, 1920

    bg = (0, 22, 13)
    gold = (210, 170, 80)
    white = (245, 245, 245)
    dark = (15, 15, 15)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(58)
    big_font = get_font(48)
    med_font = get_font(34)
    small_font = get_font(28)

    title = "حالات واتس اب اسلاميه" if lang == "ar" else "Islamic WhatsApp Status"
    subtitle = "تصميم يومي متجدد" if lang == "ar" else "Daily New Design"
    footer = "اللهم اجعلها صدقة جارية" if lang == "ar" else "May it be charity"

    kind, text, ref = get_content(lang, ctype)

    draw.rounded_rectangle((40, 40, 1040, 1880), radius=45, outline=gold, width=4)
    draw.rounded_rectangle((80, 90, 1000, 340), radius=25, outline=gold, width=3)

    draw_text(draw, 540, 155, title, title_font, gold, lang)
    draw_text(draw, 540, 235, subtitle, med_font, white, lang)
    draw_text(draw, 540, 300, date_text(lang), small_font, gold, lang, plain=True)

    draw.rounded_rectangle((130, 470, 950, 1180), radius=35, fill=dark, outline=gold, width=3)

    draw_text(draw, 540, 560, kind, big_font, gold, lang)

    y = 720
    for line in wrap_text(text, 18 if lang == "ar" else 26):
        draw_text(draw, 540, y, line, big_font, white, lang)
        y += 80

    draw_text(draw, 540, 1080, ref, med_font, gold, lang)

    draw_text(draw, 540, 1320, footer, med_font, white, lang)

    draw.rounded_rectangle((160, 1450, 920, 1560), radius=22, outline=gold, width=3)
    draw_text(draw, 540, 1505, date_text(lang), med_font, white, lang, plain=True)

    img.save(path, quality=95)


class IslamApp(App):
    def build(self):
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.makedirs(SAVE_DIR, exist_ok=True)

        self.lang = "ar"
        self.ctype = "random"
        self.temp_path = os.path.join(TEMP_DIR, "preview_status.jpg")

        root = BoxLayout(orientation="vertical", spacing=8, padding=8)

        self.preview = Image(size_hint=(1, 0.58), allow_stretch=True, keep_ratio=True)
        self.msg = Label(text="جاهز", size_hint=(1, 0.05), font_size=16)

        row1 = BoxLayout(size_hint=(1, 0.08), spacing=5)
        self.btn_ar = Button(text="العربية")
        self.btn_en = Button(text="English")
        self.btn_ar.bind(on_press=lambda x: self.change_lang("ar"))
        self.btn_en.bind(on_press=lambda x: self.change_lang("en"))
        row1.add_widget(self.btn_ar)
        row1.add_widget(self.btn_en)

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

        for b in [self.btn_random, self.btn_ayah, self.btn_hadith, self.btn_dhikr, self.btn_dua]:
            row2.add_widget(b)

        self.btn_create = Button(text="إنشاء حالة جديدة", size_hint=(1, 0.1), font_size=20)
        self.btn_save = Button(text="حفظ في المعرض", size_hint=(1, 0.1), font_size=20)

        self.btn_create.bind(on_press=self.generate)
        self.btn_save.bind(on_press=self.save_to_gallery)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(row1)
        root.add_widget(row2)
        root.add_widget(self.btn_create)
        root.add_widget(self.btn_save)

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
            self.btn_save.text = "حفظ في المعرض"
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

    def change_lang(self, lang):
        self.lang = lang
        self.refresh_ui()
        self.generate()

    def set_type(self, ctype):
        self.ctype = ctype
        self.generate()

    def generate(self, *args):
        try:
            make_status(self.temp_path, self.lang, self.ctype)
            self.preview.source = self.temp_path
            self.preview.reload()
            self.msg.text = "تم إنشاء الصورة" if self.lang == "ar" else "Image created"
        except Exception as e:
            self.msg.text = str(e)

    def save_to_gallery(self, *args):
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = os.path.join(SAVE_DIR, f"islamic_status_{now}.jpg")
            shutil.copy2(self.temp_path, final_path)
            scan_gallery(final_path)
            self.msg.text = "تم الحفظ في المعرض" if self.lang == "ar" else "Saved to Gallery"
        except Exception as e:
            self.msg.text = "Save Error: " + str(e)


IslamApp().run()
