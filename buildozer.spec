[app]

title = حالات واتس اب اسلاميه
package.name = halatwatssislamia
package.domain = com.islam

source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 5.1

requirements = python3,kivy,pillow,arabic-reshaper
orientation = portrait
fullscreen = 0

icon.filename = icon.png
android.adaptive_icon_foreground = icon_fg.png
android.adaptive_icon_background = icon_bg.png

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
