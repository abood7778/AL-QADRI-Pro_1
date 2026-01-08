@echo off
title AL-QADRI Pro
echo ========================================
echo    AL-QADRI Pro - Image Processor
echo ========================================
echo.
echo Starting server...
echo.

cd web_interface
start http://127.0.0.1:5000
python app.py
