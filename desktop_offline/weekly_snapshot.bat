@echo off
REM Weekly fund snapshot for the CFP Toolkit Offline Edition (run by Windows Task Scheduler every Sunday).
REM Downloads the latest NAV of every fund + the history of the largest funds, and saves it where the
REM Offline Edition reads it (Documents\CFP Toolkit\snapshot). Log: data\snapshot.log
cd /d "%~dp0.."
set PYTHONUTF8=1
echo ===== %date% %time% >> data\snapshot.log
"C:\Users\kokin\anaconda3\python.exe" -m module2_investment.snapshot >> data\snapshot.log 2>&1
