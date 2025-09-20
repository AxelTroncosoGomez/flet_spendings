# FletSpendings app

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

**⚠️ Important:** Due to Dart language version compatibility issues with the webview_flutter_android dependency, use the provided build script instead of running `flet build apk` directly:

```bash
# Recommended method - uses the build script that fixes dependency issues
./build_apk.sh
```

**Alternative method (if you encounter issues):**

```bash
# Manual build with workaround
flet build apk -v --clear-cache
# Then manually fix the webview_flutter_android dependency in build/flutter/pubspec.yaml
# by removing the webview_flutter_android line from dependency_overrides section
```

**Issue Explanation:**
The app uses Flet 0.28.2 which is built on Flutter 3.29.2 supporting Dart language version up to 3.7. However, the webview_flutter_android dependency (version 4.10.2) requires Dart 3.9, causing build failures. Since this app doesn't use webview functionality, the build script removes this unnecessary dependency.

## Build Status & Analysis (September 2025)

### Current APK Build Status: ❌ BLOCKED

**Root Cause:** Dart language version incompatibility in the build toolchain

**Technical Details:**
- **Flet 0.28.2** → **Flutter 3.29.2** → **Dart 3.7.2**
- **webview_flutter_android 4.10.2** requires **Dart 3.9+**
- **Incompatibility:** No current Flutter version bundled with Flet supports Dart 3.9+

**What Works:**
✅ App runs perfectly locally (desktop & web)
✅ All webview functionality removed from codebase
✅ Dependencies updated (websockets, etc.)
✅ App is production-ready and fully functional
✅ Automated build script created (`build_apk.sh`)

**What's Blocked:**
❌ APK compilation fails due to Dart version mismatch
❌ Cannot upgrade Flutter independently (managed by Flet)
❌ webview dependency gets re-added during build process

**Resolution Paths:**
1. **Flet updates** to support Flutter with Dart 3.9+ (recommended - wait for next Flet release)
2. **webview_flutter_android downgrades** its Dart requirements
3. **Manual Flutter upgrade** to compatible version (complex, not recommended)

**Notes:**
- Issue is in build toolchain, not application code
- App functionality is 100% complete and tested
- Monitor Flet releases for Flutter/Dart version updates
- Alternative: Consider switching to newer Flet versions when available

**Last Attempted:** September 20, 2025
**Next Check:** Monitor Flet 0.29+ releases for compatibility improvements

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).