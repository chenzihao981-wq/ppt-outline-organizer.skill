#!/bin/bash
# Install script for korean-exam-review-skill
# Auto-detects platform and installs to appropriate location

set -e

SKILL_NAME="korean-exam-review"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

detect_platform() {
    if [ -d "$HOME/.claude" ]; then
        echo "claude"
    elif [ -d "$HOME/.cursor" ] || [ -d ".cursor" ]; then
        echo "cursor"
    elif [ -d "$HOME/.agents" ] || [ -d ".agents" ]; then
        echo "universal"
    elif [ -d "$HOME/.gemini" ]; then
        echo "gemini"
    else
        echo "unknown"
    fi
}

install_skill() {
    local platform=$1
    local target=""

    case $platform in
        claude)
            target="$HOME/.claude/skills/$SKILL_NAME"
            ;;
        cursor)
            target="$HOME/.cursor/rules/$SKILL_NAME"
            ;;
        universal)
            target="$HOME/.agents/skills/$SKILL_NAME"
            ;;
        gemini)
            target="$HOME/.gemini/skills/$SKILL_NAME"
            ;;
        *)
            echo "Unknown platform: $platform"
            echo "Manual install: copy this directory to your skills folder"
            exit 1
            ;;
    esac

    mkdir -p "$(dirname "$target")"
    cp -R "$SKILL_DIR" "$target"
    echo "Installed to: $target"
    echo ""
    echo "To use it, open a new session and type:"
    echo "  /korean-exam-review 根据PDF课件填充复习提纲"
}

PLATFORM=$(detect_platform)
echo "Detected platform: $PLATFORM"
install_skill "$PLATFORM"
