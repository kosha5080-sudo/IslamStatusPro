from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class IslamicStatusApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        root.add_widget(Label(
            text="حالات واتس اب اسلاميه",
            font_size=28
        ))

        root.add_widget(Label(
            text="النسخة القادمة: 3 تصميمات + تاريخ يومي + آية/حديث/دعاء/ذكر",
            font_size=18
        ))

        root.add_widget(Button(
            text="إنشاء حالة اليوم",
            font_size=22,
            size_hint_y=None,
            height=70
        ))

        root.add_widget(Button(
            text="حفظ الصورة",
            font_size=22,
            size_hint_y=None,
            height=70
        ))

        return root

IslamicStatusApp().run()
