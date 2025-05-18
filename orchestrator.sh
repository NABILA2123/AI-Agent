#!/bin/bash


set -e

if ! command -v uv &> /dev/null
then
    echo "Error: 'uv' is not installed. Please install it from https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

echo "uv is installed."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
else
    echo "Virtual environment already exists. Please remove it to avoid conflicts."
    exit 1
fi

OS="$(uname -s)"
case "$OS" in
    Linux*|Darwin*)
        echo "Activating virtual environment for Linux/macOS..."
        source .venv/bin/activate
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Activating virtual environment for Windows..."
        .venv\Scripts\activate
        ;;
    *)
        echo "Unsupported OS: $OS"
        exit 1
        ;;
esac

echo "Installing dependencies from pyproject.toml..."
uv pip install -r pyproject.toml

echo "Project setup complete."