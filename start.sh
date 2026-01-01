#!/bin/bash
# VISUALX Full Stack Startup Script
# Starts both Node.js frontend and Python engine service

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo ""
echo -e "${PURPLE}╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║                                                      ║${NC}"
echo -e "${PURPLE}║          ${NC}V${PURPLE}ISUALX - AI Music Video Generator         ║${NC}"
echo -e "${PURPLE}║                  Powered by VLTRN                    ║${NC}"
echo -e "${PURPLE}║                                                      ║${NC}"
echo -e "${PURPLE}╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Shutting down services...${NC}"
    [ -n "$ENGINE_PID" ] && kill $ENGINE_PID 2>/dev/null
    [ -n "$NODE_PID" ] && kill $NODE_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check dependencies
echo -e "${BLUE}📦 Checking dependencies...${NC}"

if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is required but not installed.${NC}"
    exit 1
fi
echo "  Node.js: $(node --version)"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed.${NC}"
    exit 1
fi
echo "  Python: $(python3 --version)"

# Install Node.js dependencies if needed
if [ ! -d "node_modules" ]; then
    echo ""
    echo -e "${BLUE}📥 Installing Node.js dependencies...${NC}"
    npm install
fi

# Setup Python environment
ENGINES_DIR="$SCRIPT_DIR/engines"
if [ ! -d "$ENGINES_DIR/venv" ]; then
    echo ""
    echo -e "${BLUE}📦 Creating Python virtual environment...${NC}"
    python3 -m venv "$ENGINES_DIR/venv"
fi

echo ""
echo -e "${BLUE}🔌 Installing Python dependencies...${NC}"
source "$ENGINES_DIR/venv/bin/activate"
pip install -q --upgrade pip
pip install -q -r "$ENGINES_DIR/requirements.txt"

# Set ports
NODE_PORT="${PORT:-8080}"
ENGINE_PORT="${ENGINE_SERVICE_PORT:-5051}"

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}Starting Services${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""

# Start Engine Service in background
echo -e "${PURPLE}🚀 Starting Engine Service on port $ENGINE_PORT...${NC}"
cd "$ENGINES_DIR"
ENGINE_SERVICE_PORT=$ENGINE_PORT python3 engine_service.py &
ENGINE_PID=$!
cd "$SCRIPT_DIR"

# Wait for engine to be ready
sleep 2

# Check if engine started
if ! kill -0 $ENGINE_PID 2>/dev/null; then
    echo -e "${RED}❌ Engine service failed to start${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Engine Service running (PID: $ENGINE_PID)${NC}"

# Start Node.js server
echo ""
echo -e "${PURPLE}🚀 Starting Node.js server on port $NODE_PORT...${NC}"
PORT=$NODE_PORT ENGINE_SERVICE_URL="http://localhost:$ENGINE_PORT" node server.js &
NODE_PID=$!

# Wait for node to be ready
sleep 2

# Check if node started
if ! kill -0 $NODE_PID 2>/dev/null; then
    echo -e "${RED}❌ Node.js server failed to start${NC}"
    kill $ENGINE_PID 2>/dev/null
    exit 1
fi
echo -e "${GREEN}✅ Node.js Server running (PID: $NODE_PID)${NC}"

echo ""
echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}VISUALX is running!${NC}"
echo -e "${GREEN}=============================================${NC}"
echo ""
echo -e "  ${BLUE}Web Interface:${NC}  http://localhost:$NODE_PORT"
echo -e "  ${BLUE}Engine API:${NC}     http://localhost:$ENGINE_PORT"
echo ""
echo -e "  ${PURPLE}Press Ctrl+C to stop all services${NC}"
echo ""

# Wait for processes
wait
