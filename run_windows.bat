@echo off
setlocal
echo ---------------------------------------
echo Chatbot Backend Startup
echo ---------------------------------------

cd backend
if not exist venv (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    echo [2/3] Installing dependencies...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    echo [1/3] Virtual environment found.
    call venv\Scripts\activate
    echo [2/3] Skipping dependency install for speed.
)

echo [3/3] Starting FastAPI server...
uvicorn main:app --host 0.0.0.0 --port 8000
pause
