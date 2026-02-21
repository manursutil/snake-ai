#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$ROOT_DIR/build"

mkdir -p "$BUILD_DIR"

MODE="${1:-game}"

if [ "$MODE" = "game" ]; then
    echo "Building playable game..."

    if ! pkg-config --exists raylib; then
        echo "Error: raylib not found via pkg-config." >&2
        exit 1
    fi

    SOURCES=()
    while IFS= read -r file; do
        SOURCES+=("$file")
    done < <(find "$ROOT_DIR/src" -type f -name "*.c" | sort)

    gcc \
        -Wall -Wextra -Wpedantic -std=c11 \
        -I"$ROOT_DIR" \
        "${SOURCES[@]}" \
        $(pkg-config --cflags --libs raylib) \
        -o "$BUILD_DIR/snake"

    echo "Built: $BUILD_DIR/snake"

elif [ "$MODE" = "engine" ]; then
    echo "Building shared library for Python..."

    gcc \
        -Wall -Wextra -Wpedantic -std=c11 \
        -fPIC -shared \
        "$ROOT_DIR/src/c_engine/engine.c" \
        -o "$BUILD_DIR/libsnake.so"

    echo "Built: $BUILD_DIR/libsnake.so"

else
    echo "Unknown mode: $MODE"
    echo "Usage: ./build.sh [game|engine]"
    exit 1
fi