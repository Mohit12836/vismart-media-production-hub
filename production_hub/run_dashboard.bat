@echo off
title Vismart AI Media Hub Control Center
cd /d "%~dp0"
echo =======================================================
echo  🚀 STARTING VISMART AI MEDIA HUB (DASHBOARD)
echo  🌐 Access URL: http://localhost:5000
echo =======================================================
python -m uvicorn web.app:app --host 0.0.0.0 --port 5000
pause
