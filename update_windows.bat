@echo off
setlocal
echo ---------------------------------------
echo Chatbot Backend - Update Dependencies
echo ---------------------------------------

cd backend
if not exist venv (
    echo Virtual environment not found. Please run run_windows.bat first.
    pause
    exit /b
)

echo Activating virtual environment...
call venv\Scripts\activate
echo Updating dependencies from requirements.txt...
pip install -r requirements.txt
echo Update complete.
pause
