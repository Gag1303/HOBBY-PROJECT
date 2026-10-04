@echo off
REM Double-click this file to open the Thai Fund Dashboard in your browser.
cd /d "%~dp0"
python -m streamlit run app.py
pause
