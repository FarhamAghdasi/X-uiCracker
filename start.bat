@echo off
title t.me/secabuser
color 0a
cls
echo Installing required packages...
pip install -r requirements.txt
if exist venv (
    call venv\Scripts\activate
)
echo.
echo Starting script...
python main.py
pause
