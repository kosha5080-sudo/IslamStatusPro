import os, shutil
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.06, 0.05, 1)

STATUS_PATHS = [
    "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/.Statuses",
    "/storage/emulated/0/WhatsApp/Media/.Statuses",
]

SAVE_PATH = "/storage/emulated/0/Download/IslamStatusPro"

class IslamStatusPro(App):
    def build(self):
        self.files = []

        root = BoxLayout(orientation="vertical", padding=12, spacing=10)

        title = Label(
            text="Islam Status Pro VIP",
            font_size=26,
            size_hint_y=None,
            height=55,
            color=(1, 0.82, 0.35, 1)
        )

        self.info = Label(
            text="Press Refresh to load WhatsApp statuses",
            font_size=17,
            size_hint_y=None,
            height=40,
            color=(1, 1, 1, 1)
        )

        btns = BoxLayout(size_hint_y=None, height=55, spacing=8)

        refresh = Button(text="Refresh", font_size=18, background_color=(0.1, 0.35, 0.18, 1))
        save_all = Button(text="Save All", font_size=18, background_color=(0.55, 0.38, 0.08, 1))

        refresh.bind(on_press=lambda x: self.load_statuses())
        save_all.bind(on_press=lambda x: self.save_all())

        btns.add_widget(refresh)
        btns.add_widget(save_all)

        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.grid)

        root.add_widget(title)
        root.add_widget(self.info)
        root.add_widget(btns)
        root.add_widget(scroll)

        self.request_permissions()
        return root

    def request_permissions(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.READ_EXTERNAL_STORAGE,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_MEDIA_IMAGES,
                Permission.READ_MEDIA_VIDEO,
            ])
        except Exception:
            pass

    def get_status_dir(self):
        for path in STATUS_PATHS:
            if os.path.exists(path):
                return path
        return None

    def load_statuses(self):
        self.grid.clear_widgets()
        self.files = []

        path = self.get_status_dir()
        if not path:
            self.info.text = "WhatsApp status folder not found"
            return

        for name in os.listdir(path):
            if name.lower().endswith((".jpg", ".jpeg", ".png", ".mp4")):
                self.files.append(os.path.join(path, name))

        self.files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        if not self.files:
            self.info.text = "No statuses found. Open WhatsApp statuses first."
            return

        self.info.text = f"Found {len(self.files)} statuses"

        for file_path in self.files:
            card = BoxLayout(orientation="vertical", size_hint_y=None, height=360, spacing=6)

            if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
                img = Image(source=file_path, allow_stretch=True, keep_ratio=True, size_hint_y=None, height=260)
                card.add_widget(img)
            else:
                card.add_widget(Label(
                    text="VIDEO STATUS\n" + os.path.basename(file_path),
                    font_size=18,
                    size_hint_y=None,
                    height=260,
                    color=(1, 1, 1, 1)
                ))

            save_btn = Button(
                text="Save This Status",
                font_size=18,
                size_hint_y=None,
                height=55,
                background_color=(0.12, 0.32, 0.18, 1)
            )
            save_btn.bind(on_press=lambda x, p=file_path: self.save_file(p))

            card.add_widget(save_btn)
            self.grid.add_widget(card)

    def save_file(self, file_path):
        os.makedirs(SAVE_PATH, exist_ok=True)
        dest = os.path.join(SAVE_PATH, os.path.basename(file_path))
        shutil.copy2(file_path, dest)
        self.info.text = "Saved to Download/IslamStatusPro"

    def save_all(self):
        if not self.files:
            self.info.text = "No statuses to save"
            return

        os.makedirs(SAVE_PATH, exist_ok=True)
        for f in self.files:
            shutil.copy2(f, os.path.join(SAVE_PATH, os.path.basename(f)))

        self.info.text = f"Saved {len(self.files)} statuses"

IslamStatusPro().run()
