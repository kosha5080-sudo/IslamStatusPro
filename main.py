import os, random, datetime, json
from PIL import Image as PILImage, ImageDraw, ImageFont

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.resources import resource_find

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
except:
    arabic_reshaper = None
    get_display = None

Window.clearcolor = (0.02, 0.025, 0.02, 1)

FONT_FILE = "arabic.ttf"
SAVE_DIR = "/storage/emulated/0/Pictures/IslamStatusPro"
SETTINGS_FILE = "settings.json"

APP_TITLE_AR = "حالات واتس اب اسلاميه"
APP_TITLE_EN = "Islamic WhatsApp Status"

AYAT_AR = [
"ألا بذكر الله تطمئن القلوب",
"إن مع العسر يسرا",
"واستعينوا بالصبر والصلاة",
"وقل رب زدني علما",
"إن الله مع الصابرين",
"فاذكروني أذكركم",
"والله خير الرازقين",
"ادعوني أستجب لكم",
"ومن يتوكل على الله فهو حسبه",
"إن الله يحب المحسنين",
"إن الله غفور رحيم",
"ورحمتي وسعت كل شيء",
"لا تحزن إن الله معنا",
"رب اشرح لي صدري",
"وما توفيقي إلا بالله",
"إن ربي قريب مجيب",
"سلام عليكم بما صبرتم",
"والله يحب الصابرين",
"إن الله يحب المتوكلين",
"وكان الله على كل شيء قديرا",
"عسى الله أن يأتي بالفتح",
"فصبر جميل",
"إن الله لطيف خبير",
"إن الله سميع بصير",
"إن الله واسع عليم",
"ومن يتق الله يجعل له مخرجا",
"وقل اعملوا فسيرى الله عملكم",
"إن أكرمكم عند الله أتقاكم",
"فإن مع العسر يسرا",
"وهو أرحم الراحمين",
"ربنا آتنا في الدنيا حسنة",
"إن الله يحب التوابين",
"إن الله لا يضيع أجر المحسنين",
"وكان فضل الله عليك عظيما",
"وهو على كل شيء وكيل",
"إن الله عليم حكيم",
"إن رحمة الله قريب من المحسنين",
"الله نور السماوات والأرض",
"وما عند الله خير وأبقى",
"رب زدني علما",
"والآخرة خير وأبقى",
"ربنا لا تزغ قلوبنا",
"ربنا تقبل منا",
"ربنا اغفر لنا ذنوبنا",
"ربنا ظلمنا أنفسنا",
"ربنا عليك توكلنا",
"إياك نعبد وإياك نستعين",
"الحمد لله رب العالمين",
"مالك يوم الدين",
"اهدنا الصراط المستقيم"
]

DOAA_AR = [
"اللهم اغفر لي ولوالدي",
"اللهم ارزقني من حيث لا أحتسب",
"اللهم فرج همي ويسر أمري",
"اللهم اشف مرضانا ومرضى المسلمين",
"اللهم ثبت قلبي على دينك",
"اللهم ارزقني السعادة والطمأنينة",
"اللهم اجعل القرآن ربيع قلبي",
"اللهم اهدني واهد بي",
"اللهم حسن خاتمتي",
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
"اللهم ارزقني راحة القلب",
"اللهم طهر قلبي من الحقد",
"اللهم طهر لساني من الكذب",
"اللهم طهر عملي من الرياء",
"اللهم اجعلني مباركا أينما كنت",
"اللهم اكتب لي الخير حيث كان",
"اللهم رضني بما قسمت لي",
"اللهم اجعلني ممن توكل عليك فكفيته",
"اللهم أعني على ذكرك وشكرك",
"اللهم أعني على حسن عبادتك",
"اللهم ارزقني توبة نصوحا",
"اللهم اجعل قبري روضة من رياض الجنة",
"اللهم قني عذاب النار",
"اللهم صل وسلم على نبينا محمد",
"اللهم ارحم موتانا وموتى المسلمين",
"اللهم تقبل دعائي",
"اللهم لا تردني خائبا"
]

AZKAR_AR = [
"سبحان الله",
"الحمد لله",
"الله أكبر",
"لا إله إلا الله",
"سبحان الله وبحمده",
"سبحان الله العظيم",
"لا حول ولا قوة إلا بالله",
"أستغفر الله العظيم",
"اللهم صل وسلم على نبينا محمد",
"حسبي الله ونعم الوكيل",
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
"لا إله إلا الله محمد رسول الله",
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
"اللهم اجعلني من المتطهرين"
]

