#!/bin/bash
# Start the VISUALX Engine Service

cd "$(dirname "$0")/engines"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Start the engine service
echo "🚀 Starting VISUALX Engine Service on port 5051..."
python3 engine_service.py



