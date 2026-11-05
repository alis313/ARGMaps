"""Run after `npx cap add android`: permissions, portrait lock, launcher icons."""
import re, sys, shutil, pathlib
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
res = root / "android/app/src/main/res"
mf = root / "android/app/src/main/AndroidManifest.xml"

# 1) permissions + portrait + hardware features
s = mf.read_text(encoding="utf-8")
perms = """    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.location.gps" android:required="false" />
    <uses-feature android:name="android.hardware.sensor.compass" android:required="false" />
"""
if "ACCESS_FINE_LOCATION" not in s:
    s = s.replace("<uses-permission android:name=\"android.permission.INTERNET\" />",
                  "<uses-permission android:name=\"android.permission.INTERNET\" />\n" + perms)
if "screenOrientation" not in s:
    s = s.replace('android:launchMode="singleTask"', 'android:launchMode="singleTask"\n            android:screenOrientation="portrait"')
mf.write_text(s, encoding="utf-8")

# 2) launcher icons from the app icon (legacy square + round; adaptive removed)
src = Image.open(root / "www/icon-512.png").convert("RGBA")
sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for d, px in sizes.items():
    folder = res / f"mipmap-{d}"
    folder.mkdir(parents=True, exist_ok=True)
    im = src.resize((px, px), Image.LANCZOS)
    im.save(folder / "ic_launcher.png")
    im.save(folder / "ic_launcher_round.png")
    fg = folder / "ic_launcher_foreground.png"
    if fg.exists():
        fg.unlink()
shutil.rmtree(res / "mipmap-anydpi-v26", ignore_errors=True)

# 3) dark splash/background colour
colors = res / "values/colors.xml"
colors.write_text('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                  '    <color name="colorPrimary">#191919</color>\n'
                  '    <color name="colorPrimaryDark">#191919</color>\n'
                  '    <color name="colorAccent">#8AB4F8</color>\n</resources>\n', encoding="utf-8")
print("customized")
