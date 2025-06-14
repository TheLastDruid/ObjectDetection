@echo off
title Fast Object Detection
echo Starting Object Detection Web Interface...
call "venv\Scripts\activate.bat"
python web_interface.py
pause
