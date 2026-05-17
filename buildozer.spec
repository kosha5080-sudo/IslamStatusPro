[app]

title = Islamic Status Pro
package.name = islamicstatuspro
package.domain = com.islamstatus
source.dir = .
source.include_exts = py,png,jpg,kv,ttf
version = 1.0
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

android.release_artifact = aab
android.keystore = release.keystore
android.keyalias = islamkey
android.keystore_passwd = 123456
android.keyalias_passwd = 123456

[buildozer]

log_level = 2
warn_on_root = 1
