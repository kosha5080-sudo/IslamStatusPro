[app]

title = Islamic WhatsApp Status
package.name = halatwatssislamia
package.domain = com.islam

source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 2.0

requirements = python3,kivy,pillow,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