AHADITH_AR = [
"إنما الأعمال بالنيات",
"الدين النصيحة",
"الكلمة الطيبة صدقة",
"تبسمك في وجه أخيك صدقة",
"من حسن إسلام المرء تركه ما لا يعنيه",
"لا تغضب",
"يسروا ولا تعسروا",
"بشروا ولا تنفروا",
"الطهور شطر الإيمان",
"المسلم من سلم المسلمون من لسانه ويده",
"خيركم من تعلم القرآن وعلمه",
"من كان يؤمن بالله واليوم الآخر فليقل خيرا أو ليصمت",
"لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
"اتق الله حيثما كنت",
"اتبع السيئة الحسنة تمحها",
"خالق الناس بخلق حسن",
"الراحمون يرحمهم الرحمن",
"أحب الأعمال إلى الله أدومها وإن قل",
"من دل على خير فله مثل أجر فاعله",
"من لا يشكر الناس لا يشكر الله",
"المؤمن للمؤمن كالبنيان",
"احرص على ما ينفعك",
"استعن بالله ولا تعجز",
"لا ضرر ولا ضرار",
"الدال على الخير كفاعله",
"من صمت نجا",
"الحياء شعبة من الإيمان",
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
"إن الله يحب إذا عمل أحدكم عملا أن يتقنه",
"طلب العلم فريضة",
"خيركم خيركم لأهله",
"السواك مطهرة للفم",
"الدعاء هو العبادة",
"إن الله طيب لا يقبل إلا طيبا",
"من كان في حاجة أخيه كان الله في حاجته",
"الكلمة الطيبة صدقة",
"رحم الله رجلا سمحا",
"اللهم أعني على ذكرك وشكرك",
"لا يؤمن أحدكم حتى أكون أحب إليه",
"المؤمن القوي خير وأحب إلى الله",
"إن الصدق يهدي إلى البر"
]

# English content
AYAT_EN = [
"Indeed, with hardship comes ease.",
"Remember Allah often so you may succeed.",
"Verily, in the remembrance of Allah do hearts find rest.",
"Seek help through patience and prayer.",
"My success is only by Allah.",
"And whoever relies upon Allah, He is sufficient for him.",
"Call upon Me; I will respond to you.",
"Allah loves the doers of good.",
"Allah is with the patient.",
"Say: My Lord, increase me in knowledge."
] * 5

DOAA_EN = [
"O Allah, forgive me and my parents.",
"O Allah, grant me peace of heart.",
"O Allah, make this day blessed.",
"O Allah, guide me and guide through me.",
"O Allah, grant me a good ending.",
"O Allah, open the doors of mercy for me.",
"O Allah, provide for me from where I do not expect.",
"O Allah, make the Quran the spring of my heart.",
"O Allah, relieve my worries.",
"O Allah, accept my prayers."
] * 5

AZKAR_EN = [
"Glory be to Allah.",
"All praise is due to Allah.",
"Allah is the Greatest.",
"There is no god but Allah.",
"Glory be to Allah and praise be to Him.",
"Glory be to Allah the Great.",
"There is no power except with Allah.",
"I seek forgiveness from Allah.",
"O Allah, send blessings upon Muhammad.",
"Allah is sufficient for me."
] * 5

AHADITH_EN = [
"Actions are judged by intentions.",
"Religion is sincere advice.",
"A good word is charity.",
"Smiling at your brother is charity.",
"Do not become angry.",
"Make things easy, not difficult.",
"Give glad tidings, do not repel.",
"Purity is half of faith.",
"The best of you are those who learn and teach the Quran.",
"Whoever believes in Allah should speak good or remain silent."
] * 5

def reshape_ar(txt):
    if arabic_reshaper and get_display:
        return get_display(arabic_reshaper.reshape(txt))
    return txt

def is_arabic(lang):
    return lang == "ar"

def get_font(size):
    p = resource_find(FONT_FILE)
    if p:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

def draw_text(draw, x, y, text, font, color, lang="ar"):
    if is_arabic(lang):
        text = reshape_ar(text)
    draw.text((x, y), text, font=font, fill=color, anchor="mm")

