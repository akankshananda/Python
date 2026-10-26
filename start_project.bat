@echo off

cd /d D:\Data_X_Pl_sql\Backend

start "DataX Python Backend" cmd /k python app.py

timeout /t 3 /nobreak >nul

start "" "http://127.0.0.1:5000"