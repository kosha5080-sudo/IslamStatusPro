import os
import random
import datetime
import shutil

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


Window.clearcolor = (0, 0, 0, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"

FONT_PATH = resource_find(FONT_FILE) or FONT_FILE
UI_FONT = None
try:
    LabelBase.register(name="ArabicFont", fn_regular=FONT_PATH)
    UI_FONT = "ArabicFont"
except:
    UI_FONT = None


AYAT_AR = [
"ألا بذكر الله تطمئن القلوب",
"إن مع العسر يسرا",
"فإن مع العسر يسرا",
"واستعينوا بالصبر والصلاة",
"وقل رب زدني علما",
"فاذكروني أذكركم",
"ادعوني أستجب لكم",
"ومن يتوكل على الله فهو حسبه",
"إن الله يحب المحسنين",
"إن الله مع الصابرين",
"والله خير الرازقين",
"لا تحزن إن الله معنا",
"إن ربي قريب مجيب",
"وما توفيقي إلا بالله",
"ورحمتي وسعت كل شيء",
"إن الله غفور رحيم",
"إن الله سميع بصير",
"إن الله عليم حكيم",
"إن الله لطيف خبير",
"إن الله واسع عليم",
"إن رحمة الله قريب من المحسنين",
"الله نور السماوات والأرض",
"ومن يتق الله يجعل له مخرجا",
"ومن يتق الله يجعل له من أمره يسرا",
"وقل اعملوا فسيرى الله عملكم",
"إن أكرمكم عند الله أتقاكم",
"إن الله يحب المتوكلين",
"إن الله يحب التوابين",
"إن الله لا يضيع أجر المحسنين",
"وكان فضل الله عليك عظيما",
"وما عند الله خير وأبقى",
"والآخرة خير وأبقى",
"ربنا آتنا في الدنيا حسنة",
"ربنا لا تزغ قلوبنا",
"ربنا تقبل منا",
"ربنا اغفر لنا ذنوبنا",
"ربنا ظلمنا أنفسنا",
"ربنا عليك توكلنا",
"إياك نعبد وإياك نستعين",
"الحمد لله رب العالمين",
"اهدنا الصراط المستقيم",
"مالك يوم الدين",
"وقل جاء الحق وزهق الباطل",
"ومن أحسن قولا ممن دعا إلى الله",
"سلام عليكم بما صبرتم",
"فصبر جميل",
"إن الله على كل شيء قدير",
"إن الله كان عليكم رقيبا",
"إن الله لا يخفى عليه شيء",
"وكان الله بكل شيء عليما"
]

AHADITH_AR = [
"إنما الأعمال بالنيات",
"الدين النصيحة",
"الكلمة الطيبة صدقة",
"تبسمك في وجه أخيك صدقة",
"لا تغضب",
"يسروا ولا تعسروا",
"بشروا ولا تنفروا",
"الطهور شطر الإيمان",
"خيركم من تعلم القرآن وعلمه",
"المسلم من سلم المسلمون من لسانه ويده",
"من حسن إسلام المرء تركه ما لا يعنيه",
"من دل على خير فله مثل أجر فاعله",
"أحب الأعمال إلى الله أدومها وإن قل",
"الراحمون يرحمهم الرحمن",
"اتق الله حيثما كنت",
"خالق الناس بخلق حسن",
"اتبع السيئة الحسنة تمحها",
"من لا يَرحم لا يُرحم",
"لا ضرر ولا ضرار",
"الحياء شعبة من الإيمان",
"المؤمن للمؤمن كالبنيان",
"خير الناس أنفعهم للناس",
"من تواضع لله رفعه",
"إن الله جميل يحب الجمال",
"إن الرفق لا يكون في شيء إلا زانه",
"أفشوا السلام بينكم",
"تهادوا تحابوا",
"إماطة الأذى عن الطريق صدقة",
"البر حسن الخلق",
"المسلم أخو المسلم",
"من ستر مسلما ستره الله",
"رحم الله رجلا سمحا",
"الدعاء هو العبادة",
"إن الله طيب لا يقبل إلا طيبا",
"احرص على ما ينفعك",
"استعن بالله ولا تعجز",
"من صمت نجا",
"خيركم خيركم لأهله",
"المؤمن القوي خير وأحب إلى الله",
"من كان يؤمن بالله فليقل خيرا أو ليصمت",
"لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
"اليد العليا خير من اليد السفلى",
"نعمتان مغبون فيهما كثير من الناس",
"الدنيا سجن المؤمن وجنة الكافر",
"من كان في حاجة أخيه كان الله في حاجته",
"السواك مطهرة للفم",
"طلب العلم فريضة",
"كل معروف صدقة",
"من غشنا فليس منا",
"إن الصدق يهدي إلى البر"
]

AZKAR_AR = [
"سبحان الله",
"الحمد لله",
"الله أكبر",
"لا إله إلا الله",
"سبحان الله وبحمده",
"سبحان الله العظيم",
"أستغفر الله العظيم",
"لا حول ولا قوة إلا بالله",
"حسبي الله ونعم الوكيل",
"اللهم صل وسلم على نبينا محمد",
"لا إله إلا أنت سبحانك إني كنت من الظالمين",
"رضيت بالله ربا وبالإسلام دينا",
"سبحان الله عدد خلقه",
"سبحان الله رضا نفسه",
"سبحان الله زنة عرشه",
"سبحان الله مداد كلماته",
"الحمد لله رب العالمين",
"الله أكبر كبيرا",
"الحمد لله كثيرا",
"سبحان الله بكرة وأصيلا",
"لا إله إلا الله وحده لا شريك له",
"له الملك وله الحمد",
"وهو على كل شيء قدير",
"أستغفر الله وأتوب إليه",
"يا حي يا قيوم برحمتك أستغيث",
"اللهم إنك عفو تحب العفو فاعف عني",
"رب اغفر لي وتب علي",
"سبحانك اللهم وبحمدك",
"أشهد أن لا إله إلا أنت",
"أعوذ بكلمات الله التامات من شر ما خلق",
"بسم الله توكلت على الله",
"اللهم بك أصبحنا وبك أمسينا",
"اللهم بك نحيا وبك نموت",
"اللهم أنت ربي لا إله إلا أنت",
"خلقتني وأنا عبدك",
"وأنا على عهدك ووعدك ما استطعت",
"أبوء لك بنعمتك علي",
"وأبوء بذنبي فاغفر لي",
"إنه لا يغفر الذنوب إلا أنت",
"اللهم عافني في بدني",
"اللهم عافني في سمعي",
"اللهم عافني في بصري",
"اللهم إني أعوذ بك من الكفر والفقر",
"اللهم إني أعوذ بك من عذاب القبر",
"حسبي الله لا إله إلا هو",
"عليه توكلت",
"وهو رب العرش العظيم",
"اللهم اجعلني من التوابين",
"اللهم اجعلني من المتطهرين",
"أستغفر الله الذي لا إله إلا هو الحي القيوم"
]

DOAA_AR = [
"اللهم اغفر لي ولوالدي",
"اللهم ارزقني من حيث لا أحتسب",
"اللهم ارزقني راحة القلب",
"اللهم ثبت قلبي على دينك",
"اللهم فرج همي ويسر أمري",
"اللهم اشف مرضانا ومرضى المسلمين",
"اللهم اجعل القرآن ربيع قلبي",
"اللهم اهدني واهد بي",
"اللهم ارزقني حسن الخاتمة",
"اللهم ارزقني الفردوس الأعلى",
"اللهم بارك لي في رزقي",
"اللهم اشرح صدري ويسر أمري",
"اللهم اجعل يومي خيرا وبركة",
"اللهم استر عيوبي واغفر ذنوبي",
"اللهم قني شر نفسي",
"اللهم اجعلني من الشاكرين",
"اللهم اجعلني من الذاكرين",
"اللهم لا تجعل الدنيا أكبر همي",
"اللهم أصلح لي شأني كله",
"اللهم ارزقني قلبا سليما",
"اللهم اجعلني سببا للخير",
"اللهم ارزقني علما نافعا",
"اللهم ارزقني عملا متقبلا",
"اللهم ارزقني رزقا طيبا",
"اللهم احفظ أهلي وأحبتي",
"اللهم اجبر خاطري جبرا يليق بكرمك",
"اللهم افتح لي أبواب رحمتك",
"اللهم افتح لي أبواب رزقك",
"اللهم ارزقني حسن الظن بك",
"اللهم اجعلني من عبادك الصالحين",
"اللهم ارفع قدري واشرح صدري",
"اللهم اجعل لي من كل هم فرجا",
"اللهم اجعل لي من كل ضيق مخرجا",
"اللهم طهر قلبي من الحقد",
"اللهم طهر لساني من الكذب",
"اللهم طهر عملي من الرياء",
"اللهم اجعلني مباركا أينما كنت",
"اللهم اكتب لي الخير حيث كان",
"اللهم رضني بما قسمت لي",
"اللهم أعني على ذكرك وشكرك",
"اللهم أعني على حسن عبادتك",
"اللهم ارزقني توبة نصوحا",
"اللهم اجعل قبري روضة من رياض الجنة",
"اللهم قني عذاب النار",
"اللهم صل وسلم على نبينا محمد",
"اللهم ارحم موتانا وموتى المسلمين",
"اللهم تقبل دعائي",
"اللهم لا تردني خائبا",
"اللهم اجعلها صدقة جارية",
"اللهم ارزقني الطمأنينة"
]

AYAT_EN = [
"Indeed, with hardship comes ease.",
"Remember Allah often.",
"Call upon Me; I will respond.",
"Allah is with the patient.",
"Allah loves the doers of good.",
] * 10

AHADITH_EN = [
"A good word is charity.",
"Actions are judged by intentions.",
"Do not become angry.",
"Make things easy.",
"Purity is half of faith.",
] * 10

AZKAR_EN = [
"Glory be to Allah.",
"All praise is due to Allah.",
"I seek forgiveness from Allah.",
"Allah is the Greatest.",
"There is no god but Allah.",
] * 10

DOAA_EN = [
"O Allah guide me.",
"O Allah forgive me.",
"O Allah grant me peace.",
"O Allah bless my day.",
"O Allah accept my prayer.",
] * 10


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
        months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
        days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
        return f"{ar(days[today.weekday()])} - {today.day} {ar(months[today.month - 1])} {today.year}"
    return today.strftime("%A - %d %B %Y")


def draw_text(draw, x, y, text, font, color, lang="ar", plain=False):
    if lang == "ar" and not plain:
        text = ar(text)
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


def request_android_permissions():
    try:
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
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
        request_android_permissions()

        self.lang = "ar"
        self.ctype = "random"

        self.temp_dir = self.user_data_dir
        os.makedirs(self.temp_dir, exist_ok=True)
        self.temp_path = os.path.join(self.temp_dir, "preview_status.jpg")

        root = BoxLayout(orientation="vertical", spacing=8, padding=8)

        self.preview = Image(size_hint=(1, 0.58), allow_stretch=True, keep_ratio=True)

        self.msg = Label(text=ui_ar("جاهز"), size_hint=(1, 0.05), font_size=16)
        if UI_FONT:
            self.msg.font_name = UI_FONT

        row1 = BoxLayout(size_hint=(1, 0.08), spacing=5)
        self.btn_ar = Button(text="")
        self.btn_en = Button(text="")
        self.btn_ar.bind(on_press=lambda x: self.change_lang("ar"))
        self.btn_en.bind(on_press=lambda x: self.change_lang("en"))
        row1.add_widget(self.btn_ar)
        row1.add_widget(self.btn_en)

        row2 = BoxLayout(size_hint=(1, 0.08), spacing=5)
        self.btn_random = Button(text="")
        self.btn_ayah = Button(text="")
        self.btn_hadith = Button(text="")
        self.btn_dhikr = Button(text="")
        self.btn_dua = Button(text="")

        self.btn_random.bind(on_press=lambda x: self.set_type("random"))
        self.btn_ayah.bind(on_press=lambda x: self.set_type("ayah"))
        self.btn_hadith.bind(on_press=lambda x: self.set_type("hadith"))
        self.btn_dhikr.bind(on_press=lambda x: self.set_type("dhikr"))
        self.btn_dua.bind(on_press=lambda x: self.set_type("dua"))

        for b in [self.btn_random, self.btn_ayah, self.btn_hadith, self.btn_dhikr, self.btn_dua]:
            row2.add_widget(b)

        self.btn_create = Button(text="", size_hint=(1, 0.1), font_size=20)
        self.btn_save = Button(text="", size_hint=(1, 0.1), font_size=20)

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

    def apply_font(self):
        if UI_FONT:
            for b in [
                self.btn_ar, self.btn_en, self.btn_random, self.btn_ayah,
                self.btn_hadith, self.btn_dhikr, self.btn_dua,
                self.btn_create, self.btn_save
            ]:
                b.font_name = UI_FONT
            self.msg.font_name = UI_FONT

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
            self.preview.source = ""
            self.preview.source = self.temp_path
            self.preview.reload()
            self.msg.text = ui_ar("تم إنشاء الصورة") if self.lang == "ar" else "Image created"
        except Exception as e:
            self.msg.text = "Error: " + str(e)

    def save_to_gallery(self, *args):
        try:
            os.makedirs(SAVE_DIR, exist_ok=True)
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            final_path = os.path.join(SAVE_DIR, f"islamic_status_{now}.jpg")
            shutil.copy2(self.temp_path, final_path)
            scan_gallery(final_path)
            self.msg.text = ui_ar("تم الحفظ في المعرض") if self.lang == "ar" else "Saved to Gallery"
        except Exception as e:
            self.msg.text = "Save Error: " + str(e)


IslamApp().run()
