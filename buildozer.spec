[app]

title = حالات واتس اب اسلاميه
package.name = halatwatssislamia
package.domain = com.islam

source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.0

requirements = python3,kivy,pillow,arabic-reshaper
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO

android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 25b
android.accept_sdk_license = True
android.skip_update = False

[buildozer]

log_level = 2
warn_on_root = 1
