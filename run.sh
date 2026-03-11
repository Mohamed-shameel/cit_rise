#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# CIT RISE — Start Script
# Starts the FastAPI backend and React frontend in parallel.
# Usage: bash run.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

RED='\033[0;31m'; GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()    { echo -e "${CYAN}[CIT RISE]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

cleanup() {
  echo ""
  info "Shutting down..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
  wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null
  success "All processes stopped."
}
trap cleanup EXIT INT TERM

# ── Check .env ────────────────────────────────────────────────────────────────
if [ ! -f "$BACKEND_DIR/.env" ]; then
  warn ".env not found in backend/. Creating one now."
  echo "Enter your Gemini API key (get free at https://aistudio.google.com/app/apikey):"
  read -r GEMINI_KEY
  echo "GEMINI_API_KEY=$GEMINI_KEY" > "$BACKEND_DIR/.env"
  success ".env created."
fi

# ── Check Python venv ─────────────────────────────────────────────────────────
VENV_PYTHON=""
if [ -f "$BACKEND_DIR/venv/Scripts/python.exe" ]; then
  VENV_PYTHON="$BACKEND_DIR/venv/Scripts/python.exe"       # Windows/MSYS
elif [ -f "$BACKEND_DIR/venv/bin/python" ]; then
  VENV_PYTHON="$BACKEND_DIR/venv/bin/python"               # Linux/macOS
fi

if [ -z "$VENV_PYTHON" ]; then
  info "No venv found — creating one and installing dependencies..."
  python -m venv "$BACKEND_DIR/venv" || error "python not found. Install Python 3.8+."
  if [ -f "$BACKEND_DIR/venv/Scripts/pip.exe" ]; then
    "$BACKEND_DIR/venv/Scripts/pip.exe" install -r "$BACKEND_DIR/requirements.txt" -q
    VENV_PYTHON="$BACKEND_DIR/venv/Scripts/python.exe"
  else
    "$BACKEND_DIR/venv/bin/pip" install -r "$BACKEND_DIR/requirements.txt" -q
    VENV_PYTHON="$BACKEND_DIR/venv/bin/python"
  fi
  success "Python venv ready."
fi

# ── Check uvicorn ─────────────────────────────────────────────────────────────
UVICORN=""
if [ -f "$BACKEND_DIR/venv/Scripts/uvicorn.exe" ]; then
  UVICORN="$BACKEND_DIR/venv/Scripts/uvicorn.exe"
elif [ -f "$BACKEND_DIR/venv/bin/uvicorn" ]; then
  UVICORN="$BACKEND_DIR/venv/bin/uvicorn"
else
  error "uvicorn not found in venv. Run: pip install -r backend/requirements.txt"
fi

# ── Check Node / npm ──────────────────────────────────────────────────────────
if ! command -v npm &>/dev/null; then
  error "npm not found. Install Node.js 16+ from https://nodejs.org"
fi

# ── Install frontend deps if needed ──────────────────────────────────────────
if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
  info "Installing frontend dependencies (first run only)..."
  cd "$FRONTEND_DIR" && npm install --silent
  success "npm install done."
fi

# ── Start Backend ─────────────────────────────────────────────────────────────
info "Starting FastAPI backend on http://localhost:8000 ..."
cd "$BACKEND_DIR"
"$UVICORN" main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
success "Backend PID: $BACKEND_PID"

# ── Wait for backend to be ready ──────────────────────────────────────────────
info "Waiting for backend to start..."
for i in $(seq 1 20); do
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    success "Backend is up!"
    break
  fi
  sleep 1
  if [ "$i" -eq 20 ]; then
    warn "Backend took too long to respond — frontend starting anyway."
  fi
done

# ── Start Frontend ────────────────────────────────────────────────────────────
info "Starting React frontend on http://localhost:3000 ..."
cd "$FRONTEND_DIR"
BROWSER=none npm start &
FRONTEND_PID=$!
success "Frontend PID: $FRONTEND_PID"

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  CIT RISE is running!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Frontend  →  ${CYAN}http://localhost:3000${NC}"
echo -e "  Backend   →  ${CYAN}http://localhost:8000${NC}"
echo -e "  API Docs  →  ${CYAN}http://localhost:8000/docs${NC}"
echo -e ""
echo -e "  Demo login: ${YELLOW}student_demo${NC} (student) / ${YELLOW}admin_001${NC} (admin)"
echo -e ""
echo -e "  Press ${RED}Ctrl+C${NC} to stop both servers."
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Keep alive — wait for both processes
wait "$BACKEND_PID" "$FRONTEND_PID"
