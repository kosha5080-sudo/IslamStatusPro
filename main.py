from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

Window.clearcolor = (0.1, 0.1, 0.1, 1)

class MainApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.input = TextInput(
            hint_text='اكتب الحالة هنا',
            multiline=True,
            font_size=24,
            size_hint=(1, .6)
        )

        self.label = Label(
            text='الحالة ستظهر هنا',
            font_size=28
        )

        btn = Button(
            text='عرض الحالة',
            font_size=24,
            size_hint=(1, .2)
        )

        btn.bind(on_press=self.show_text)

        layout.add_widget(self.input)
        layout.add_widget(btn)
        layout.add_widget(self.label)

        return layout

    def show_text(self, instance):
        self.label.text = self.input.text

MainApp().run()
