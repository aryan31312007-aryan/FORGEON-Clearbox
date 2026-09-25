# 📱 FORGEON ClearBox v2.0 - Android APK Conversion Guide

This project is now fully configured as a **Mobile Progressive Web App (PWA)** and **Native Android Application (APK)** with low-latency Web Audio DSP support.

---

## 🛠️ What Has Been Configured & Created

1. **Responsive Mobile UI & Touch Support ([index.html](file:///c:/testing%20folder%20microcontroller/index.html))**:
   - Stacked single-column visualizer layout on mobile devices (`@media (max-width: 768px)`).
   - Touch-optimized slider controls and preset buttons.
   - Fullscreen viewport settings (`viewport-fit=cover`, dark theme `#0B0F17`).

2. **Mobile App Icons & Manifest**:
   - App Launcher Icons: `icon-192.png`, `icon-512.png`, `favicon.ico`.
   - Web App Manifest: [manifest.json](file:///c:/testing%20folder%20microcontroller/manifest.json).
   - Offline Service Worker: [sw.js](file:///c:/testing%20folder%20microcontroller/sw.js).

3. **Android Native Configuration**:
   - Microphone Permissions added: `<uses-permission android:name="android.permission.RECORD_AUDIO" />`.
   - Capacitor Configuration: [capacitor.config.json](file:///c:/testing%20folder%20microcontroller/capacitor.config.json).
   - Node Web Bundler Script: [build_app.js](file:///c:/testing%20folder%20microcontroller/build_app.js).

4. **1-Click Cloud APK Build Workflow**:
   - GitHub Actions Pipeline: [.github/workflows/android.yml](file:///c:/testing%20folder%20microcontroller/.github/workflows/android.yml).

---

## 🚀 3 Ways to Get Your `.apk` File

### Method 1: Web2APK / PWABuilder (Instant 1-Click APK — No Installation Required)
1. Host or deploy your `www/` folder (or upload `index.html` to Vercel / Netlify / GitHub Pages).
2. Go to **[PWABuilder.com](https://www.pwabuilder.com)** or **[Web2APK](https://www.web2apk.com)**.
3. Paste your URL or upload the web package.
4. Click **Generate Android Package (.apk)** and download your ready-to-install Android APK file!

---

### Method 2: GitHub Actions (Free 1-Click Cloud Build)
1. Push this workspace code to your GitHub Repository.
2. Go to the **Actions** tab in your GitHub Repository.
3. The workflow **"Build Android APK"** will run automatically in ~2 minutes.
4. Click on the completed run and download **`ClearBox-DSP-v2.0.apk`** under Artifacts!

---

### Method 3: Local Android Studio / Capacitor Build (Offline)
If you have Android Studio installed on your computer:
```bash
npm install
node build_app.js
npx cap add android
npx cap sync android
npx cap open android
```
In Android Studio: Click **Build > Build Bundle(s) / APK(s) > Build APK(s)**.

---

## 📱 Installing on Android Phone
1. Transfer the `.apk` file to your Android phone.
2. Tap the file to install (allow "Install from Unknown Sources" if prompted).
3. Grant **Microphone Access Permission** when opened for live audio noise suppression!