def date_text(lang):
    today = datetime.date.today()
    if lang == "ar":
        months = ["يناير","فبراير","مارس","أبريل","مايو","يونيو","يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
        days = ["الإثنين","الثلاثاء","الأربعاء","الخميس","الجمعة","السبت","الأحد"]
        return f"{days[today.weekday()]} - {today.day} {months[today.month-1]} {today.year}"
    return today.strftime("%A - %d %B %Y")

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

def choose_content(lang, ctype):
    if lang == "ar":
        data = {
            "ayah": ("آية اليوم", AYAT_AR, "آية قرآنية"),
            "hadith": ("حديث اليوم", AHADITH_AR, "حديث شريف"),
            "dhikr": ("ذكر اليوم", AZKAR_AR, "ذكر"),
            "dua": ("دعاء اليوم", DOAA_AR, "دعاء"),
        }
    else:
        data = {
            "ayah": ("Daily Verse", AYAT_EN, "Quranic verse"),
            "hadith": ("Daily Hadith", AHADITH_EN, "Hadith"),
            "dhikr": ("Daily Dhikr", AZKAR_EN, "Dhikr"),
            "dua": ("Daily Dua", DOAA_EN, "Dua"),
        }

    if ctype == "random":
        ctype = random.choice(["ayah", "hadith", "dhikr", "dua"])

    title, arr, ref = data[ctype]
    return title, random.choice(arr), ref

def theme_colors(design):
    if design == 1:
        return (4,20,14), (15,15,15), (212,170,80), (245,245,240)
    if design == 2:
        return (238,227,206), (252,246,232), (150,105,45), (25,55,35)
    return (5,6,7), (18,18,18), (225,178,70), (245,245,245)

def make_image(path, lang="ar", ctype="random", design=1):
    w, h = 1080, 1920
    bg, card, gold, white = theme_colors(design)

    img = PILImage.new("RGB", (w, h), bg)
    draw = ImageDraw.Draw(img)

    title_font = get_font(58)
    mid = get_font(48)
    small = get_font(34)
    tiny = get_font(28)

    app_title = APP_TITLE_AR if lang == "ar" else APP_TITLE_EN
    subtitle = "تصميم يومي متجدد" if lang == "ar" else "Daily Islamic Status"
    footer = "اللهم اجعلها صدقة جارية" if lang == "ar" else "May it be ongoing charity"

    kind, text, ref = choose_content(lang, ctype)

    draw.rounded_rectangle((40, 40, w-40, h-40), radius=45, outline=gold, width=4)
    draw.rounded_rectangle((80, 90, w-80, 350), radius=30, outline=gold, width=3)

    draw_text(draw, w/2, 150, app_title, title_font, gold, lang)
    draw_text(draw, w/2, 235, subtitle, small, white, lang)
    draw_text(draw, w/2, 305, date_text(lang), tiny, gold, lang)

    draw.rounded_rectangle((130, 470, w-130, 1180), radius=35, fill=card, outline=gold, width=3)

    draw_text(draw, w/2, 560, kind, mid, gold, lang)

    y = 710
    limit = 18 if lang == "ar" else 24
    for line in wrap_text(text, limit):
        draw_text(draw, w/2, y, line, mid, white, lang)
        y += 82

    draw_text(draw, w/2, 1085, ref, small, gold, lang)
    draw_text(draw, w/2, 1320, footer, small, white, lang)

    draw.rounded_rectangle((150, 1450, w-150, 1560), radius=25, outline=gold, width=3)
    draw_text(draw, w/2, 1505, date_text(lang), small, white, lang)

    img.save(path, quality=95)

class MyApp(App):
    def build(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.lang = "ar"
        self.ctype = "random"
        self.design = 1
        self.last_path = ""

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        self.preview = Image(size_hint=(1, 0.62), allow_stretch=True, keep_ratio=True)
        self.msg = Label(text=reshape_ar("جاهز"), size_hint=(1, 0.05), font_size=16)

        lang_row = BoxLayout(size_hint=(1, 0.07), spacing=5)
        b_ar = Button(text="Arabic", font_size=15)
        b_en = Button(text="English", font_size=15)
        b_ar.bind(on_press=lambda x: self.set_lang("ar"))
        b_en.bind(on_press=lambda x: self.set_lang("en"))
        lang_row.add_widget(b_ar)
        lang_row.add_widget(b_en)

        type_row = BoxLayout(size_hint=(1, 0.07), spacing=5)
        types = [
            ("Random", "random"),
            ("Ayah", "ayah"),
            ("Hadith", "hadith"),
            ("Dhikr", "dhikr"),
            ("Dua", "dua"),
        ]
        for label, val in types:
            b = Button(text=label, font_size=13)
            b.bind(on_press=lambda x, v=val: self.set_type(v))
            type_row.add_widget(b)

        design_row = BoxLayout(size_hint=(1, 0.07), spacing=5)
        for i in [1, 2, 3]:
            b = Button(text=f"Design {i}", font_size=14)
            b.bind(on_press=lambda x, d=i: self.set_design(d))
            design_row.add_widget(b)

        create_btn = Button(text="Create New Status", size_hint=(1, 0.1), font_size=20)
        create_btn.bind(on_press=self.generate)

        root.add_widget(self.preview)
        root.add_widget(self.msg)
        root.add_widget(lang_row)
        root.add_widget(type_row)
        root.add_widget(design_row)
        root.add_widget(create_btn)

        self.generate()
        return root

    def set_lang(self, lang):
        self.lang = lang
        self.generate()

    def set_type(self, ctype):
        self.ctype = ctype
        self.generate()

    def set_design(self, design):
        self.design = design
        self.generate()

    def generate(self, *args):
        try:
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = os.path.join(SAVE_DIR, f"status_{now}.jpg")
            make_image(path, self.lang, self.ctype, self.design)
            self.last_path = path
            self.preview.source = path
            self.preview.reload()
            self.msg.text = "Saved in Pictures/IslamStatusPro"
        except Exception as e:
            self.msg.text = str(e)

MyApp().run()
