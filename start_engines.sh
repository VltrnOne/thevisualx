#!/bin/bash
# VISUALX Engine Service Startup Script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINES_DIR="$SCRIPT_DIR/engines"

echo "=============================================="
echo "VISUALX Engine Service"
echo "Powered by VLTRN"
echo "=============================================="

cd "$ENGINES_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "📍 Python: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Set port
PORT="${ENGINE_SERVICE_PORT:-5051}"

echo ""
echo "=============================================="
echo "Starting VISUALX Engine Service"
echo "Port: $PORT"
echo "Audio Analysis: $(python3 -c 'import librosa; print("Enabled")' 2>/dev/null || echo 'Disabled')"
echo "=============================================="

# Start the engine service
python3 engine_service.py
