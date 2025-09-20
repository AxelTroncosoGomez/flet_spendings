#!/bin/bash

echo "🔧 Starting APK build with webview dependency removal..."

# Step 1: Start Flet build process
echo "📱 Starting Flet build process..."
FLUTTER_ROOT=/home/axel/flutter/3.29.2 uv run flet build apk &
BUILD_PID=$!

# Wait for the pubspec.yaml to be created
echo "⏳ Waiting for Flutter project setup..."
while [ ! -f "build/flutter/pubspec.yaml" ]; do
    sleep 2
    if ! ps -p $BUILD_PID > /dev/null; then
        echo "❌ Build process failed before pubspec.yaml creation"
        exit 1
    fi
done

# Step 2: Remove webview dependency
echo "🔪 Removing webview_flutter_android dependency..."
sed -i '/webview_flutter_android:/d' build/flutter/pubspec.yaml

echo "✅ Webview dependency removed successfully!"
echo "📋 Updated pubspec.yaml:"
echo "==================="
cat build/flutter/pubspec.yaml | grep -A5 -B5 "dependency_overrides"
echo "==================="

# Wait for the build to complete or fail
wait $BUILD_PID
BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -eq 0 ]; then
    echo "🎉 APK build completed successfully!"
    echo "📱 APK location: build/flutter/build/app/outputs/flutter-apk/app-release.apk"
else
    echo "❌ Build failed with exit code: $BUILD_EXIT_CODE"
    echo "🔄 Attempting manual build without webview..."

    # Try continuing the build manually
    cd build/flutter
    /home/axel/flutter/3.29.2/bin/flutter pub get
    /home/axel/flutter/3.29.2/bin/flutter build apk --release

    if [ $? -eq 0 ]; then
        echo "🎉 Manual build completed successfully!"
        echo "📱 APK location: build/flutter/build/app/outputs/flutter-apk/app-release.apk"
    else
        echo "❌ Manual build also failed"
        exit 1
    fi
fi