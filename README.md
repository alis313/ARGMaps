# ARG — Android app (Geologix)

Underground Utilities AR System. This repo wraps the ARG web app (`www/`) in a native Android shell using Capacitor.
Everything still runs on the phone; no server.

## Get the APK (no Android Studio needed)
1. Create a new GitHub repo (e.g. `arg-android`) and upload ALL files of this folder (keep the `.github` folder).
2. Open the repo → **Actions** → **Build ARG APK** → wait for the green check (about 5–8 minutes). It also runs on every push to `main`.
3. Open the finished run → **Artifacts** → download **ARG-apk** → unzip → `app-debug.apk`.
4. Copy it to the phone, open it, allow "Install unknown apps", install.
5. On first launch allow **Camera** and **Location** (precise).

## Updating the app
Edit files in `www/` (it is the same code as the PWA), commit, and Actions builds a new APK.
To install over the old one, keep the same repo (the debug signing key is generated per build run,
so if Android refuses to update, uninstall first — export a backup from Settings before that).

## Build on your own computer (optional)
Needs Node 20, JDK 21, Android Studio/SDK.
    npm install
    npx cap add android
    python3 scripts/customize-android.py
    npx cap sync android
    cd android && ./gradlew assembleDebug
APK: android/app/build/outputs/apk/debug/app-debug.apk
